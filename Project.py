import time
from pymultiwii import MultiWii
from bme280 import readAltitude
import Constantes

SET_MOTOR = 214

serialPort = "/dev/ttyUSB0"
board = MultiWii(serialPort)
Acc_Cal = raw_input("Desea Calibrar el Acelerometro? Y/N: ")
if Acc_Cal == 'Y':
#Calibracion del Acelerometro 
	print(".")
	print(". .")
	print(". . .")
	print("Acelerometro Calibrado!")
	board.sendCMD(0, MultiWii.ACC_CALIBRATION, [])
else:
	pass

board.getData(MultiWii.RAW_IMU)
print("Lectura Inicial del Acelerometro:\tX: " + str(board.rawIMU['ax']) + " Y: " + str(board.rawIMU['ay']) + " Z: " + str(board.rawIMU['az']))
#Obtener Altitud
#Altitude = readAltitude()
#print("Altitud Inicial:" + str(Altitude))
#auxAlt = Altitude
#Almacenamiento de la constante auxiliar
#File = open("Constantes.py", "w")
#File.write(str(auxAlt) + "\n")
#File.close
#File = open("Constantes.py", "r")
#auxAlt = File.read()
#File.close
#Height = Altitude - float(auxAlt)
#print("Altura Inicial: " + str(Height))

#Potencia General Inicial de Motores
Power = int(input("Digite un Valor de Potencia para los Motores entre [1000-2000]: "))
#Ganancia Individual de los Motores
print("La Ganancia Inicial de los Motores sera igual a 1")
GM1,GM2,GM3,GM4 = 1,1,1,1

while True:
	try:
		if True:
			#Altitude = readAltitude()		
			#Height = Altitude - float(auxAlt)
			#print("Altura Actual: " + str(Altitude)) 
			board.getData(MultiWii.RAW_IMU)
			print("\t\t\tDatos de Vuelo:")
			print("Lectura Actual del Acelerometro:\tX: " + str(board.rawIMU['ax']) + " Y: " + str(board.rawIMU['ay']) + " Z: " + str(board.rawIMU['az']))
			#board.getData(MultiWii.ATTITUDE)
			#print("Orientacion:")
			#print("Pitch: " + str(board.attitude['angx']) + " Roll: " + str(board.attitude['angy']))
			#print("Aceleracion en Z: " + str(board.attitude['heading']))
			#print("Lectura del Giroscopio:")
			#print("X: " + str(board.rawIMU['gx']) + " Y: " + str(board.rawIMU['gy']) + " Z: " + str(board.rawIMU['gz']))
			#ROLL/PITCH/YAW/THROTTLE/AUX1/AUX2 -> Receptor de 6 canales.
			#M4(CW)-M2(CCW)                                           
			#      ^                                          		
			#M3(CCW)-M1(CW) Configuracion en X
			#print("Altura:" + str(Height) + " m\n")
  
			print("Ganancia Actual de los Motores:\t\t[" + str(GM1) + "," + str(GM2) + "," + str(GM3) + "," + str(GM4) + "]")
			#Asignar Potencia a los Motores
			Throttle = [GM1*Power,GM2*Power,GM3*Power,GM4*Power] #M1/M2/M3/M4			
			print("Potencia Actual de los Motores:\t\t[" + str(Throttle[0]) + "," + str(Throttle[1]) + "," + str(Throttle[2]) + "," + str(Throttle[3]) + "]")
			#Aceleracion de los Motores
			board.sendCMD(8,SET_MOTOR,Throttle)
           		#Modificar Ganancia de los Motores
			Mod_Gain = raw_input("Desea Cambiar la Ganancia de los Motores?  Y/N: ")
                        if Mod_Gain == 'Y':
                                print("Digite un Valor entre 0-100%: ")
                                GM1 = (float(input("Asignar Ganancia del Motor 1: "))/100)
                                GM2 = (float(input("Asignar Ganancia del Motor 2: "))/100)
                                GM3 = (float(input("Asignar Ganancia del Motor 3: "))/100)
                                GM4 = (float(input("Asignar Ganancia del Motor 4: "))/100)
                        else:
                                pass

	except KeyboardInterrupt:
		Throttle = [1000,1000,1000,1000]			
		board.sendCMD(8,SET_MOTOR,Throttle)
		print("\n")
		break
