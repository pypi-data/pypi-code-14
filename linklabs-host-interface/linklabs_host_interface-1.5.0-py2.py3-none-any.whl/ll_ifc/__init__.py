#! /usr/bin/env python
"""
This module defines an interface for commanding a LinkLabs module
via the host interface over a serial connection.
"""

from binascii import hexlify, unhexlify
from collections import namedtuple
from contextlib import contextmanager
import logging
import struct
from time import time, sleep

from serial import Serial
from serial.tools import list_ports

LOG = logging.getLogger(__name__)

IRQ_FLAGS = {
    'WDOG_RESET': 0x00000001,
    'RESET': 0x00000002,
    'TX_DONE': 0x00000010,
    'TX_ERROR': 0x00000020,
    'RX_DONE': 0x00000100,
    'CONNECTED': 0x00001000,
    'DISCONNECTED': 0x00002000,
    'CRYPTO_ESTABLISHED': 0x00010000,
    'APP_TOKEN_CONFIRMED': 0x00020000,
    'DOWNLINK_REQUEST_ACK': 0x00040000,
    'INITIALIZATION_COMPLETE': 0x00080000,
    'CRYPTO_ERROR': 0x00100000,
    'APP_TOKEN_ERROR': 0x00200000,
    'ASSERT': 0x80000000,
}

IFC_ACK_CODES = {
    'ACK': 0,
    'NACK_CMD_NOT_SUPPORTED': 1,
    'NACK_INCORRECT_CHKSUM': 2,
    'NACK_PAYLOAD_LEN_OOR': 3,
    'NACK_PAYLOAD_OOR': 4,
    'NACK_BOOTUP_IN_PROGRESS': 5,
    'NACK_BUSY_TRY_AGAIN': 6,
    'NACK_APP_TOKEN_REG': 7,
    'NACK_PAYLOAD_LEN_EXCEEDED': 8,
    'NACK_NOT_IN_MAILBOX_MODE': 9,
    'NACK_PAYLOAD_BAD_PROPERTY': 10,
    'NACK_NODATA': 11,
    'NACK_QUEUE_FULL': 12,
    'NACK_OTHER': 99,
}

OPCODES = {
    'VERSION': 0,
    'IFC_VERSION': 1,
    'OP_STATE': 2,
    'OP_TX_STATE': 3,
    'OP_RX_STATE': 4,
    'FREQUENCY': 6,
    'TX_POWER': 7,
    'RESET_SETTINGS': 8,
    'GET_RADIO_PARAMS': 9,
    'SET_RADIO_PARAMS': 10,
    'PKT_SEND_QUEUE': 11,
    'TX_POWER_GET': 12,
    'SYNC_WORD_SET': 13,
    'SYNC_WORD_GET': 14,
    'IRQ_FLAGS': 15,
    'IRQ_FLAGS_MASK': 16,
    'SLEEP': 20,
    'SLEEP_BLOCK': 21,
    'PKT_ECHO': 31,
    'PKT_RECV': 40,
    'MSG_RECV_RSSI': 41,
    'PKT_RECV_CONT': 42,
    'MSG_RECV': 43,
    'MODULE_ID': 50,
    'STORE_SETTINGS': 51,
    'DELETE_SETTINGS': 52,
    'RESET_MCU': 60,
    'TRIGGER_BOOTLOADER': 61,
    'MAC_MODE_SET': 70,
    'MAC_MODE_GET': 71,
    'PKT_SEND_ACK': 90,
    'PKT_SEND_UNACK': 91,
    'MSG_SEND': 92,
    'CONN_FILT_SET': 93,
    'CONN_FILT_GET': 94,
    'OP_RESERVED1': 97,
    'TX_CW': 98,
    'RX_MODE_SET': 110,
    'RX_MODE_GET': 111,
    'QOS_REQUEST': 112,
    'QOS_GET': 113,
    'ANTENNA_SET': 114,
    'ANTENNA_GET': 115,
    'NET_TOKEN_SET': 116,
    'NET_TOKEN_GET': 117,
    'NET_INFO_GET': 118,
    'STATS_GET': 119,
    'RSSI_SET': 120,
    'RSSI_GET': 121,
    'DL_BAND_CFG_GET': 122,
    'DL_BAND_CFG_SET': 123,
    'APP_TOKEN_SET': 124,
    'APP_TOKEN_GET': 125,
    'APP_TOKEN_REG_GET': 126,
    'CRYPTO_KEY_XCHG_REQ': 128,
    'MAILBOX_REQUEST': 129,
    'TIMESTAMP': 131,
    'SEND_TIMESTAMP': 132,
    'GET_ASSERT': 248,
    'SET_ASSERT': 249,
    'HARDWARE_TYPE': 254,
    'FIRMWARE_TYPE': 255,
}

