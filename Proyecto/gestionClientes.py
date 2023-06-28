import json
from InterfazBusqueda import Modificar as IB

class Cliente(IB):

    def info_cliente(self):
        self.IdPersonal=input("Ingrese el nombre y apellido del cliente, o en su defecto su Razon Social: ")
        for i in range(list(Cliente.l_TiposCliente)):
            print(f"{i+1}.- {Cliente.l_TiposCliente[i]}")
        while True:
            try:
                self.TipoCliente=int(input("Ingrese el número del tipo de cliente: "))
                self.TipoCliente=Cliente.l_TiposCliente[self.TipoCliente]
                break
            except ValueError:
                print("ADVERTENCIA: Por favor ingrese el campo con el tipo de información requerida")
            except IndexError:
                print("ADVERTENCIA: Por favor ingrese una opción válida")

        for i in range(list(Cliente.l_TiposIdNumerica)):
            print(f"{i+1}.- {Cliente.l_TiposIdNumerica[i]}")
        while True:
            try:
                self.TipoIdNumerica=int(input("Ingrese el número del tipo de identificación numérica: "))
                self.TipoIdNumerica=Cliente.l_TiposIdNumerica[self.TipoIdNumerica]
                break
            except ValueError:
                print("ADVERTENCIA: Por favor ingrese el campo con el tipo de información requerida")
            except IndexError:
                print("ADVERTENCIA: Por favor ingrese una opción válida")
        while True:
            if self.TipoIdNumerica=="Cédula":
                self.IdNumerica=input("Ingrese su cédula como un número de 8 dígitos: ")
                if not self.IdNumerica.isnumeric() or len(self.IdNumerica)!=8:
                    print("ADVERTENCIA: Por favor ingrese el campo con el tipo de información requerida")
                    continue
            elif self.TipoIdNumerica=="RIF":
                self.IdNumerica=input("Ingrese su RIF del siguiente modo:\nXXXXXXXX-X (8 dígitos, un guión y el último dígito): ")
                if len(self.IdNumerica)!=10 or len(self.IdNumerica.split("-"))!=2:
                    print("ADVERTENCIA: Por favor ingrese el campo con el tipo de información requerida")
                    continue
                self.IdNumerica=self.IdNumerica.split("-")
                if not self.IdNumerica[0].isnumeric() or not self.IdNumerica[1].isnumeric():
                    print("ADVERTENCIA: Por favor ingrese el campo con el tipo de información requerida")
                    continue
                self.IdNumerica="-".join(self.IdNumerica)
            break
        while True:
            self.correo=input("Ingrese un correo electrónico (debe de contener un solo @, seguido por un dominio): ")
            if len(self.correo.split("@"))!=2 or "." not in self.correo[self.correo.index("@"):]:
                print("ADVERTENCIA: Por favor ingrese el campo con el tipo de información requerida")
                continue
            break
        self.DirEnvio=input("Ingrese su dirección de envío: ")
        while True:
            self.telefono=input("Ingrese su número telefónico en el formato de un número de 11 dígitos de longitud: ")
            if len(self.telefono)!=11 or not self.telefono.isnumeric():
                print("ADVERTENCIA: Por favor ingrese el campo con el tipo de información requerida")
                continue
            self.telefono=int(self.telefono)
            break

        infoKeys=[i if not type(i)==list else self.TipoIdNumerica for i in Cliente.l_keys.keys()]
        return dict(zip(infoKeys, [self.IdPersonal, self.TipoCliente, self.IdNumerica, self.correo, self.DirEnvio, self.telefono]))

    def registrar(self, json_name):
        self.info=self.info_cliente()

        print("-"*30)
        for k, v in self.info.items():
            print(
                f"{k}: {v}"
            )
        print("-"*30)
        
        while True:
            confirmacion=input("Está seguro de que quiere registrar este cliente?    Y/N\n").upper()
            if confirmacion not in ["Y", "N"]:
                print("ADVERTENCIA: Por favor ingrese una opción válida")
                continue
            break

        if confirmacion=="N":
            return

        with open(json_name, "r+") as P:
            lista_clientes=json.loads(P.read())
            lista_clientes.append(self.info)
            json.dump(lista_clientes, P, indent=2)

        print("Nuevo cliente registrado".center(35, "-"))

    def _modificar(self, l_keys, search_keys, venta, cantidad, cancelar):
        super()._modificar(l_keys, search_keys, venta, cantidad, cancelar)

    def menu(self):
        Cliente.l_keys={"Identificación":str, "Tipo de cliente":str, ["Cédula", "RIF"]:str, "E-mail":str, "Dirección":str, "Teléfono":int}
        print(
            "[ Gestión de Ventas ]".center(54, "*")+"\n"
            "1.- Registrar un nuevo cliente\n"
            "2.- Buscar clientes en la base de datos\n"
            "3.- Modificar información de clientes existentes\n"
            "4.- Eliminar clientes de la tienda\n"
            "5.- Regresar\n"
        )
        while True:
            opcion=input("Ingrese el número de la acción a realizar: ")
            if opcion not in ["1", "2", "3", "4", "5"]:
                print("ADVERTENCIA: Por favor ingrese un número de acción válido")
                continue
            break
        if opcion=="1":
            self.registrar(Cliente.json_name)
        
        if opcion=="2":
            self.display_search(Cliente.Classname, Cliente.search_keys)
        
        if opcion=="3":
            self.reinsertar(Cliente.l_keys, Cliente.search_keys)
        
        if opcion=="4":
            self.extraer(Cliente.search_keys, True)
        
        if opcion=="5":
            return
        
        input("Presione Enter para continuar")
        self.menu()

    def __init__(self, json_name, identificar=False):
        super().__init__(json_name)
        Cliente.l_TiposCliente=["Natural", "Jurídico"]
        Cliente.l_TiposIdNumerica=["Cédula", "RIF"]
        Cliente.search_keys={Cliente.l_TiposIdNumerica:"Cédula: 30567501\nRIF: 30567501-5", "E-mail":"tienda.natural@gmail.com"}
        if identificar:
            return self.identificar(Cliente.search_keys)
        return Cliente.menu()


def main():
    pass

if __name__=="__main__":
    main()
