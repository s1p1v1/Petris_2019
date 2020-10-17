#!/usr/bin/env python3

#    object figure
#   Объект игровая фигура

import math, copy


class Point_coord:
    # Позиция точки как элемента фигуры
    def __init__(self, sediment, y, x, width_window):
        # "осадок" из фигур внизу окна (по сути, список точек)
        self.sediment = sediment
        # позиция по горизонтали (в игровом окне)
        self.x = x
        # позиция по вертикали (в игровом окне)
        self.y = y
        # границы игрового поля с учетом правой рамки (?)
        #self.max_x_right = width_window - 1    # для curses
        self.max_x_right = width_window + 1     # для tkinter
        self.min_x_left = 0

    def shift(self, direction, step=1):
        # сместить на позицию
        # left-1, drop-2, right-3
        if direction == 1:
            self.x -= step
        elif direction == 3:
            self.x += step
        elif direction == 2:
            self.y += step

    def turn(self, corner):
        # повернуть кратно 1/4 оборота
        # right-1, half turn-2, left-3, turnover-4
        sin_corner = math.sin(corner * math.pi * 0.5)
        cos_corner = math.cos(corner * math.pi * 0.5)
        x_corner = self.x * cos_corner - self.y * sin_corner
        y_corner = self.x * sin_corner + self.y * cos_corner
        self.x = int(round(x_corner, 1))
        self.y = int(round(y_corner, 1))

    def cross_border(self):
        # определяем признак позиции точки в границах игрового поля

        # присоединение к "осадку"
        for n in self.sediment.list_point:
            if n.x == self.x and n.y == self.y:
                return 2

        # проверить выход за боковые границы игрового окна
        if self.x == self.max_x_right:
            # дошли до правого края окна
            return 3

        elif self.x == self.min_x_left:
            # дошли до левого края окна
            return 1

        else:
            return 0


class Game_figure():
    # Описание игровой фигуры (комбинация 4х точек) и координаты центральной точки
    # ее появления на игровом поле
    def __init__(self, sediment, y, x, width_window, figure_number=0):
        self.list_point = []  # список точек в текущем положении
        self.list_point_new = []  # список точек после текущего шага
        self.sediment = sediment  # фигура "осадок игровых фигур"
        self.figure_number = figure_number  # вид игровой фигуры
        # признак присоединения фигуры к "осадку" (для проверки в условиях игровой ситуации)
        self.sticking = False

        # width_window -= 2   # поправка на рамку окна для curses

        if figure_number == 0:
            # квадрат
            self.list_point.append(Point_coord(sediment, y, x, width_window))  # center
            self.list_point.append(Point_coord(sediment, y - 1, x, width_window))
            self.list_point.append(Point_coord(sediment, y, x - 1, width_window))
            self.list_point.append(Point_coord(sediment, y - 1, x - 1, width_window))
        elif figure_number == 1:
            # линия
            self.list_point.append(Point_coord(sediment, y, x, width_window))  # center
            self.list_point.append(Point_coord(sediment, y, x - 1, width_window))
            self.list_point.append(Point_coord(sediment, y, x + 1, width_window))
            self.list_point.append(Point_coord(sediment, y, x + 2, width_window))
        elif figure_number == 2:
            # левый угол
            self.list_point.append(Point_coord(sediment, y, x, width_window))  # center
            self.list_point.append(Point_coord(sediment, y, x - 1, width_window))
            self.list_point.append(Point_coord(sediment, y, x + 1, width_window))
            self.list_point.append(Point_coord(sediment, y - 1, x - 1, width_window))
        elif figure_number == 3:
            # правый угол
            self.list_point.append(Point_coord(sediment, y, x, width_window))  # center
            self.list_point.append(Point_coord(sediment, y, x - 1, width_window))
            self.list_point.append(Point_coord(sediment, y, x + 1, width_window))
            self.list_point.append(Point_coord(sediment, y - 1, x + 1, width_window))
        elif figure_number == 4:
            # зигзаг влево
            self.list_point.append(Point_coord(sediment, y, x, width_window))  # center
            self.list_point.append(Point_coord(sediment, y + 1, x, width_window))
            self.list_point.append(Point_coord(sediment, y, x - 1, width_window))
            self.list_point.append(Point_coord(sediment, y + 1, x + 1, width_window))
        elif figure_number == 5:
            # зигзаг вправо
            self.list_point.append(Point_coord(sediment, y, x, width_window))  # center
            self.list_point.append(Point_coord(sediment, y - 1, x + 1, width_window))
            self.list_point.append(Point_coord(sediment, y - 1, x, width_window))
            self.list_point.append(Point_coord(sediment, y, x - 1, width_window))
        elif figure_number == 6:
            # кнопка
            self.list_point.append(Point_coord(sediment, y, x, width_window))  # center
            self.list_point.append(Point_coord(sediment, y - 1, x, width_window))
            self.list_point.append(Point_coord(sediment, y, x + 1, width_window))
            self.list_point.append(Point_coord(sediment, y, x - 1, width_window))

    def control_intersections(self):
        # перебираем все точки фигуры после очередного ее движения
        # для оценки их наложения на границы игрового окна или на осадок

        for i in self.list_point_new:
            intersection = i.cross_border()

            if intersection == 2:
                return 2  # имеется наложение на осадок

            elif intersection == 1 or intersection == 3:
                return 1  # имеется наложение на боковые границы игрового поля

        return 0  # наложение отсутствует

    def shift(self, direction):
        # сместить на позицию
        # left-1, drop-2, right-3

        # делаем очередной шаг виртуально
        self.list_point_new.clear()
        self.list_point_new = copy.deepcopy(self.list_point)

        for i in self.list_point_new:
            i.shift(direction)

        # проверяем наложение точек фигуры на боковые границы игрового поля
        # или "осадок" после очередного шага
        intersec = self.control_intersections()

        if intersec == 2:
            # присоединение к "осадку"
            self.sediment.suck(self)
            self.sticking = True
            # удаление точек фигуры, поскольку теперь она часть "осадка"
            self.list_point = []

            # сокращение "осадка"
            self.sediment.reduce()

        elif intersec == 1:
            # наложение на левую/правую границы игрового поля
            pass

        else:
            # закрепляем очередной шаг реально
            for i in self.list_point:
                i.shift(direction)

    def turn(self, corner):
        # повернуть кратно 1/4 оборота
        # right-1, half turn-2, left-3, turnover-4

        # делаем очередной поворот виртуально
        self.list_point_new = copy.deepcopy(self.list_point)

        if self.figure_number != 0:
            center_point_x = self.list_point_new[0].x
            center_point_y = self.list_point_new[0].y
            for i in self.list_point_new:
                # приведение к собственным координатам (центр фигуры - точка 2)
                i.x -= center_point_x
                i.y -= center_point_y
                # поворот вокруг собственного центра
                i.turn(corner)
                # приведение к глобальной системе координат (окно)
                i.x += center_point_x
                i.y += center_point_y

        # проверяем наложение точек фигуры на боковые границы игрового поля
        # или на "осадок" после очередного поворота

        position = self.control_intersections()

        if not position:
            # выполняем очередной шаг реально
            if self.figure_number != 0:
                center_point_x = self.list_point[0].x
                center_point_y = self.list_point[0].y
                for i in self.list_point:
                    # приведение к собственным координатам (центр фигуры - точка 2)
                    i.x -= center_point_x
                    i.y -= center_point_y
                    # поворот вокруг собственного центра
                    i.turn(corner)
                    # приведение к глобальной системе координат (окно)
                    i.x += center_point_x
                    i.y += center_point_y

