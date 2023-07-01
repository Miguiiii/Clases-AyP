import json
from BusquedaAvanzada import Avanzada as IB
from gestionVentas import Venta as V
import datetime as DT

class Pago(IB):
    
    def _buscar_venta(self, stats):
        print("Busque la venta que desea pagar")
        venta=V("Ventas.json", stats)
        self.VentaAPagar=venta.identificar(venta.search_keys)
        if self.VentaAPagar==False or self.VentaAPagar["Pago"]!="Pendiente":
            print("ADVERTENCIA: Se necesita una venta registrada o con pago pendiente para realizar un pago")
            while True:
                cancelar=input("Quiere cancelar el registro de este pago?    Y/N\n").upper()
                if cancelar not in ["Y", "N"]:
                    print("ADVERTENCIA: Por favor ingrese una opción válida")
                    continue
                break
            if cancelar=="Y":
                print("Registro de pago CANCELADO".center(40, "*"))
                return False
            else:
                self._buscar_venta(stats)

    def info_pago(self, stats):
        cancelar=self._buscar_venta(stats)
        if cancelar==False:
            return False
        self.IdCliente=self.VentaAPagar["Cliente"]
        self.MontoPago=self.VentaAPagar["Monto total"]
        self.MonedaPago=Pago.l_Monedas_Pago[0]
        if self.VentaAPagar["Método de pago"]=="Divisas":
            while True:
                print("Monedas de Pago".center(35, "*"))
                for i in range(len(Pago.l_Monedas_Pago)):
                    print(f"{i+1}.- {Pago.l_Monedas_Pago[i]}")
                try:
                    self.MonedaPago=int(input("Ingrese el número de la moneda de pago a usar: "))-1
                    self.MonedaPago=Pago.l_Monedas_Pago[self.MonedaPago]
                    break
                except ValueError:
                    print("ADVERTENCIA: Por favor rellene el campo con el tipo de información requerida")
                except IndexError:
                    print("ADVERTENCIA: Por favor ingrese una opción válida")
        print(f"Moneda de pago establecida: {self.MonedaPago}")

        while True:
            print("Tipos de Pago".center(35, "*"))
            for i in range(len(Pago.l_Tipos_Pago)):
                print(f"{i+1}.- {Pago.l_Tipos_Pago[i]}")
            try:
                self.TipoPago=int(input("Ingrese el número del tipo de pago a usar: "))-1
                self.TipoPago=Pago.l_Tipos_Pago[self.TipoPago]
                break
            except ValueError:
                print("ADVERTENCIA: Por favor rellene el campo con el tipo de información requerida")
            except IndexError:
                print("ADVERTENCIA: Por favor ingrese una opción válida")

        self.fecha=self.VentaAPagar["Fecha"]
        if self.VentaAPagar["Método de pago"]=="Crédito":
            while True:
                self.fecha=self.VentaAPagar["Fecha"]
                print("La compra se realizó a Crédito. Eliga una fecha de pago:")
                print(f"Fecha de la compra: {self.fecha}")
                print(
                    "1.- 15 días después de la compra\n"
                    "2.- 30 días después de la compra"
                )
                try:
                    n_dias=int(input("Ingrese el número de la opción a elegir: "))
                    if n_dias not in [1, 2]:
                        raise IndexError
                    break
                except ValueError:
                    print("ADVERTENCIA: Por favor rellene el campo con el tipo de información requerida")
                except IndexError:
                    print("ADVERTENCIA: Por favor ingrese una opción válida")
            if n_dias==1:
                n_dias=DT.timedelta(days=15)
            else:
                n_dias=DT.timedelta(days=30)
            self.fecha=self.fecha.split("/")
            f_original=DT.date(int(self.fecha[2]), int(self.fecha[1]), int(self.fecha[0]))
            self.fecha=f_original+n_dias
            self.fecha=self.fecha.strftime("%d/%m/%Y")
        print(f"Fecha de pago establecida: {self.fecha}")

    def _display_info(self, stats):
        cancelar=self.info_pago(stats)

        if cancelar==False:
            return False
        print("[ Pago a registar ]".center(39, "-"))
        print("Cliente:")
        for k, v in self.IdCliente.items():
            print(f"    {k}: {v}")
        print("Productos comprados:")
        for k, v in self.VentaAPagar["Productos"].items():
            print(f"    {v} {k}")
        print(
            f"Monto del pago: {self.MontoPago}\n"
            f"Moneda de pago: {self.MonedaPago}\n"
            f"Tipo de pago: {self.TipoPago}\n"
            f"Fecha del pago: {self.fecha}\n"
        )

        while True:
            confirmacion=input("Está seguro de que quiere registrar este pago?    Y/N\n").upper()
            if confirmacion not in ["Y", "N"]:
                print("ADVERTENCIA: Por favor ingrese una opción válida")
                continue
            break

        if confirmacion=="N":
            return False

    def registrar_pago(self, json_name, stats):
        cancelar=self._display_info(stats)

        if cancelar==False:
            return

        informacion=dict(zip(Pago.l_keys, [self.IdCliente, self.MontoPago, self.MonedaPago, self.TipoPago, self.fecha]))
        with open(json_name, "r") as file:
            pagos=json.load(file)
        pagos.append(informacion)
        with open(json_name, "w") as file:
            json.dump(pagos, file, indent=2)

        with open(stats, "r") as s:
            estadisticas=json.load(s)
            p_stats=estadisticas["Pagos"]
            e_stats=estadisticas["Envios"]
        
        self.fecha=self.fecha.split("/")
        dia, mes, año=int(self.fecha[0]), int(self.fecha[1]), int(self.fecha[2])
        fecha=DT.date(año, mes, dia)
        dia=fecha.strftime("%j")
        semana=fecha.strftime("%W")
        mes, año=str(mes), str(año)

        p_totales=p_stats["Pagos totales"]
        p_totales[año]=p_totales.get(año, {"dias":{}, "semanas":{}, "meses":{}})
        p_totales[año]["dias"][dia]=p_totales[año]["dias"].get(dia, 0)+1
        p_totales[año]["semanas"][semana]=p_totales[año]["semanas"].get(semana, 0)+1
        p_totales[año]["meses"][mes]=p_totales[año]["meses"].get(mes, 0)+1
        p_stats["Pagos totales"]=p_totales
        p_stats["Clientes con pagos pendientes"][self.IdCliente["Nombre"]]-=1
        if p_stats["Clientes con pagos pendientes"][self.IdCliente["Nombre"]]==0:
            p_stats["Clientes con pagos pendientes"].pop(self.IdCliente["Nombre"])
        estadisticas["Pagos"]=p_stats

        e_stats["Clientes con envíos pendientes"][self.IdCliente["Nombre"]]=e_stats["Clientes con envíos pendientes"].get(self.IdCliente["Nombre"])
        estadisticas["Envios"]=e_stats
        with open(stats, "w") as s:
            json.dump(estadisticas, s, indent=2)

        with open("Ventas.json", "r") as file:
            ventas=json.load(file)
            IndiceVenta=ventas.index(self.VentaAPagar)
        ventas[IndiceVenta]["Pago"]="Realizado"

        with open("Ventas.json", "w") as file:
            json.dump(ventas, file, indent=2)

        print("El pago se ha registrado exitosamente".center(35, "-")+"\n")

    def menu(self):
        print(
            "\n"+"[ Gestion de Pagos ]".center(54, "-")+"\n"
            "1.- Registrar un nuevo pago\n"
            "2.- Buscar pagos en la base de datos\n"
            "3.- Ver estadísticas de pagos\n"
            "4.- Regresar\n"
        )

        while True:
            opcion=input("Ingrese el número de la acción a realizar: ")
            if opcion not in ["1", "2", "3", "4"]:
                print("ADVERTENCIA: Por favor ingrese un número de acción válido")
                continue
            break

        if opcion=="1":
            self.registrar_pago(Pago.json_name, Pago.stats)
        
        elif opcion=="2":
            self.display_search(Pago.Classname, Pago.search_keys)
        
        # elif opcion=="3":
        #     return
        
        elif opcion=="4":
            return
        
        input("Presione Enter para continuar")
        self.menu()

    def __init__(self, json_name, stats_json):
        super().__init__(json_name, stats_json)
        Pago.l_Tipos_Pago=["PdV", "PM", "Zelle", "Efectivo", "Transferencia", "Pago Móvil"]
        Pago.l_Monedas_Pago=["Bolívar", "Dólar", "Euro"]
        Pago.l_keys={
            "Cliente":dict,
            "Monto del Pago":float,
            "Moneda de pago":Pago.l_Monedas_Pago,
            "Tipo de Pago":Pago.l_Tipos_Pago,
            "Fecha":str
        }
        Pago.search_keys.update({"Tipo de pago":Pago.l_Tipos_Pago, "Moneda de pago":Pago.l_Monedas_Pago})
        Pago.Stats_keys={"Pagos totales": {}, "Clientes con pagos pendientes":list}


def main():
    pass

if __name__=="__main__":
    main()