DL_MODES = {
    'off': 0,
    'always': 1,
    'mailbox': 2,
}

ANTENNAS = {
    'ufl': 1,
    'trace': 2,
}

MAC_MODES = {
    'NoMac': 0,
    'Symphony': 3,
}

HW_TYPES = {'LLRLP20_V2': 1, 'LLRXR26_V2': 2, 'LLRLP20_V3': 3, 'LLRXR26_V3': 4, 'LLREPEATER': 5}

SUBCLASS_TYPES = {'MODULE': 1, 'REPEATER': 2}

REPEATER_STATE_FIELDS = {
    'MAC_STATE': 0,
    'REPEATER_MODE': 1,
    'CONNECTION_LED_IS_ON': 2,
    'CONNECTION_LED_IS_FLASHING': 3,
    'CONNECTION_LED_COLOR': 4,
}

REPEATER_LED_COLOR_VALUE = {
    'RED': 0,
    'GREEN': 255,
}

REPEATER_TEST_CMDS = {'TRIGGER_WDOG': 0x0001, 'EXT_BUTTON_SHORT': 0x0002, 'EXT_BUTTON_LONG': 0x0004}

CONNECTION_FILTER = {'ANY': 0, 'GATEWAYS_ONLY': 1, 'REPEATERS_ONLY': 2}

NetworkInfo = namedtuple('NetworkInfo', [
    'network_id_node', 'network_id_gw', 'gateway_channel', 'gateway_frequency', 'last_rx_tick',
    'rssi', 'snr', 'connection_status', 'scanning', 'gateway_id'
])

ReceivedMessage = namedtuple('ReceivedMessage', ['payload', 'rssi', 'snr', 'port'])

OPEN_NET_TOKEN = hexlify(b'OPEN')
ALLOWED_PORT_RANGE = range(0, 128)
VID_PID = '10c4:ea60'


