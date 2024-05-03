#import color, color_sensor, motor, time
#import runloop
#from hub import port, button

COLOR = ["WHITE", "ORANGE", "GREEN", "RED", "BLUE", "YELLOW"] #Библиотека цветов нужно дополнить!
#scan_now
size = 8
#scan_color[]
qw = 30 #Сдвиг назад на клетку (нужно значени)

#переменные влада
# массив расположения цветов в кубике
cube_color_pos = [[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]]
#массив соотносящихся значений которые выдаёт color_sensor с массивом COLOR то есть
#число выдаваемое функцией сканирования цвета соответствует цвету из массива
posituon_scan_base = 0
COLOR_reletive_pos = {"WHITE": 0, "ORANGE": 0, "GREEN": 0, "RED": 0, "BLUE": 0, "YELLOW": 0}
#констуркиця await подразумевает собой что наша программа откладывает выполнение программы
#до тех пор пока мы не выполним какую либо функцию или что либо
#также необходимо функцию назначать async то есть асинхронной
#то есть что бы откладывать на потом программу необходимо прописывать ключевое слово о том
#что мы выполняем это с возможностью отложения на потом программы
async def turn(index):
    #функция поворота кубика
    for i in range(index):#количество повторений переворотов(для удобства)
        await motor.run_for_degrees(port.F, -180, 450, stop=motor.SMART_BRAKE)#поднятие механизма(поворот кубика)
        await motor.run_for_degrees(port.F, 180, 450, stop=motor.SMART_BRAKE)#опускание механизма(доворот кубика)
async def rotate(deg):
    #функция поворота кубика
    await motor.run_for_degrees(port.D, int(deg)*3, 600, stop=motor.SMART_BRAKE)#значения поворота уможается на 3 так как
    #передаточное отношения поворота большого мотока к повороту корзины с кубиком равно 3 к 1
async def fixation():
    #функия накидывания механизма на кубик и его фиксации
    await motor.run_for_degrees(port.F, -90, 500, stop=motor.SMART_BRAKE)#опускание механизма на кубик
async def return_fixation():
    #функия cкидывания механизма c кубик
    await motor.run_for_degrees(port.F, 90, 500, stop=motor.SMART_BRAKE)#поднятие механизма с кубика
