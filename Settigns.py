import pygame as pg

def setBackground(typeOfBack):

	# загружаем изображение
	background_image = pg.image.load("background.png")

	# подгоняем масштаб под размер окна
	background_image = pg.transform.scale(background_image, window_size)


	# задаем цвет фона
	background_color = (0, 0, 255)  # синий

	# заполняем фон заданным цветом
	screen.fill(background_color)

	# накладываем изображение на поверхность
	screen.blit(background_image, (0, 0))

# обновляем экран для отображения изменений
pg.display.flip()

# показываем окно, пока пользователь не нажмет кнопку "Закрыть"
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()

