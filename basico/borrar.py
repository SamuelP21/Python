my_dict = {"Nombre": "Brais", "Apellido": "Moure", "Edad": 35, 1: "Python"}

for element in my_dict.values():
    print(element)
    if element == "Edad":
        break
else:
    print("El bluce for para diccionario ha finalizado")

for element in my_dict:
    print(element)
    if element == "Edad":
        continue
    print("Se ejecuta")
else:
    print("El bluce for para diccionario ha finalizado")

class person:
    def __init__(self):
        pass