import requests
from rauth import OAuth2Service
import os
from dotenv import load_dotenv
import hashlib
import sys
import json
import datetime

load_dotenv('.env')

if sys.version_info[0] == 3:
    raw_input = input

client_id = os.getenv('WAKATIME_CLIENT_ID')
client_secret = os.getenv('WAKATIME_CLIENT_SECRET')

service = OAuth2Service(
    client_id=client_id,
    client_secret=client_secret,
    name='wakatime',
    authorize_url='https://wakatime.com/oauth/authorize',
    access_token_url='https://wakatime.com/oauth/token',
    base_url='https://wakatime.com/api/v1/')


redirect_uri = 'https://wakatime.com/oauth/test'
state = hashlib.sha1(os.urandom(40)).hexdigest()
params = {'scope': 'email,read_stats,read_logged_time',
          'response_type': 'code',
          'state': state,
          'redirect_uri': redirect_uri}

url = service.get_authorize_url(**params)

print('**** Visit this url in your browser ****'.format(url=url))
print('*' * 80)
print(url)
print('*' * 80)
print('**** After clicking Authorize, paste code here and press Enter ****')
code = raw_input('Enter code from url: ')

# Make sure returned state has not changed for security reasons, and exchange
# code for an Access Token.
headers = {'Accept': 'application/x-www-form-urlencoded'}
print('Getting an access token...')
session = service.get_auth_session(headers=headers,
                                   data={'code': code,
                                         'grant_type': 'authorization_code',
                                         'redirect_uri': redirect_uri})

print('Getting current user from API...')
user = session.get('users/current').json()
print('Authenticated via OAuth as {0}'.format(user['data']['email']))
print("Getting user's coding stats from API...")
stats = session.get('users/current/summaries?range=Last Month').json()

f = open('data.json', 'w')
json.dump(stats['data'], f, indent=4)
f.close()