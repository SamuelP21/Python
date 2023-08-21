### Lists ###

# Definición

my_list = list()
my_other_list = []

print(len(my_list))

my_list = [35, 24, 62, 52, 30, 30, 17]

print(my_list)
print(len(my_list))

my_other_list = [28, 1.67, "Samuel", "Zabla"]

print(type(my_list))
print(type(my_other_list))

# Acceso a elementos y búsqueda

print(my_other_list[0])
print(my_other_list[1])
print(my_other_list[-1])
print(my_other_list[-4])
print(my_list.count(30)) # cuenta la cantidad de elementos de la lista en este caso con el valor 30 
# print(my_other_list[4]) IndexError
# print(my_other_list[-5]) IndexError

print(my_other_list.index("Zabala"))

age, height, name, surname = my_other_list
print(name)

name, height, age, surname = my_other_list[2], my_other_list[1], my_other_list[0], my_other_list[3]
print(age)

# Concatenación

print(my_list + my_other_list)
#print(my_list - my_other_list)

# Creación, inserción, actualización y eliminación

my_other_list.append("SamuelZP8") #lo inserta al final de la lista
print(my_other_list)

my_other_list.insert(1, "Rojo") # le decimos en que posicion lo vamos a insertar
print(my_other_list)

my_other_list[1] = "Azul"
print(my_other_list)

my_other_list.remove("Azul")
print(my_other_list)

my_list.remove(30)
print(my_list)

print(my_list.pop())# pop elimina el ultimo y devuelve el valor que hemos eliminado de la lista
print(my_list)

my_pop_element = my_list.pop(2) # aqui le digo el el indice 2 lo desapile y lo devuelva
print(my_pop_element)
print(my_list)

del my_list[2] #elimina de la lista el indice 2 sin retorno
print(my_list)

# Operaciones con listas

my_new_list = my_list.copy()

my_list.clear()
print(my_list)
print(my_new_list)

my_new_list.reverse() # se le da la vuelta a la lista
print(my_new_list)

my_new_list.sort() # ordena en forma ascendente
print(my_new_list)

# Sublistas

print(my_new_list[1:3])

# Cambio de tipo

my_list = "Hola Python"
print(my_list)
print(type(my_list))