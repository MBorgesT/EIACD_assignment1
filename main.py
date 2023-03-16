from view.gui import GUI

gui = GUI()
gui.run()
'''
from model.klotski import Klotski
game = Klotski()
game.read_board('inputs/board1.txt')

result = game.greedy_search()
print(len(result.move_history))
'''