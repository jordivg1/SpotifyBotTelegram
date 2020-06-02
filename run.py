import exam
import apiexample
from exam import SpotifyBot as Bot
import logging
import warnings
import json

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                level=logging.INFO)


def main():
    with open('keys.json', 'r') as config_file:
        config = json.loads(config_file.read())
    bot = Bot(config)
    bot.run()

if __name__ == '__main__':
    main()