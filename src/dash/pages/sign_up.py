import dash
from dash import html, get_relative_path, dcc,callback,Output,Input, no_update
import dash_bootstrap_components as dbc
from flask import flash
from src.models.models import User, db
from flask_login import login_user
from dash.exceptions import PreventUpdate
from werkzeug.security import generate_password_hash, check_password_hash

sing_up_layout = html.Div([
        dcc.Location(id='page_redirect_sign', refresh=True),
        dbc.Container([
            
            dbc.Row([
                dbc.Col(lg=3, md=2),
                dbc.Col([
                    dbc.Col(html.I(className='fa fa-key'),
                                    lg=12, class_name='login-key'),
                    dbc.Col('ADMIN PANEL',
                            class_name='login-title'),

                    dbc.Col([
                            dbc.Col([
                                html.Form([
                                    html.Div([
                                        html.Label('USERNAME' , className='form-control-label'),
                                        dcc.Input(id='username_input_sign', className='form-control', autoComplete="off")
                                    ],className='form-group'),
                                    html.Div([
                                        html.Label('PASSWORD',className='form-control-label'),
                                        dcc.Input(type='password', id='password_sign',className='form-control')
                                    ]),
                                    dbc.Col([
                                        dbc.Col([
                                        dcc.Loading( html.Button('SING UP', id='sign_up_button', type='button', className='btn btn-outline-primary'),)
                                        ], lg=12, class_name='login-btm login-button')
                                    ], lg=12, class_name='loginbttm')], autoComplete="off")
                                
                            ], lg=12, class_name='login-form')
                             
                        ],lg=12, class_name='login-form'),
                    
                    html.Div([
                        
                    ],id='mensagens_sign')
                    
                ],lg=6, md=8, class_name='login-box')
            ])   
            
        ], fluid=False)
])


@callback([Output('page_redirect_sign','pathname'),Output('mensagens_sign','children')],
          [Input('username_input_sign','value'),
              Input('password_sign','value'),
              Input('sign_up_button','n_clicks')])
def process_login(username,password,btn):
    if not btn:
        raise PreventUpdate

    if btn > 0 :
        if username and password:
            if User.query.filter_by(username=username).first():
                return no_update, html.Div([html.H3('Usuario ja cadastrado')])
            new_user = User(username=username,password=generate_password_hash(password, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user,remember=True)
            return get_relative_path('/login'), {}
        else:
            return no_update, html.Div([html.H3('Preencha todos os campos')])
