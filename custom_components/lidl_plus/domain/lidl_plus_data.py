from dataclasses import dataclass
from .lidl_plus_coupon import LidlPlusCoupon


@dataclass
class LidlPlusData:
    coupons: dict[str, LidlPlusCoupon]
