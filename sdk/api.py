from .reconstruct import ReconstructDescriptor 
from requests import Response, exceptions 
from .notify import NotifyDescriptor 
from .model import ModelDescriptor 
from .types import DATASOURCE 
from typing import Optional 
import requests 


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
  
  def mapping(self, 
              descriptor: ReconstructDescriptor, 
              notify: NotifyDescriptor, 
              download_url: str,
              upload_url: str,
              **args): 
    """ 建图 """ 
    response: Response = requests.post( 
      url=self.prepare_url('/api/v1/mapping/', args.get('base_url')), 
      headers={ 'Content-Type': 'application/json' }, 
      json = { 
        descriptor, 
        notify, 
        download_url,
        upload_url,
      } 
    ) 
    
    if response.status_code != 200: 
      raise exceptions.HTTPError(response=response) 
  
    return response.json() 
  
  def localize(self, scene_id: str, image, camera, **args): 
    """ 定位 """ 
    response: Response = requests.post( 
      url=self.prepare_url('/api/v1/localize/', args.get('base_url')), 
      files={ 'file': image }, 
      json = { 
        scene_id, 
        camera 
      } 
    ) 
    
    if response.status_code != 200: 
      raise exceptions.HTTPError(response=response) 
    
    return response.json() 
  
  def model(self, 
            descriptor: ModelDescriptor, 
            notify: NotifyDescriptor, 
            download_url: str, 
            upload_url: str, 
            **args): 
    """ 建模 """
    response: Response = requests.post(
      url=self.prepare_url('/api/v1/model/', args.get('base_url')),
      headers={ 'Content-Type': 'application/json' },
      json = {
        descriptor,
        notify,
        download_url,
        upload_url
      }
    )
    
    if response.status_code != 200:
      raise exceptions.HTTPError(response=response)
    
    return response.json()

