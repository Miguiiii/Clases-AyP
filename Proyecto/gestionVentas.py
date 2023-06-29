import json
from InterfazBusqueda import Busqueda as IB
from gestionClientes import Cliente as C

class Venta(IB):

    def buscar_cliente(self):
        C("Clientes.json", True)

    def info_venta(self):
        self.IdCliente=None
        self.productos=None
        self.CantidadProductos=None
        self.MetodoPago=None
        self.MetodoEnvio=None
        self.subtotal=0
        self.descuentos=0
        self.IVA=0
        self.IGTF=0
        self.total=0

    def menu(self):
        print(
            "[ Gestion de Ventas ]".center(54, "-")+"\n"
            "1.- Registrar una nueva venta\n"
            "2.- Buscar ventas en la base de datos\n"
            "3.- Ver estadísticas de ventas\n"
            "4.- Regresar\n"
        )

        while True:
            opcion=input("Ingrese el número de la acción a realizar: ")
            if opcion not in ["1", "2", "3"]:
                print("ADVERTENCIA: Por favor ingrese un número de acción válido")
                continue
            break
        
        if opcion=="1":
            self.registrar(Venta.json_name)
        
        if opcion=="2":
            self.display_search(Venta.Classname, Venta.search_keys)
        
        if opcion=="3":
            return

        if opcion=="4":
            return
        
        input("Presione Enter para continuar")
        self.menu()

    def __init__(self, json_name):
        super().__init__(json_name)
    
    def DesgloseCompra(self):
        pass


def main():
    pass

if __name__=="__main__":
    main()