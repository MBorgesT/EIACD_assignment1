'''
from view.gui import GUI

gui = GUI()
gui.run()
'''
from model.klotski import Klotski
from time import time
game = Klotski()

game.read_board('inputs/set2/board2.txt')
start = time()
result = game.a_star(50, 50, 15)
print(time() - start)
print(len(result.move_history))
