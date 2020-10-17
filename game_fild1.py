#!/usr/bin/env python3

#import tkinter, time, random, functools

# Клетки на игровом поле
class Playing_fild:
    # Таблица из клеток на игровом поле
    def __init__(self, game_fild, n_lines, n_cols, pix_per_sell=10):
        # Параметры клетки и таблицы
        self.game_fild = game_fild
        self.n_lines = n_lines
        self.n_cols = n_cols
        self.pix_per_sell = pix_per_sell
        # Массив клеток с базовым цветом
        self.sell_array = []
        for n in range(n_lines):
            y = n * self.pix_per_sell
            y1 = y + self.pix_per_sell
            for k in range(n_cols):
                x = k * self.pix_per_sell
                x1 = x + self.pix_per_sell
                sell = self.game_fild.create_rectangle(x, y, x1, y1, fill='lightgrey', outline='lightgrey')
                self.sell_array.append(sell)

    # Перекрашивание клетки
    def coloriz(self, y, x, color='blue'):

        l = (y - 1) * self.n_cols + x
        # print(l, len(self.sell_array))
        sell = self.sell_array[l - 1]
        self.game_fild.itemconfig(sell, fill=color)

    # Раскрашивание всего игрового поля
    def colorized_fild (self, figure, sediment):
        for sell in self.sell_array:
            self.game_fild.itemconfig(sell, fill='lightgrey')

        for point in figure.list_point:
            self.coloriz(point.y, point.x, color='blue')

        for point in sediment.list_point:
            self.coloriz(point.y, point.x, color='red')


'''
# Изобразитель фигур на игровом поле
def imager(area, figure, display=True, color='blue'):
    if not display:
        color = 'lightgrey'
        # отобразить точки фигуры на игровом поле на текущем шаге

    # print(figure.list_point)
    for figure_point in figure.list_point:
        area.coloriz(figure_point.y, figure_point.x, color)

'''
