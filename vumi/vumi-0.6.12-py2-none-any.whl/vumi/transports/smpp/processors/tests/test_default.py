from twisted.internet.task import Clock

from vumi.errors import ConfigError
from vumi.tests.helpers import VumiTestCase
from vumi.transports.tests.helpers import TransportHelper
from vumi.transports.smpp.smpp_transport import SmppTransceiverTransport
from vumi.transports.smpp.tests.fake_smsc import FakeSMSC


class DefaultProcessorTestCase(VumiTestCase):

    def setUp(self):
        self.clock = Clock()
        self.fake_smsc = FakeSMSC()
        self.tx_helper = self.add_helper(
            TransportHelper(SmppTransceiverTransport))

    def test_data_coding_strings(self):
        cfg = {
            'system_id': 'foo',
            'password': 'bar',
            'transport_name': self.tx_helper.transport_name,
            'twisted_endpoint': self.fake_smsc.endpoint,
            'deliver_short_message_processor_config': {
                'data_coding_overrides': {
                    'not-an-int': 'utf-8',
                }
            },
        }
        return self.assertFailure(
            self.tx_helper.get_transport(cfg), ConfigError)
