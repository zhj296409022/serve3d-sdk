from typing import Dict, Literal

DATA_DIR = '/tmp/serve3d' 
""" 临时构建根目录 """ 

DATASOURCE = Literal['video', 'colmap_sparse', 'nerf'] 

RETRIEVAL_TYPE = Literal['cosplace', 'netvlad'] 

FEATURE_TYPE = Literal['disk'] 

FEATURE_MATCH_TYPE = Literal['disk+lightglue'] 

RETRIEVAL_DIMS: Dict[RETRIEVAL_TYPE, int] = { 
  'cosplace': 2048, 
  'netvlad': 4096 
} 

EXTRACTORS = {
  'superpoint_aachen': {
    'model': {
      'name': 'superpoint',
      'nms_radius': 3,
      'max_keypoints': 4096,
    },
    'preprocessing': {
      'grayscale': True,
      'resize_max': 1024,
    },
  },
  'superpoint_max': {
    'model': {
      'name': 'superpoint',
      'nms_radius': 3,
      'max_keypoints': 4096,
    },
    'preprocessing': {
      'grayscale': True,
      'resize_max': 1600,
      'resize_force': True,
    },
  },
  'superpoint_inloc': {
    'model': {
      'name': 'superpoint',
      'nms_radius': 4,
      'max_keypoints': 4096,
    },
    'preprocessing': {
      'grayscale': True,
      'resize_max': 1600,
    },
  },
  'r2d2': {
    'model': {
      'name': 'r2d2',
      'max_keypoints': 5000,
    },
    'preprocessing': {
      'grayscale': False,
      'resize_max': 1024,
    },
  },
  'd2net-ss': {
    'model': {
      'name': 'd2net',
      'multiscale': False,
    },
    'preprocessing': {
      'grayscale': False,
      'resize_max': 1600,
    },
  },
  'sift': {
    'model': {
      'name': 'dog'
    },
    'preprocessing': {
      'grayscale': True,
      'resize_max': 1600,
    },
  },
  'sosnet': {
    'model': {
      'name': 'dog',
      'descriptor': 'sosnet'
    },
    'preprocessing': {
      'grayscale': True,
      'resize_max': 1600,
    },
  },
  'disk': {
    'model': {
        'name': 'disk',
        'max_keypoints': 5000,
    },
    'preprocessing': {
        'grayscale': False,
        'resize_max': 1600,
    },
  }
}

RETRIEVALS = {
  'dir': {
    'model': {'name': 'dir'},
    'preprocessing': {'resize_max': 1024},
  },
  'netvlad': {
    'model': {'name': 'netvlad'},
    'preprocessing': {'resize_max': 1024},
  },
  'openibl': {
    'model': {'name': 'openibl'},
    'preprocessing': {'resize_max': 1024},
  },
  'cosplace': {
    'model': {'name': 'cosplace'},
    'preprocessing': {'resize_max': 1024},
  }
}

MATCHES = {
  'superpoint+lightglue': {
    'model': {
      'name': 'lightglue',
      'features': 'superpoint',
    },
  },
  'disk+lightglue': {
    'model': {
      'name': 'lightglue',
      'features': 'disk',
    },
  },
  'superglue': {
    'model': {
      'name': 'superglue',
      'weights': 'outdoor',
      'sinkhorn_iterations': 50,
    },
  },
  'superglue-fast': {
    'model': {
      'name': 'superglue',
      'weights': 'outdoor',
      'sinkhorn_iterations': 5,
    },
  },
  'NN-superpoint': {
    'model': {
      'name': 'nearest_neighbor',
      'do_mutual_check': True,
      'distance_threshold': 0.7,
    },
  },
  'NN-ratio': {
    'model': {
      'name': 'nearest_neighbor',
      'do_mutual_check': True,
      'ratio_threshold': 0.8,
    }
  },
  'NN-mutual': {
    'model': {
      'name': 'nearest_neighbor',
      'do_mutual_check': True,
    },
  },
  'adalam': {
    'model': {
      'name': 'adalam'
    },
  }
}

DEFAULT_CONFIG = {
  'feature': EXTRACTORS['disk'],
  'feature_match': MATCHES['disk+lightglue'],
  'retrieval': RETRIEVALS['netvlad']
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