class GenericConnection(object):
    """
    The interface to a LinkLabs module. The `device` parameter is the
    serial port device this connection will be made over.
    """

    def __init__(self, device):
        """
        """
        self.sdev = Serial(port=device, baudrate=115200, timeout=1.0)
        if not self.sdev.isOpen():
            raise OpenError("Cannot open device {}".format(device))
        self.frame_start_byte = 0xc4
        self.dummy_byte = 0xff
        self.num_dummy_bytes = 4
        self.message_counter = 0
        self.response_header_length = 5
        self.frame_start_timeout = 1.0

    def close(self):
        """ Closes the serial port owned by this object. """
        self.sdev.close()

    def __enter__(self):
        """ Called by contextmanager """
        return self

    def __exit__(self, type_, value, traceback):
        """ Called by contextmanager """
        self.close()

    def __str__(self):
        return self.get_unique_id()

    def __repr__(self):
        unique_id = self.get_unique_id()
        device_port = self.sdev.port
        return self.__class__.__name__ + "('{}') -> {}".format(device_port, unique_id)

    def _send_command(self, opcode, send_buff=None):
        """
        Sends a command to the device, waits for the response, and
        returns the response payload.
        """
        self._send_packet(opcode, send_buff if send_buff else [])
        response = self._receive_packet(opcode, self.message_counter)
        self.message_counter = (self.message_counter + 1) % 256

        return response

    def _send_packet(self, opcode, send_buff):
        """ Sends a framed uart transmission to the device. """
        buff = bytearray()

        buff.append(self.frame_start_byte)
        buff.append(opcode)
        buff.append(self.message_counter)

        len_msb = (len(send_buff) >> 8) & 0xFF
        len_lsb = (len(send_buff) >> 0) & 0xFF
        buff.append(len_msb)
        buff.append(len_lsb)

        buff = buff + bytearray(send_buff)

        checksum = compute_checksum(buff)
        buff.append((checksum >> 8) & 0xFF)
        buff.append((checksum >> 0) & 0xFF)

        # Start the buffer with several dummy bytes
        dummy = bytearray([self.dummy_byte] * self.num_dummy_bytes)
        buff = dummy + buff

        LOG.debug("Sending frame %s to %s", hexlify(buff), self.sdev.port)
        written_size = self.sdev.write(buff)
        if written_size != len(buff):
            raise CommsError("Not enough bytes written.")
        self.sdev.flush()

    def _receive_packet(self, opcode, message_counter):
        """
        Receive a framed uart transmission from the device. Will return
        the packet payload (without any framing header or CRC).
        """
        start = time()
        while True:
            if time() - start > self.frame_start_timeout:
                raise CommsError("Did not get frame start within timeout.")
            byte = self.sdev.read()
            if byte:
                if ord(byte) == self.frame_start_byte:
                    break
                else:
                    LOG.warning("Bad frame start byte: %r", byte)

        resp_header = bytearray(self.sdev.read(self.response_header_length))
        resp_opcode = resp_header[0]
        resp_message_counter = resp_header[1]
        resp_ack = resp_header[2]
        resp_payload_len = (resp_header[3] << 8) + resp_header[4]
        LOG.debug("Received frame header %s from %s", hexlify(resp_header), self.sdev.port)

        if resp_opcode != opcode:
            raise CommsError("Did not get the same opcode we sent: "
                             "Received {} not {}".format(resp_opcode, opcode))
        if resp_message_counter != message_counter:
            raise CommsError("Did not get the same message counter we sent.")

        if resp_ack != IFC_ACK_CODES['ACK']:
            # Read checksum bytes before raising the exception
            resp_checksum_buff = bytearray(self.sdev.read(2))

            nack = next((nack for nack, val in IFC_ACK_CODES.items() if val == resp_ack), None)
            if nack is None:
                LOG.warning("Unknown NACK: %s", resp_ack)
                nack = 'NACK_OTHER'

            raise NackError(resp_ack, "Received NACK from module: {}".format(nack))

        resp_payload = bytearray(self.sdev.read(resp_payload_len))
        LOG.debug("Received frame payload %s from %s", hexlify(resp_payload), self.sdev.port)
        if len(resp_payload) != resp_payload_len:
            raise CommsError("Could not read the number of bytes promised by the module.")

        resp_checksum_buff = bytearray(self.sdev.read(2))
        resp_checksum = (resp_checksum_buff[0] << 8) + resp_checksum_buff[1]
        checksum = compute_checksum(bytearray([self.frame_start_byte]) + resp_header + resp_payload)
        if resp_checksum != checksum:
            raise CommsError("Checksum mismatch.")

        LOG.debug("Received checksum bytes %s from %s", hexlify(resp_checksum_buff), self.sdev.port)
        self.sdev.flush()

        return resp_payload

    def get_hw_type(self):
        """ Returns the device' hardware type. """
        resp_payload = self._send_command(OPCODES['HARDWARE_TYPE'])
        return resp_payload[0]

    def get_version(self):
        """ Returns the module's firmware version as a tuple of (major, minor, tag). """
        resp_payload = self._send_command(OPCODES['VERSION'])
        return resp_payload[0], resp_payload[1], (resp_payload[2] << 8) + resp_payload[3]

    def get_unique_id(self):
        """ Returns the UUID of the module. """
        uuid = self._send_command(OPCODES['MODULE_ID'])
        (uuid_int, ) = struct.unpack('>Q', bytes(uuid))
        uuid_int &= int('1' * 36, 2)
        return "$301$0-0-0-{:09X}".format(uuid_int)