def move_cube(cube_color_pos, i, color_move, COLOR_reletive_pos):
    i_pos = 0
    if i == 0:
        runloop.run(fixation())
        runloop.run(rotate(-90))
        runloop.run(return_fixation())
        i_pos = COLOR_reletive_pos.get(color_move)
        #изменение положения кубов
        #изменение верхней грани 
        cub_now = cube_color_pos[i_pos][7]
        corner_now = cube_color_pos[i_pos][8]
        cube_color_pos[i_pos][7] = cube_color_pos[i_pos][1]
        cube_color_pos[i_pos][8] = cube_color_pos[i_pos][2]
        for j in range(1,7):#однотипные изменения с второй по шестую грань и угол
            cube_color_pos[i_pos][i] = cube_color_pos[i_pos][i+2]
        cube_color_pos[i_pos][5] = cub_now#перенос последних граней и углов на предпоследнии 
        cube_color_pos[i_pos][6] = corner_now
        if i_pos == 0:
            cub_now = cube_color_pos[5][7]
            corner_now = cube_color_pos[5][6]
            corner_now_2 = cube_color_pos[5][8]
            cube_color_pos[5][7] = cube_color_pos[i_pos + 1][5]
            cube_color_pos[5][6] = cube_color_pos[i_pos + 1][4]
            cube_color_pos[5][8] = cube_color_pos[i_pos + 1][6]
            cube_color_pos[i_pos + 1][5] = cube_color_pos[4][7]
            cube_color_pos[i_pos + 1][4] = cube_color_pos[4][6]
            cube_color_pos[i_pos + 1][6] = cube_color_pos[4][8]
            cube_color_pos[4][7] = cube_color_pos[3][1]
            cube_color_pos[4][6] = cube_color_pos[3][8]
            cube_color_pos[4][8] = cube_color_pos[3][2]
            cube_color_pos[3][1] = cub_now
            cube_color_pos[3][8] = corner_now
            cube_color_pos[3][2] = corner_now_2
        elif i_pos == 3:
            cub_now = cube_color_pos[5][1]
            corner_now = cube_color_pos[5][8]
            corner_now_2 = cube_color_pos[5][2]
            cube_color_pos[5][1] = cube_color_pos[0][5]
            cube_color_pos[5][8] = cube_color_pos[0][4]
            cube_color_pos[5][2] = cube_color_pos[0][6]
            cube_color_pos[0][5] = cube_color_pos[4][5]
            cube_color_pos[0][4] = cube_color_pos[4][4]
            cube_color_pos[0][6] = cube_color_pos[4][6]
            cube_color_pos[4][5] = cube_color_pos[i_pos - 1][1]
            cube_color_pos[4][4] = cube_color_pos[i_pos - 1][2]
            cube_color_pos[4][6] = cube_color_pos[i_pos - 1][8]
            cube_color_pos[i_pos - 1][1] = cub_now
            cube_color_pos[i_pos - 1][2] = corner_now_2
            cube_color_pos[i_pos - 1][8] = corner_now
        elif i_pos == 2:
            cub_now = cube_color_pos[5][3]
            corner_now = cube_color_pos[5][4]
            corner_now_2 = cube_color_pos[5][2]
            cube_color_pos[5][2] = cube_color_pos[i_pos + 1][5]
            cube_color_pos[5][3] = cube_color_pos[i_pos + 1][4]
            cube_color_pos[5][4] = cube_color_pos[i_pos + 1][6]
            cube_color_pos[i_pos + 1][5] = cube_color_pos[4][3]
            cube_color_pos[i_pos + 1][4] = cube_color_pos[4][2]
            cube_color_pos[i_pos + 1][6] = cube_color_pos[4][4]
            cube_color_pos[4][3] = cube_color_pos[i_pos - 1][1]
            cube_color_pos[4][2] = cube_color_pos[i_pos - 1][2]
            cube_color_pos[4][4] = cube_color_pos[i_pos - 1][8]
            cube_color_pos[i_pos - 1][1] = cub_now
            cube_color_pos[i_pos - 1][2] = corner_now
            cube_color_pos[i_pos - 1][8] = corner_now_2
        elif i_pos == 1:
            cub_now = cube_color_pos[5][5]
            corner_now = cube_color_pos[5][4]
            corner_now_2 = cube_color_pos[5][6]
            cube_color_pos[5][5] = cube_color_pos[i_pos + 1][5]
            cube_color_pos[5][4] = cube_color_pos[i_pos + 1][4]
            cube_color_pos[5][6] = cube_color_pos[i_pos + 1][6]
            cube_color_pos[i_pos + 1][5] = cube_color_pos[4][1]
            cube_color_pos[i_pos + 1][4] = cube_color_pos[4][8]
            cube_color_pos[i_pos + 1][6] = cube_color_pos[4][2]
            cube_color_pos[4][1] = cube_color_pos[i_pos - 1][1]
            cube_color_pos[4][8] = cube_color_pos[i_pos - 1][2]
            cube_color_pos[4][2] = cube_color_pos[i_pos - 1][8]
            cube_color_pos[i_pos - 1][1] = cub_now
            cube_color_pos[i_pos - 1][2] = corner_now_2
            cube_color_pos[i_pos - 1][8] = corner_now
        elif i_pos == 4:
            cub_now = cube_color_pos[0][3]
            corner_now = cube_color_pos[0][4]
            corner_now_2 = cube_color_pos[0][2]
            cube_color_pos[0][3] = cube_color_pos[1][3]
            cube_color_pos[0][4] = cube_color_pos[1][4]
            cube_color_pos[0][2] = cube_color_pos[1][2]
            cube_color_pos[1][3] = cube_color_pos[2][3]
            cube_color_pos[1][2] = cube_color_pos[2][2]
            cube_color_pos[1][4] = cube_color_pos[2][4]
            cube_color_pos[2][3] = cube_color_pos[3][3]
            cube_color_pos[2][4] = cube_color_pos[3][4]
            cube_color_pos[2][2] = cube_color_pos[3][2]
            cube_color_pos[3][3] = cub_now
            cube_color_pos[3][4] = corner_now
            cube_color_pos[3][2] = corner_now_2
        elif i_pos == 5:
            cub_now = cube_color_pos[0][7]
            corner_now = cube_color_pos[0][6]
            corner_now_2 = cube_color_pos[0][8]
            cube_color_pos[0][7] = cube_color_pos[3][7]
            cube_color_pos[0][6] = cube_color_pos[3][6]
            cube_color_pos[0][8] = cube_color_pos[3][8]
            cube_color_pos[3][7] = cube_color_pos[2][7]
            cube_color_pos[3][6] = cube_color_pos[2][6]
            cube_color_pos[3][8] = cube_color_pos[2][8]
            cube_color_pos[2][7] = cube_color_pos[1][7]
            cube_color_pos[2][6] = cube_color_pos[1][6]
            cube_color_pos[2][8] = cube_color_pos[1][8]
            cube_color_pos[1][7] = cub_now
            cube_color_pos[1][6] = corner_now
            cube_color_pos[1][8] = corner_now_2
    elif i == 1:
        await fixation()
        await rotate(180)
        await return_fixation()
        i_pos = COLOR_reletive_pos.get(color_move)
        #изменение положения кубов
        #изменение верхней грани
        cub_now = cube_color_pos[i_pos][7]
        corner_now = cube_color_pos[i_pos][8]
        cub_now_2 = cube_color_pos[i_pos][5]
        corner_now_2 = cube_color_pos[i_pos][6]
        cube_color_pos[i_pos][7] = cube_color_pos[i_pos][3]
        cube_color_pos[i_pos][8] = cube_color_pos[i_pos][4]
        cube_color_pos[i_pos][5] = cube_color_pos[i_pos][1]
        cube_color_pos[i_pos][6] = cube_color_pos[i_pos][2]
        cube_color_pos[i_pos][1] = cub_now_2
        cube_color_pos[i_pos][2] = corner_now_2
        cube_color_pos[i_pos][3] = cub_now#перенос последних граней и углов на предпоследнии 
        cube_color_pos[i_pos][4] = corner_now
        if i_pos == 0:
        elif i_pos == 1:
        elif i_pos == 2:
        elif i_pos == 3:            
        elif i_pos == 4:
        elif i_pos == 5:
    else:
        print("Error, move")
