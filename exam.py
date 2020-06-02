import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from telegram.ext import Updater,CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler
import apiexample
import os

#Aquí estan los comandos de telegram.Para probarlo hay que buscar el usuario @Spoti_DRCAVbot.
#Mientras esté ejecutando este código el bot nos contestará.He implementado unos comando básicos
#sacados de la documentación de la api de telegram_bot y he implementado por mi mismo el comando
#/spotiexample.Lo que hace es imprimir las canciones que te devuelve la función definida en el otro
#codigo.


class SpotifyBot(object):

    def __init__(self,config):
        self.config = config
        self.id = config['client_id']
        self.secret = config['client_secret']
        self.yt_key = config['youtube_key']
        self.telegram = config['telegram_key']
        self.spoti = apiexample.setspoticredentials(self.id,self.secret)
        self.youtube = apiexample.setyoutube(self.yt_key)


    def start(self,update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me! Use /help for commands!")

    def help(self,update, context):
        frase_ayuda="Commands are: \n" + "/caps: minus to caps your text! \n" + "/search: search an artist top tracks! \n" + "/yt: search a video in youtube! \n" + "/link: type the numbers of your favourite songs in '/search' separated by spaces \n "\
        + "/top50: get the top50 global songs ranking \n" + "/top50pick + number: to get the song in this position \n " + "/newpl + name: creates a new playlist with the input name\n" + "/searchpl + playlist name: search an existing playlist\n"\
        + "/add + track name: adds the searched song to the selected playlist \n" + "/playedsongs: shows the last 10 songs played for the current user"
        context.bot.send_message(chat_id=update.effective_chat.id, text=frase_ayuda)

    def spotiexample(self,update, context):
        results = apiexample.tracksearchbyartist(' '.join(context.args),self.spoti)
        self.lastsearch = results
        listsong =apiexample.numberlist(results)
        context.bot.send_message(chat_id=update.effective_chat.id, text=listsong)

    def top50(self,update, context):
        songs,top50 = apiexample.top50playlist(self.spoti)
        list = '\n'.join(top50)
        context.bot.send_message(chat_id=update.effective_chat.id, text=list)
        #muestra toda la lista top50 global

    def top50pick(self,update, context):
        name,artist = apiexample.pickIndexTop50(' '.join(context.args),self.spoti)
        preview = apiexample.previewSong(' '.join(context.args),self.spoti)
        text = str(name) + ' - ' + str(artist) + '\n' + str(preview) + '\n'
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        #muestra canción-artista y una preview de 30 segundos del pick elegido de la lista top50pick

    def youtubeexample(self,update,context):
        videoid = apiexample.searchytid(' '.join(context.args),self.youtube)
        linkyt='https://www.youtube.com/watch?v=' + videoid[0]
        context.bot.send_message(chat_id=update.effective_chat.id, text=linkyt)

    def link(self,update,context):

        for x in context.args:
            videoid = apiexample.searchytid(self.lastsearch[int(x) - 1],self.youtube)
            linkyt='https://www.youtube.com/watch?v=' + videoid[0]
            context.bot.send_message(chat_id=update.effective_chat.id, text=linkyt)

    def inline_yt(self,update, context):
        query = update.inline_query.query

        if not query:
            return
        results = []
        ytbe = apiexample.searchytid(query,self.youtube)
        results.append(
            InlineQueryResultArticle(
            id=query.upper(),
            title = 'Video',
            input_message_content=InputTextMessageContent('https://www.youtube.com/watch?v=' + ytbe[0]),
            thumb_url=ytbe[1]
            )
        )
        context.bot.answer_inline_query(update.inline_query.id, results)

    def unknown(self,update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command. Use /help and see the available commands")

    def create_playlist(self,update,context):
        playlist = apiexample.create_playlist(' '.join(context.args),self.spoti)
        self.lastsearch = playlist['id']
        text = 'Playlist ' + playlist['name'] + ' successfully created'
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        #Crea la playlist i indica el missatge de que [nom_playlist] s'ha creat correctament

    def search_playlist(self,update,context):
        playlist = apiexample.search_playlist(' '.join(context.args),self.spoti)
        self.lastsearch = playlist['playlists']['items'][0]['id']
        text = 'Playlist ' + playlist['playlists']['items'][0]['name'] + ' selected'
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        #Busca la playlist i indica que s'ha seleccionat la playlist trobada

    def add_track(self,update,context):
        #playlist = apiexample.search_playlist(self.lastsearch[0],self.spoti)
        track = apiexample.add_track(' '.join(context.args),self.lastsearch,self.spoti)
        text = apiexample.playlist(self.lastsearch,self.spoti)
        list = '\n'.join(text)
        context.bot.send_message(chat_id=update.effective_chat.id, text=list)
        #Afegeix la cançó escrita a la playlist que s'ha seleccionat previament, i mostra la llista de totes les cançons de la playlist

    def user_playedsongs(self, update, context):
        songs = apiexample.search_playedsongs(self.spoti)
        listsongs =apiexample.numberlist(songs)
        self.lastsearch = listsongs
        context.bot.send_message(chat_id=update.effective_chat.id, text=listsongs)



    def run(self):
        updater = Updater(token=self.telegram, use_context=True)
        dispatcher = updater.dispatcher


        start_handler = CommandHandler('start', self.start)
        dispatcher.add_handler(start_handler)

        help_handler = CommandHandler('help', self.help)
        dispatcher.add_handler(help_handler)

        spotiexample_handler = CommandHandler('search', self.spotiexample)
        dispatcher.add_handler(spotiexample_handler)

        top50_handler = CommandHandler('top50', self.top50)
        dispatcher.add_handler(top50_handler)

        top50pick_handler = CommandHandler('top50pick', self.top50pick)
        dispatcher.add_handler(top50pick_handler)

        ytexample_handler = CommandHandler('yt', self.youtubeexample)
        dispatcher.add_handler(ytexample_handler)

        create_playlist_handler = CommandHandler('newpl',self.create_playlist)
        dispatcher.add_handler(create_playlist_handler)

        search_playlist_handler = CommandHandler('searchpl',self.search_playlist)
        dispatcher.add_handler(search_playlist_handler)

        spotilink_handler = CommandHandler('link', self.link)
        dispatcher.add_handler(spotilink_handler)

        add_track_handler = CommandHandler('add', self.add_track)
        dispatcher.add_handler(add_track_handler)

        add_track_handler = CommandHandler('playedsongs', self.user_playedsongs)
        dispatcher.add_handler(add_track_handler)

        inline_yt_handler = InlineQueryHandler(self.inline_yt)
        dispatcher.add_handler(inline_yt_handler)

        unknown_handler = MessageHandler(Filters.command, self.unknown)
        dispatcher.add_handler(unknown_handler)

        updater.start_polling()
        updater.idle()
