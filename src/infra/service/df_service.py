import pandas as pd
import sys
import os
projeto_dir = os.path.abspath('..')
sys.path.append(projeto_dir)

from src.infra.api.ibge_api_consumer import IbgeApiConsumer
from src.infra.config.bussines_rules import SEGMENTOS , CANAIS

df = pd.DataFrame()

initial_path = 'src/infra/service/'

arquivos =[f'{initial_path}dt1.csv',f'{initial_path}dt2.csv',f'{initial_path}dt3.csv',f'{initial_path}dt4.csv']


for csv in arquivos:
    df1 = pd.read_csv(csv,sep=';')
    df = pd.concat([df,df1],axis=0)


def create_collumn_cidade():
    lista_municipios_df = list(df['municipio-id'].unique())
    api = IbgeApiConsumer()
    municipio_id_name = {}

    for municipio in lista_municipios_df:
        result = api.get_municipios(municipio)
        municipio_id_name[str(municipio)] = result['nome']
        
    def get_name_municipio(id):
        name = municipio_id_name[str(id)]
        return name

    df['cidade'] = df['municipio-id'].apply(get_name_municipio)
    return df

def get_name_by_identificador(id:str or int,identificador:dict):
    for tupla in identificador.items():
        if(id in tupla[1]):
            return tupla[0]
    return 'OUTROS' 

 ## caso nao houvesse esse retorno 'OUTROS' poderia ser tratado depois dessa forma df['segmento'].fillna('OUTROS',inplace=True)

def create_collumn_segmento():
    def get_name_segmento(id_cnae):
        return get_name_by_identificador(id_cnae,SEGMENTOS)
            
    df['segmento'] = df['cnae_principal'].apply(get_name_segmento)
    return df
  
def create_collumn_canal():
    def get_name_canal(segmento):
        return get_name_by_identificador(segmento,CANAIS)

    df['canal'] = df['segmento'].apply(get_name_canal)
    return df

def update_dataframe():
    create_collumn_cidade()
    create_collumn_segmento()
    create_collumn_canal()
    
    
def get_df():
    update_dataframe()
    return df