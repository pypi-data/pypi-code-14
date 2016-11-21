import json
import unittest
import random
# noinspection PyPackageRequirements
from unix_dates import UnixDate, UnixTimeDelta
from itculate_sdk.api import ApiConnection, SDKError
from itculate_sdk.data_types import Vertex, Edge, TimeSeriesSample, percent_value, price_value
from itculate_sdk.data_types.types import DataType, TypedValue, CapacityDataType, RealTypedValue, Units, \
    DataTypeWithUnit, RealTypedValueWithUnit, capacity_value, throughput_value
from itculate_sdk.upload import Upload


class TestDataTypes(unittest.TestCase):
    def test_vertex(self):
        v = Vertex(vertex_type="SomeType",
                   name="The Vertex",
                   keys={"pk": "unique"},
                   primary_key_id="pk",
                   attr1="attr1",
                   attr2="attr2",
                   attr3="attr3")

        self.assertEqual(v.name, "The Vertex")
        self.assertEqual(v.type, "SomeType")
        self.assertDictEqual(v.keys, {"pk": "unique"})
        self.assertEqual(v["attr1"], "attr1")

        # Make sure keys are read-only
        try:
            v["_keys"].update({})
            self.fail("Should not be here")

        except TypeError:
            pass

        # Make sure internal variables are read-only
        try:
            v["_type"] = {}
            self.fail("Should not be here")

        except AssertionError:
            pass

        # Make sure document are read-only
        try:
            v.document["type"] = {}
            self.fail("Should not be here")

        except TypeError:
            pass

    def test_edge(self):
        e = Edge(edge_type="SomeType",
                 source_keys={"pk": "unique1"},
                 target_keys={"pk": "unique2"})

        self.assertDictEqual(e.source_keys, {"pk": "unique1"})
        self.assertDictEqual(e.target_keys, {"pk": "unique2"})
        self.assertEqual(e.type, "SomeType")

        # Make sure document are read-only
        try:
            e.document["type"] = {}
            self.fail("Should not be here")

        except TypeError:
            pass

        # Make sure we cannot create an edge with same source and target keys
        try:
            Edge(edge_type="SomeType",
                 source_keys={"pk": "unique"},
                 target_keys={"pk": "unique"})

            self.fail("Should not be here")

        except AssertionError:
            pass

    def test_sample(self):
        now = UnixDate.now()

        counters = {
            "c1": 0.1,
            "c2": 0.2,
        }

        sample = TimeSeriesSample(key="pk1",
                                  vertex_type="SomeType",
                                  timestamp=now,
                                  counters=counters)

        self.assertEqual(sample.type, "SomeType")
        self.assertEqual(sample.key, "pk1")
        self.assertEqual(sample.timestamp, now)
        self.assertDictEqual(sample.counters, counters)

        # Make sure document are read-only
        try:
            sample.document["type"] = {}
            self.fail("Should not be here")

        except TypeError:
            pass

    def test_data_type(self):
        dt = DataType(label="test_type1")
        self.assertEqual(dt.type, "")
        self.assertIsNotNone(dt.label)

        dt = DataType(label="test_label")
        self.assertEqual(dt.label, "test_label")
        self.assertIsNotNone(json.dumps(dt.meta_data), "Meta data has to be serializable")
        self.assertEqual(dt.meta_data, {
            "type": "",
            "label": "test_label",
            "visible": True,
            "importance": 1000
        })

    def test_typed_single_value(self):
        dt = DataType(label="test_typed_single_value")

        v1 = RealTypedValue(1.0, dt)
        self.assertEqual(v1.value, 1.0)
        self.assertEqual(v1.data_type, dt)

        self.assertFalse(v1 == 1.0, msg="Compare is not supported with scalars")
        self.assertFalse(v1 == TypedValue(1.1, dt))
        self.assertTrue(v1 == TypedValue(1.0, dt))

        v2 = RealTypedValue(2.0, dt)
        self.assertTrue(v2 > v1)
        self.assertTrue(v2 >= v1)
        self.assertTrue(v1 < v2)
        self.assertTrue(v1 <= v2)

        # Check operations
        self.assertTrue(v1 * 4 > v2)
        self.assertTrue(v1 == v2 / 2)
        self.assertTrue(v1 + v2 == v1 * 3)
        self.assertTrue(v2 - v1 == v1)

        # Check other numeric types
        TypedValue(2, dt)

    def test_data_type_with_unit(self):
        class DumbDataType(CapacityDataType):
            pass

        dt = DumbDataType(label="test_label")
        self.assertEqual(dt.type, "Dumb")
        self.assertEqual(dt.units, DumbDataType.units_def)
        self.assertEqual(dt.bases, DumbDataType.bases_def)
        self.assertEqual(dt.unit, Units.GB)
        self.assertEqual(dt.base, 1024.0)
        self.assertIsNotNone(json.dumps(dt.meta_data), "Meta data has to be serializable")
        self.assertEqual(dt.meta_data, {
            "type": dt.type,
            "label": "test_label",
            "units": DumbDataType.units_def,
            "bases": DumbDataType.bases_def,
            "unit": dt.unit,
            "base": dt.base,
            "importance": 1000,
            "visible": True,
        })

        # Test conversions
        self.assertEqual(dt.convert(1024.0, from_unit=Units.MB, to_unit=Units.GB), 1.0)
        self.assertEqual(dt.convert(1.0, from_unit=Units.GB, to_unit=Units.MB), 1024.0)
        self.assertEqual(dt.convert(1.0,
                                    from_unit=Units.GB,
                                    from_base=1000.0,
                                    to_unit=Units.MB,
                                    to_base=1000.0), 1000.0)
        self.assertEqual(dt.convert(1.0, from_unit=Units.GB, from_base=1000.0, to_unit=Units.TB, to_base=1000.0), 0.001)

        # Test default params
        self.assertEqual(dt.convert(1024.0, from_unit=Units.MB), 1.0)
        self.assertEqual(dt.convert(1.0, from_unit=Units.KB, to_unit=Units.KB, to_base=1000.0), 1.024)

    def test_typed_value_with_unit(self):
        class DT(DataTypeWithUnit):
            units_def = ("Bytes", "KB")
            bases_def = (1024.0, 1000.0)

            def __init__(self, label):
                super(DT, self).__init__(unit=Units.KB, base=1024.0, label=label)

        dt = DT("test_label")

        self.assertEqual(RealTypedValueWithUnit(dt, 10.0).value, 10.0)
        self.assertEqual(RealTypedValueWithUnit(dt, 1024.0, Units.BYTES).value, 1.0)
        self.assertEqual(RealTypedValueWithUnit(dt, 1024.0, Units.BYTES).convert(to_unit=Units.KB), 1.0)
        self.assertEqual(RealTypedValueWithUnit(dt, 1024.0, Units.BYTES).convert(to_unit=Units.KB,
                                                                                 to_base=1000.0), 1.024)


