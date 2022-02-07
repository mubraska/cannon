from display import Display
from game import Game

if __name__ == '__main__':
    g = Game()
    d = Display(g, True, False)
    d.run()
