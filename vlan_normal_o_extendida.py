import os
os.system("clear")
vlanNum = int(input("Ingrese un numero de VLAN: ")) 
if vlanNum >= 1 and vlanNum <= 1005: 
	print("Esta es una VLAN de Rango Normal") 
elif vlanNum >=1005 and vlanNum <= 4095: 
	print("Esta es una VLAN de Rango Extendida") 
else: 
	print("Esta no es una VLAN de Rango Extendida o Rango Normal.") 
