import pygame

pygame.init()
width, height = 400, 300
dis = pygame.display.set_mode((width,height))


pygame.display.set_caption('Snake')
game_over=False

while not game_over:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			game_over = True
		print(event)   # выводит на экран все действия игры
	
	pygame.draw.rect(dis,(0,0,255),[200,150,10,10])
    pygame.display.update()
	
pygame.quit()
quit()
