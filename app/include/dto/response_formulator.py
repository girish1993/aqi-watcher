from pydantic.dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class Locations:
    id: int
    city: Optional[str]
    name: Optional[str]
    country: Optional[str]
    coordinates: Dict[str, float]
    lastUpdated: str
    firstUpdated: str
    measurements: int
    bounds: List[float]


@dataclass
class Parameters:
    id: int
    unit: str
    count: int
    average: float
    lastValue: float
    parameter: str
    displayName: str
    lastUpdated: str
    firstUpdated: str
    location_id: int = None


@dataclass
class Measurements:
    locationId: int
    location: str
    parameter: str
    value: float
    date: Dict[str, str]
    unit: str
    coordinates: Dict[str, float]
    country: str
    city: Optional[str]
    entity: Optional[str]


class DataFactory:
    _CLASS_MAPPING: dict = {
        "locations": Locations,
        "parameters": Parameters,
        "measurements": Measurements
    }
    _results = {}

    @classmethod
    def create_instance_and_populate(cls, key: str, data: List[Dict]) -> None:
        list_of_locations = []
        list_of_associated_params = []
        cls_type = cls._CLASS_MAPPING.get(key, None)

        if cls_type is None:
            raise ValueError(f"No response formatter for {key}")
        if cls_type == Locations:
            for item in data:
                list_of_locations.append(cls_type(**item).__dict__)
                for param_item in item.get("parameters"):
                    parameter = cls._CLASS_MAPPING.get("parameters")(**param_item)
                    parameter.location_id = item.get("id")
                    list_of_associated_params.append(parameter.__dict__)
            cls._results[key] = list_of_locations
            cls._results["parameters"] = list_of_associated_params
        else:
            cls._results[key] = [cls_type(**item).__dict__ for item in data]

    @classmethod
    def formulate(cls, data: List[List[Dict]]) -> Dict[str, List[Dict]]:
        for item in data:
            for res_obj in item:
                key = next(iter(res_obj))
                data = res_obj.get(key)
                cls.create_instance_and_populate(key=key, data=data)

        results = [{k: len(v)} for k, v in cls._results.items()]
        print("results before returning", results)
        return cls._results