def color_rgbi(rgbi):
    #фунция получения цвета кубика рубика(необходимо донастроить!!!)
    if rgbi[0] > 450 and rgbi[0] < 700 and rgbi[1] > 100 and rgbi[1] < 400 and rgbi[2] > 150 and rgbi[2] < 400:
        return "RED"
    if rgbi[0] > 700 and rgbi[0] < 1100 and rgbi[1] > 300 and rgbi[1] < 600 and rgbi[2] > 300 and rgbi[2] < 600:
        return "ORANGE"
    elif rgbi[0] > 200 and rgbi[0] < 350 and rgbi[1] > 350 and rgbi[1] < 700 and rgbi[2] > 200 and rgbi[2] < 500:
        return "GREEN"
    elif rgbi[0] > 50 and rgbi[0] < 350 and rgbi[1] > 250 and rgbi[1] < 600 and rgbi[2] > 350 and rgbi[2] < 800:
        return "BLUE"
    elif rgbi[0] > 800 and rgbi[0] < 1100 and rgbi[1] > 700 and rgbi[1] < 1100 and rgbi[2] > 550 and rgbi[2] < 800:
        return "YELLOW"
    elif rgbi[0] > 1000 and rgbi[0] < 1200 and rgbi[1] > 1000 and rgbi[1] < 1200 and rgbi[2] > 900 and rgbi[2] < 1200:
        return "WHITE"

"""async def scan():
    await motor.run_for_degrees(port.B, 470, 500)
    await color_sensor.color(port.A) is color.scan_now:
        for i in range (scan_now != COLOR[i]):
            if scan_now == COLOR[i]:
                scan_color.append(scan_now)
    rotate(qw)
    for j in range (4):
        for i in range(size):
            await color_sensor.color(port.A) is color.scan_now:
            for i in range (scan_now != COLOR[i]):
                if scan_now == COLOR[i]:
                    scan_color.append(scan_now)
                    rotat(45)
        rotate()
    rotat(90)
    turn()"""
