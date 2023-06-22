import os, requests, json, gestionClientes, gestionEnvios, gestionEstadisticas, gestionPagos, gestionProductos, gestionVentas

class App:
  productos="Productos.json"
  clientes="Clientes.json"
  envios="Envios.json"
  ventas="Ventas.json"
  pagos="Pagos.json"
  estadisticas="Estadisticas.json"
  
  def _borrado_datos(self): 
    for i in [App.productos, App.clientes, App.envios, App.ventas, App.pagos, App.estadisticas]:
      os.remove(i)

  def _pre_cargado(self):
    url="https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-3/api-proyecto/e20c412e7e1dcc3b089b0594b5a42f30ac15e49b/products.json"
    p=requests.get(url).json()
    for i in p:
      i["disponibilidad"]=10
    with open(App.productos, "w") as P_file:
      json.dump(p, P_file, indent=2)
    for i in [App.clientes, App.envios, App.ventas, App.pagos, App.estadisticas]:
      with open(i, "w") as f:
        json.dump([], f, indent=2)

  def menu(self):
    print(
      "[ Menú ]".center(42, "-")+"\n"
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
        print("ADVERTENCIA: Por favor ingrese un número de acción válido")
        continue
      break

    if opcion=="1":
      gestionProductos.Producto(App.productos)
    
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

    elif opcion=="8":
      while True:
        confirmacion=input("¿Está seguro de que quiere salir del programa?    Y/N\n").upper()
        if confirmacion not in ["Y", "N"]:
          print("ADVERTENCIA: Por favor ingrese una opción válida")
          continue
        break

      if confirmacion=="Y":
        print("Muchas gracias por usar nuestro programa".center(50, "-"))
        self._borrado_datos()
        return

    return self.menu()
  
  def __init__(self):
    if not os.path.exists(App.productos):
      self._pre_cargado()
    print("\nBienvenido al sistema en línea de la tienda de productos naturales")
    self.menu()