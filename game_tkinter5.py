#!/usr/bin/env python3

import tkinter, time, datetime, random, functools, csv, os
import figure5, game_fild1

from tkinter import messagebox

def insert():
    global player_name, frame1, e1
    pn = e1.get()
    if pn: player_name = pn
    print('player_identification', player_name)
    frame1.destroy()


# Виджет регистрации/идентификации игрока в базе игроков (файл players_base.csv)
def player_identification():
    global frame1, e1

    #e1 = pymsgbox.prompt('Укажите имя игрока', 'PeTriS') # требуется модуль pymsgbox

    frame1 = tkinter.Frame(window, bg='green', width=250, height=100)
    frame1.pack_propagate(False)
    frame1.pack()

    l1 = tkinter.Label(frame1, text="Укажите имя игрока", width=50, height=1)
    l1.pack()
    e1 = tkinter.Entry(frame1, width=50)
    e1.pack()
    b1 = tkinter.Button(frame1, text="Ввод", command=insert)
    b1.pack()


# Рассчет игровой статистики (рейтинга игрока) на текущую дату/время (по данным из файла players_base.csv)
def player_statistics():

    # Создаем словарь игроков, анализируя все строки в базе (файле результатов) типа:
    # player_name: [count_games, best_res, middle_res]

    r3 = {}
    try:
        with open('players_base.csv', newline='') as csvfile:
            r = csv.reader(csvfile)
            for row in r:
                print(row)
                try:
                    player_name = row[0]
                    count_games = int(row[2])
                    best_res = int(row[3])
                    middle_res = float(row[4])

                    player_attr_list = r3.get(player_name)
                    # print('1', player_name, player_attr_list)

                    # Если имя игрока уже встречалось в базе
                    if player_attr_list:
                        # проверяем/меняем лучший результат (берем наибольший)
                        if player_attr_list[1] < best_res:
                            player_attr_list[1] = best_res

                        # корректируем средний результат
                        player_attr_list[2] = (player_attr_list[2] * player_attr_list[0] +
                                               middle_res * count_games) / (player_attr_list[0] + count_games)

                        # добавляем количество игр из новой записи
                        player_attr_list[0] += count_games

                        # обновляем значение ключа
                        r3[player_name] = player_attr_list
                    else:
                        # добавляем новую запись в словарь
                        r3.update({player_name: [count_games, best_res, middle_res]})

                    # print('2', player_name, player_attr_list)

                except:
                    continue

    except:
        #print('Файл players_base.csv отсутствует...')
        pass

    print(r3)
    return r3


# Окно сообщения с выбором варианта рейтинга (по лучшему/среднему результату всех игр)
def select_rating():
    global player_name

    answer = messagebox.askyesno(title="Выбор варианта рейтинга",
                                 message="По лучшему (Да) или среднему (Нет) результату всех игр?")
    # Смотрим базу игроков
    p_dict = player_statistics()

    # Если отсутствует файл базы игроков
    if p_dict == {}:
        print('Файл players_base.csv отсутствует...')
        messagebox.showwarning(title="Выбор варианта рейтинга",
                               message="К сожалению, отсутствует файл базы игроков".format(player_name))
        return

    # Если игрок новый (пока не играл)
    if player_name not in p_dict:
        print(player_name, 'отсутствует в базе')
        messagebox.showinfo(title="Выбор варианта рейтинга",
                               message="{} отсутствует в базе игроков".format(player_name))
        return

    if answer == True:
        msg = rating_of_players(player_name, p_dict, type_rating=0)
        messagebox.showinfo(title="Рейтинг по лучшему результату всех игр", message=msg)
    else:
        msg = rating_of_players(player_name, p_dict, type_rating=1)
        messagebox.showinfo(title="Рейтинг по среднему результату всех игр", message=msg)

    print('рейтинг игрока', player_name)


