from flask import Flask
from flask_login import current_user,logout_user
from dash import Dash, html, dcc, callback, Output, Input,strip_relative_path,get_relative_path
import dash_bootstrap_components as dbc
import dash
from src.dash.pages.home import home_layout
from src.dash.pages.login import login_layout
from src.dash.pages.logout import logout_layout
from src.dash.pages.sign_up import sing_up_layout
from importlib import import_module

dash_app = Dash(title='App Dash',
    suppress_callback_exceptions=True,
    prevent_initial_callbacks=True,
    serve_locally=True,
    assets_folder='assets',
    update_title='carregando...',
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ],
    url_base_pathname='/',
    use_pages=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    )



dash_app.layout = dbc.Container([
    dcc.Location(id='url', refresh=False),
    dcc.Location(id='redirect', refresh=True),
    dcc.Store(id='login-status', storage_type='session'),
    html.Div(id='user-status-div'),
    html.Br(),
    html.Hr(),
    html.Br(),
    html.Div(id='page-content')],
)

@callback(
        Output('page-content', 'children'), 
        Output('redirect', 'pathname'),
        [Input('url', 'pathname')])
def display_page(pathname):
    ''' callback to determine layout to return '''
    view = None
    url = dash.no_update
    if pathname == '/login':
        view = login_layout
    elif pathname == '/signup':
        view = sing_up_layout
    elif pathname == '/':
        if current_user.is_authenticated:
            view = home_layout
        else:
            view = 'Redirecting to login...'
            url = '/login'
    elif pathname == '/logout':
        if current_user.is_authenticated:
            logout_user()
            view = logout_layout
        else:
            view = login_layout
            url = '/login'

    return view, url

def init_app(app: Flask):
    dash_app.init_app(app)
    
    