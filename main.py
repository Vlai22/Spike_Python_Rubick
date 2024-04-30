import color, color_sensor, motor, time
import runloop
from hub import port, button
import array as arr

COLOR = ["WHITE", "ORANGE", "GREEN", "RED", "BLUE", "YELLOW"] #Библиотека цветов нужно дополнить!
#scan_now
size = 8
#scan_color[]
qw = 30 #Сдвиг назад на клетку (нужно значени)

#переменные влада
# массив расположения цветов в кубике
cube_color_pos = 0
#массив соотносящихся значений которые выдаёт color_sensor с массивом COLOR то есть
#число выдаваемое функцией сканирования цвета соответствует цвету из массива
posituon_scan_base = 0
#констуркиця await подразумевает собой что наша программа откладывает выполнение программы
#до тех пор пока мы не выполним какую либо функцию или что либо
#также необходимо функцию назначать async то есть асинхронной
#то есть что бы откладывать на потом программу необходимо прописывать ключевое слово о том
#что мы выполняем это с возможностью отложения на потом программы
async def turn():
    #функция поворота кубика
    await motor.run_to_relative_position(port.F, -180, 600,,motor.SMART_BRAKE)#поднятие механизма(поворот кубика)
    await motor.run_to_relative_position(port.F, 180, 600,,motor.SMART_BRAKE)#опускание механизма(доворот кубика)

async def rotate(deg):
    #функция поворота кубика
    await motor.run_to_relative_position(port.D, int(deg)*3, 700,,motor.SMART_BRAKE)#значения поворота уможается на 3 так как
    #передаточное отношения поворота большого мотока к повороту корзины с кубиком равно 3 к 1

def color_rgbi(rgbi):
    #фунция получения цвета кубика рубика(необходимо донастроить!!!)
    if rgbi[0] > 450 and rgbi[0] < 700 and rgbi[1] > 100 and rgbi[1] < 300 and rgbi[2] > 150 and rgbi[2] < 400:
        return "RED"
    if rgbi[0] > 800 and rgbi[0] < 1100 and rgbi[1] > 350 and rgbi[1] < 600 and rgbi[2] > 300 and rgbi[2] < 600:
        return "ORANGE"
    if rgbi[0] > 200 and rgbi[0] < 350 and rgbi[1] > 350 and rgbi[1] < 700 and rgbi[2] > 200 and rgbi[2] < 500:
        return "GREEN"
    if rgbi[0] > 50 and rgbi[0] < 350 and rgbi[1] > 250 and rgbi[1] < 600 and rgbi[2] > 350 and rgbi[2] < 800:
        return "BLUE"
    if rgbi[0] > 700 and rgbi[0] < 1000 and rgbi[1] > 600 and rgbi[1] < 1000 and rgbi[2] > 550 and rgbi[2] < 800:
        return "YELLOW"
    if rgbi[0] > 1000 and rgbi[0] < 1200 and rgbi[1] > 1000 and rgbi[1] < 1200 and rgbi[2] > 900 and rgbi[2] < 1200:
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
async def scan_3x3(i):
    #функция сканирования одной стороны
    await motor.run_for_degrees(port.B, -140, 500)#перемещаемся на кубик под центром
    cube_color_pos[i][1] = color_rgbi(color_sensor.rgbi(port.A))#сканируем и записываем на соответсвующую грень
    for j in range(7)
        await rotate(45)#вращаем для счивывания каждого куба
        if j%2 == 0 
            await motor.run_for_degrees(port.B, -50, 600)#корректируем положение датчика цвета на крайний куб 
        else:
            await motor.run_for_degrees(port.B, 50, 600)#корректируем положение датчика цвета на средний куб
        cube_color_pos[i][j+2] = color_rgbi(color_sensor.rgbi(port.A))#сканируем и записываем на соответстсвующую грань
    await rotate(45)#выравниваем куб
    await motor.run_for_degrees(port.B, -350, 500)#возвращаем датчик цвета в положение чтения нижнего куба от центра

