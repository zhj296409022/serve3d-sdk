from typing import Literal, Dict, Optional 
from abc import abstractmethod 
import requests 
import json 


NOTIFY_TYPE = Literal['url'] 


class Notify: 
  """ 回调描述 """ 
  
  def __init__(self, notify: Optional[Dict] = None):  
    if notify is not None: 
      self.from_json(notify) 
  
  @abstractmethod 
  def notify(self, data: Dict): pass 
  
  @abstractmethod 
  def from_json(self): pass 
  
  def to_json(self):
    return self.__dict__


class URLNotify: 
  """ 回调 """ 

  url: str 
  """ 回调目标 """ 

  def notify(self, data: Dict): 
    url = self.url 
    
    response = requests.post(url, headers={ 
      "Content-Type": "Application/json" 
    }, json=json.dumps(data)) 
    
    if response.status_code != 200:
      return { 
        'code': response.status_code, 
        'msg': response.text 
      } 
    
    return { 'code': 200 } 
  
  def from_json(self, notify: Dict): 
    self.url = notify['url'] 


def create_notify(notify: Dict): 
  type = notify.get('type')
  
  if type == 'url': 
    return URLNotify(notify) 
  else:
    raise Exception(f'do not support notify type: {type} ')

