from abc import ABC, abstractmethod
from typing import Tuple

from geopy.distance import geodesic


class AbstractDistanceCounter(ABC):

    @staticmethod
    @abstractmethod
    def count_distance(*args, **kwargs):
        pass


class DistanceCounter(AbstractDistanceCounter):

    @staticmethod
    def count_distance(fst_point: Tuple[float, float], dst_point: Tuple[float, float]) -> float:
        return round(geodesic(fst_point, dst_point).miles, 2)
