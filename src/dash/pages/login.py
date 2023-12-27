import dash
from dash import html, get_relative_path, dcc,callback,Output,Input, no_update,State
import dash_bootstrap_components as dbc
from flask import flash
from src.models.models import User, db
from flask_login import login_user
from dash.exceptions import PreventUpdate
from werkzeug.security import generate_password_hash, check_password_hash


login_layout = dbc.Container([
    dcc.Location(id='url',  pathname='/login', refresh=True),
    dcc.Location(id='redirect_sign_up', refresh=True),
    dbc.Row([
        dbc.Col(lg=3, md=2),
        dbc.Col([
            html.H2('ADMIN PANEL', className='display-4 text-center mt-4 mb-4 text-primary'),
            dbc.Col([
                html.Form([
                    dbc.CardGroup([
                        dbc.Label('Username', className='form-control-label h5'),
                        dbc.Input(id='username_input', type='text', className='form-control', autoComplete="off"),
                    ]),
                    dbc.CardGroup([
                        dbc.Label('Password', className='form-control-label h5'),
                        dbc.Input(id='password_input', type='password', className='form-control'),
                    ]),
                    dbc.Col([
                        dbc.Button('Login', id='login_button', type='button', className='btn btn-primary mt-3 btn-block'),
                    ], lg=12, class_name='login-btm login-button')
                ])
            ], lg=12, class_name='login-form'),
            html.Div([
                dbc.Button("Don't have an account? Sign up here", id='sign_up_redirect', type='button', className='btn btn-link mt-3')
            ]),
            html.Div(id='mensagens', className='text-danger mt-3')
        ], lg=6, md=8, class_name='login-box text-center')
    ])
], fluid=True)


@callback([Output('redirect_sign_up','pathname')],
           Input('sign_up_redirect','n_clicks'))
def redirect_to_sing_up(btn):
    if btn and btn > 0:
        return [get_relative_path('/signup')]
    raise PreventUpdate

@callback([Output('url','pathname'),Output('mensagens','children')],
          [State('username_input', 'value'),
           State('password_input', 'value')],
              Input('login_button','n_clicks'))
def process_login(username,password,btn):
    if not btn:
        raise PreventUpdate

    if btn > 0 :
        if username and password:
            user = User.query.filter_by(username=username).first()
            if user:
                if check_password_hash(user.password,password):
                    login_user(user,remember=True) ## remember this user is logged in
                    return get_relative_path('/'), [{}]
                else:
                    return no_update, html.Div([html.H3('Senha incorreta')])
            else:
                return no_update, html.Div([html.H3('Usuario Nao encontrado')])
                    
        else:
            return no_update, html.Div([html.H3('Preecha todos os campos obrigatórios')])
