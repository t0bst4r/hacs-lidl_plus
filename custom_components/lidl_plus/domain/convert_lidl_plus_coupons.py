from .lidl_plus_coupon import LidlPlusCoupon


def convert_lidl_plus_coupons(coupon_result: any) -> dict[str, LidlPlusCoupon]:
    sections = coupon_result["sections"]
    result = {}
    for section in sections:
        coupons = section["coupons"]
        for coupon in coupons:
            result[coupon["id"]] = LidlPlusCoupon(
                id=coupon["id"], section=section["name"], title=coupon["title"],
                offerTitle=coupon["offerTitle"], offerDescription=coupon["offerDescriptionShort"],
                isActive=coupon["isActivated"], endValidityDate=coupon["endValidityDate"]
            )
    return result
