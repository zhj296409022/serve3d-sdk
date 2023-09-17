from typing import Literal, Dict, Optional 
from abc import abstractmethod 
import requests 
import json 


NOTIFY_TYPE = Literal['url'] 


class NotifyDescriptor: 
  """ 回调描述 """ 
  
  def __init__(self, notify: Optional[Dict] = None): 
    if notify is not None:
      self.from_json(notify)
  
  @abstractmethod 
  def from_json(self): pass 


class URLNotifyDescriptor: 
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


def create_notify(type: NOTIFY_TYPE, notify: Dict): 
  if type == 'url': 
    return URLNotifyDescriptor(notify) 

