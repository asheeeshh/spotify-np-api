import requests
from flask import Flask, jsonify, Response, make_response, request
from dotenv import load_dotenv, find_dotenv
from os import getenv
import json

load_dotenv(find_dotenv())

def get_token():
    '''Get a new access token'''
    r = requests.post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'refresh_token',
        'refresh_token': 'AQCexYh0TaRjBqNBtHP0TFqBo0W-go753coL8IfmirUNuZIGx7rCMwqcL7TU7Hf4VZWLQSQYmqA3e7AvYS0PeUlvX6JV4Yyd3zWgTU7nNvdGynV3K7JY6SxmKX7jYB1Oiko',
        'client_id': 'a4596c8dfa19468693d1421a3a02d561',
        'client_secret': 'ae8083f9ebe34a488831866c4fee3307',
    })
    try:
        return r.json()['access_token']
    except BaseException:
        raise Exception(r.json())


def spotify_request(endpoint):
    '''Make a request to the specified endpoint'''
    r = requests.get(
        f'https://api.spotify.com/v1/{endpoint}',
        headers={'Authorization': f'Bearer {get_token()}'}
    )
    return {} if r.status_code == 204 else r.json()

def get_np():
    data = spotify_request('me/player/currently-playing')
    if data:
        item = data['item']
    else:
        item = spotify_request('me/player/recently-played?limit=3')['items'][0]['track']
    return {
        'artist': item['artists'][0]['name'].replace('&', '&amp;'),
        'song': item['name'].replace('&', '&amp;'),
    }

app = Flask(__name__)

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    return make_response(jsonify(get_np()), 200)

if __name__ == '__main__':
    app.run(debug=True)