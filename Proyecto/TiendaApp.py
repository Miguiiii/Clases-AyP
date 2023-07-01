import os, requests, json, gestionClientes, gestionEnvios, gestionPagos, gestionProductos, gestionVentas

class App:
  #Establece los nombres de los archivos JSON en los que se almacenerá la información
  productos="Productos.json"
  clientes="Clientes.json"
  envios="Envios.json"
  ventas="Ventas.json"
  pagos="Pagos.json"
  estadisticas="Estadisticas.json"
  
  #Esta función elimina cada uno de los archivos JSON
  def _borrado_datos(self): 
    for i in [App.productos, App.clientes, App.envios, App.ventas, App.pagos, App.estadisticas]:
      os.remove(i)

  #Esta función crea cada uno de los archivos JSON, y escribe en ellos una base para el resto del programa
  #En el de productos escribe lo extraído de la API
  #En el de estadísticas escribe las diferentes estaísticas necesarias para las Ventas, Pagos, y Envíos, respectivamente, y las deja vacías
  #En el resto escribe una lista vacía
  def _pre_cargado(self):
    url="https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-3/api-proyecto/main/products.json"
    p=requests.get(url).json()
    with open(App.productos, "w") as P_file:
      json.dump(p, P_file, indent=2)
    for i in [App.clientes, App.envios, App.ventas, App.pagos, App.estadisticas]:
      with open(i, "w") as f:
        json.dump([], f, indent=2)
    with open(App.estadisticas, "w") as Est:
      stats={
        "Ventas":{
          "Totales":{},
          "Productos":{},
          "Frecuentes":{}
        },
        "Pagos":{
          "Totales":{},
          "Pendientes":{}
        },
        "Envios":{
          "Totales":{},
          "Productos":{},
          "Pendientes":{}
        }
      }
      json.dump(stats, Est, indent=2)

  def menu(self):
    #Opciones del menú principal de la aplicación
    print(
      "\n"+"[ Menú ]".center(42, "-")+"\n"
      "1.- Gestionar productos\n"
      "2.- Gestionar clientes\n"
      "3.- Gestionar ventas\n"
      "4.- Gestionar pagos\n"
      "5.- Gestionar envíos\n"
      "6.- Información\n"
      "7.- Reestablecer el estado inicial del programa\n"
      "8.- Salir\n"
    )
    while True:
      #Verificación de que se ingrese una opción válida
      opcion=input("Ingrese el número de la acción a realizar: ")
      if opcion=="Borrar base de datos": #Opcion secreta para que quien maneje el programa elimine los datos, no se supone que un usuario normal la use
        break
      if opcion not in ["1", "2", "3", "4", "5", "6", "7", "8"]:
        print("ADVERTENCIA: Por favor ingrese un número de acción válido")
        continue
      break

    if opcion=="1":
      #Llama al menú de Gestión de Productos y establece su archivo JSON (App.productos)
      gestionProductos.Producto(App.productos).menu()
    
    elif opcion=="2":
      #Hace lo mismo que la anterior
      gestionClientes.Cliente(App.clientes).menu()

    elif opcion=="3":
      #Las siguientes hacen lo mismo, pero también le pasan el nombre del JSON de las estadísticas
      gestionVentas.Venta(App.ventas, App.estadisticas).menu(App.ventas, App.estadisticas)

    elif opcion=="4":
      gestionPagos.Pago(App.pagos, App.estadisticas).menu(App.pagos, App.estadisticas)

    elif opcion=="5":
      gestionEnvios.Envio(App.envios, App.estadisticas).menu(App.envios, App.estadisticas)

    elif opcion=="6":
      #Explica brevemente lo esencial del programa
      print(
        "\n"+"[ Información ]".center(70, "-")+"\n\n"
        "PRODUCTOS: Esta aplicación viene con una serie de productos ya cargados en la base de datos,\n"
        "sin embargo, usted como usuario es libre de agregar, modificar, y eliminar productos a su placer.\n\n"
        "CLIENTES: El usuario de esta aplicación es libre de agregar, modificar y eliminar clientes\n"
        "de la base de datos de la tienda. Se le recomienda crear un cliente antes de registrar una venta.\n\n"
        "VENTAS: El usuario puede registrar ventas, para ello es necesario que exista al menos un cliente\n"
        "en la base de datos. Un mismo cliente puede ser asociado a varias ventas distitnas.\n\n"
        "PAGOS: El usuario puede registrar un pago perteneciente a una venta ya registrada. Es necesario\n"
        "tener registrado una venta para poder realizar un pago, y solo se puede registrar un pago por venta.\n\n"
        "ENVÍOS: El usuario puede registrar un envío perteneciente a un pago ya registrado. Es necesario\n"
        "tener registrado un pago para poder realizar un envío, y solo se puede registrar un envío por pago.\n\n"
        "ESTADÍSTICAS: El usuario puede visualizar las estadísticas de los últimos tres tipos de datos.\n\n"
        "BÚSQUEDA: El usuario puede buscar en la base de datos cualquiera de los datos anteriormente mencionados.\n"
      )
      input("Presione Enter para regresar al menú principal")

    elif opcion=="7":
      #Pregunta por una confirmación, y luego borra todos los archivos y vuelve a realizar el pre-cargado 
      while True:
        confirmacion=input("¿Está seguro de que quiere reestablecer el estado inicial del programa?\n"
                           "Se borrarán todos los datos actuales.    Y/N\n").upper()

        if confirmacion not in ["Y", "N"]:
          print("ADVERTENCIA: Por favor ingrese una opción válida")
          continue
        break

      if confirmacion=="Y":
        print("Se procederá a borrar los datos existentes y se cargarán los datos de pre-cargado".center(101, "*"))
        self._borrado_datos()
        self._pre_cargado()

    elif opcion=="8" or opcion=="Borrar base de datos":
      #Cierra la aplicación
      while True:
        confirmacion=input("¿Está seguro de que quiere salir del programa?    Y/N\n").upper()
        if confirmacion not in ["Y", "N"]:
          print("ADVERTENCIA: Por favor ingrese una opción válida")
          continue
        break

      if confirmacion=="Y":
        print("Muchas gracias por usar nuestro programa".center(50, "-"))
        if opcion=="Borrar base de datos": #Activa la opcion secreta de eliminar los datos
          self._borrado_datos()
        return

    #Esto hace que, a menos que eligas la opción 8, siempre se vuelva a mostar este mismo menú de la aplicación
    return self.menu()
  
  def __init__(self):
    #Revisa si ya existe el JSON de los productos, porque si existe, el resto también, y si no existen, llama a la función de pre-cargado
    if not os.path.exists(App.productos):
      self._pre_cargado()
    print("\nBienvenido al sistema en línea de la tienda de productos naturales")
    self.menu()