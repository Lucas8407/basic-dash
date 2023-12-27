import dash
from dash import html,get_relative_path
from dash.exceptions import PreventUpdate
from flask_login import login_required
from dash import html, get_relative_path, dcc,callback,Output,Input, no_update,State
import dash_bootstrap_components as dbc
from src.infra.service.questions import Questions
import plotly.express as px
import pandas as pd
import openpyxl
    
questions = Questions()

lista_cidade = list(questions._df['cidade'].unique())
lista_segmento = list(questions._df['segmento'].unique())

home_layout = html.Div([
        dcc.Location(id='redirect_logout', refresh=True),
        html.H1('Análise de empresas'),
        dbc.Container([
            
            dbc.Row([
                dbc.Col([
                     dbc.Accordion([
                        dbc.AccordionItem([ ## item 1
                            dbc.Row([
                                dbc.Col([
                                    html.P("Selecione o Canal"),
                                    dcc.Dropdown(
                                    id='slct_canal',
                                    options=[
                                        {"label":"Especializado","value":"Especializado"},
                                        {"label":"Autoserviço","value":"Autoserviço"},
                                        {"label":"Distribuidor","value":"Distribuidor"},
                                        {"label":"Outros","value":"Outros"}],
                                        multi=False,
                                        value='Especializado',
                                        style={'width': '100%','border-radius':'8px'})
                                ]),
                                dbc.Col([
                                    html.P("Selecione o Municipio"),
                                    dcc.Dropdown(
                                    id='slct_cidade',
                                    options=[ {'label': cidade, 'value': cidade} for cidade in lista_cidade],
                                    multi=False,
                                    value='Garibaldi',
                                    style={'width': '100%','border-radius':'8px'})
                                ]),
                                
                            ]),
                            
                            dbc.Row([
                                dbc.Col([
                                        
                                ],id='conteudo_q1'),
                         
                            ],className='mt-3')
                        ],title="Quantas empresas são especialistas na minha região ?"),
                        ## item 2 --------------------------------------------------
                        dbc.AccordionItem([
                            dbc.Row([
                                
                            ],id='maior_cidade'),
                            dbc.Row([
                                dbc.Col([
                                   
                                ],id='conteudo_q2'),
                                dbc.Col([
                                    dcc.Graph(id='bairro_bar', figure={})
                                ],id='grafico_q2')
                            ]),   
                        ],title="Qual a cidade possui mais estabelecimento no segmento Pet Shop, e qual a quantidade por bairro",item_id='q2'),
                        
                        dbc.AccordionItem([
                            dbc.Row([
                                dbc.Col([
                                    
                                ],id='conteudo_q3')
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    dcc.Graph(id='hipermercado_pie', figure={})
                                ])
                            ])
                        ], title='Existem Hipermercados na minha região, quantos, quais são as cidades?',item_id='q3'),
                        dbc.AccordionItem([
                            dbc.Row([
                                dbc.Col([
                                    dbc.Button('Gerar Excel',id='btn_xlsx'),
                                    dcc.Download(id="download-dataframe-xlsx"),
                                ],id='conteudo_q4')
                            ]),
                        ], title='Posso gerar Excel das informações?',item_id='q4')
                    ],start_collapsed=True, id='accordion'),
                   
                ])
                
            ]),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    dbc.Button('Sair', id='logout')
                ])
            ])
            
        ])
    ])

@callback(
    [Output("conteudo_q1", "children")], 
    [Input("slct_canal", "value"),
     Input("slct_cidade", "value")]
)
def empresas_by_canal(canal,cidade):
    df = questions.empresas_canal_by_cidade(str(canal).upper(),str(cidade))
    quantidade = df.shape[0]
    
    return [html.H5(f'Existem um total de {quantidade} empresas com o canal {canal} para a cidade de {cidade}')]


@callback(
    [Output("conteudo_q2", "children"),Output('bairro_bar','figure'),Output('maior_cidade','children')], 
    [Input("accordion", "active_item"),]
)
def cidade_segmento_by_bairro(item):
    if item:
        df = questions.cidade_segmento_by_bairro()[0]
        cidade = questions.cidade_segmento_by_bairro()[1]   
        fig = px.bar(
            data_frame=df,
            x='count',
            y='bairro',
            hover_data=['count', 'bairro'],
            labels={'Bairros:'},
        )

        table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
        return [table] , fig , [html.H5(f'A cidade com mais estabelecimentos de PetShop é {cidade}')]
    raise PreventUpdate

@callback(
    [Output("conteudo_q3", "children"),Output('hipermercado_pie','figure')], 
    [Input("accordion", "active_item")]
)
def hipermercado_by_regiao(item):
    if item:
        df = questions.hipermercados_regiao('RS') ## estado fixo pois não há outros estados no data frame poderia ser feito um select se fosse o caso
        if df.empty:
            return  [html.H5(f'Não existem hipermercados para a região do estado de Rio Grande do Sul')], {}
        else:
            df.groupby('segmento')['estado-sigla'].count()
            fig = px.pie(
                    data_frame=questions._df,  
                    color='segmento', 
                    names='segmento',  
                    title='Distribuição do total de Segmentos dos municípios atentdidos',
            )
            count = df.shape[0]
            cidades_hiper = list(df['cidade'].unique())
            return [html.H5(f'Existem um total de {count} hipermercados para as cidades {cidades_hiper} no estado de Rio Grande do Sul')], fig
    raise PreventUpdate


@callback(
    Output("download-dataframe-xlsx", "data"),
    Input("btn_xlsx", "n_clicks"),
    prevent_initial_call=True,
)
def gerar_excel(btn):
    if btn and btn > 0:
        return dcc.send_data_frame(questions._df.to_excel, "analise-empresas.xlsx", sheet_name="analise-empresas")
    raise PreventUpdate

@callback(
    Output("redirect_logout", "pathname"),
    Input("logout", "n_clicks"),
    prevent_initial_call=True,
)
def sair(btn):
    if btn and btn > 0:
         return get_relative_path('/logout')
    raise PreventUpdate