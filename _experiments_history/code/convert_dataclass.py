
from dataclasses import dataclass, asdict


def convert_dataclass(data: dataclass, added_dict: dict, target_dataclass: dataclass):
    data_dict = asdict(data)
    return target_dataclass(**data_dict, **added_dict)

