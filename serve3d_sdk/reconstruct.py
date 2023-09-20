from .types import FEATURE_TYPE, FEATURE_MATCH_TYPE, RETRIEVAL_TYPE, \
  DEFAULT_CONFIG, DATA_DIR, Descriptor 
from typing import Literal, Dict, Optional 
from pathlib import Path 
import json 

METHOD = Literal['monocular', 'monocular+depth', 'monocular+inertial'] 

SCENE = Literal['indoor', 'outdoor'] 


class MonocularMethodConfig: 
  retrieval: RETRIEVAL_TYPE 
  """ 检索算法, 暂时不要填 """ 
  feature: FEATURE_TYPE 
  """ 特征提取算法 """ 
  feature_match: FEATURE_MATCH_TYPE 
  """ 特征匹配算法 """
  keyframe_min_match_num: int = 100 
  """  """ 
  keyframe_min_match_score: float = 0.4 
  """  """ 
  keyframe_max_skip_num: int = 4 
  """ 最大未选择跳过帧数 """ 
  min_match_count: int = 30 
  """ 最少匹配点数 """ 


class ReconstructDescriptor(Descriptor): 
  method: METHOD 
  """ 构建方法 """ 
  scene: SCENE 
  """ 构建场景 """ 


class BuildReconstructDescriptor(ReconstructDescriptor): 
  """ 构建描述符 """ 
  def __init__(self, id: str, root: str=DATA_DIR): 
    super().__init__() 
    self.id = id 
    self.root = Path(root) 
    
  @property 
  def tmp_path(self): 
    return self.root.joinpath('tmp') 
    
  @property 
  def cache_path(self): 
    return self.root.joinpath(self.id, 'manifest.json') 
  
  @property 
  def root_dir(self): 
    return self.root.joinpath(self.id, 'mapping') 
  
  @property 
  def scene_dir(self): 
    return self.root.joinpath(self.id) 

  def cache(self): 
    cache = {} 
    
    for key, value in self.__dict__.values(): 
      if not isinstance(key, str): 
        cache[key] = str(value) 
      else: 
        cache[key] = value 
    
    s = json.dumps(cache) 
    with open(self.cache_path, 'w', encoding='utf8') as f: 
      f.write(s) 
  
  def from_json(self, json: Dict): 
    self.__dict__.update(json) 
    self.root_dir = Path(self.root_dir) 

  @staticmethod 
  def load(path: Path): 
    if not path.exists(): return None 
    
    with open(str(path), 'r', encoding='utf8') as f: s = f.read() 

    descriptor = ReconstructDescriptor('') 
    descriptor.from_json(json.loads(s)) 

    return descriptor 


def create_descriptor(json: Dict, root_dir: str): 
  """ 创建构建描述 """ 
  descriptor = ReconstructDescriptor('', root_dir) 
  descriptor.from_json(json) 
  
  for key in ['id', 'source', 'usage']: 
    if not hasattr(descriptor, key): 
      raise Exception(f'{key} must not be empty!') 
  
  return descriptor 

def create_config(json: Optional[Dict]):
  json = {**DEFAULT_CONFIG, **(json or {})} 
  
  config = MonocularMethodConfig()
  config.__dict__.update(json)
  
  return config

