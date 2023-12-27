from src.infra.service.df_service import get_df
import pandas as pd
from dash import dcc

class Questions():
    
    def __init__(self) -> None:
        self._df = get_df() ##n fiz get pro df da classe, to chamando direto
    
    def empresas_canal_by_cidade(self,canal:str, cidade: str) -> pd.DataFrame:
        df_empresas_espec_by_regiao = self._df.loc[(self._df['canal'] == canal) & (self._df['cidade'] == cidade)]
        return df_empresas_espec_by_regiao

    def cidade_segmento_by_bairro(self) -> (pd.DataFrame, str):
        df_pet_shop = self._df.loc[(self._df['segmento'] == 'PET SHOP')]
        cidade_mais_estabelecimentos  = df_pet_shop['cidade'].value_counts().idxmax()
        df_cidade = df_pet_shop[df_pet_shop['cidade'] == cidade_mais_estabelecimentos]
        bairros_contagem = df_cidade['bairro'].value_counts().reset_index()
        return bairros_contagem , cidade_mais_estabelecimentos
    
    def hipermercados_regiao(self, estado):
        df_hipermercado = self._df.loc[(self._df['segmento'] == 'HIPERMERCADO') & (self._df['estado-sigla'] == estado)]
        return df_hipermercado
    
