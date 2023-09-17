from typing import Dict, Literal

DATASOURCE = Literal['video', 'colmap_sparse', 'nerf'] 

RETRIEVAL_TYPE = Literal['cosplace', 'netvlad'] 

FEATURE_TYPE = Literal['disk'] 

FEATURE_MATCH_TYPE = Literal['disk+lightglue'] 

RETRIEVAL_DIMS: Dict[RETRIEVAL_TYPE, int] = { 
  'cosplace': 2048, 
  'netvlad': 4096 
} 

DEFAULT_CONFIG = {
  'feature': {
    'name': 'disk',
    'model': {
        'name': 'disk',
        'max_keypoints': 5000,
    },
    'preprocessing': {
        'grayscale': False,
        'resize_max': 1600,
    },
  },
  'feature_match': {
    'name': 'disk+lightglue',
    'model': {
        'name': 'lightglue',
        'features': 'disk',
    },
  },
  'retrieval': {
    'name': 'netvlad',
    'model': {'name': 'netvlad'},
    'preprocessing': {'resize_max': 1024},
  }
}

class JsonDescriptor:
  
  def to_json(self):
    return self.__dict__

  def from_json(self, json: Dict):
    self.__dict__.update(json)


class Descriptor(JsonDescriptor):
  """ 构建描述 """
  id: str
  """ 全局唯一id """
  input: DATASOURCE
  """ 输入格式 """
  output: DATASOURCE
  """ 输出格式 """