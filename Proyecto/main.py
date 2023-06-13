import os, requests, json

def pre_cargado():
    url="https://github.com/Algoritmos-y-Programacion-2223-3/api-proyecto/blob/main/products.json"
    productos=requests.get(url).text

def main():
    while True:
        print(
            "Bienvenido al sistema en línea de la tienda de productos naturales.\n"
            "1.- Gestionar productos\n"
            "2.- Gestionar ventas\n"
            "3.- Gestionar clientes\n"
            "4.- Gestionar pagos\n"
            "5.- Gestionar envíos\n"
            "6.- Visualizar estadísticas\n"
            "7.- Reestablecer el estado inicial del programa\n"
            "8.- Salir"
              )
        while True:
            opcion=input("Ingrese el número de la acción a realizar: ")
            if opcion not in ["1", "2", "3", "4", "5", "6", "7", "8"]:
                print("ADVERTENCIA: Por favor ingrese un número de acción válido.")
                continue
            break
        if opcion=="1":
            pre_cargado()
        
        if opcion=="2":
            continue

        if opcion=="3":
            continue

        if opcion=="4":
            continue

        if opcion=="5":
            continue

        if opcion=="6":
            continue

        if opcion=="8":
            confirmación=input("¿Está seguro de que quiere salir del programa?    Y/N\n")
            if confirmación.upper()=="Y":
                print("Muchas gracias por usar nuestro programa".center(50, "-"))
                break


if __name__=="__main__":
    pre_cargado()