from getpass import getpass
import requests as rq

BASE_URL = 'https://api.avg300.com/api/v1'


def get(path, headers={}, data={}):
    return rq.get(BASE_URL+path, json=data, headers=headers)


def post(path, headers={}, data={}):
    return rq.post(BASE_URL+path, json=data, headers=headers)

# Login


username = input("Usuario o mail:\n")
password = getpass(prompt="Contraseña:\n")

LOGIN_PATH = '/auth/login/'
login_data = {
    'username': username,
    'password': password
}
login_res = post(LOGIN_PATH, data=login_data).json()

if 'token' not in login_res:
    print('Usuario o contraseña invalidos')
    exit(1)

token = 'Token ' + login_res['token']
print("Bienvenido al cargador de Roster de Softbol\n")
