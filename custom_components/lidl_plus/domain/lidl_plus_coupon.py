from dataclasses import dataclass


@dataclass
class LidlPlusCoupon:
    id: str
    title: str
    offerTitle: str
    offerDescription: str
    isActive: bool
    endValidityDate: str
    section: str