async def scan_3x3(i, cube_color_pos, posituon_scan_base):
    #функция сканирования одной стороны
    await motor.run_for_degrees(port.B, -130, 500, stop=motor.SMART_BRAKE)#перемещаемся на кубик под центром
    cube_color_pos[i][1] = color_rgbi(color_sensor.rgbi(port.A))#сканируем и записываем на соответсвующую грень
    for j in range(7):
        runloop.run(rotate(45))#вращаем для счивывания каждого куба
        if j%2 == 0:
            if j == 0 :
                await motor.run_for_degrees(port.B, -60, 500, stop=motor.SMART_BRAKE)#корректируем положение датчика цвета на крайний куб
            await motor.run_for_degrees(port.B, -30, 500, stop=motor.SMART_BRAKE)#корректируем положение датчика цвета на крайний куб
        else:
            await motor.run_for_degrees(port.B, 30, 500, stop=motor.SMART_BRAKE)#корректируем положение датчика цвета на средний куб
        cube_color_pos[i][j+2] = color_rgbi(color_sensor.rgbi(port.A))#сканируем и записываем на соответстсвующую грань
    runloop.run(rotate(45))#выравниваем куб
    await motor.run_for_degrees(port.B, -305, 500, stop=motor.SMART_BRAKE)#возвращаем датчик цвета в положение чтения нижнего куба от центра

def calibr():
#функция высталвения кубика в нулевое положение
    calibr_bool = False#переменная означающая завершение калибровки
    calibr_time = 0
    while not calibr_bool:#цикл выставления более 300 нажатий не может быть так как этого достаточно
    #для полноценного выставления нулевого положения
        calibr_time += 1#счётчик нажатия
        if button.pressed(button.LEFT) is True:
            runloop.run(rotate(3))#небольшой поворот в правую сторону
        if button.pressed(button.RIGHT) is True:
            runloop.run(rotate(-3))#небольшой поворот в правую сторону
        if calibr == True:#выход из цикла если условие сканирования сработало
            break
        calibr_time = time.ticks_ms()
        while button.pressed(button.LEFT):
            if time.ticks_ms() - calibr_time > 1000:
                calibr_bool = True
                break

async def scan_full(cube_color_pos):
    #функция полного сканирования
    now_color = None#переменная для хранения цвета центра
    for i in range(6):#перечисляем все грани
        await motor.run_for_degrees(port.B, 485, 800, stop=motor.SMART_BRAKE)#выставляем мотор на центер кубика рубика
        now_color = color_rgbi(color_sensor.rgbi(port.A))#получаем цвет первой стороны сканирования
        cube_color_pos[i][0] = now_color #записываем сторону в массив и её первое значение которое означает центр
        runloop.run(scan_3x3(i,cube_color_pos, posituon_scan_base))#вызываем функцию сканирования одной стороны
        if i == 3:#если наша сторона 4 то мы поворачиваем кубив в другую сторону с целью сканирования всех 6 граней
            runloop.run(rotate(90))
        runloop.run(turn(1))
        if i == 4:#если нынешняя сторона сторона 5 то переворачиваем дважды для выбора последней стороны
            runloop.run(turn(1))

