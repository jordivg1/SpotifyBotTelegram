import sys
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import os
import json
import webbrowser
import logging
from googleapiclient.discovery import build
#Este codigo utiliza las librerias de spotipy para conectarse con la API de spotify. Spotify CLIENT_ID Y CLIENT_SECRET
#son dos parametros para conectarse a la API.Lo que hace la función es basicamente devolverte la lista de canciones de una artista
#Hay que instalarse las librerias de spotipy para que funcione.
def setyoutube(ytkey):
    api_key = ytkey
    youtube = build('youtube', 'v3', developerKey=api_key, cache_discovery=False)
    return youtube

def setspoticredentials(spid,spsecret):
    #os.environ['SPOTIPY_CLIENT_ID'] = spid
    #os.environ['SPOTIPY_CLIENT_SECRET'] = spsecret
    #spoticre = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    scope = 'playlist-modify-public playlist-modify-private user-read-email user-read-private'
    token = util.prompt_for_user_token(username=None, scope=scope, client_id=spid, client_secret=spsecret, redirect_uri = 'https://google.com', cache_path='tokens.json')
    #return spoticre
    return spotipy.Spotify(token)

def tracksearchbyartist(eje,spotify):
    print("Running")
    artista = spotify.search(q='artist:' + eje,limit=1, type='artist')
    results = spotify.artist_top_tracks(artista['artists']['items'][0]['uri'])
    trackss=[]
    for track in results['tracks'][:10]:
        trackss.append(track['name'])
    return trackss

def top50playlist(spotify):
    playlist_id = 'spotify:playlist:37i9dQZEVXbMDoHDwVN2tF'
    pl = spotify.playlist(playlist_id, fields=None, market=None)
    tracks = pl["tracks"]
    songs = tracks["items"]
    top50 = []
    artists = []
    for i in range(len(songs)):
        top50.append(str(i+1) +'-'+ songs[i]["track"]["name"])
    return (songs,top50)

def pickIndexTop50(index,spotify):
    songs,top50 = top50playlist(spotify)
    name = songs[int(index)-1]["track"]["name"]
    artist = songs[int(index)-1]['track']['artists'][0]['name']
    return (name, artist)

def previewSong(index,spotify):
    songs,top50 = top50playlist(spotify)
    return songs[int(index)-1]['track']['preview_url']

def searchytid(ejee, youtubee):
    req = youtubee.search().list(part='snippet',
                            q=ejee,
                            type='video',
                            maxResults=1)
    res = req.execute()
    ress=[]
    ress.append(res['items'][0]['id']['videoId'])
    ress.append(res['items'][0]['snippet']['thumbnails']['default']['url'])
    return ress


def numberlist(lista):
    i = 1
    numlist = ""
    for x in lista:
        numlist =numlist + str(i)  + '*'  + x + '\n'
        i = i+1
    return numlist


def create_playlist(name_playlist,spotify):
    playlist=spotify.user_playlist_create(user=spotify.me()['id'], name=name_playlist, public=True, description='Test DRCAV des de Telegram')
    return playlist
    #Crea una nova playlist amb el nom que li passen

def search_playlist(name_playlist,spotify):
    playlist = spotify.search(q=name_playlist,limit=1, type='playlist')
    return playlist
    #Busca una playlist pel nom que li passen

def add_track(track_name,playlist,spotify):
    track = spotify.search(q=track_name,limit=1, type='track')
    track_id = track['tracks']['items'][0]['id']
    playlist = spotify.user_playlist_add_tracks(user=spotify.me()['id'], playlist_id=playlist, tracks={track_id}, position=None)
    return playlist
    #Afegeix una cançó on se li passa la cerca a la playlist previament seleccionada

def playlist(playlist_id,spotify):
    pl = spotify.playlist(playlist_id, fields=None, market=None)
    tracks = pl["tracks"]
    songs = tracks["items"]
    list = []
    for i in range(len(songs)):
        list.append(str(i+1) +'-'+ songs[i]["track"]["name"])
    return list
    #Retorna una llista de cançons d'una playlist

def search_playedsongs(spotify):
    ps = spotify.current_user_recently_played(10, None, None)
    songs = ps["items"]
    list = []
    for i in range(len(songs)):
        list.append(str(songs[i]["track"]["name"]))
    return list