class ModuleConnection(GenericConnection):
    """
    The interface to a LinkLabs module. The `device` parameter should be a path
    to the module. If none is specified, then the constructor will attempt
    to find one.
    """

    def __init__(self, device=None):
        device = device if device else self._find_module_device()
        LOG.info("Connecting to Module on %s", device)
        # The base class actually opens the connection
        super(ModuleConnection, self).__init__(device)

    @staticmethod
    def _find_module_device():
        for port in list_ports.grep('10c4'):
            with GenericConnection(port[0]) as conn:
                if conn.get_hw_type() != HW_TYPES['LLREPEATER']:
                    return port[0]
        raise OpenError("Cannot find module")

    def set_mac_mode(self, mac):
        """
        Sets the MAC mode of the module. Valid values of the parameter `mac` are
        'Symphony' or 'NoMac'.
        """
        if mac in MAC_MODES:
            self._send_command(OPCODES['MAC_MODE_SET'], [MAC_MODES[mac]])
        else:
            raise ValueError("Unknown MAC mode: {}".format(mac))

    def get_mac_mode(self):
        """ Returns either 'Symphony' or 'NoMac'. """
        resp = self._send_command(OPCODES['MAC_MODE_GET'])
        mode = resp[0]
        for mac_mode, mac_mode_byte in MAC_MODES.items():
            if mac_mode_byte == mode:
                return mac_mode

        raise CommsError("Unknown MAC mode: {}".format(mode))

    def send_message(self, message, ack=False, port=0):
        """ Sends an uplink message to the gateway. """
        if len(message) > 256:
            raise ValueError("Message too long ({}). Max message size is 256 bytes.".format(
                len(message)))
        if port not in ALLOWED_PORT_RANGE:
            raise ValueError("Port must be within [0, 127]")
        self._send_command(OPCODES['MSG_SEND'], bytearray([int(ack), port]) + message)

    def get_irq_flags(self):
        """ Returns a list of irq flags (as strings). """
        resp = self._send_command(OPCODES['IRQ_FLAGS'], [0] * 4)
        flags_int = (resp[0] << 24) + (resp[1] << 16) + (resp[2] << 8) + resp[3]
        return [f for f in IRQ_FLAGS if IRQ_FLAGS[f] & flags_int]

    def clear_irq_flags(self, flags='all'):
        """
        Clears the irq flags. `flags` is a list of irq flag strings. If
        the parameter is not given, then all flags are cleared.
        """
        flag_dict = IRQ_FLAGS if flags == 'all' else {f: IRQ_FLAGS[f] for f in flags}
        flag_int = 0
        for flag_val in flag_dict.values():
            flag_int |= flag_val
        flag_buff = [0xFF & (flag_int >> n) for n in [24, 16, 8, 0]]
        self._send_command(OPCODES['IRQ_FLAGS'], flag_buff)

    def delete_settings(self):
        """ Returs the module to factory defaults. """
        LOG.info("Resetting module %s to factory defaults.", self)
        self._send_command(OPCODES['DELETE_SETTINGS'])
        _wait_for_reboot()

    def reset_mcu(self):
        """ Reset the module """
        self._send_command(OPCODES['RESET_MCU'])
        _wait_for_reboot()

    def reboot_into_bootloader(self):
        """ Reboots the module into bootloader mode. """
        # Use the _send_packet method because the module
        # reboots before sending the response.
        self._send_packet(OPCODES['TRIGGER_BOOTLOADER'], [])

    def set_network_token(self, token):
        """ Sets the network token for the module. The token should be a hex string. """
        network_token = unhexlify(token)
        self._send_command(OPCODES['NET_TOKEN_SET'], network_token)

    def get_network_token(self):
        """ Sets the network token for the module. The token should be a hex string. """
        network_token = self._send_command(OPCODES['NET_TOKEN_GET'])
        return hexlify(network_token)

    def set_app_token(self, token):
        """ Sets the application token for the module. The token should be a hex string. """
        app_token = unhexlify(token)
        self._send_command(OPCODES['APP_TOKEN_SET'], app_token)

    def get_app_token(self):
        """ Sets the application token for the module. The token should be a hex string. """
        app_token = self._send_command(OPCODES['APP_TOKEN_GET'])
        return hexlify(app_token)

    def is_app_token_registered(self):
        """ Returns whether this module's app token has been confirmed by the gateway. """
        return bool(self._send_command(OPCODES['APP_TOKEN_REG_GET'])[0])

    def set_qos(self, qos):
        """
        Requests a quality of service level from the gateway. `qos` can be
        an integer from 0 through 15.
        """
        self._send_command(OPCODES['QOS_REQUEST'], [qos])

    def get_qos(self):
        """ Returns the module's quality of service level. """
        return int(self._send_command(OPCODES['QOS_GET'])[0])

    def set_downlink_mode(self, mode):
        """
        Sets the downlink mode of the module.
        Valid modes are 'off', 'always', and 'mailbox'.
        """
        self._send_command(OPCODES['RX_MODE_SET'], [DL_MODES[mode]])

    def get_downlink_mode(self):
        """ Returns a boolean indicating whether or not the module is in downlink mode. """
        dl_mode_int = self._send_command(OPCODES['RX_MODE_GET'])[0]
        for mode in DL_MODES:
            if DL_MODES[mode] == dl_mode_int:
                return mode
        raise CommsError("Unknown downlink mode: {}".format(dl_mode_int))

    def retrieve_packet(self):
        """
        Get a downlink packet from the module.
        Returns the packet, as well as RSSI and SNR values.
        """
        buff = self._send_command(OPCODES['MSG_RECV'])
        if buff:
            (rssi, snr, port) = struct.unpack_from('<hbB', bytes(buff))
            message = buff[4:]
            return ReceivedMessage(message, rssi, snr, port)

    def get_network_info(self):
        """ Gets current network info from the module. Returns a NetworkInfo object. """
        net_info_struct_str = '>LLbLLhbBBQ'
        info = NetworkInfo(*struct.unpack_from(net_info_struct_str,
                                               bytes(self._send_command(OPCODES['NET_INFO_GET']))))

        # Convert some values from integers.
        info = info._replace(network_id_node='{:8X}'.format(info.network_id_node),
                             network_id_gw='{:8X}'.format(info.network_id_gw),
                             gateway_id='$101$0-0-0-{:8x}'.format(info.gateway_id),
                             scanning=bool(info.scanning))

        if info.connection_status == 0:
            info = info._replace(connection_status='Initializing')
        elif info.connection_status == 1:
            info = info._replace(connection_status='Disconnected')
        elif info.connection_status == 2:
            info = info._replace(connection_status='Connected')

        return info

    def get_state(self):
        """ Returns a triple: (state, tx_state, rx_state) """
        states = {1: 'Connected', 2: 'Disconnected', 3: 'Initializing', 255: 'Error'}
        state = states[self._send_command(OPCODES['OP_STATE'])[0]]

        tx_states = {1: 'Transmitting', 2: 'Success', 255: 'Error'}
        tx_state = tx_states[self._send_command(OPCODES['OP_TX_STATE'])[0]]

        rx_states = {0: 'NoMsg', 1: 'Msg'}
        rx_state = rx_states[self._send_command(OPCODES['OP_RX_STATE'])[0]]

        return state, tx_state, rx_state

    def mailbox_request(self):
        """ Pings the gateway to check this module's mailbox. """
        self._send_command(OPCODES['MAILBOX_REQUEST'])

    def set_antenna(self, antenna):
        """ Sets the antenna. The `antenna` argument must be 'trace' or 'ufl'. """
        self._send_command(OPCODES['ANTENNA_SET'], [ANTENNAS[antenna]])

    def get_antenna(self):
        """ Gets the current active antenna. Returns either 'ufl' or 'trace'. """
        antenna_byte = self._send_command(OPCODES['ANTENNA_GET'])[0]
        for (antenna, antenna_num) in ANTENNAS.items():
            if antenna_num == antenna_byte:
                return antenna

        raise CommsError("Unknown antenna number")

    def set_connection_filter(self, filter_value):
        """
        Sets the connection filter for the module. `filter_value` should be a value in
        the CONNECTION_FILTER dictionary.
        """
        self._send_command(OPCODES['CONN_FILT_SET'], bytearray([int(filter_value)]))

    def get_connection_filter(self):
        """ Returns the current connection filter value for the module. """
        return int(self._send_command(OPCODES['CONN_FILT_GET'])[0])


