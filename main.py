import color, color_sensor, motor, runloop
from hub import port 

COLOR[] = {"WHITE", "ORANGE", "GREEN", "RED", "BLUE", "YELLOW"} #Библиотека цветов нужно дополнить!
scan_now
size = 8
scan_color[]
qw = 30 #Сдвиг назад на клетку (нужно значени)

#переменные влада
# массив расположения цветов в кубике
cube_color_pos[6][9] = {{0,0,0,0,COLOR[0],0,0,0,0},{0,0,0,0,COLOR[1],0,0,0,0},
                    {0,0,0,0,COLOR[2],0,0,0,0},{0,0,0,0,COLOR[3],0,0,0,0},
                    {0,0,0,0,COLOR[4],0,0,0,0},{0,0,0,0,COLOR[5],0,0,0,0}} 
#массив соотносящихся значений которые выдаёт color_sensor с массивом COLOR то есть 
#число выдаваемое функцией сканирования цвета соответствует цвету из массива 
color_color_enser[] = {10,8,6,9,3,7}   

#констуркиця await подразумевает собой что наша программа откладывает выполнение программы 
#до тех пор пока мы не выполним какую либо функцию или что либо
#также необходимо функцию назначать async то есть асинхронной
#то есть что бы откладывать на потом программу необходимо прописывать ключевое слово о том 
#что мы выполняем это с возможностью отложения на потом программы 

async def turn():
    #функция поворота кубика 
    await motor.run_for_degrees(port.F, -180, 500)#поднятие механизма(поворот кубика)
    await motor.run_for_degrees(port.F, 180, 500)#опускание механизма(доворот кубика)

async def rotate(deg):
    #функция поворота кубика
    await motor.run_for_degrees(port.D, int(deg)*3, 500)#значения поворота уможается на 3 так как 
    #передаточное отношения поворота большого мотока к повороту корзины с кубиком равно 3 к 1

async def scan():
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
     turn()

async def scan_vlad():
    now_color = None
    name_color = None
    await motor.run_for_degrees(port.B, 470, 500)#выставляем мотор на центер кубика рубика
    await now_color = color_sensor.color(port.A)#переедаём в переменную полученый с сенсора
    #данные, они отображаются в виде цифры по этому необходимо их проеобраховать в название
    await for i in range(len(COLOR)):
            if now_color[i] is COLOR[i]:
                name_color = COLOR[i]
    await for i in range(LEN(COLOR)):
    

    
    


async def main():
    runloop.run(rotate(90))
    runloop.run(turn())   
runloop.run(scan())
    print("Ошибка")