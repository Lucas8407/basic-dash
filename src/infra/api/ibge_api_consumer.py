import requests
from requests import Request
from typing import Type, Tuple, Dict
#from src.infra.api.http_request_error import HttpRequestError
from collections import namedtuple

class IbgeApiConsumer:
    '''Class to get municios id from ibge api'''
    
    def __init__(self) -> None:
        self.get_municipios_response = namedtuple('GET_municipios','status_code request response')
     
    def get_municipios(self,municipio_id: int) -> any:
        url = 'https://servicodados.ibge.gov.br/api/v1/localidades/municipios/{id}'
        url = url.format(id=municipio_id)
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print('Erro na solicitação:', response.status_code)