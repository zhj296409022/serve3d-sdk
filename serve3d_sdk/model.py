from typing import Literal 
from .types import DATASOURCE, Descriptor


SCENE = Literal['small_object', 'human', 'scene']

METHOD = Literal['neus2', 'gaussian_splatting']


class ModelDescriptor(Descriptor): 
  """ 输出格式 """
  method: METHOD 
  """ 方法 """ 
  scene: SCENE 
  """ 场景 """ 

