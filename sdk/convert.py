from datasource import Datasource, COLMAPSparseMappingDatasource 
from typing import Dict 

def colmap2nerf(input: COLMAPSparseMappingDatasource): 
  """ colmap格式转nerf """ 
  pass 

def convert(input_format: Datasource, output_format: Datasource, input: Datasource): 
  key = f'{input_format}_{output_format}' 
  fn = converters.get(key) 
  
  if fn is None: 
    raise Exception(f'can not convert from {input_format} to {output_format}') 
  
  return fn(input) 

converters: Dict[str, callable] = { 
  'colmap_nerf': colmap2nerf 
} 

