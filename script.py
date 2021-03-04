from getpass import getpass
import requests as rq
import pandas as pd

BASE_URL = 'https://api.avg300.com/api/v1'


def get(path, headers=None, data=None):
    return rq.get(BASE_URL+path, json=data, headers=headers)


def post(path, headers=None, data=None):
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
leagues_res = get(LEAGUES_PATH, headers=token_map).json()
print('Ligas dispoinbles\n')
for idx, league in enumerate(leagues_res):
    print(idx, ')', league['name'], '\n')
league_idx = int(
    input('Ingrese el numero de liga correspondiente: '))
league = leagues_res[league_idx]
print('Liga:', league['name'])

# Tournament selection
league_path = '/leagues/'+league['id']
league_res = get(league_path, headers=token_map).json()
tournaments = league_res['tournaments']
print('Torneos disponibles\n')
for idx, tournament in enumerate(tournaments):
    print(idx, ')', tournament['name'], '\n')
tournament_idx = int(input('Ingrese el numero de torneo correspondiente: '))
tournament = tournaments[tournament_idx]
print('Torneo:', tournament['name'])

# Team selection

teams_path = '/teams?league='+tournament['id']
teams_res = get(teams_path, headers=token_map).json()
print("Equipos\n")
for idx, team in enumerate(teams_res):
    print(idx, ')', team['name'], '\nManager:',
          team['manager'], '\nGrupo:', team['group_name'])
team_idx = int(input('Ingrese el numero de equipo:'))
team = teams_res[team_idx]
print("Equipo:", team['name'])

# Roster parsing and load

playerData = {
    'active': True,
    'bat_1b': 0,
    'bat_2b': 0,
    'bat_3b': 0,
    'bat_ab': 0,
    'bat_ab_risp': 0,
    'bat_avg': 0,
    'bat_avg_risp': 0,
    'bat_bb': 0,
    'bat_hbp': 0,
    'bat_hits': 0,
    'bat_hits_risp': 0,
    'bat_hr': 0,
    'bat_obpe': 0,
    'bat_ops': 0,
    'bat_pa': 0,
    'bat_rbi': 0,
    'bat_runs': 0,
    'bat_sb': 0,
    'bat_scb': 0,
    'bat_sf': 0,
    'bat_slg': 0,
    'fld_assists': 0,
    'fld_caught_stealing': 0,
    'fld_errors': 0,
    'fld_fielding_percentage': 0,
    'fld_games': 0,
    'fld_putouts': 0,
    'fld_steals_allowed': 0,
    'league': tournament['id'],
    'league_team': None,
    'pit_batting_average_against': 0,
    'pit_bf': 0,
    'pit_ci': 0,
    'pit_er': 0,
    'pit_era': 0,
    'pit_hit_batters': 0,
    'pit_hits': 0,
    'pit_ip': 0,
    'pit_k_per_innings': 0,
    'pit_loss': 0,
    'pit_order': 0,
    'pit_save': 0,
    'pit_scb': 0,
    'pit_scf': 0,
    'pit_strikeout_to_walk': 0,
    'pit_strikeouts': 0,
    'pit_walks': 0,
    'pit_whip': 0,
    'pit_win': 0,
    'player': None,
    'player_birthday': "",
    'player_first_name': "",
    'player_jersey': "",
    'player_last_name': "",
    'position': "0",
    'team': team['id']
}

filename = input(
    "Ingrese el nombre del archivo(sin la extension .xlsx) con el roster. Recuerde que debe estar en la misma ubicación que el programa\n")
filename += '.xlsx'
try:
    df = pd.read_excel(filename)
except FileNotFoundError as err:
    print("Archivo inexistente. Verifique el nombre y/o ubicacion")
    exit(1)

print(df)