class ModuleDriver(ModuleConnection):
    """
    This class extends the ModuleConnection class to provide higher level
    functionality.
    """

    def __init__(self, *args, **kwargs):
        super(ModuleDriver, self).__init__(*args, **kwargs)
        self.transmit_timeout = 60.0
        self.reboot_delay_s = 3.0

    def wait_for_flags(self, flags, timeout_s=None, bad_flags=None):
        """
        Waits for all flags in `flags` to show up.
        If `timeout_s` is None, wait indefinitely.
        """
        bad_flags = bad_flags or []
        start = time()
        while time() - start < timeout_s if timeout_s is not None else True:
            mod_flags = self.get_irq_flags()
            for flag in bad_flags:
                if flag in mod_flags:
                    raise BadFlagError(flag)
            if all(f in mod_flags for f in flags):
                break
            else:
                sleep(0.1)
        else:
            raise FlagTimeoutError("Timeout waiting for flags {}".format(flags))

    def set_up(self, app_token, network_token=OPEN_NET_TOKEN, qos=0, downlink_mode='off'):
        """
        Sets up the module so that it's ready to uplink or downlink.
        Throws an exception if it can't connect to a gateway with the provided network
        and application tokens.
        """

        self.set_mac_mode('Symphony')

        self.set_network_token(network_token)
        self.set_app_token(app_token)
        self.set_qos(qos)
        self.set_downlink_mode(downlink_mode)

        timeout_s = 120.0
        start = time()
        while time() - start < timeout_s:
            (state, _, _) = self.get_state()
            if state == 'Initializing':
                LOG.debug("Initializing...")
            elif state == 'Connected':
                LOG.info("Successfully set up %s", self)
                break
            elif state == 'Disconnected':
                raise GatewayConnectionError("{} could not connect to a gateway".format(self))
            else:
                raise GatewayConnectionError("Error setting up {}: {}".format(self, state))
        else:
            raise GatewayConnectionError("Timeout in setting up {}".format(self))

    def send_message_checked(self, message, port=0, acked=True):
        """
        Sends an ACK'd message, and waits for the status of that message.
        Throws an exception if the message was not successful.
        """
        self.clear_irq_flags(['TX_DONE', 'TX_ERROR'])
        self.send_message(message, ack=acked, port=port)

        LOG.debug("Waiting for ACK for module %s.", self)
        self.wait_for_flags(['TX_DONE'], self.transmit_timeout, bad_flags=['TX_ERROR'])

    def get_received_message(self):
        """
        Returns a downlink message if there is one, else returns None
        """
        if 'RX_DONE' in self.get_irq_flags():
            self.clear_irq_flags(['RX_DONE'])
            pkt = self.retrieve_packet()
            if pkt is None:
                LOG.warning("RX_DONE flag set but no packet available.")
            return pkt

    def wait_for_received_message(self, timeout_s=None):
        """
        Waits up to `timeout_s` seconds for a received message, and returns it if one was received.
        Otherwise throws an exception after `timeout` seconds.
        If `timeout_s` is None, wait indefinitely.
        """
        self.wait_for_flags(['RX_DONE'], timeout_s)
        return self.get_received_message()


