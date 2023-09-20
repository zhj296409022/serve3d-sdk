from .reconstruct import ReconstructDescriptor, MonocularMethodConfig 
from requests import Response, exceptions 
from .notify import Notify 
from .model import ModelDescriptor 
from typing import Optional, Dict 
from .types import DATASOURCE 
import requests 


class _Request: 
  upload_url: Optional[str] 
  """ 完成后的上传 """ 
  
  download_url: Optional[str] 
  """ 处理前下载数据源 """ 
  
  def parse(self, json: Dict): 
    self.upload_url = json.get('upload_url', None) 
    self.download_url = json.get('download_url', None) 

  def to_dict(self): 
    return self.__dict__ 


class ReconstructionRequest(_Request): 

  descriptor: ReconstructDescriptor 
  
  notify: Notify 
  
  config: Optional[MonocularMethodConfig] 

  def parse(self, json: Dict): 
    super().parse(json)
    
    self.descriptor = ReconstructDescriptor() 
    self.descriptor.from_json(json['descriptor']) 
    self.notify = Notify(json['notify']) 

    return self 

  def to_dict(self): 
    ret = super().to_dict()
    ret['descriptor'] = self.descriptor.to_json() 
    ret['notify'] = self.notify.to_json() 
    return ret 


class ModelRequest(_Request): 

  descriptor: ModelDescriptor 
  
  def parse(self, json: Dict): 
    super().parse(json)
    self.descriptor = ModelDescriptor()
    self.descriptor.from_json(json['descriptor'])
  
  def to_dict(self):
    ret = super().to_dict(self)
    ret['descriptor'] = self.descriptor.to_json() 
    
    return ret


class Client: 
  def __init__(self, base_url: Optional[str] = None): 
    self.base_url = base_url 
    
  def prepare_url(self, url: str, base_url: str): 
    if base_url is not None: 
      return f'{base_url}{url}' 
    elif self.base_url is not None: 
      return f'{self.base_url}{url}' 
    else: 
      raise Exception('base_url is None') 
    
  def get_download_url(self, scene_id: str, type: DATASOURCE, **args): 
    """ 获取下载链接 """
    response: Response = requests.get( 
      url = self.prepare_url(f'/api/v1/scene/{scene_id}/download/', args.get('base_url')),
      headers={ 'Content-Type': 'application/json' }, 
      json = { 
        scene_id, 
        type 
      } 
    ) 
    
    if response.status_code != 200: 
      raise exceptions.HTTPError(response=response) 
  
    return response.json() 

  def get_upload_url(self, scene_id: str, type: DATASOURCE, **args):
    """ 获取上传链接 """ 
    response: Response = requests.get(
      url = self.prepare_url(f'/api/v1/scene/{scene_id}/upload/', args.get('base_url')), 
      headers={ 'Content-Type': 'application/json' }, 
      json = {
        scene_id, 
        type 
      } 
    ) 
    
    if response.status_code != 200: 
      raise exceptions.HTTPError(response=response) 

    return response.json() 

  def mapping(self, request: ReconstructionRequest, **args): 
    """ 建图 """ 
    response: Response = requests.post( 
      url=self.prepare_url('/api/v1/mapping/', args.get('base_url')), 
      headers={ 
               'Content-Type': 'application/json',
               'method': 'mapping'
      }, 
      json = request.to_dict() 
    ) 
    
    if response.status_code != 200: 
      raise exceptions.HTTPError(response=response) 
  
    return response.json() 
  
  def model(self, request: ModelRequest, **args): 
    """ 建模 """ 
    response: Response = requests.post( 
      url=self.prepare_url('/api/v1/model/', args.get('base_url')), 
      headers={ 
               'Content-Type': 'application/json',
               'method': 'model'
      }, 
      json = request.to_dict() 
    ) 
    
    if response.status_code != 200: 
      raise exceptions.HTTPError(response=response) 

    return response.json() 

  def localize(self, data: Dict, image, **args): 
    """ 定位 """ 
    response: Response = requests.post( 
      url=self.prepare_url('/api/v1/localize/', args.get('base_url')), 
      headers={
        'method': 'localize'
      },
      files={ 'file': image }, 
      json = data 
    ) 
    
    if response.status_code != 200: 
      raise exceptions.HTTPError(response=response) 

    return response.json() 

