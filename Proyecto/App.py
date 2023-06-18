import os, requests, json, gestionClientes, gestionEnvios, gestionEstadisticas, gestionPagos, gestionProductos, gestionVentas

class App:
  productos="Productos.txt"
  clientes="Clientes.txt"
  envios="Envios.txt"
  ventas="Ventas.txt"
  pagos="Pagos.txt"
  estadisticas="Estadisticas.txt"
  
  def borrado_datos():
    for i in [productos, clientes, envios, ventas, pagos, estadisticas]:
        if os.path.exists(i):
            os.remove(i)

  def pre_cargado():
    url="https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-3/api-proyecto/e20c412e7e1dcc3b089b0594b5a42f30ac15e49b/products.json"
    with open(productos, "w") as p:
        p.write(requests.get(url).text)
