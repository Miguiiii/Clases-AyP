import json
from BusquedaAvanzada import Avanzada as IB
from gestionVentas import Venta as V
import datetime as DT

class Envio(IB):
    #Esta clase es esencialmente idéntica a la de Pago
    def _buscar_pago(self, stats):
        print("Busque la orden de compra que desea enviar")
        venta=V("Ventas.json", stats)
        self.OrdenCompra=venta.identificar(venta.search_keys)
        if self.OrdenCompra==False or self.OrdenCompra["Pago"]=="Pendiente" or self.OrdenCompra["Envio"]!="Pendiente":
            print("ADVERTENCIA: Se necesita una venta registrada, con pago ya realizado o con su envío pendiente para ordenar un envío")
            while True:
                cancelar=input("Quiere cancelar el registro de este envío?    Y/N\n").upper()
                if cancelar not in ["Y", "N"]:
                    print("ADVERTENCIA: Por favor ingrese una opción válida")
                    continue
                break
            if cancelar=="Y":
                print("Registro de envío CANCELADO".center(40, "*"))
                return False
            else:
                self._buscar_pago(stats)

    def info_pago(self, stats):
        cancelado=self._buscar_pago(stats)
        if cancelado==False:
            return False
        self.IdCliente=self.OrdenCompra["Cliente"]
        self.ProductosEnviando=self.OrdenCompra["Productos"]
        self.ServicioEnvio=self.OrdenCompra["Método de envío"]
        self.CostoEnvio=self.OrdenCompra["Costo de envío"]
        self.informacion=[self.IdCliente, self.ProductosEnviando, self.ServicioEnvio, self.CostoEnvio]
        if self.ServicioEnvio=="Delivery":
            Envio.l_keys.insert(3, "Datos del motorizado")
            while True:
                nombre_motorizado=input("Ingrese el nombre del motorizado: ")
                if nombre_motorizado=="":
                    print("ADVERTENCIA: Por favor rellene el campo con el tipo de información requerida")
                    continue
                break
            while True:
                try:
                    tele_motorizado=input("Ingrese el teléfono del motorizado en el formato de un número de 11 dígitos: ")
                    if len(tele_motorizado)!=11:
                        print("ADVERTENCIA: Por favor rellene el campo con el formato requerida")
                        continue
                    if not tele_motorizado.isnumeric():
                        print("ADVERTENCIA: Por favor rellene el campo con el tipo de información requerida")
                        continue
                    break
                except ValueError:
                    print("ADVERTENCIA: Por favor rellene el campo con el tipo de información requerida")
            self.DatosMotorizado={"Nombre del motorizado":nombre_motorizado, "Teléfono del motorizado":tele_motorizado}
            self.informacion.insert(3, self.DatosMotorizado)
        while True:
            self.fecha=input("Ingrese la fecha en la que se está realizando esta venta\n"
                             "La fecha debe de estar en el formato dd/mm/aaaa (día/mes/año)\n")
            if len(self.fecha.split("/"))!=3:
                print("ADVERTENCIA: Ingrese la fecha en el formato especificado\n")
                print("Error 1")
                continue
            self.fecha=self.fecha.split("/")

            try:
                self.fecha=DT.date(int(self.fecha[2]), int(self.fecha[1]), int(self.fecha[0]))
                fecha_venta=self.OrdenCompra["Fecha"]
                fecha_venta=fecha_venta.split("/")
                fecha_venta=DT.date(int(fecha_venta[2]), int(fecha_venta[1]), int(fecha_venta[0]))
                if fecha_venta>self.fecha:
                    print("ADVERTENCIA: No puede ingresar una fecha de envío previa a la fecha de la compra")
                    continue
                self.fecha=self.fecha.strftime("%d/%m/%Y")
                break
            except:
                print("ADVERTENCIA: Ingrese la fecha en el formato especificado\n")
                print("Error 2")
                continue
        self.informacion.append(self.fecha)

    def _display_info(self, stats):
        cancelado=self.info_pago(stats)
        if cancelado==False:
            return False
        
        self.informacion=dict(zip(Envio.l_keys, self.informacion))
        print("[ Envío a registar ]".center(40, "-"))
        for key, value in self.informacion.items():
            if type(value)==dict:
                for k, v in value.items():
                    print(f"    {k}: {v}")
                continue
            print(f"{key}: {value}")
        print("-"*40)
        while True:
            confirmacion=input("Está seguro de que quiere registrar este envío?    Y/N\n").upper()
            if confirmacion not in ["Y", "N"]:
                print("ADVERTENCIA: Por favor ingrese una opción válida")
                continue
            break

        if confirmacion=="N":
            return False

    def registrar_envio(self, json_name, stats):
        cancelado=self._display_info(stats)
        if cancelado==False:
            return
        
        with open(json_name, "r") as file:
            envios=json.load(file)
        envios.append(self.informacion)
        with open(json_name, "w") as file:
            json.dump(envios, file, indent=2)

        with open(stats, "r") as s:
            estadisticas=json.load(s)
            e_stats=estadisticas["Envios"]
        
        self.fecha=self.fecha.split("/")
        dia, mes, año=int(self.fecha[0]), int(self.fecha[1]), int(self.fecha[2])
        fecha=DT.date(año, mes, dia)
        dia=fecha.strftime("%j")
        semana=fecha.strftime("%W")
        mes, año=str(mes), str(año)

        e_totales=e_stats["Totales"]
        e_totales[año]=e_totales.get(año, {"dias":{}, "semanas":{}, "meses":{}})
        e_totales[año]["dias"][dia]=e_totales[año]["dias"].get(dia, 0)+1
        e_totales[año]["semanas"][semana]=e_totales[año]["semanas"].get(semana, 0)+1
        e_totales[año]["meses"][mes]=e_totales[año]["meses"].get(mes, 0)+1
        e_stats["Totales"]=e_totales
        for p, c in self.ProductosEnviando.items():
            e_stats["Productos"][p]=e_stats["Productos"].get(p, 0)+c
        
        e_stats["Pendientes"][self.IdCliente["Nombre"]]-=1
        if e_stats["Pendientes"][self.IdCliente["Nombre"]]==0:
            e_stats["Pendientes"].pop(self.IdCliente["Nombre"])
        estadisticas["Envios"]=e_stats

        with open(stats, "w") as s:
            json.dump(estadisticas, s, indent=2)

        with open("Ventas.json", "r") as file:
            ventas=json.load(file)
            IndiceVenta=ventas.index(self.OrdenCompra)
        ventas[IndiceVenta]["Envio"]="Realizado"

        with open("Ventas.json", "w") as file:
            json.dump(ventas, file, indent=2)

        print(
            "El envío se ha registrado exitosamente".center(35, "-")+"\n"
        )

    def _set_atributos(self, json_name, stats_json):
        super().__init__(json_name, stats_json)
        Envio.l_keys=[
            "Cliente",
            "Productos",
            "Servicio del envío",
            "Costo del servicio",
            "Fecha"
        ]
        Envio.Stats_keys=["Envíos totales", "Productos más enviados", "Clientes con envíos pendientes"]

    def menu(self, json_name, stats_json):
        self._set_atributos(json_name, stats_json)
        print(
            "\n"+"[ Gestion de Pagos ]".center(54, "-")+"\n"
            "1.- Registrar un nuevo envío\n"
            "2.- Buscar envíos en la base de datos\n"
            "3.- Ver estadísticas de envios\n"
            "4.- Regresar\n"
        )

        while True:
            opcion=input("Ingrese el número de la acción a realizar: ")
            if opcion not in ["1", "2", "3", "4"]:
                print("ADVERTENCIA: Por favor ingrese un número de acción válido")
                continue
            break

        if opcion=="1":
            self.registrar_envio(Envio.json_name, Envio.stats)
        
        elif opcion=="2":
            self.display_search(Envio.Classname, Envio.search_keys)
        
        elif opcion=="3":
            self.menu_estad(Envio.Stats_keys)
        
        elif opcion=="4":
            return

    def __init__(self, json_name, stats_json):
        self._set_atributos(json_name, stats_json)
        
