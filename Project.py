import time
from pymultiwii import MultiWii
from bme280 import readAltitude

SET_MOTOR = 214

serialPort = "/dev/ttyUSB0"
board = MultiWii(serialPort)
#Calibracion del Acelerometro - No viable debido a construccion fisica del Drone.
#board.sendCMD(0, MultiWii.ACC_CALIBRATION, [])
#Obtener Altitud
Altitude = readAltitude()
auxAlt = Altitude

while True:
	try:
		#Normalizar Altura
		Height = 0 + (Altitude - auxAlt)
		print("Altura:" + Height)
		while Height <= 2:		
			board.getData(MultiWii.RAW_IMU)
			print("Lectura del Acelerometro:")
			print("X: " + str(board.rawIMU['ax']) + " Y: " + str(board.rawIMU['ay']) + " Z: " + str(board.rawIMU['az']))
			board.getData(MultiWii.ATTITUDE)
			print("Orientacion:")
			print("Pitch:" + str(board.attitude['angx']) + "Roll:" + str(board.attitude['angy']))
			print("Aceleracion en Z:" + str(board.attitude['heading']))
			#print("Lectura del Giroscopio:")
			#print("X: " + str(board.rawIMU['gx']) + " Y: " + str(board.rawIMU['gy']) + " Z: " + str(board.rawIMU['gz']))
			#ROLL/PITCH/YAW/THROTTLE/AUX1/AUX2 -> Receptor de 6 canales.
			#M4(CW)-M2(CCW)                                           
			#      ^                                          		
			#M3(CCW)-M1(CW) Configuracion en X
		
			data = [1000,1000,1000,1000] #M1/M2/M3/M4			
			board.sendCMD(8,SET_MOTOR,data)
	except KeyboardInterrupt:
		data = [1000,1000,1000,1000]			
		board.sendCMD(8,SET_MOTOR,data)
		break
