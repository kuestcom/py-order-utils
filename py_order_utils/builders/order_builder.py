from ..signer import Signer
from .base_builder import BaseBuilder
from .exception import ValidationException
from ..constants import ZERO_BYTES32
from time import time_ns
from ..utils import generate_seed, normalize_address, prepend_zx
from ..model.order import Order, SignedOrder, OrderData
from ..model.sides import BUY, SELL
from ..model.signatures import EOA, KUEST_EIP1271, KUEST_GNOSIS_SAFE, KUEST_PROXY


class OrderBuilder(BaseBuilder):
    """
    Order builder
    """

    def __init__(
        self,
        exchange_address: str,
        chain_id: int,
        signer: Signer,
        salt_generator=generate_seed,
    ):
        super().__init__(exchange_address, chain_id, signer, salt_generator)

    def build_order(self, data: OrderData) -> Order:
        """
        Builds an order
        """
        if data.timestamp is None or str(data.timestamp) == "0":
            data.timestamp = str(time_ns() // 1_000_000)

        if not self._validate_inputs(data):
            raise ValidationException("Invalid order inputs")

        if data.signer is None:
            data.signer = data.maker

        if data.signer != self.signer.address():
            raise ValidationException("Signer does not match")

        if data.expiration is None:
            data.expiration = "0"

        if data.signatureType is None:
            data.signatureType = EOA

        if data.metadata is None:
            data.metadata = ZERO_BYTES32

        if data.builder is None:
            data.builder = ZERO_BYTES32

        return Order(
            salt=int(self.salt_generator()),
            maker=normalize_address(data.maker),
            signer=normalize_address(data.signer),
            tokenId=int(data.tokenId),
            makerAmount=int(data.makerAmount),
            takerAmount=int(data.takerAmount),
            side=int(data.side),
            signatureType=int(data.signatureType),
            timestamp=int(data.timestamp),
            metadata=data.metadata,
            builder=data.builder,
        )

    def build_order_signature(self, _order: Order) -> str:
        """
        Signs the order
        """
        return prepend_zx(self.sign(self._create_struct_hash(_order)))

    def build_signed_order(self, data: OrderData) -> SignedOrder:
        """
        Helper function to build and sign a order
        """
        order = self.build_order(data)
        sig = self.build_order_signature(order)

        return SignedOrder(order, sig, expiration=str(data.expiration or "0"))

    def _validate_inputs(self, data: OrderData) -> bool:
        return not (
            # ensure required values exist
            data.maker is None
            or data.tokenId is None
            or data.makerAmount is None
            or data.takerAmount is None
            or data.side is None
            or data.side not in [BUY, SELL]
            or not data.expiration.isnumeric()
            or int(data.expiration) < 0
            or data.timestamp is None
            or not str(data.timestamp).isnumeric()
            or int(data.timestamp) < 0
            or data.signatureType is None
            or data.signatureType
            not in [EOA, KUEST_GNOSIS_SAFE, KUEST_PROXY, KUEST_EIP1271]
        )
