#
# PySNMP MIB module RBN-TC (http://pysnmp.sf.net)
# ASN.1 source file://\usr\share\snmp\RBN-TC.my
# Produced by pysmi-0.0.6 at Wed Aug 03 15:27:38 2016
# On host ? platform ? version ? by user ?
# Using Python version 2.7.12 (v2.7.12:d33e0cf91556, Jun 27 2016, 15:19:22) [MSC v.1500 32 bit (Intel)]
#
( Integer, ObjectIdentifier, OctetString, ) = mibBuilder.importSymbols("ASN1", "Integer", "ObjectIdentifier", "OctetString")
( NamedValues, ) = mibBuilder.importSymbols("ASN1-ENUMERATION", "NamedValues")
( ConstraintsUnion, SingleValueConstraint, ConstraintsIntersection, ValueSizeConstraint, ValueRangeConstraint, ) = mibBuilder.importSymbols("ASN1-REFINEMENT", "ConstraintsUnion", "SingleValueConstraint", "ConstraintsIntersection", "ValueSizeConstraint", "ValueRangeConstraint")
( rbnModules, ) = mibBuilder.importSymbols("RBN-SMI", "rbnModules")
( NotificationGroup, ModuleCompliance, ) = mibBuilder.importSymbols("SNMPv2-CONF", "NotificationGroup", "ModuleCompliance")
( Integer32, MibScalar, MibTable, MibTableRow, MibTableColumn, NotificationType, MibIdentifier, IpAddress, TimeTicks, Counter64, Unsigned32, ModuleIdentity, Gauge32, iso, ObjectIdentity, Bits, Counter32, ) = mibBuilder.importSymbols("SNMPv2-SMI", "Integer32", "MibScalar", "MibTable", "MibTableRow", "MibTableColumn", "NotificationType", "MibIdentifier", "IpAddress", "TimeTicks", "Counter64", "Unsigned32", "ModuleIdentity", "Gauge32", "iso", "ObjectIdentity", "Bits", "Counter32")
( DisplayString, TextualConvention, ) = mibBuilder.importSymbols("SNMPv2-TC", "DisplayString", "TextualConvention")
rbnTC = ModuleIdentity((1, 3, 6, 1, 4, 1, 2352, 5, 2)).setRevisions(("2014-07-19 17:00", "2011-01-19 18:00", "2009-10-20 17:00", "2004-06-19 17:00", "2003-03-17 17:00", "2002-11-11 00:00", "2002-06-26 00:00", "2000-07-14 00:00",))
class RbnCircuitHandle(OctetString, TextualConvention):
    displayHint = '1d:1d:2x-2x-2x'
    subtypeSpec = OctetString.subtypeSpec+ValueSizeConstraint(8,8)
    fixedLength = 8

class RbnKBytes(Integer32, TextualConvention):
    displayHint = 'd'
    subtypeSpec = Integer32.subtypeSpec+ValueRangeConstraint(0,2147483647)

class RbnPercentage(Integer32, TextualConvention):
    displayHint = 'd%'
    subtypeSpec = Integer32.subtypeSpec+ValueRangeConstraint(0,100)

class RbnSlot(Unsigned32, TextualConvention):
    displayHint = 'd'
    subtypeSpec = Unsigned32.subtypeSpec+ValueRangeConstraint(0,255)

class RbnPort(Unsigned32, TextualConvention):
    displayHint = 'd'
    subtypeSpec = Unsigned32.subtypeSpec+ValueRangeConstraint(0,255)

class RbnVidOrUntagged(Integer32, TextualConvention):
    displayHint = 'd'
    subtypeSpec = Integer32.subtypeSpec+ValueRangeConstraint(1,4096)

class RbnPortMediumType(Integer32, TextualConvention):
    subtypeSpec = Integer32.subtypeSpec+SingleValueConstraint(0, 11, 12, 13, 14,)
    namedValues = NamedValues(("unknown", 0), ("dsl", 11), ("cable", 12), ("wireless", 13), ("satellite", 14),)

class RbnUnsigned64(OctetString, TextualConvention):
    displayHint = '8d'
    subtypeSpec = OctetString.subtypeSpec+ValueSizeConstraint(8,8)
    fixedLength = 8

class RbnSubscriberState(Integer32, TextualConvention):
    subtypeSpec = Integer32.subtypeSpec+SingleValueConstraint(9, 13,)
    namedValues = NamedValues(("up", 9), ("standby-up", 13),)

mibBuilder.exportSymbols("RBN-TC", rbnTC=rbnTC, RbnSlot=RbnSlot, RbnPercentage=RbnPercentage, RbnPort=RbnPort, RbnKBytes=RbnKBytes, PYSNMP_MODULE_ID=rbnTC, RbnVidOrUntagged=RbnVidOrUntagged, RbnCircuitHandle=RbnCircuitHandle, RbnPortMediumType=RbnPortMediumType, RbnSubscriberState=RbnSubscriberState, RbnUnsigned64=RbnUnsigned64)