def cube_edge_search(eage_cubes_pos, index):
    for j in range(index):#поиск 4 частей креста кубика
        if eage_cubes_pos[j][0] >= 0 and eage_cubes_pos[j][0] <=3:#если сторона кубика принадлежит 1 из у граней идущих по порядку
            if eage_cubes_pos[j][1] == 1:#если нижняя сторона креста кубика
                if eage_cubes_pos[j][0] !=3:#проверяем равно ли 3 или нет то есть равно ли крайней гране из 4
                    eage_cubes_pos[j][2] = eage_cubes_pos[j][0] + 1 #если не равно третьему то берём слудующую сторону
                    eage_cubes_pos[j][3] = 5#вернхий верхнюю грань
                else:#если грань крайняя то берём перую и её верхний куб
                    eage_cubes_pos[j][2] = 0
                    eage_cubes_pos[j][3] = 5
            elif eage_cubes_pos[j][1] == 5:#если гнать верхняя
                if eage_cubes_pos[j][0] !=0:#определяем не последняя ли сторона
                    eage_cubes_pos[j][2] = eage_cubes_pos[j][0] - 1#если не последняя то выбираем предыдущую сторону
                    eage_cubes_pos[j][3] = 1#и выбираем нижнюю грань
                else: #если сторона первая то выбираем четвёртую сторону
                    eage_cubes_pos[j][2] = 3
                    eage_cubes_pos[j][3] = 1#нижнюю грань
            elif eage_cubes_pos[j][1] == 3:#если у нас правая грань
                eage_cubes_pos[j][2] = 4#то выбираем в любом случае четвёртую сторону
                if eage_cubes_pos[j][0] == 0:#проверяем на какой из сторон белая грань и соответсвно выбираем соседа
                    eage_cubes_pos[j][3] = 5
                elif eage_cubes_pos[j][0] == 1:
                    eage_cubes_pos[j][3] = 7
                elif eage_cubes_pos[j][0] == 2:
                    eage_cubes_pos[j][3] = 1
                else:
                    eage_cubes_pos[j][3] = 3
            else: #если у нас левая грань
                eage_cubes_pos[j][2] = 5#то выбираем в любом случае четвёртую сторону
                if eage_cubes_pos[j][0] == 0:#проверяем на какой из сторон белая грань и соответсвно выбираем соседа
                    eage_cubes_pos[j][3] = 1
                elif eage_cubes_pos[j][0] == 1:
                    eage_cubes_pos[j][3] = 7
                elif eage_cubes_pos[j][0] == 2:
                    eage_cubes_pos[j][3] = 5
                else:
                    eage_cubes_pos[j][3] = 3
        elif eage_cubes_pos[j][0] == 4:
            if eage_cubes_pos[j][0] == 1:#нижняя грань стороны
                eage_cubes_pos[j][2] = 2
            elif eage_cubes_pos[j][0] == 3:#правая грань стороны
                eage_cubes_pos[j][2] = 3
            elif eage_cubes_pos[j][0] == 5:#верхняя грань стороны
                eage_cubes_pos[j][2] = 0
            else:#левая грань стороны
                eage_cubes_pos[j][2] = 1
            eage_cubes_pos[j][3] = 3
        else:
            if eage_cubes_pos[j][0] == 1:#нижняя грань стороны
                eage_cubes_pos[j][2] = 0
            elif eage_cubes_pos[j][0] == 3:#правая грань стороны
                eage_cubes_pos[j][2] = 3
            elif eage_cubes_pos[j][0] == 5:#верхняя грань стороны
                eage_cubes_pos[j][2] = 2
            else:#левая грань стороны
                eage_cubes_pos[j][2] = 1
            eage_cubes_pos[j][3] = 7
    return eage_cubes_pos
