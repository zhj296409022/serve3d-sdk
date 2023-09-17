from .reconstruct import DATASOURCE_DIR
from .types import DATASOURCE
from pathlib import Path 
import json 

class Datasource: 
  def __init__(self, dir: str=DATASOURCE_DIR): 
    self.root_dir = Path(dir)
    
  def ensure(self, path: Path, is_dir: bool = False): 
    """ 保证创建不出错 """ 
    if is_dir: 
      if not path.exists(): 
        path.mkdir(parents=True, exist_ok=True) 
    else: 
      if not path.parent.exists(): 
        path.parent.mkdir(parents=True, exist_ok=True) 

    return path


class VideoDatasource(Datasource):
  
  type: DATASOURCE = 'video'
  
  @property
  def video_path(self):
    return self.root_dir.joinpath('video.mp4')
  
  @property
  def camera_intrinsics_path(self):
    return self.root_dir.joinpath('intrinsics.json')
  
  @property
  def transform_path(self):
    return self.root_dir.joinpath('transforms.json')

  def read_camera_intrinsics(self):
    return json.loads(self.camera_intrinsics_path) 
  
  def read_transform(self):
    return json.loads(self.transform_path) 


class MappingDatasource(Datasource):
  
  @property 
  def images_dir(self): 
    return self.ensure(self.root_dir.joinpath('images'), is_dir=True)

  @property
  def dir(self):
    return self.ensure(self.root_dir.joinpath('mapping'), is_dir=True)
  

class COLMAPSparseMappingDatasource(MappingDatasource):
  
  type: DATASOURCE = 'colmap_sparse'
  
  @property 
  def db_path(self): 
    return self.dir.joinpath('database.sqlite3') 
  
  @property
  def sfm_pair_path(self):
    return self.dir.joinpath('sfm_pair.txt') 
  
  @property 
  def sfm_dir(self): 
    return self.ensure(self.dir.joinpath('sparse', '0'), is_dir=True)


class NERFModelDatasource(Datasource):
  
  type: DATASOURCE = 'nerf'
  
  @property
  def dir(self):
    return self.ensure(self.root_dir.joinpath('model')) 
  
  @property
  def images_dir(self): 
    return self.dir.joinpath('images') 
  
  @property 
  def transforms_path(self): 
    return self.dir.joinpath('transforms.json') 
  

def create_datasource(type: DATASOURCE, dir: str):
  if type == 'video':
    return VideoDatasource(dir)
  elif type == 'colmap':
    return COLMAPSparseMappingDatasource(dir)
  elif type == 'nerf':
    return NERFModelDatasource(dir)
  else:
    raise Exception(f'do not support datasource type: {type}')