async def calibr():
#функция высталвения кубика в нулевое положение
    calibr_bool = False#переменная означающая завершение калибровки
    calibr_time = 0
    while calibr_time < 300:#цикл выставления более 300 нажатий не может быть так как этого достаточно 
    #для полноценного выставления нулевого положения
        calibr_time += 1#счётчик нажатия
        if button.pressed(button.LEFT) is True:
            time_start = time.ticks_ms()#переменная времени для отслеживания длительного нажатия
            while button.pressed(button.LEFT):#удерживание левой кнопки 
                if time.ticks_ms() - time_start > 1000:#условие запуска сканирования
                    calibr_bool = True
                    break
            if calibr_bool == False#если мы не удерживаем клавишу в течениии 1 секунды то чуть чуть поворачиваем корзину
                await rotate(3)
        if button.pressed(button.RIGHT) is True:
            await rotate(-3)#небольшой поворот в правую сторону
        if calibr == True:#выход из цикла если условие сканирования сработало
            break

async def scan_full():
    #функция полного сканирования
    now_color = None#переменная для хранения цвета центра
    for i in range(6):#перечисляем все грани
        posituon_scan_base = motor.relative_position(port.B)+10#конфигурация относитульного пложения с целью точной работы механизма
        await motor.run_to_relative_position(port.B, posituon_scan_base+485, 1000,,motor.SMART_BRAKE)#выставляем мотор на центер кубика рубика
        now_color = color_rgbi(color_sensor.rgbi(port.A))#получаем цвет первой стороны сканирования 
        cube_color_pos[i][0] = now_color#записываем сторону в массив и её первое значение которое означает центр
        runloop.run(scan_3x3(i))#вызываем функцию сканирования одной стороны
        if i == 3:#если наша сторона 4 то мы поворачиваем кубив в другую сторону с целью сканирования всех 6 граней
            await rotate(90)
        await turn()
        if i == 4:#если нынешняя сторона сторона 5 то переворачиваем дважды для выбора последней стороны 
            await turn()

async def assembly_white():
    #функция сбора белой стороны
    white_cubes_pos = 0 
    pos_i = 0
    pos_j = 0 
    for i in range(4):#сборка 4 граней белого креста
        for j in range(6):#поиск белых кубов 
            for k in range(9):
                if cube_color_pos[j][k] == "WHITE":
                    white_cubes_pos[i][0] = j#если мы наши белый куб то записываем первым сторону на которой он 
                    white_cubes_pos[i][1] = k#вторым позиция на которой он находится 
                    i+=1
        for j in range(4):#поиск 4 частей креста кубика
            if white_cubes_pos[j][0] >= 0 and white_cubes_pos[j][0] <=3:#если сторона кубика принадлежит 1 из у граней идущих по порядку
                if white_cubes_pos[j][1] == 1:
                    if white_cubes_pos[j][0] !=3 
                        white_cubes_pos[j][2] = white_cubes_pos[j][0] + 1
                        white_cubes_pos[j][3] = 5
                    else:
                        white_cubes_pos[j][2] = 0
                        white_cubes_pos[j][3] = 5
                elif white_cubes_pos[j][1] == 5
                    if white_cubes_pos[j][0] !=0:
                        white_cubes_pos[j][2] = white_cubes_pos[j][0] - 1
                        white_cubes_pos[j][3] = 1 
                    else: 
                        white_cubes_pos[j][2] = 3
                        white_cubes_pos[j][3] = 1
                elif white_cubes_pos[j][1] == 3:
                    white_cubes_posp[j][2] == 4
                    if white_cubes_pos 

            else:
                if white_cubes_pos[j][0] >= 0 and white_cubes_pos <= 3:
                    
                else: 





async def main():
    runloop.run(calibr())#запуск калибровки положения кубика
    runloop.run(scan_full())#запуск полного сканирования кубика

runloop.run(main())