async def assembly_white():
    #функция сбора белой стороны
    white_cubes_pos = None
    pos_i = 0
    for i in range(12):#поиск 12 граней
        for j in range(6):
            for k in range(9):
                if cube_color_pos[j][k] == "WHITE":#поиск белых кубов
                    white_cubes_pos[i][0] = j#если мы наши белый куб то записываем первым сторону на которой он
                    white_cubes_pos[i][1] = k#вторым позиция на которой он находится
                elif cube_color_pos[j][k] == "YELLOW"#поиск желтых кубов
                    white_cubes_pos[i][0] = j#если мы наши белый куб то записываем первым сторону на которой он
                    white_cubes_pos[i][1] = k#вторым позиция на которой он находится
                elif cube_color_pos[j][k] == "BLUE" or cube_color_pos[j][k] == "GREEN"#поиск кубов не принадлежащих белым или желтым но являющиеся граням
                    if j >= 0 and j <= 3:
                        if k == 1:
                            if j != 3:
                                if cube_color_pos[j+1][5] != "YELLOW" and cube_color_pos[j+1][5] != "WHITE":
                                    white_cubes_pos[i][0] = j#если мы наши белый куб то записываем первым сторону на которой он
                                    white_cubes_pos[i][1] = k#вторым позиция на которой он находится
                            else:
                                if cube_color_pos[0][5] != "YELLOW" and cube_color_pos[0][5] != "WHITE":
                                    white_cubes_pos[i][0] = j#если мы наши белый куб то записываем первым сторону на которой он
                                    white_cubes_pos[i][1] = k#вторым позиция на которой он находится
                        elif k == 5:
                            if j !=0:
                                if cube_color_pos[j-1][1] != "YELLOW" and cube_color_pos[j-1][1] != "WHITE":
                                    white_cubes_pos[i][0] = j
                                    white_cubes_pos[i][1] = k
                            else:
                                if cube_color_pos[3][1] != "YELLOW" and cube_color_pos[3][1] != "WHITE":
                                    white_cubes_pos[i][0] = j
                                    white_cubes_pos[i][1] = k
                        elif k == 3:
                            if j == 0:
                                if cube_color_pos[4][7] != "YELLOW" and cube_color_pos[4][7] != "WHITE":
                                    white_cubes_pos[i][0] = j
                                    white_cubes_pos[i][1] = k
                            elif j == 1:
                                if cube_color_pos[4][1] != "YELLOW" and cube_color_pos[4][1] != "WHITE":
                                    white_cubes_pos[i][0] = j
                                    white_cubes_pos[i][1] = k
                            elif j == 2:
                                if cube_color_pos[4][3] != "YELLOW" and cube_color_pos[4][3] != "WHITE":
                                    white_cubes_pos[i][0] = j
                                    white_cubes_pos[i][1] = k
                            elif j == 3:
                                if cube_color_pos[4][5] != "YELLOW" and cube_color_pos[4][5] != "WHITE":
                                    white_cubes_pos[i][0] = j
                                    white_cubes_pos[i][1] = k
                        elif k == 7:
                            if j == 0:
                                if cube_color_pos[4][7] != "YELLOW" and cube_color_pos[4][7] != "WHITE":
                                    white_cubes_pos[i][0] = j
                                    white_cubes_pos[i][1] = k
                            elif j == 1:
                                if cube_color_pos[4][5] != "YELLOW" and cube_color_pos[4][5] != "WHITE":
                                    white_cubes_pos[i][0] = j
                                    white_cubes_pos[i][1] = k
                            elif j == 2:
                                if cube_color_pos[4][3] != "YELLOW" and cube_color_pos[4][3] != "WHITE":
                                    white_cubes_pos[i][0] = j
                                    white_cubes_pos[i][1] = k
                            elif j == 3:
                                if cube_color_pos[4][1] != "YELLOW" and cube_color_pos[4][1] != "WHITE":
                                    white_cubes_pos[i][0] = j
                                    white_cubes_pos[i][1] = k
                    elif j == 4:
                        if k == 1:
                            if cube_color_pos[1][3] != "YELLOW" and cube_color_pos[1][3] != "WHITE":
                                    white_cubes_pos[i][0] = j
                                    white_cubes_pos[i][1] = k
                        elif k == 5:
                            if cube_color_pos[3][3] != "YELLOW" and cube_color_pos[3][3] != "WHITE":
                                    white_cubes_pos[i][0] = j
                                    white_cubes_pos[i][1] = k
                        elif k == 3:
                            if cube_color_pos[2][3] != "YELLOW" and cube_color_pos[2][3] != "WHITE":
                                    white_cubes_pos[i][0] = j
                                    white_cubes_pos[i][1] = k
                        elif k == 7:
                            if cube_color_pos[0][3] != "YELLOW" and cube_color_pos[0][3] != "WHITE":
                                    white_cubes_pos[i][0] = j
                                    white_cubes_pos[i][1] = k
                    elif j == 5:
                        if k == 1:
                            if cube_color_pos[3][3] != "YELLOW" and cube_color_pos[3][3] != "WHITE":
                                    white_cubes_pos[i][0] = j
                                    white_cubes_pos[i][1] = k
                        elif k == 5:
                            if cube_color_pos[1][3] != "YELLOW" and cube_color_pos[1][3] != "WHITE":
                                    white_cubes_pos[i][0] = j
                                    white_cubes_pos[i][1] = k
                        elif k == 3:
                            if cube_color_pos[2][3] != "YELLOW" and cube_color_pos[2][3] != "WHITE":
                                    white_cubes_pos[i][0] = j
                                    white_cubes_pos[i][1] = k
                        elif k == 7:
                            if cube_color_pos[0][3] != "YELLOW" and cube_color_pos[0][3] != "WHITE":
                                    white_cubes_pos[i][0] = j
                                    white_cubes_pos[i][1] = k

    white_cubes_pos = cube_edge_search(white_cubes_pos, 4)
    for i in range(6):#поиск относительной сканирования позиции цветов
        for j in range(6):
            if cube_color_pos[i][0] == COLOR[j]:
                COLOR_reletive_pos[j] = i
    for i in range(4):
        if white_cubes_pos[i][0] != COLOR_reletive_pos.WHITE:
            if white_cubes_pos[i][0] == COLOR_reletive_pos.YELLOW:#алгоритм для желтого цвета
                if i == 0:
                    if COLOR_reletive_pos.YELLOW >= 0 and COLOR_reletive_pos.YELLOW <= 3:
                        if COLOR_reletive_pos.YELLOW == 0:
                            await rotate(-90)
                        elif COLOR_reletive_pos.YELLOW == 1:
                            await rotate(-180)
                        elif COLOR_reletive_pos.YELLOW == 2:
                            await rotate(90)
                        await turn(1)
                    elif COLOR_reletive_pos.YELLOW == 4:
                        await turn(2)
                if white_cubes_pos[i][1] == 1:
                    await turn(3)
                    await fixation()
                    await rotate(180)
                    await return_fixation()
                    await turn(2)
                elif white_cubes_pos[i][1] == 3:
                    await rotate(90)
                    await turn(3)
                    await fixation()
                    await rotate(180)
                    await return_fixation()
                    await turn(2)
                elif white_cubes_pos[i][1] == 5:
                    await turn(1)
                    await fixation()
                    await rotate(180)
                    await return_fixation()
                    await turn(2)
                elif white_cubes_pos[i][1] == 7:
                    await rotate(90)
                    await turn(1)
                    await fixation()
                    await rotate(180)
                    await return_fixation()
                    await turn(2)
                else:
                    print("Not found on yellow edge white cubs")
            elif white_cubes_pos[i][1] == 5:
