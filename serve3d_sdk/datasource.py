from .types import DATASOURCE, DATA_DIR 
from typing import Dict 
from pathlib import Path 
import requests 
import zipfile 
import shutil 
import json 
import os 


class Datasource: 
  
  type: DATASOURCE = None
  
  def __init__(self, id: str, dir: str=DATA_DIR): 
    self.root_dir = Path(dir).joinpath(id, 'dataset') 
    
    if not self.root_dir.exists(): 
      self.root_dir.mkdir(parents=True, exist_ok=True) 

  def ensure(self, path: Path, is_dir: bool = False): 
    """ 保证创建不出错 """ 
    if is_dir: 
      if not path.exists(): 
        path.mkdir(parents=True, exist_ok=True) 
    else: 
      if not path.parent.exists(): 
        path.parent.mkdir(parents=True, exist_ok=True)  

    return path 
  
  def exists(self):
    return self.root_dir.exists()
  

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
  def sparse_dir(self): 
    return self.ensure(self.dir.joinpath('sparse'), is_dir=True) 

  @property 
  def sfm_dir(self): 
    return self.ensure(self.dir.joinpath('sparse', '0'), is_dir=True) 
  
  @property
  def db_path(self):
    return self.root_dir.joinpath("database.sqlite3")

  @property
  def pointcloud_path(self):
    return self.sfm_dir.joinpath('points.bin')


class BuildCOLMAPSparseMappingDatasource(MappingDatasource): 
  
  type: str = 'build_colmap_sparse'
  
  @property 
  def db_path(self): 
    return self.dir.joinpath('database.sqlite3') 
  
  @property 
  def sfm_pair_path(self): 
    return self.dir.joinpath('sfm_pair.txt') 


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


def zip_file(path: Path, output: Path): 
  with zipfile.ZipFile(output, 'w') as zip: 
    if not path.is_dir(): 
      zip.write(filename=str(path), arcname=path.name) 
    else: 
      for folder_name, sub_folders, files in os.walk(str(path)): 
        for item in files: 
          filename = os.path.join(folder_name, item) 
          zip.write(filename=filename, arcname=Path(filename).name) 

def upload_datasource(url: str, dir: Path, tmp_path: Path): 
  """ 上传数据源 """ 
  zip_file(dir, tmp_path) 
  with open(tmp_path, 'rb') as f: 
    response = requests.post(url = url, files = { 'file': f }) 
    shutil.rmtree(tmp_path) 
    if response.status_code != 200: 
      raise Exception('upload failed: ' + response.reason) 

def download_datasource(url: str, dir: Path): 
  """ 下载zip到本地 """ 
  response = requests.get(url, stream=True) 

  if not dir.exists(): dir.mkdir(parents=True, exist_ok=True) 

  with zipfile.ZipFile(response.content) as zipFile: 
    zipFile.extractall(dir) 

def open_datasource(id: str, dir: str=DATA_DIR): 
  """ 创建数据源 """ 
  with open(Path(dir).joinpath(id, 'dataset', 'manifest.json'), 'r', encoding='utf8') as fd: 
    s = fd.read() 
  manifest: Dict = json.loads(s) 
  type: DATASOURCE = manifest.get(type) 
  
  return find_datasource(type, id, dir) 

def find_datasource(type: DATASOURCE, id: str, dir: str=DATA_DIR): 
  if type == 'video': 
    return VideoDatasource(id, dir) 
  elif type == 'colmap': 
    return COLMAPSparseMappingDatasource(id, dir) 
  elif type == 'nerf': 
    return NERFModelDatasource(id, dir) 
  else: 
    raise Exception(f'do not support datasource type: {type}') 

