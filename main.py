import color, color_sensor, motor, runloop
from hub import port 

COLOR[] = {"WHITE", "RED", "GREEN"} #Библиотека цветов нужно дополнить!
scan_now
size = 8
scan_color[]
qw = 30 #Сдвиг назад на клетку (нужно значени)

async def turn():
    #функция поворота кубика 
    await motor.run_for_degrees(port.F, -180, 500)#поднятие механизма(поворот кубика)
    await motor.run_for_degrees(port.F, 180, 500)#опускание механизма(доворот кубика)

async def rotate(deg):
    await motor.run_for_degrees(port.D, int(deg)*3, 500)

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
async def main():
    runloop.run(rotate(90))
    runloop.run(turn())   
runloop.run(scan())
    print("Ошибка")