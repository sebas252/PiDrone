import time
from pymultiwii import MultiWii
from bme280 import readAltitude
import Constantes

SET_MOTOR = 214

serialPort = "/dev/ttyUSB0"
board = MultiWii(serialPort)
#Calibracion del Acelerometro - No viable debido a construccion fisica del Drone.
#board.sendCMD(0, MultiWii.ACC_CALIBRATION, [])
#Obtener Altitud
Altitude = readAltitude()
print("Altitud Inicial:" + str(Altitude))
auxAlt = Altitude
#Almacenamiento de la constante auxiliar
File = open("Constantes.py", "w")
File.write("Aux=" + str(auxAlt) + "\n")
File.close
Height = 0 + (Altitude - auxAlt)
#Potencia para armar Motores
M1,M2,M3,M4 = 1080,1080,1080,1080

while True:
	try:
		if True:		
			Height = 0 + (Altitude - float(Constantes.Aux)) 
			board.getData(MultiWii.RAW_IMU)
			print("Lectura del Acelerometro:")
			print("X: " + str(board.rawIMU['ax']) + " Y: " + str(board.rawIMU['ay']) + " Z: " + str(board.rawIMU['az']))
			board.getData(MultiWii.ATTITUDE)
			print("Orientacion:")
			print("Pitch: " + str(board.attitude['angx']) + " Roll: " + str(board.attitude['angy']))
			print("Aceleracion en Z: " + str(board.attitude['heading']))
			#print("Lectura del Giroscopio:")
			#print("X: " + str(board.rawIMU['gx']) + " Y: " + str(board.rawIMU['gy']) + " Z: " + str(board.rawIMU['gz']))
			#ROLL/PITCH/YAW/THROTTLE/AUX1/AUX2 -> Receptor de 6 canales.
			#M4(CW)-M2(CCW)                                           
			#      ^                                          		
			#M3(CCW)-M1(CW) Configuracion en X
			print("Altura:" + str(Height) + " m\n")
			#if board.attitude['angx'] < 0 and board.attitude['angy'] < 0:
			#	M2 += 50
			#	M3 += 50
			#	M4 += 100
			#if board.attitude['angx'] > 0 and board.attitude['angy']  
			data = [M1,M2,M3,M4] #M1/M2/M3/M4			
			board.sendCMD(8,SET_MOTOR,data)
	except KeyboardInterrupt:
		data = [1000,1000,1000,1000]			
		board.sendCMD(8,SET_MOTOR,data)
		print("\n")
		break
