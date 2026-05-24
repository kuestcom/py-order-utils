from unittest import TestCase
from py_order_utils.builders.exception import ValidationException
from py_order_utils.model.order import OrderData
from py_order_utils.model.sides import BUY
from py_order_utils.builders import OrderBuilder
from py_order_utils.model.signatures import EOA
from py_order_utils.signer import Signer
from py_order_utils.constants import ZERO_ADDRESS, ZERO_BYTES32

# publicly known private key
private_key = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
signer = Signer(key=private_key)
maker_address = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"
salt = 479249096354
chain_id = 80002
amoy_contracts = {
    "exchange": "0x4bB1871fdaE80331ce5fF87547b8ff886D1695a5",
    "negRiskExchange": "0xdb1E374a05130d7DE3F16677066553F225D2eE53",
    "collateral": "0x41E94Eb019C0762f9Bfcf9Fb1E58725BfB0e7582",
    "conditional": "0x4682048725865bf17067bd85fF518527A262A9C7",
}


def mock_salt_generator():
    return salt


class TestOrderBuilder(TestCase):
    def test_validate_order(self):
        builder = OrderBuilder(amoy_contracts["exchange"], chain_id, signer)

        # Valid order
        data = self.generate_data()
        self.assertTrue(builder._validate_inputs(data))

        # Invalid if any of the required fields are missing
        data = self.generate_data()
        data.maker = None
        self.assertFalse(builder._validate_inputs(data))

        # Invalid if any of the required fields are invalid
        data = self.generate_data()
        data.timestamp = "-1"
        self.assertFalse(builder._validate_inputs(data))

        data = self.generate_data()
        data.expiration = "not a number"
        self.assertFalse(builder._validate_inputs(data))

        # Invalid signature type
        data = self.generate_data()
        data.signatureType = 100
        self.assertFalse(builder._validate_inputs(data))

    def test_validate_order_neg_risk(self):
        builder = OrderBuilder(amoy_contracts["negRiskExchange"], chain_id, signer)

        # Valid order
        data = self.generate_data()
        self.assertTrue(builder._validate_inputs(data))

        # Invalid if any of the required fields are missing
        data = self.generate_data()
        data.maker = None
        self.assertFalse(builder._validate_inputs(data))

        # Invalid if any of the required fields are invalid
        data = self.generate_data()
        data.timestamp = "-1"
        self.assertFalse(builder._validate_inputs(data))

        data = self.generate_data()
        data.expiration = "not a number"
        self.assertFalse(builder._validate_inputs(data))

        # Invalid signature type
        data = self.generate_data()
        data.signatureType = 100
        self.assertFalse(builder._validate_inputs(data))

    def test_build_order(self):
        builder = OrderBuilder(amoy_contracts["exchange"], chain_id, signer)

        invalid_data_input = self.generate_data()
        invalid_data_input.tokenId = None

        # throw if invalid order input
        with self.assertRaises(ValidationException):
            builder.build_order(invalid_data_input)

        invalid_data_input = self.generate_data()
        invalid_data_input.signer = ZERO_ADDRESS

        # throw if invalid signer
        with self.assertRaises(ValidationException):
            builder.build_order(invalid_data_input)

        _order = builder.build_order(self.generate_data())

        # Ensure correct values on  order
        self.assertTrue(isinstance(_order["salt"], int))
        self.assertEqual(maker_address, _order["maker"])
        self.assertEqual(maker_address, _order["signer"])
        self.assertEqual(1234, _order["tokenId"])
        self.assertEqual(100000000, _order["makerAmount"])
        self.assertEqual(50000000, _order["takerAmount"])
        self.assertEqual(BUY, _order["side"])
        self.assertEqual(EOA, _order["signatureType"])
        self.assertEqual(1234567890000, _order["timestamp"])
        self.assertEqual(ZERO_BYTES32, _order["metadata"])
        self.assertEqual(ZERO_BYTES32, _order["builder"])

        # specific salt
        builder = OrderBuilder(
            amoy_contracts["exchange"], chain_id, signer, mock_salt_generator
        )

        _order = builder.build_order(self.generate_data())

        # Ensure correct values on order
        self.assertTrue(isinstance(_order["salt"], int))
        self.assertEqual(salt, _order["salt"])
        self.assertEqual(maker_address, _order["maker"])
        self.assertEqual(maker_address, _order["signer"])
        self.assertEqual(1234, _order["tokenId"])
        self.assertEqual(100000000, _order["makerAmount"])
        self.assertEqual(50000000, _order["takerAmount"])
        self.assertEqual(BUY, _order["side"])
        self.assertEqual(EOA, _order["signatureType"])
        self.assertEqual(1234567890000, _order["timestamp"])
        self.assertEqual(ZERO_BYTES32, _order["metadata"])
        self.assertEqual(ZERO_BYTES32, _order["builder"])

    def test_build_order_neg_risk(self):
        builder = OrderBuilder(amoy_contracts["negRiskExchange"], chain_id, signer)

        invalid_data_input = self.generate_data()
        invalid_data_input.tokenId = None

        # throw if invalid order input
        with self.assertRaises(ValidationException):
            builder.build_order(invalid_data_input)

        invalid_data_input = self.generate_data()
        invalid_data_input.signer = ZERO_ADDRESS

        # throw if invalid signer
        with self.assertRaises(ValidationException):
            builder.build_order(invalid_data_input)

        _order = builder.build_order(self.generate_data())

        # Ensure correct values on  order
        self.assertTrue(isinstance(_order["salt"], int))
        self.assertEqual(maker_address, _order["maker"])
        self.assertEqual(maker_address, _order["signer"])
        self.assertEqual(1234, _order["tokenId"])
        self.assertEqual(100000000, _order["makerAmount"])
        self.assertEqual(50000000, _order["takerAmount"])
        self.assertEqual(BUY, _order["side"])
        self.assertEqual(EOA, _order["signatureType"])
        self.assertEqual(1234567890000, _order["timestamp"])
        self.assertEqual(ZERO_BYTES32, _order["metadata"])
        self.assertEqual(ZERO_BYTES32, _order["builder"])

        # specific salt
        builder = OrderBuilder(
            amoy_contracts["negRiskExchange"], chain_id, signer, mock_salt_generator
        )

        _order = builder.build_order(self.generate_data())

        # Ensure correct values on order
        self.assertTrue(isinstance(_order["salt"], int))
        self.assertEqual(salt, _order["salt"])
        self.assertEqual(maker_address, _order["maker"])
        self.assertEqual(maker_address, _order["signer"])
        self.assertEqual(1234, _order["tokenId"])
        self.assertEqual(100000000, _order["makerAmount"])
        self.assertEqual(50000000, _order["takerAmount"])
        self.assertEqual(BUY, _order["side"])
        self.assertEqual(EOA, _order["signatureType"])
        self.assertEqual(1234567890000, _order["timestamp"])
        self.assertEqual(ZERO_BYTES32, _order["metadata"])
        self.assertEqual(ZERO_BYTES32, _order["builder"])

    def test_build_order_signature(self):
        builder = OrderBuilder(
            amoy_contracts["exchange"], chain_id, signer, mock_salt_generator
        )

        _order = builder.build_order(self.generate_data())

        # Ensure struct hash is expected(generated via ethers)
        expected_struct_hash = (
            "0xb13efa2da1cf85e6afb56e42033b7d95ffb19edd33c6202c0c03c96d079ba05e"
        )
        struct_hash = builder._create_struct_hash(_order)
        self.assertEqual(expected_struct_hash, struct_hash)

        expected_signature = "0xd120be386428c4949ad7b55c5cad6c01430abdffc3025ddafec83f040275b8ac7289c140f94481aa5df2449a0c95e254e00efb7e562503098692a9d28a0f1edf1c"
        sig = builder.build_order_signature(_order)
        self.assertEqual(expected_signature, sig)

    def test_build_order_signature_neg_risk(self):
        builder = OrderBuilder(
            amoy_contracts["negRiskExchange"], chain_id, signer, mock_salt_generator
        )

        _order = builder.build_order(self.generate_data())

        # Ensure struct hash is expected(generated via ethers)
        expected_struct_hash = (
            "0x147e15edb27e66e6fe90d966775ba2488a1772753f3c5132239776a94dc07543"
        )
        struct_hash = builder._create_struct_hash(_order)
        self.assertEqual(expected_struct_hash, struct_hash)

        expected_signature = "0x5a50841d44661363e3d0d913c12423b487c19a613172d804892a0a45c9cc1a7f4f077b5a5073a23fb30571115fa524163a7b9cc859476001a7f46d0b86457dcf1b"
        sig = builder.build_order_signature(_order)
        self.assertEqual(expected_signature, sig)

    def test_build_signed_order(self):
        builder = OrderBuilder(
            amoy_contracts["exchange"], chain_id, signer, mock_salt_generator
        )

        signed_order = builder.build_signed_order(self.generate_data())

        expected_signature = "0xd120be386428c4949ad7b55c5cad6c01430abdffc3025ddafec83f040275b8ac7289c140f94481aa5df2449a0c95e254e00efb7e562503098692a9d28a0f1edf1c"
        self.assertEqual(expected_signature, signed_order.signature)
        self.assertTrue(isinstance(signed_order.order["salt"], int))
        self.assertEqual(salt, signed_order.order["salt"])
        self.assertEqual(maker_address, signed_order.order["maker"])
        self.assertEqual(maker_address, signed_order.order["signer"])
        self.assertEqual(1234, signed_order.order["tokenId"])
        self.assertEqual(100000000, signed_order.order["makerAmount"])
        self.assertEqual(50000000, signed_order.order["takerAmount"])
        self.assertEqual(BUY, signed_order.order["side"])
        self.assertEqual(EOA, signed_order.order["signatureType"])
        self.assertEqual(1234567890000, signed_order.order["timestamp"])
        self.assertEqual(ZERO_BYTES32, signed_order.order["metadata"])
        self.assertEqual(ZERO_BYTES32, signed_order.order["builder"])

    def test_build_signed_order_neg_risk(self):
        builder = OrderBuilder(
            amoy_contracts["negRiskExchange"], chain_id, signer, mock_salt_generator
        )

        signed_order = builder.build_signed_order(self.generate_data())

        expected_signature = "0x5a50841d44661363e3d0d913c12423b487c19a613172d804892a0a45c9cc1a7f4f077b5a5073a23fb30571115fa524163a7b9cc859476001a7f46d0b86457dcf1b"
        self.assertEqual(expected_signature, signed_order.signature)
        self.assertTrue(isinstance(signed_order.order["salt"], int))
        self.assertEqual(salt, signed_order.order["salt"])
        self.assertEqual(maker_address, signed_order.order["maker"])
        self.assertEqual(maker_address, signed_order.order["signer"])
        self.assertEqual(1234, signed_order.order["tokenId"])
        self.assertEqual(100000000, signed_order.order["makerAmount"])
        self.assertEqual(50000000, signed_order.order["takerAmount"])
        self.assertEqual(BUY, signed_order.order["side"])
        self.assertEqual(EOA, signed_order.order["signatureType"])
        self.assertEqual(1234567890000, signed_order.order["timestamp"])
        self.assertEqual(ZERO_BYTES32, signed_order.order["metadata"])
        self.assertEqual(ZERO_BYTES32, signed_order.order["builder"])

    def generate_data(self) -> OrderData:
        return OrderData(
            maker=maker_address,
            tokenId="1234",
            makerAmount="100000000",
            takerAmount="50000000",
            side=BUY,
            timestamp="1234567890000",
            metadata=ZERO_BYTES32,
            builder=ZERO_BYTES32,
        )