class Sediment():
    # "Осадок" из игровых фигур внизу (на дне) игрового поля
    def __init__(self, height_window, width_window, max_sediment_level):
        self.list_point = []  # список координат точек "осадка"

        # наибольшая возможная глубина "осадка" (от высоты игрового окна)
        self.max_y_down = height_window

        # наибольшая ширина осадка (от ширины игрового окна)
        self.max_x_right = width_window

        # текущая глубина "осадка"
        self.sediment_level = height_window

        # первоначальное число слоев осадка
        self.count_sediment_level = 1

        # минимальная глубина "осадка" (уровень переполнения)
        self.max_sediment_level = max_sediment_level

        # признак переполнения игрового окна "осадком"
        self.sediment_overflow = False

        # первоначальный "фиктивный" слой "осадка" (список точек)
        self.list_point_primary = []
        for x in range(1, self.max_x_right+1):
            self.list_point_primary.append(Point_coord(self, self.max_y_down, x, width_window))

        self.list_point.extend(self.list_point_primary)


    def suck(self, figure):
        # поглотить очередную игровую фигуру
        self.list_point.extend(figure.list_point)

    def level_control(self):
        # определяем текущую глубину осадка

        # список y-координат всех точек "осадка"
        y_list_point = [point.y for point in self.list_point]

        # y-координата самой верхней точки "осадка"
        self.sediment_level = min(y_list_point)

        # если глубина "осадка" достигла уровня появления новых игровых фигур
        # с точностью до 2-х рядов
        if self.sediment_level-2 <= self.max_sediment_level:
            # останов игры
            self.sediment_overflow = True

    def reduce(self):
        # убрать слой осадка, который заполнен точками полностью (кроме начального)

        # список номеров слоев для удаления
        k_del = []
        # словарь остающихся слоев (номер слоя - список точек)
        l_dict = {}

        # перебираем существующие слои "осадка" сверху вниз
        y = range(self.sediment_level-2, self.max_y_down)
        for k in y:
            # составляем список точек каждого слоя
            level_point_list = []
            for l in self.list_point:
                if l.y == k:
                    level_point_list.append(l)

            len_lpl = len(level_point_list)

            # если длина списка точек слоя из "осадка" равна ширине игрового окна,
            # записываем его номер в список удаляемых и удаляем точки слоя из "осадка"
            if len_lpl >= self.max_x_right:
                k_del.append(k)
                self.list_point[:] = [x for x in self.list_point if x not in level_point_list]

            # иначе добавляем слой в словарь остающихся
            else:
                l_dict.update({k: level_point_list})

        # "осаживаем" (сдвигаем вниз) слои, расположенные выше удаляемых

        s = 0  # смещение точек по y-координате

        # перебираем существующие слои "осадка" снизу вверх
        z = range(self.max_y_down - 1, self.sediment_level - 3, -1) # для curses
        for n in z:

            # для остающихся слоев
            if n not in k_del:

                # добавляем к y-координате смещение
                for i in l_dict[n]:
                    i.y += s

            # при удаленнии слоя увеличиваем смещение для вышерасположенных
            else:
                s += 1
