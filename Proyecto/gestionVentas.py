import json
from BusquedaAvanzada import Avanzada as IB
from gestionClientes import Cliente as C
from gestionProductos import Producto as P
import datetime as DT
class Venta(IB):

    def _buscar_cliente(self):
        #Crea un objeto de Cliente, el cual permite identificar un cliente en la base de datos
        print("Busque el cliente al que quiere registrar en la venta")
        cliente=C("Clientes.json")
        self.IdCliente=cliente.identificar(cliente.search_keys)
        if self.IdCliente==False:
            print("ADVERTENCIA: Se necesita un cliente registrado para registrar una venta")
            while True:
                cancelar=input("Quiere cancelar el registro de esta venta?    Y/N\n").upper()
                if cancelar not in ["Y", "N"]:
                    print("ADVERTENCIA: Por favor ingrese una opción válida")
                    continue
                break
            if cancelar=="Y":
                #Esto permite cancelar la compra si no encuentras un cliente, o si prefieres no realizarla en este punto
                print("Registro de venta CANCELADO".center(40, "*"))
                return False
            else:
                self._buscar_cliente()
        
    def _buscar_productos(self):
        #Crea un objeto de producto y es usado para extraer productos, su cantidad para comprar y su índice en la base de datos (esto último por si se cancela la venta)
        print("Busque los productos que desea comprar")
        prod=P("Productos.json")
        self.l_productos_comprados={}
        self.l_index_productos=[]
        while True:
            encontrado=prod.reinsertar(prod.l_keys, prod.search_keys, venta=True)
            if encontrado==False:
                continue
            ind, comp=encontrado
            cant=comp.pop("quantity")
            comp.pop("description")
            comp.pop("category")
            comp=tuple(comp.items())
            #Una venta solo guarda el nombre y precio de un producto (además de la cantidad comprada)
            self.l_productos_comprados[comp]=self.l_productos_comprados.get(comp, 0)+cant
            if len(self.l_productos_comprados)>len(self.l_index_productos):
                self.l_index_productos.append(ind)
            
            #Este bloque muestra los productos que se han añadido hasta el momento, su cantidad y el precio de cada uno (tomando en cuenta la cantidad en el carrito)
            print("\n"+60*"-"+"\n")
            print("Carrito de compra:\n")
            print(
                f"Cantidad - Producto".ljust(45, " ")+"Costo".rjust(15, " ")+"\n"
                )
            for p, c in self.l_productos_comprados.items():
                nombre, precio=p[0][1], p[1][1]
                print(
                    f"{c}","{}".format(nombre).ljust(45, " ")+f"{precio*c}".rjust(12, " ")
                    )
            print("\n"+60*"-"+"\n")
            while True:
                continuar=input("Quiere continuar agregando productos al carrito de venta?    Y/N\n").upper()
                if continuar not in ["Y", "N"]:
                    print("ADVERTENCIA: Por favor ingrese una opción válida")
                    continue
                break
            if continuar=="N":
                return

    def info_venta(self):
        #Llama a la función para obtener el cliente de la venta
        self._buscar_cliente()
        if self.IdCliente==False:
            #Si no se encuentra uno o se cancela la compra, la función se detiene aquí
            return False
        #Crea el "carrito de compra"
        self._buscar_productos()
        while True:
            print("Métodos de Pago".center(35, "*"))
            for i in range(len(Venta.Metodos_Pago)):
                print(f"{i+1}.- {Venta.Metodos_Pago[i]}")
            try:
                self.MetPago=int(input("AVISO: El pago a crédito solo está disponible para los clientes Jurídicos\nIngrese el número del método de pago a usar: "))-1
                self.MetPago=Venta.Metodos_Pago[self.MetPago]
                if self.MetPago=="Crédito":
                    if not self.IdCliente["Tipo de cliente"]=="Jurídico":
                        print("ADVERTENCIA: Solo los clientes Jurídicos pueden elegir la opción de pago a Crédito")
                        continue
                break
            except ValueError:
                print("ADVERTENCIA: Por favor rellene el campo con el tipo de información requerida")
            except IndexError:
                print("ADVERTENCIA: Por favor ingrese una opción válida")

        while True:
            print("Métodos de Envío".center(35, "*"))
            for i in range(len(Venta.Metodos_Envio)):
                print(f"{i+1}.- Método: {Venta.Metodos_Envio[i]}".ljust(22, " ")+f"Costo: {Venta.Costos_Envio[i]}".rjust(10, " "))
            try:
                self.MetEnvio=int(input("Ingrese el número del método de envio a usar: "))-1
                self.PrecioEnvio=Venta.Costos_Envio[self.MetEnvio]
                self.MetEnvio=Venta.Metodos_Envio[self.MetEnvio]
                break
            except ValueError:
                print("ADVERTENCIA: Por favor rellene el campo con el tipo de información requerida")
            except IndexError:
                print("ADVERTENCIA: Por favor ingrese una opción válida")
        #Este bloque calcula todo lo que tiene que ver con el monto final
        self.subtotal=sum([p[1][1]*c for p, c in self.l_productos_comprados.items()])
        self.descuentos=0
        self.IVA=0.16
        self.IGTF=0
        if self.IdCliente["Tipo de cliente"]=="Jurídico" and self.MetPago=="Contado":
            self.descuentos=0.05
        if self.MetPago=="Divisas":
            self.IGTF=0.03
        self.total=self.subtotal*(1+self.IVA+self.IGTF-self.descuentos)+self.PrecioEnvio
        self.total=round(self.total, 2)
        self.PagoPendiente="Pendiente"
        self.EnvioPendiente="Pendiente"
        
        while True:
            #Este bloque usa el modulo datetime para verificar que la fecha introducida es una correcta
            self.fecha=input("Ingrese la fecha en la que se está realizando esta venta\n"
                             "La fecha debe de estar en el formato dd/mm/aaaa (día/mes/año)\n")
            if len(self.fecha.split("/"))!=3:
                print("ADVERTENCIA: Ingrese la fecha en el formato especificado\n")
                continue
            self.fecha=self.fecha.split("/")

            try:
                f=DT.date(int(self.fecha[2]), int(self.fecha[1]), int(self.fecha[0]))
                self.fecha=f.strftime("%d/%m/%Y")
                break
            except:
                print("ADVERTENCIA: Ingrese la fecha en el formato especificado\n")
                continue

    def DesgloseCompra(self):
        cancelar=self.info_venta()
        if cancelar==False:
            #Si se cancela la compra, esta función para aquí
            return False
        
        #Esta función imprime la "factura" de la compra
        print(60*"-"+"\n")
        print(
            "Compra por el cliente".ljust(30, " ")+"{}".format(self.IdCliente["Nombre"]).rjust(30, " ")+"\n"
            "Fecha".ljust(30, " ")+f"{self.fecha}".rjust(30, " ")
            )
        print("\n"+60*"-"+"\n")
        print(
            f"Cantidad - Producto".ljust(35, " ")+"Costo".rjust(25, " ")+"\n"
        )
        for p, c in self.l_productos_comprados.items():
            nombre, precio=p[0][1], p[1][1]
            print(
                f"{c} - {nombre}".ljust(45, " ")+"{}".format(precio*c).rjust(15, " ")
                )
        print("\n"+60*"-"+"\n")

        print(
            "Subtotal".ljust(30, " ")+f"{self.subtotal}".rjust(30, " ")+"\n"
            "Descuentos".ljust(30, " ")+f"{round(self.descuentos*self.subtotal, 2)}".rjust(30, " ")+"\n"
            "IVA".ljust(30, " ")+f"{round(self.IVA*self.subtotal, 2)}".rjust(30, " ")+"\n"
            "IGTF".ljust(30, " ")+f"{round(self.IGTF*self.subtotal, 2)}".rjust(30, " ")+"\n"
            "Costo del Envío".ljust(30, " ")+f"{self.PrecioEnvio}".rjust(30, " ")+"\n\n"
            "Total".ljust(30, " ")+f"{self.total}".rjust(30, " ")+"\n"
        )
        print(60*"-"+"\n")
        while True:
            #Da una última oportunidad para cancelar la compra
            confirmacion=input("Está seguro de que quiere registrar esta venta?    Y/N\n").upper()
            if confirmacion not in ["Y", "N"]:
                print("ADVERTENCIA: Por favor ingrese una opción válida")
                continue
            break

        if confirmacion=="N":
            return False
        
    def registrar(self, json_name, stats_json):
        #Hace todo lo necesario para registrar la compra en la base de datos
        cancelar=self.DesgloseCompra()
        if cancelar==False:
            if not hasattr(self, "l_productos_comprados"):
                return False
            can=P("Productos.json")
            cantidades=list(self.l_productos_comprados.values())

            for i in range(len(cantidades)):
                can.reinsertar(can.l_keys, can.search_keys, cancelar=True, P_Cancelado=(self.l_index_productos[i], cantidades[i]))
            return
        self.l_productos_comprados={p[0][1]:c for p, c in self.l_productos_comprados.items()}

        informacion=dict(zip(Venta.l_keys, [self.IdCliente, self.l_productos_comprados, self.MetPago, self.MetEnvio, self.PrecioEnvio, self.total, self.fecha, self.PagoPendiente, self.EnvioPendiente]))
        
        with open(json_name, "r") as file:
            ventas=json.load(file)
        ventas.append(informacion)
        with open(json_name, "w") as file:
            json.dump(ventas, file, indent=2)
        
        #De aquí en adelante, se encarga de actualizar las estadísticas
        with open(stats_json, "r") as s:
            estadisticas=json.load(s)
            v_stats=estadisticas["Ventas"]
            p_stats=estadisticas["Pagos"]
            e_stats=estadisticas["Envios"]

        self.fecha=self.fecha.split("/")
        dia, mes, año=int(self.fecha[0]), int(self.fecha[1]), int(self.fecha[2])
        fecha=DT.date(año, mes, dia)
        dia=fecha.strftime("%j")
        semana=fecha.strftime("%W")
        mes, año=str(mes), str(año)
        #Registra/aumenta en 1 la cantidad de ventas de la fecha registrada
        v_totales=v_stats["Totales"]
        v_totales[año]=v_totales.get(año, {"dias":{}, "semanas":{}, "meses":{}})
        v_totales[año]["dias"][dia]=v_totales[año]["dias"].get(dia, 0)+1
        v_totales[año]["semanas"][semana]=v_totales[año]["semanas"].get(semana, 0)+1
        v_totales[año]["meses"][mes]=v_totales[año]["meses"].get(mes, 0)+1
        v_stats["Totales"]=v_totales
        #Registra los productos vendidos
        for p, c in self.l_productos_comprados.items():
            v_stats["Productos"][p]=v_stats["Productos"].get(p, 0)+c
        #Registra los clientes frecuentes
        v_stats["Frecuentes"][self.IdCliente["Nombre"]]=v_stats["Frecuentes"].get(self.IdCliente["Nombre"], 0)+1
        estadisticas["Ventas"]=v_stats

        #Registra el cliente como Pendiente por Pagar y Pendiente por Enviar
        p_stats["Pendientes"][self.IdCliente["Nombre"]]=p_stats["Pendientes"].get(self.IdCliente["Nombre"], 0)+1
        estadisticas["Pagos"]=p_stats
        e_stats["Pendientes"][self.IdCliente["Nombre"]]=e_stats["Pendientes"].get(self.IdCliente["Nombre"], 0)+1
        estadisticas["Envios"]=e_stats

        with open(stats_json, "w") as s:
            json.dump(estadisticas, s, indent=2)

        with open("Productos.json", "r") as file:
            productos=json.load(file)
        for i in productos:
            if i["quantity"]==0:
                productos.remove(i)
        with open("Productos.json", "w") as file:
            json.dump(productos, file, indent=2)
        print(
            "La venta se ha registrado exitosamente".center(35, "-")+"\n"
        )

    def _set_atributos(self, json_name, stats_json):
        #Establece los atributos principales de la clase Venta
        super().__init__(json_name, stats_json)
        Venta.Metodos_Pago=["Contado", "Crédito", "Divisas"]
        Venta.Metodos_Envio=["Zoom", "MRW", "Delivery"]
        Venta.Costos_Envio=[12, 8, 5]
        Venta.l_keys={
            "Cliente":dict,
            "Productos":dict,
            "Método de pago":Venta.Metodos_Pago,
            "Método de envío":Venta.Metodos_Envio,
            "Costo de envío":Venta.Costos_Envio,
            "Monto total":float,
            "Fecha":str,
            "Pago":str,
            "Envio":str
        }
        Venta.search_keys.update({"Monto total":float})
        Venta.Stats_keys=["Ventas totales", "Productos más vendidos", "Clientes más frecuentes"]

    def menu(self, json_name, stats_json):
        #Se llama constantemente a la funcion _get_atributos para que los atributos principales sean los de la clase Venta, y no los de Productos o Cliente al ser creados en funciones más arriba
        self._set_atributos(json_name, stats_json)
        print(
            "\n"+"[ Gestion de Ventas ]".center(54, "-")+"\n"
            "1.- Registrar una nueva venta\n"
            "2.- Buscar ventas en la base de datos\n"
            "3.- Ver estadísticas de ventas\n"
            "4.- Regresar\n"
        )

        while True:
            opcion=input("Ingrese el número de la acción a realizar: ")
            if opcion not in ["1", "2", "3", "4"]:
                print("ADVERTENCIA: Por favor ingrese un número de acción válido")
                continue
            break

        if opcion=="1":
            self.registrar(Venta.json_name, Venta.stats)
        
        elif opcion=="2":
            self.display_search(Venta.Classname, Venta.search_keys)
        
        elif opcion=="3":
            #Muestra el menú de estadísticas (Módulo BusquedaAvanzada)
            self.menu_estad(Venta.Stats_keys)

        elif opcion=="4":
            return
        
        input("Presione Enter para continuar")
        self.menu(json_name, stats_json)

    def __init__(self, json_name, stats_json):
        self._set_atributos(json_name, stats_json)
    