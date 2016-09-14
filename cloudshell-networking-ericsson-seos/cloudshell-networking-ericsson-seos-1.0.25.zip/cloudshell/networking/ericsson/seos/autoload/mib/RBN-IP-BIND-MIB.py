#
# PySNMP MIB module RBN-IP-BIND-MIB (http://pysnmp.sf.net)
# ASN.1 source file://\usr\share\snmp\RBN-IP-BIND-MIB.my
# Produced by pysmi-0.0.6 at Wed Aug 03 15:27:38 2016
# On host ? platform ? version ? by user ?
# Using Python version 2.7.12 (v2.7.12:d33e0cf91556, Jun 27 2016, 15:19:22) [MSC v.1500 32 bit (Intel)]
#
( Integer, ObjectIdentifier, OctetString, ) = mibBuilder.importSymbols("ASN1", "Integer", "ObjectIdentifier", "OctetString")
( NamedValues, ) = mibBuilder.importSymbols("ASN1-ENUMERATION", "NamedValues")
( ConstraintsUnion, SingleValueConstraint, ConstraintsIntersection, ValueSizeConstraint, ValueRangeConstraint, ) = mibBuilder.importSymbols("ASN1-REFINEMENT", "ConstraintsUnion", "SingleValueConstraint", "ConstraintsIntersection", "ValueSizeConstraint", "ValueRangeConstraint")
( ifIndex, InterfaceIndexOrZero, ) = mibBuilder.importSymbols("IF-MIB", "ifIndex", "InterfaceIndexOrZero")
( rbnMgmt, ) = mibBuilder.importSymbols("RBN-SMI", "rbnMgmt")
( RbnCircuitHandle, ) = mibBuilder.importSymbols("RBN-TC", "RbnCircuitHandle")
( SnmpAdminString, ) = mibBuilder.importSymbols("SNMP-FRAMEWORK-MIB", "SnmpAdminString")
( NotificationGroup, ModuleCompliance, ObjectGroup, ) = mibBuilder.importSymbols("SNMPv2-CONF", "NotificationGroup", "ModuleCompliance", "ObjectGroup")
( Integer32, MibScalar, MibTable, MibTableRow, MibTableColumn, NotificationType, MibIdentifier, IpAddress, TimeTicks, Counter64, Unsigned32, ModuleIdentity, Gauge32, iso, ObjectIdentity, Bits, Counter32, ) = mibBuilder.importSymbols("SNMPv2-SMI", "Integer32", "MibScalar", "MibTable", "MibTableRow", "MibTableColumn", "NotificationType", "MibIdentifier", "IpAddress", "TimeTicks", "Counter64", "Unsigned32", "ModuleIdentity", "Gauge32", "iso", "ObjectIdentity", "Bits", "Counter32")
( DisplayString, TextualConvention, ) = mibBuilder.importSymbols("SNMPv2-TC", "DisplayString", "TextualConvention")
rbnIpBindMib = ModuleIdentity((1, 3, 6, 1, 4, 1, 2352, 2, 26)).setRevisions(("2011-01-19 18:00", "2002-08-20 12:00",))
rbnIpBindMibNotifications = MibIdentifier((1, 3, 6, 1, 4, 1, 2352, 2, 26, 0))
rbnIpBindMibObjects = MibIdentifier((1, 3, 6, 1, 4, 1, 2352, 2, 26, 1))
rbnIpBindMibConformance = MibIdentifier((1, 3, 6, 1, 4, 1, 2352, 2, 26, 2))
rbnIpBindTable = MibTable((1, 3, 6, 1, 4, 1, 2352, 2, 26, 1, 1), )
rbnIpBindEntry = MibTableRow((1, 3, 6, 1, 4, 1, 2352, 2, 26, 1, 1, 1), ).setIndexNames((0, "IF-MIB", "ifIndex"), (0, "RBN-IP-BIND-MIB", "rbnIpBindCircuitHandle"))
rbnIpBindCircuitHandle = MibTableColumn((1, 3, 6, 1, 4, 1, 2352, 2, 26, 1, 1, 1, 1), RbnCircuitHandle())
rbnIpBindIfIndex = MibTableColumn((1, 3, 6, 1, 4, 1, 2352, 2, 26, 1, 1, 1, 2), InterfaceIndexOrZero()).setMaxAccess("readonly")
rbnIpBindHierarchicalIfIndex = MibTableColumn((1, 3, 6, 1, 4, 1, 2352, 2, 26, 1, 1, 1, 3), InterfaceIndexOrZero()).setMaxAccess("readonly")
rbnIpBindCircuitDescr = MibTableColumn((1, 3, 6, 1, 4, 1, 2352, 2, 26, 1, 1, 1, 4), SnmpAdminString().subtype(subtypeSpec=ValueSizeConstraint(0,192))).setMaxAccess("readonly")
rbnIpBindContextName = MibTableColumn((1, 3, 6, 1, 4, 1, 2352, 2, 26, 1, 1, 1, 5), SnmpAdminString().subtype(subtypeSpec=ValueSizeConstraint(0,63))).setMaxAccess("readonly")
rbnIpBindCompliances = MibIdentifier((1, 3, 6, 1, 4, 1, 2352, 2, 26, 2, 1))
rbnIpBindGroups = MibIdentifier((1, 3, 6, 1, 4, 1, 2352, 2, 26, 2, 2))
rbnIpBindCompliance = ModuleCompliance((1, 3, 6, 1, 4, 1, 2352, 2, 26, 2, 1, 1)).setObjects(*(("RBN-IP-BIND-MIB", "rbnIpBindDisplayGroup"),))
rbnIpBindDisplayGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 2352, 2, 26, 2, 2, 1)).setObjects(*(("RBN-IP-BIND-MIB", "rbnIpBindIfIndex"), ("RBN-IP-BIND-MIB", "rbnIpBindHierarchicalIfIndex"), ("RBN-IP-BIND-MIB", "rbnIpBindCircuitDescr"), ("RBN-IP-BIND-MIB", "rbnIpBindContextName"),))
mibBuilder.exportSymbols("RBN-IP-BIND-MIB", PYSNMP_MODULE_ID=rbnIpBindMib, rbnIpBindCompliance=rbnIpBindCompliance, rbnIpBindCircuitDescr=rbnIpBindCircuitDescr, rbnIpBindMibNotifications=rbnIpBindMibNotifications, rbnIpBindTable=rbnIpBindTable, rbnIpBindEntry=rbnIpBindEntry, rbnIpBindDisplayGroup=rbnIpBindDisplayGroup, rbnIpBindMibConformance=rbnIpBindMibConformance, rbnIpBindCircuitHandle=rbnIpBindCircuitHandle, rbnIpBindCompliances=rbnIpBindCompliances, rbnIpBindGroups=rbnIpBindGroups, rbnIpBindContextName=rbnIpBindContextName, rbnIpBindMib=rbnIpBindMib, rbnIpBindHierarchicalIfIndex=rbnIpBindHierarchicalIfIndex, rbnIpBindMibObjects=rbnIpBindMibObjects, rbnIpBindIfIndex=rbnIpBindIfIndex)
