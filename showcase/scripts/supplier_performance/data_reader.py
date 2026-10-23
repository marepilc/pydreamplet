import json
from dataclasses import dataclass
from enum import IntEnum

from tools.runtime import (
    get_data_path,
)


class Segmentation(IntEnum):
    PHASE_OUT = 0
    STRATEGIC = 1
    PREFERRED = 2
    REGULAR = 3


@dataclass
class Supplier:
    name: str
    category: str
    qn: int
    ppm: int
    qty: int
    spend: int
    segmentation: Segmentation


# Get the data
def get_data() -> list[Supplier]:
    suppliers: list[Supplier] = []
    data_path = get_data_path("suppliers.json")
    with open(data_path, "r") as f:
        data = json.load(f)
        for item in data:
            suppliers.append(
                Supplier(
                    name=item["supplierName"],
                    category=item["category"],
                    qn=item["qn"],
                    ppm=item["ppm"],
                    qty=item["qty"],
                    spend=item["spend"],
                    segmentation=Segmentation(item["segmentation"]),
                )
            )
    return suppliers
