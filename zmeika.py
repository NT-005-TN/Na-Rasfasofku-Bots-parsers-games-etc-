import keyboard  # using module keyboard
from random import randint
import time

class RunGame():
	def __init__(self, width, height):
		self.width = width
		self.height = height
			
	def start(self):
		isApple = False
		self.isApple = isApple
		height, width = self.height, self.width
		field = [[0 for _ in range(height)] for _ in range(width)]
		
		x, y = randint(1, width-2), randint(1, height-2)
		print('Start pos:', y, x)
		self.x = x
		self.y = y

		field[x][y] = 1
		self.field = field
	
	def LookField(self):
		field = self.field
		for x1 in range(len(field)):
			print(field[x1])
		print()	
		
	def move(self):
		x, y = self.x, self.y
		width, height = self.width, self.height
		
		if keyboard.is_pressed('q'):
			if 1 <= x <= width-2:
				field[x][y] = 0
				x -= 1
				field[x][y] = 1
				time.sleep(0.2)
				

Game = RunGame(5,5)
Game.start()
Game.LookField()
while True:
	Game.move()
	Game.LookField()

'''
while True:  # making a loop
	try:  # used try so that if user pressed other than the given key error will not be shown
		if keyboard.is_pressed('q'):  # if key 'q' is pressed
			print('You Pressed A Key!')
			
	except:
		print('Err')
'''
