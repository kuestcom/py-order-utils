from dataclasses import dataclass

from ..constants import ZERO_BYTES32
from .signatures import EOA
from kuest_eip712_structs import Address, Bytes, EIP712Struct, Uint


@dataclass
class OrderData:
    """
    Inputs to generate orders
    """

    maker: str = None
    """
    Maker of the order, i.e the source of funds for the order
    """

    tokenId: str = None
    """
    Token Id of the CTF ERC1155 asset to be bought or sold.
    If BUY, this is the tokenId of the asset to be bought, i.e the makerAssetId
    If SELL, this is the tokenId of the asset to be sold, i.e the  takerAssetId
    """

    makerAmount: str = None
    """
    Maker amount, i.e the max amount of tokens to be sold
    """

    takerAmount: str = None
    """
    Taker amount, i.e the minimum amount of tokens to be received
    """

    side: int = None
    """
    The side of the order, BUY or SELL
    """

    signer: str = None
    """
    Signer of the order. Optional, if it is not present the signer is the maker of the order.
    """

    expiration: str = "0"
    """
    Timestamp after which the order is expired.
    Optional, if it is not present the value is '0' (no expiration)
    """

    signatureType: int = EOA
    """
    Signature type used by the Order. Default value 'EOA'
    """

    timestamp: str = None
    """
    Millisecond timestamp included in the signed V2 order. Defaults at build time.
    """

    metadata: str = ZERO_BYTES32
    """
    Metadata bytes32 included in the signed V2 order.
    """

    builder: str = ZERO_BYTES32
    """
    Builder code bytes32 included in the signed V2 order.
    """


class Order(EIP712Struct):
    """
    Order
    """

    # NOTE: Important to keep in mind, fields are ordered

    salt = Uint(256)
    """
    Unique salt to ensure entropy
    """

    maker = Address()
    """
    Maker of the order, i.e the source of funds for the order
    """

    signer = Address()
    """
    Signer of the order
    """

    tokenId = Uint(256)
    """
    Token Id of the CTF ERC1155 asset to be bought or sold.
    If BUY, this is the tokenId of the asset to be bought, i.e the makerAssetId
    If SELL, this is the tokenId of the asset to be sold, i.e the  takerAssetId
    """

    makerAmount = Uint(256)
    """
    Maker amount, i.e the max amount of tokens to be sold
    """

    takerAmount = Uint(256)
    """
    Taker amount, i.e the minimum amount of tokens to be received
    """

    side = Uint(8)
    """
    The side of the order, BUY or SELL
    """

    signatureType = Uint(8)
    """
    Signature type used by the Order
    """

    timestamp = Uint(256)
    """
    Millisecond timestamp included in the signed order.
    """

    metadata = Bytes(32)
    """
    Metadata bytes32 included in the signed order.
    """

    builder = Bytes(32)
    """
    Builder code bytes32 included in the signed order.
    """

    def dict(self):
        return {
            "salt": self["salt"],
            "maker": self["maker"],
            "signer": self["signer"],
            "tokenId": self["tokenId"],
            "makerAmount": self["makerAmount"],
            "takerAmount": self["takerAmount"],
            "side": self["side"],
            "signatureType": self["signatureType"],
            "timestamp": self["timestamp"],
            "metadata": self["metadata"],
            "builder": self["builder"],
        }


@dataclass
class SignedOrder:
    """
    Order + Signature
    """

    order: Order
    signature: str
    expiration: str = "0"

    def dict(self):
        d = self.order.dict()
        d["signature"] = self.signature
        if d["side"] == 0:
            d["side"] = "BUY"
        else:
            d["side"] = "SELL"
        d["expiration"] = str(self.expiration)
        d["timestamp"] = str(d["timestamp"])
        d["makerAmount"] = str(d["makerAmount"])
        d["takerAmount"] = str(d["takerAmount"])
        d["tokenId"] = str(d["tokenId"])
        return d
