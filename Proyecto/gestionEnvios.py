import json
from InterfazBusqueda import Busqueda as IB

class Envio(IB):

    def __init__(self):
        self.OrderCompra=None
        self.ServicioEnvio=None
        if self.ServicioEnvio=="Delivery":
            self.DatosMotorizado=None
        self.CostoEnvio=0

def main():
    pass

if __name__=="__main__":
    main()