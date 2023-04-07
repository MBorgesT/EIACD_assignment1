'''
from view.gui import GUI

gui = GUI()
gui.run()
'''
from model.klotski import Klotski
from time import time
game = Klotski()

game.read_board('inputs/set1/board8.txt')
start = time()
result = game.a_star(12, 1, 2)
print(time() - start)
print(len(result.move_history))