class RepeaterConnection(GenericConnection):
    """
    The interface to a LinkLabs repeater. The `device` parameter should be a path
    to the module. If none is specified, then the constructor will attempt
    to find one.
    """

    def __init__(self, device=None):
        device = device if device else self._find_repeater_device()
        LOG.info("Connecting to Repeater on %s", device)
        # The base class actually opens the connection
        super(RepeaterConnection, self).__init__(device)

        self.reboot_delay_sec = 10
        self.reboot_delay_sec_factory_reset = 20
        self.flash_vars_delay_sec = 2

    @staticmethod
    def _find_repeater_device():
        for port in list_ports.grep(VID_PID):
            with GenericConnection(port[0]) as conn:
                if conn.get_hw_type() == HW_TYPES['LLREPEATER']:
                    return port[0]
        raise OpenError("Cannot find repeater")

    def delete_settings(self):
        """ Returs the module to factory defaults. """
        LOG.info("Resetting module %s to factory defaults.", self)
        self._send_command(OPCODES['DELETE_SETTINGS'])
        _wait_for_reboot(self.reboot_delay_sec_factory_reset)

    def reset_mcu(self):
        """ Reset the module """
        self._send_command(OPCODES['RESET_MCU'])
        _wait_for_reboot(self.reboot_delay_sec)

    def reboot_into_bootloader(self):
        """ Reboots the repeater into bootloader mode. """
        self._send_command(OPCODES['TRIGGER_BOOTLOADER'])
        _wait_for_reboot(self.reboot_delay_sec)

    def set_network_token(self, token):
        """ Sets the network token for the module. The token should be a hex string. """
        network_token = unhexlify(token)
        self._send_command(OPCODES['NET_TOKEN_SET'], network_token)
        sleep(self.flash_vars_delay_sec)

    def get_network_token(self):
        """ Sets the network token for the module. The token should be a hex string. """
        network_token = self._send_command(OPCODES['NET_TOKEN_GET'])
        return hexlify(network_token)

    def get_state(self):
        """ Gets the 'state' of the repeater via the OP_STATE command """
        resp = self._send_command(OPCODES['OP_STATE'])
        return resp

    def get_assert(self):
        """ Gets assert info, if there is any """
        try:
            resp = self._send_command(OPCODES['GET_ASSERT'])
        except NackError as err:
            if 'NACK_OTHER' in str(err):
                return None
            else:
                raise

        line_num = struct.unpack_from('>L', bytes(resp))[0]
        filename = str(resp[4:-1])
        return line_num, filename

    def set_assert(self):
        """ Gets assert info, if there is any """
        try:
            self._send_command(OPCODES['SET_ASSERT'])
        except CommsError as err:
            if 'timeout' in str(err):
                pass
            else:
                raise RuntimeError("Unexpected error from SET_ASSERT")

    def test_ext_button(self, long_press):
        """ Triggers a simulated external button press (long and short) """
        try:
            if long_press is True:
                cmd_int = REPEATER_TEST_CMDS['EXT_BUTTON_LONG']
                delay_sec = 10
            else:
                cmd_int = REPEATER_TEST_CMDS['EXT_BUTTON_SHORT']
                delay_sec = 3

            cmd_buff = [0xFF & (cmd_int >> n) for n in [8, 0]]
            self._send_command(OPCODES['OP_RESERVED1'], cmd_buff)

            sleep(delay_sec)

        except CommsError as err:
            if 'timeout' in str(err):
                pass
            else:
                raise RuntimeError("Unexpected error from test_ext_button")


