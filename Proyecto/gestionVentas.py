import json
from BusquedaAvanzada import Avanzada as IB
from gestionClientes import Cliente as C
from gestionProductos import Producto as P
import datetime as DT
class Venta(IB):

    def _buscar_cliente(self):
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
                print("Registro de venta CANCELADO".center(40, "*"))
                return False
            else:
                self._buscar_cliente()
        
    def _buscar_productos(self):
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
            # print(comp)
            # print(dict(comp))
            self.l_productos_comprados[comp]=self.l_productos_comprados.get(comp, 0)+cant
            if len(self.l_productos_comprados)>len(self.l_index_productos):
                self.l_index_productos.append(ind)
            # print(self.l_productos_comprados)
            # print(self.l_index_productos)
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
        self._buscar_cliente()
        if self.IdCliente==False:
            return False
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
                print(f"{i+1}.- {Venta.Metodos_Envio[i]}")
            try:
                self.MetEnvio=int(input("Ingrese el número del método de envio a usar: "))-1
                self.PrecioEnvio=Venta.Costos_Envio[self.MetEnvio]
                self.MetEnvio=Venta.Metodos_Envio[self.MetEnvio]
                break
            except ValueError:
                print("ADVERTENCIA: Por favor rellene el campo con el tipo de información requerida")
            except IndexError:
                print("ADVERTENCIA: Por favor ingrese una opción válida")
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
        
        while True:
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
            return False
        print(60*"-"+"\n")
        print(
            "Compra por el cliente {}".format(self.IdCliente["Nombre"].center(60, " ")+"\n"
            f"Fecha: {self.fecha}").center(60, " ")
        )
        print("\n"+60*"-"+"\n")
        print(
            f"Cantidad - Producto".ljust(35, " ")+"Costo".rjust(25, " ")+"\n"
        )
        for p, c in self.l_productos_comprados.items():
            nombre, precio=p[0][1], p[1][1]
            print(
                f"{c} {nombre}".ljust(45, " ")+"{}".format(precio*c).rjust(15, " ")
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
            confirmacion=input("Está seguro de que quiere registrar esta venta?    Y/N\n").upper()
            if confirmacion not in ["Y", "N"]:
                print("ADVERTENCIA: Por favor ingrese una opción válida")
                continue
            break

        if confirmacion=="N":
            return False
        
    def registrar(self, json_name, stats_json):
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

        informacion=dict(zip(Venta.l_keys, [self.IdCliente, self.l_productos_comprados, self.MetPago, self.MetEnvio, self.PrecioEnvio, self.total, self.fecha, self.PagoPendiente]))
        
        with open(json_name, "r") as file:
            ventas=json.load(file)
        ventas.append(informacion)
        with open(json_name, "w") as file:
            json.dump(ventas, file, indent=2)
        
        with open(stats_json, "r") as s:
            estadisticas=json.load(s)
            v_stats=estadisticas["Ventas"]
            p_stats=estadisticas["Pagos"]
        self.fecha=self.fecha.split("/")
        dia, mes, año=int(self.fecha[0]), int(self.fecha[1]), int(self.fecha[2])
        fecha=DT.date(año, mes, dia)
        dia=fecha.strftime("%j")
        semana=fecha.strftime("%W")
        mes, año=str(mes), str(año)

        v_totales=v_stats["Ventas totales"]
        v_totales[año]=v_totales.get(año, {"dias":{}, "semanas":{}, "meses":{}})
        v_totales[año]["dias"][dia]=v_totales[año]["dias"].get(dia, 0)+1
        v_totales[año]["semanas"][semana]=v_totales[año]["semanas"].get(semana, 0)+1
        v_totales[año]["meses"][mes]=v_totales[año]["meses"].get(mes, 0)+1
        v_stats["Ventas totales"]=v_totales
        for p, c in self.l_productos_comprados.items():
            v_stats["Productos más vendidos"][p]=v_stats["Productos más vendidos"].get(p, 0)+c
        v_stats["Clientes más frecuentes"][self.IdCliente["Nombre"]]=v_stats["Clientes más frecuentes"].get(self.IdCliente["Nombre"], 0)+1
        estadisticas["Ventas"]=v_stats
        p_stats["Clientes con pagos pendientes"][self.IdCliente["Nombre"]]=p_stats["Clientes con pagos pendientes"].get(self.IdCliente["Nombre"], 0)+1
        estadisticas["Pagos"]=p_stats
        with open(stats_json, "w") as s:
            json.dump(estadisticas, s, indent=2)

        print("La venta se ha registrado exitosamente".center(35, "-")+"\n")

    def menu(self):
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
        
        # elif opcion=="3":
        #     return

        elif opcion=="4":
            return
        
        input("Presione Enter para continuar")
        self.menu()

    def __init__(self, json_name, stats_json):
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
            "Pago":str
        }
        Venta.search_keys.update({"Monto total":float})
        Venta.Stats_keys={"Ventas totales":{}, "Productos más vendidos":{}, "Clientes más frecuentes":{}}
    


def main():
    Venta("Ventas.json").menu()

if __name__=="__main__":
    main()