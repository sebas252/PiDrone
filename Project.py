import time
from pymultiwii import MultiWii
#from bme280 import readAltitude
import Ganancias

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

#Obtencion de los Valores de Ganancia Obtenidos
File = open("Ganancias.py", "r")
File.read()
GM1 = float(Ganancias.GM1)
GM2 = float(Ganancias.GM2)
GM3 = float(Ganancias.GM3)
GM4 = float(Ganancias.GM4)
File.close

#G_M1 = GM1
#G_M2 = GM2
#G_M3 = GM3
#G_M4 = GM4

#Potencia General Inicial de Motores
Power = float(input("Digite un Valor de Potencia para los Motores entre [1000-2000]: "))
armPower = 1080
#Ganancia Unitaria Individual de los Motores
#print("La Ganancia Inicial de los Motores sera igual a 1")
#GM1,GM2,GM3,GM4 = 1,1,1,1

#Funcion para Realizar la Lectura de los Instrumentos de Vuelo
def Flight_Data(Throttle):
	board.getData(MultiWii.RAW_IMU)
	print("\n\t\t\tDatos de Vuelo:")
	print("Lectura Actual del Acelerometro:\tX: " + str(board.rawIMU['ax']) + " Y: " + str(board.rawIMU['ay']) + " Z: " + str(board.rawIMU['az']))
	board.getData(MultiWii.ATTITUDE)
	print("Orientacion de Vuelo:\t\t\tPitch: " + str(board.attitude['angx']) + " Roll: " + str(board.attitude['angy']))
	#print("Lectura del Giroscopio:")
	#print("X: " + str(board.rawIMU['gx']) + " Y: " + str(board.rawIMU['gy']) + " Z: " + str(board.rawIMU['gz']))
	#ROLL/PITCH/YAW/THROTTLE/AUX1/AUX2 -> Receptor de 6 canales.
	#M4(CW)-M2(CCW)
	#      ^
	#M3(CCW)-M1(CW) Configuracion en X
	#print("Altura:" + str(Height) + " m\n")
	print("Ganancia Actual de los Motores:\t\t[" + str(GM1) + "," + str(GM2) + "," + str(GM3) + "," + str(GM4) + "]")
	#Asignar Potencia a los Motores
	#Throttle = [GM1*Power,GM2*Power,GM3*Power,GM4*Power] #M1/M2/M3/M4
	print("Potencia Actual de los Motores:\t\t[" + str(Throttle[0]) + "," + str(Throttle[1]) + "," + str(Throttle[2]) + "," + str(Throttle[3]) + "]\n")

def Leveled_Flight(actualPower,desiredPower,GainM1,GainM2,GainM3,GainM4):
#Roll hacia la Derecha:			Valores Positivos.
#Roll hacia la Izquierda:		Valores Negativos.
#Pitch hacia Atras (Inclinar Nariz):	Valores Positivos.
#Pitch hacia Adelante (Declinar Nariz):	Valores Negativos.
	board.getData(MultiWii.ATTITUDE)
	Pitch = board.attitude['angx']
	Roll = board.attitude['angy']
	idealPitch = 0
	idealRoll = 0
	G_M1,G_M2,G_M3,G_M4 = GainM1,GainM2,GainM3,GainM4
	#Valores Recomendables para la Realimentacion y la Compensacion [0.001-0.1]
	Realim = 0.004
	Comp = 0.008

	if actualPower < desiredPower:
		if Pitch > idealPitch:
			#Realimentacion
			G_M2 -= Realim
			G_M4 -= Realim
			#Compensacion
			G_M1 += Comp
			G_M3 += Comp
	
		elif Pitch < idealPitch:
			#Realimentacion
			G_M1 -= Realim
			G_M3 -= Realim
			#Compensacion
			G_M2 += Comp
			G_M4 += Comp
	
		elif Roll > idealRoll:
			#Realimentacion
			G_M3 -= Realim
			G_M4 -= Realim
			#Compensacion
			G_M1 += Comp
			G_M2 += Comp

		elif Roll < idealRoll:
			#Realimentacion
			G_M1 -= Realim
			G_M2 -= Realim
			#Compensacion
			G_M3 += Comp
			G_M4 += Comp
	
		elif Pitch == idealPitch:
			pass
	
		elif Roll == idealRoll:
			pass
	
		actualPower += 5
		return actualPower,G_M1,G_M2,G_M3,G_M4
	
	elif actualPower == desiredPower:
		actualPower += 3
		return actualPower,G_M1,G_M2,G_M3,G_M4

	else:
		if Pitch > idealPitch:
                        #Realimentacion
                        G_M2 -= Realim
                        G_M4 -= Realim
                        #Compensacion
                        G_M1 += Comp
                        G_M3 += Comp

                elif Pitch < idealPitch:
                        #Realimentacion
                        G_M1 -= Realim
                        G_M3 -= Realim
                        #Compensacion
                        G_M2 += Comp
                        G_M4 += Comp

                elif Roll > idealRoll:
                        #Realimentacion
                        G_M3 -= Realim
                        G_M4 -= Realim
                        #Compensacion
                        G_M1 += Comp
                        G_M2 += Comp
		
		elif Roll < idealRoll:
                        #Realimentacion
                        G_M1 -= Realim
                        G_M2 -= Realim
                        #Compensacion
                        G_M3 += Comp
                        G_M4 += Comp

                elif Pitch == idealPitch:
                        pass

                elif Roll == idealRoll:
                        pass
		
		actualPower -= 5
		return actualPower,G_M1,G_M2,G_M3,G_M4

while True:
	try:  	                                    		
		flightPower,GM1,GM2,GM3,GM4 = Leveled_Flight(armPower,Power,GM1,GM2,GM3,GM4)
		armPower = flightPower
		Throttle = [GM1*flightPower,GM2*flightPower,GM3*flightPower,GM4*flightPower] #M1/M2/M3/M4
		Flight_Data(Throttle)
		#Aceleracion de los Motores
		board.sendCMD(8,SET_MOTOR,Throttle)
        	#Modificar Ganancia de los Motores
		#Mod_Gain = raw_input("Desea Cambiar la Ganancia de los Motores?  Y/N: ")
                #if Mod_Gain == 'Y':
        	#       print("Digite un Valor entre 0-100%: ")
                #	GM1 = (float(input("Asignar Ganancia del Motor 1: "))/100)
                #       GM2 = (float(input("Asignar Ganancia del Motor 2: "))/100)
                #       GM3 = (float(input("Asignar Ganancia del Motor 3: "))/100)
                #       GM4 = (float(input("Asignar Ganancia del Motor 4: "))/100)
                #else:
                #       pass
		Mod_Power = raw_input("Desea Modificar la Potencia General de los Motores? Y/N: ")
		if Mod_Power == 'Y':
			Power = float(input("Digite con Precaucion un valor entre [1000-2000]: "))
		else:
			pass

	except KeyboardInterrupt:
		Throttle = [1000,1000,1000,1000]			
		board.sendCMD(8,SET_MOTOR,Throttle)
		#Almacenamiento de Cambios en Ganancias
		File = open("Ganancias.py", "w")
		#File.write("GM1 = " + str(GM1) + "\nGM2 = " + str(GM2) + "\nGM3 = " + str(GM3) + "\nGM4 = " + str(GM4) + "\n")
		#Reinicializacion de las Ganancias
		File.write("GM1 = 1\nGM2 = 1\nGM3 = 1\nGM4 = 1\n")
		File.close
		#print("\nGanancias Almacenadas Correctamente en el Archivo Ganancias.py\n")
		print("\nGanancias Reinicializadas\n")
		break
