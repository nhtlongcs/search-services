from typing import Generic, TypeVar

import numpy as np
from pydantic import BaseModel, validator

T = TypeVar('T')

class NumpyArrayModel(BaseModel, Generic[T]):
    data: list[T]
    shape: list[int]

    @classmethod
    def from_numpy(cls, arr: np.ndarray):
        data = arr.flatten().tolist()
        shape = arr.shape
        return cls(data=data, shape=shape)
    
class FeatureModel(BaseModel):
    feature: NumpyArrayModel[float]
    
    @classmethod
    def from_numpy(cls, arr: np.ndarray):
        return cls(feature=NumpyArrayModel.from_numpy(arr))
    