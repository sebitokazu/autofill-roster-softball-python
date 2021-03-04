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
token_map = {'authorization': token}
print("Bienvenido al cargador de Roster de Softbol\n")

# League selection

LEAGUES_PATH = '/leagues'
leagues_res = get(BASE_URL + LEAGUES_PATH, headers=token_map).json()
print('Ligas dispoinbles\n')
for idx, league in enumerate(leagues_res):
    print(idx, ')', league['name'], '\n')
league_idx = int(
    input('Ingrese el numero de liga correspondiente: '))
league = leagues_res[league_idx]
print('Liga:', league['name'])

# Tournament selection
league_path = '/league/'+league['id']
league_res = get(BASE_URL + league_path, headers=token_map).json()
tournaments = league_res['tournaments']
print('Torneos disponibles\n')
for idx, tournament in enumerate(tournaments):
    print(idx, ')', tournament['name'], '\n')
tournament_idx = int(input('Ingrese el numero de torneo correspondiente: '))
tournament = tournaments[tournament_idx]
print('Torneo:', tournament['name'])
