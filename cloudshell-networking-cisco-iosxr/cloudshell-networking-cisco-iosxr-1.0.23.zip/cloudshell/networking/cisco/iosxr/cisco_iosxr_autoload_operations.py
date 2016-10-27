from cloudshell.networking.cisco.autoload.cisco_generic_snmp_autoload import CiscoGenericSNMPAutoload


class CiscoIOSXRSNMPAutoload(CiscoGenericSNMPAutoload):
    def __init__(self, snmp_handler=None, logger=None, supported_os=None):
        """Basic init with injected snmp handler and logger

        :param snmp_handler:
        :param logger:
        :return:
        """

        CiscoGenericSNMPAutoload.__init__(self, snmp_handler, logger, supported_os)

    def _get_power_supply_parent_id(self, port):
        parent_id = int(self.entity_table[port]['entPhysicalContainedIn'])
        result = ''
        if parent_id in self.entity_table.keys() and 'entPhysicalClass' in self.entity_table[parent_id]:
            if self.entity_table[parent_id]['entPhysicalClass'] == 'container':
                result = (self._get_power_supply_parent_id(parent_id) +
                          self.entity_table[parent_id]['entPhysicalParentRelPos'])
        return result
