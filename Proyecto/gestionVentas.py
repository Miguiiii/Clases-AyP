import json
from InterfazBusqueda import Busqueda as IB

class Venta(IB):

    def __init__(self):
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
    
    def DesgloseCompra(self):
        pass


def main():
    pass

if __name__=="__main__":
    main()