"""async def main():
    runloop.run(scan_full(cube_color_pos))#запуск полного сканирования кубика
runloop.run(motor.run_for_degrees(port.B, 480,500, stop=motor.SMART_BRAKE))
runloop.sleep_ms(10)
cube_color_pos[0][0] = color_rgbi(color_sensor.rgbi(port.A))
runloop.run(motor.run_for_degrees(port.B, -130,500, stop=motor.SMART_BRAKE))
runloop.sleep_ms(10)
cube_color_pos[0][1] = color_rgbi(color_sensor.rgbi(port.A))
runloop.run(rotate(45))
runloop.run(motor.run_for_degrees(port.B, -60,500, stop=motor.SMART_BRAKE))
cube_color_pos[0][2] = color_rgbi(color_sensor.rgbi(port.A))
runloop.run(rotate(45))
runloop.run(motor.run_for_degrees(port.B, 30,500, stop=motor.SMART_BRAKE))
cube_color_pos[0][3] = color_rgbi(color_sensor.rgbi(port.A))
runloop.run(scan_3x3(0,cube_color_pos, 3))"""

#тестирования переписовки поворота кубика
"""cube_color_pos = [["WHITE","WHITE","RED", "YELLOW", "RED", "BLUE","BLUE","RED","RED"],["ORANGE","WHITE","WHITE", "RED", "GREEN", "ORANGE","GREEN","WHITE","ORANGE"],
["YELLOW","BLUE","YELLOW", "GREEN", "ORANGE", "RED","BLUE","BLUE","YELLOW"],["RED","WHITE","BLUE", "BLUE", "ORANGE", "RED","ORANGE","GREEN","WHITE"],
["GREEN","GREEN","GREEN", "ORANGE", "BLUE", "ORANGE","YELLOW","ORANGE","YELLOW"],["BLUE","YELLOW","GREEN", "YELLOW", "WHITE", "GREEN","WHITE","YELLOW","RED"]]
COLOR_reletive_pos.update({"WHITE" : 0})
COLOR_reletive_pos.update({"ORANGE" : 1})
COLOR_reletive_pos.update({"RED" : 3})
COLOR_reletive_pos.update({"BLUE" : 5})
COLOR_reletive_pos.update({"GREEN" : 4})
COLOR_reletive_pos.update({"YELLOW" : 2})
move_cube(cube_color_pos, 0, "WHITE", COLOR_reletive_pos)
print(cube_color_pos)"""