#   Лучшие игроки и позиция указанного игрока
def rating_of_players(p_name, p_dict, type_rating=0):
    # type_rating=0 - best_res
    # type_rating=1 - middle_res

    # сортируем ключи словаря игроков по убыванию рейтинга (best_res либо middle_res)
    if type_rating:
        i = 2  # middle_res
        text = 'среднему'
    else:
        i = 1  # best_res
        text = 'лучшему'
    sorted_by_res = sorted(p_dict.items(), key=lambda kv: kv[1][i], reverse=1)
    message1 = 'Позиция по {} результату всех игр из {} игроков: \n'.format(text, len(p_dict))
    print(message1)
    f = 0
    # сильнейшие игроки
    message2 = ''
    message3 = ''
    message = ''
    for k in sorted_by_res[:3]:
        print(sorted_by_res.index(k) + 1, k[0])
        #message2 = str(sorted_by_res.index(k) + 1) + k[0] + '\n'
        message2 = '{}) {} ({} - баллов )\n'.format(sorted_by_res.index(k) + 1, k[0], k[1][i])
        message = message + message2

        if k[0] == p_name: f = 1

    if not f:
        # позиция игрока в отсортированном списке
        position_player_by_best_res = sorted_by_res.index((p_name, p_dict[p_name])) + 1
        print(position_player_by_best_res, p_name, '(', p_dict[p_name][i], '- баллов )')
        message3 = '{}) {} ({} - баллов )'.format(position_player_by_best_res, p_name, p_dict[p_name][i])

    return message1 + message + message3



# Расчет сеансовых параметров игровой статистики игрока и сохранение их в базу игроков
def saving_game_result():
    global player_name, data_time, games_res, count_games

    count_games = len(games_res)  # число игр сеанса
    # проверка наличия элементов массива результатов
    if count_games:
        best_res = sorted(games_res, reverse=True)[0]  # лучший игровой результат за сеанс
        middle_res = sum(games_res) / count_games  # средний игровой результат за сеанс

    else:
        best_res = 0
        middle_res = 0

    print(player_name, data_time.strftime("%Y-%m-%d-%H:%M:%S"), count_games,
          best_res, middle_res)

    if count_games:
        with open('players_base.csv', 'a', newline='') as csvfile:
            data_writer = csv.writer(csvfile)
            data_writer.writerow([player_name, data_time.strftime("%Y-%m-%d-%H:%M:%S"),
                                 count_games, best_res, middle_res])

    window.destroy()


# сообщение озавершениии игрового цикла текстом в игровом поле
def mess_game_over(game_fild, width_window, height_window):
    
      game_fild.create_text(width_window*0.5, height_window*0.5, text="Игра завершена!",
                          justify='center', font="Verdana 16", fill='green')


# управление фигурой посредством клавиатуры
def dialog(event, arg):

    play_fild = arg[0]
    sediment = arg[1]
    figure = arg[2]
    platform = arg[3]

    # проверка операционной платформы
    if platform == 'posix':
        #print('Linux')
        k1 = 114
        k2 = 113
        k3 = 116
        k4 = 52
        k5 = 53
        k6 = 24

    else:
        #print('MS Windows')
        k1 = 39     # "Rightarrow" right shift
        k2 = 37     # "Leftarrow" left shift
        k3 = 40     # "Downarrow" falling down
        k4 = 90     # "Z" left (anti-clockwise) turn
        k5 = 88     # "X" right (clockwise) rotation
        k6 = 24     # "O" pause

    k = event.keycode
    #print(str(k) + " key pressed")

    if k == k1:
        # сдвиг вправо
        figure.shift(3)
    elif k == k2:
        # сдвиг влево
        figure.shift(1)
    elif k == k3:
        # цикл шагов вниз до "осадка"
        while not figure.sticking:
            figure.shift(2)
    elif k == k4:
        # поворот влево
        figure.turn(3)
    elif k == k5:
        # поворот вправо
        figure.turn(1)
    elif k == k6:
        # пауза
        pass

    play_fild.colorized_fild(figure, sediment)


