from config import Config
from game import Game

if __name__ == "__main__":
    config = Config()
    game = Game(**config.dictionarize())
    game.main()