class TestConnection(unittest.TestCase):
    def test_connection_with_no_credentials(self):
        # Make a call that does not require authentication
        connection = ApiConnection(api_key="", api_secret="")
        connection.get("health")

    def test_connection_with_local_credentials(self):
        # Check with default parameters
        connection = ApiConnection()
        connection.get("tenants")

        # Now check with a role that doesn't exist in the local credentials file (will fall back to admin)
        connection = ApiConnection(role="user")
        connection.get("tenants")

    def test_exceptions(self):
        bad_connection = ApiConnection(api_key="aa", api_secret="aa")

        try:
            bad_connection.get("tenants")
            self.fail("Should not be here!")

        except SDKError as e:
            self.assertEqual(e.status_code, 401)


class TestUpload(unittest.TestCase):
    def test(self):
        upload = Upload(tenant_id="537L0ViKOa09vElRYVsDSO", collector_id="test_upload_collector")

        v1 = Vertex(vertex_type="Type1",
                    name="v1",
                    keys={"pk": "v1"},
                    primary_key_id="pk",
                    attr1=capacity_value(20.0),
                    attr2=throughput_value(100.0))

        v2 = Vertex(vertex_type="Type1",
                    name="v2",
                    keys={"pk": "v2"},
                    primary_key_id="pk",
                    attr1=10,
                    attr2=20)

        v3 = Vertex(vertex_type="Type1",
                    name="v3",
                    keys={"pk": "v3"},
                    primary_key_id="pk",
                    attr3=price_value(100.0))

        vertices = [v1, v2, v3]

        edges = [
            Edge(edge_type="Type1", source_vertex=v1, target_vertex=v2),
            Edge(edge_type="Type1", source_vertex=v2, target_vertex=v3),
        ]

        # Create a time series
        samples = []
        start_time = UnixDate.now() - UnixTimeDelta.calc(minutes=300)
        for i in range(500):
            ts = start_time + UnixTimeDelta.calc(minutes=i)
            samples.append(TimeSeriesSample(vertex=v1,
                                            timestamp=ts,
                                            counters={
                                                "counter1": percent_value(random.randrange(0, 100)),
                                                "counter2": capacity_value(random.randrange(500, 2500)),
                                            }))

            samples.append(TimeSeriesSample(vertex=v2,
                                            timestamp=ts,
                                            counters={
                                                "counter1": percent_value(random.randrange(0, 100)),
                                                "counter2": capacity_value(random.randrange(500, 2500)),
                                            }))

            samples.append(TimeSeriesSample(vertex=v2,
                                            timestamp=ts,
                                            counters={
                                                "counter3": percent_value(random.random()),
                                            }))

        upload.upload(vertices=vertices, edges=edges, samples=samples)