def compute_checksum(buff):
    """ Computes the 16-bit CRC of the buffer. Returns the checksum as an integer. """
    checksum = 0
    for byte in buff:
        checksum = ((checksum >> 8) | (checksum << 8)) & 0xFFFF
        checksum = checksum ^ byte
        checksum = checksum ^ ((checksum & 0xFF) >> 4)
        checksum = checksum ^ ((checksum << 12) & 0xFFFF)
        checksum = checksum ^ ((checksum & 0xFF) << 5)
    return checksum


# TODO - Make a method of the generic connection, and redefine the delay and string for each device
def _wait_for_reboot(DELAY_SEC=3):
    """ We need to wait a few seconds after the module reboots before communicating with it. """
    LOG.debug("Sleeping after rebooting module.")
    sleep(DELAY_SEC)


class LLIfcError(Exception):
    """ Base exception for all ll_ifc errors. """


class CommsError(LLIfcError):
    """
    Represents a low level communications failure between the host
    computer and the Symphony module.
    """


class NackError(CommsError):
    """ Thrown when a host interface NACK is sent by the module. """


class BadFlagError(LLIfcError):
    """ Thrown when a bad flag (e.g. TX_ERROR) is raised by the Symphony module. """


class FlagTimeoutError(LLIfcError):
    """
    Thrown when a timeout occurs when waiting for a flag to be raised by the Symphony module.
    """


class OpenError(LLIfcError):
    """ Thrown when there is a problem opening or finding an attached Symphony module. """


class GatewayConnectionError(LLIfcError):
    """ Thrown when a module can't connect to a gateway. """


@contextmanager
def _get_all_connections():
    """
    Returns a list of `GenericConnection` objects for each attached
    device with the correct VID and PID.
    """
    connections = [GenericConnection(dev) for [dev, _, _] in list_ports.grep(VID_PID)]
    yield connections
    for connection in connections:
        connection.close()


@contextmanager
def get_all_devices():
    """
    Returns a list of devices that are either `ModuleDriver` objects
    or `RepeaterConnection` objects.

    This uses must be used with a 'with' statement:

    Example
    =======
    >>> with ll_ifc.get_all_devices() as devices:
    >>>     for device in devices:
    >>>         print(device)
    """
    # A mapping of device path to class
    device_paths = {}
    with _get_all_connections() as connections:
        for connection in connections:
            hw_type = connection.get_hw_type()
            path = connection.sdev.port
            if hw_type in HW_TYPES.values():
                cls = RepeaterConnection if hw_type == HW_TYPES['LLREPEATER'] else ModuleDriver
                device_paths[path] = cls
            else:
                raise ValueError("Hardware type unknown: {}", hw_type)

    devices = [cls(path) for (path, cls) in device_paths.items()]

    yield devices

    for device in devices:
        device.close()


@contextmanager
def get_all_repeaters():
    """ Returns a list (within a contextmanager) of all attached repeaters. """
    with get_all_devices() as devs:
        yield [dev for dev in devs if isinstance(dev, RepeaterConnection)]


@contextmanager
def get_all_modules():
    """ Returns a list (within a contextmanager) of all attached modules. """
    with get_all_devices() as devs:
        yield [dev for dev in devs if isinstance(dev, ModuleConnection)]
