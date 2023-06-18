import App

def main():
    App.borrado_datos()
    App.pre_cargado()
    while True:
        print(
            "Bienvenido al sistema en línea de la tienda de productos naturales\n"
            "1.- Gestionar productos\n"
            "2.- Gestionar ventas\n"
            "3.- Gestionar clientes\n"
            "4.- Gestionar pagos\n"
            "5.- Gestionar envíos\n"
            "6.- Visualizar estadísticas\n"
            "7.- Reestablecer el estado inicial del programa\n"
            "8.- Salir\n"
              )
        while True:
            opcion=input("Ingrese el número de la acción a realizar: ")
            if opcion not in ["1", "2", "3", "4", "5", "6", "7", "8"]:
                print("ADVERTENCIA: Por favor ingrese un número de acción válido".center(67, "*"))
                continue
            break
        if opcion=="1":
            print(
                "1.- Agregar un nuevo producto\n"
                "2.- Buscar productos en la base de datos\n"
                "3.- Modificar información de productos existentes\n"
                "4.- Eliminar productos de la tienda\n"
            )
        
        elif opcion=="2":
            print(
                "1.- Registrar una nueva venta\n"
                "2.- Generar factura de compra\n"
                "3.- Buscar ventas en la base de datos\n"
            )

        elif opcion=="3":
            print(
                "1.- Registrar un nuevo cliente\n"
                "2.- Buscar clientes en la base de datos\n"
                "3.- Modificar información de clientes existentes\n"
                "4.- Eliminar clientes de la tienda\n"
            )

        elif opcion=="4":
            print(
                "1.- Registrar un nuevo pago\n"
                "2.- Buscar pagos en la base de datos\n"
            )

        elif opcion=="5":
            print(
                "1.- Registrar un nuevo envío\n"
                "2.- Buscar envíos en la base de datos\n"
            )

        elif opcion=="6":
            print(
                "1.- Estadísticas de ventas\n"
                "2.- Estadísticas de pagos\n"
                "3.- Estadísticas de envíos\n"
                "4.- Generar gráficos de estadísticas\n"
            )

        elif opcion=="7":
            while True:
                confirmacion=input("¿Está seguro de que quiere reestablecer el estado inicial del programa?    Y/N\n").upper()
      
                if confirmacion not in ["Y", "N"]:
                    print("Por favor ingrese una opción válida")
                    continue
                break

            if confirmacion=="Y":
                print("Se procederá a borrar los datos existentes y se cargarán los datos de pre-cargado".center(101, "*"))
                App.borrado_datos()
                App.pre_cargado()
                continue

        elif opcion=="8":
            while True:
                
                confirmacion=input("¿Está seguro de que quiere salir del programa?    Y/N\n").upper()

                if confirmacion not in ["Y", "N"]:
                    print("Por favor ingrese una opción válida")
                    continue
                break

            if confirmacion=="Y":
                print("Muchas gracias por usar nuestro programa".center(50, "-"))
                App.borrado_datos()
                break


if __name__=="__main__":
    main()