# игровой цикл (до переполнения "осадка")
def game(n_lines, n_cols, y1):

    global games_res

    # Игровое поле
    game_fild = tkinter.Canvas(window, width=width_window, height=height_window, bg='white')
    game_fild.pack()

    play_fild = game_fild1.Playing_fild(game_fild, n_lines, n_cols, pix_per_sell)

    # создаем первичный осадок
    s = figure5.Sediment(n_lines, n_cols, y1)

    # позиция создания произвольной игровой фигуры (с учетом не пересечения верхней
    # границы игрового поля и наибольшей глубины "осадка")
    y0 = y1 + 1
    # Результатом игры считаем количество фигур в "осадке" на момент завершения
    figure_count = 0


    # запускаем игровой цикл...
    while not s.sediment_overflow:

        print('количество фигур =', str(figure_count))

        # создаем произвольную игровую фигуру в произвольной позиции
        f = figure5.Game_figure(s, y0, random.randint(2, n_cols - 2), n_cols,
                                figure_number=random.randint(0, 6))

        # в произвольном положении
        f.turn(random.randint(1, 4))

        # исходное раскрашивание игрового поля
        play_fild.colorized_fild(f, s)

        # пока фигура не "выпала в осадок", она падает и управляется с клавиатуры
        while not f.sticking:

            window.update()

            # запускаем контроль клавиатуры
            # привязки событий клавиш
            #x = [game_fild, s, f]
            x = [play_fild, s, f, os.name]

            window.bind('<Key>', functools.partial(dialog, arg=x))

            # вниз (по умолчанию)
            f.shift(2)

            # пауза
            time.sleep(1)

            # текущее раскрашивание игрового поля
            play_fild.colorized_fild(f, s)

        # увеличиваем результат игры

        figure_count += 1
        window.title('Game PeTriS, ' + str(figure_count))

        # если высшая точка "осадка" достигла уровня появления фигур,
        # игровой цикл завершен!

        s.level_control()
        if s.sediment_overflow:

            print("Игра завершена")

            # Запись результата игры в массив сеанса
            games_res.append(figure_count)

            # Сообщение озавершении игры текстом в игровом поле
            mess_game_over(game_fild, width_window, height_window)
            window.update()
            time.sleep(1)

            # удаление всех виджетов игрового поля
            game_fild.destroy()
            print('Начать новую игру')
            break

# текстовое сообщение с правилами игры и пр. инфой
def help_game():

    print('вывод окна с текстом справочной информации...')

    # сокращенная справочная информация
    text = '''
            Правила игры соответствуют классическому тетрису.
        Случайные "тетрики" падают сверху, поворачиваясь вкруг своей
        оси и смещаясь по горизонтали под управлением игрока 
        (посредством клавиатуры), и в итоге присоединяются к "осадку". 
            Сплошные горизонтальные слои осадка (кроме самого нижнего)
        исчезают, а вышележащие "проседают" вниз.
            Сеанс игры завершается при достижении верхней точкой "осадка"
        уровня генерации "тетриков".
        
                Клавиши управления падающим "тетриком":
                    Сдвиг вправо на одну позицию - "Rightarrow" 
                    Сдвиг влево на одну позицию - "Leftarrow"
                    Падение вниз до "осадка" - "Downarrow"
                    Поворот на 90 град. влево - "Z"
                    Поворот на 90 град. вправо - "X"
                        
            Результатом игры считается количество "тетриков", перешедших
        в "осадок" в течение сеанса.
            Для зарегистрированного игрока сеансовый результат влияет на
        его рейтинг.                
    '''

    # вывод информации из текстового файла (help.txt)
    with open("help.txt") as f:
            text = f.read()

    messagebox.showinfo(title="Справочная информация", message=str(text))


global player_name, data_time, games_res  # count_games, best_res, middle_res

# Параметры статистики игроков
player_name = 'Anonymous'               #   псевдоним игрока
data_time = datetime.datetime.now()     #   дата/время начала игрового сеанса
games_res = []                          #   массив результатов игр сеанса
'''
count_games                             #   число игр сеанса
best_res                                #   лучший игровой результат
middle_res                              #   средний игровой результат за сеанс
'''



# Родительское окно приложения
window = tkinter.Tk()
window.title('Game PeTriS')
window.geometry("300x150")

# Игровое меню
game_menu = tkinter.Menu(window)
window.config(menu=game_menu)

# Пункты игрового меню:

# - запуск игрового цикла
play = game_menu.add_command(label='Играть', command=lambda: game(n_lines, n_cols, y1))
# - выход
#quit = game_menu.add_command(label='Выход', command=lambda: window.destroy())
quit = game_menu.add_command(label='Выход', command=saving_game_result)
# - статистика игр
statistic = game_menu.add_command(label='Статистика игр', command=lambda: select_rating())
# - справка по игре
help = game_menu.add_command(label='Справка по игре', command=lambda: help_game())

# Регистрация/идентификация игрока
reg = game_menu.add_command(label='Регистрация игрока', command=lambda: player_identification())


# пауза
#window.after(10000, window.update())

# Параметры игрового поля
n_lines = 15  # высота/глубина
n_cols = 10  # ширина
y1 = 2      # наименьшая глубина "осадка"
pix_per_sell = 50  # размер клетки
height_window = n_lines * pix_per_sell
width_window = n_cols * pix_per_sell

# Увеличиваем родительское окно до размеров игрового поля
window.geometry('{}x{}'.format(width_window, height_window))
window.resizable(0, 0)

window.mainloop()