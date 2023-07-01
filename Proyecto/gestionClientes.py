import json
from InterfazBusqueda import Modificar as IB

class Cliente(IB):

    def info_cliente(self):
        while True:
            self.IdPersonal=input("Ingrese el nombre y apellido del cliente, o en su defecto su Razon Social: ")
            if self.IdPersonal!="":
                break
            print("ADVERTENCIA: Por favor ingrese el campo con el tipo de información requerida")

        for i in range(len(Cliente.l_TiposCliente)):
            print(f"{i+1}.- {Cliente.l_TiposCliente[i]}")
        while True:
            try:
                self.TipoCliente=int(input("Ingrese el número del tipo de cliente: "))-1
                self.TipoCliente=Cliente.l_TiposCliente[self.TipoCliente]
                break
            except ValueError:
                print("ADVERTENCIA: Por favor ingrese el campo con el tipo de información requerida")
            except IndexError:
                print("ADVERTENCIA: Por favor ingrese una opción válida")

        for i in range(len(Cliente.l_TiposIdNumerica)):
            print(f"{i+1}.- {Cliente.l_TiposIdNumerica[i]}")
        while True:
            try:
                self.TipoIdNumerica=int(input("Ingrese el número del tipo de identificación numérica: "))-1
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
            if len(self.correo.split("@"))!=2 or self.correo[:self.correo.index("@")]=="" or "." not in self.correo[self.correo.index("@"):] or any([i=="" for i in self.correo[self.correo.index("@"):].split(".")]):
                print("ADVERTENCIA: Por favor ingrese el campo con el tipo de información requerida")
                continue
            break
        self.DirEnvio=input("Ingrese su dirección de envío: ")
        while True:
            self.telefono=input("Ingrese su número telefónico en el formato de un número de 11 dígitos de longitud: ")
            if len(self.telefono)!=11 or not self.telefono.isnumeric():
                print("ADVERTENCIA: Por favor ingrese el campo con el tipo de información requerida")
                continue
            break

        infoKeys=[i if not type(i)==tuple else self.TipoIdNumerica for i in Cliente.l_keys.keys()]
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

        with open(json_name, "r") as C:
            lista_clientes=json.load(C)
            lista_clientes.append(self.info)
        with open(json_name, "w") as C:
            json.dump(lista_clientes, C, indent=2)

        print("Nuevo cliente registrado".center(35, "-")+"\n")

    def _modificar(self, l_keys, search_keys, venta, cantidad):
        encontrado=super()._modificar(l_keys, search_keys, venta, cantidad)
        if encontrado==False:
            return False
        while True:
            print("[ Cliente a modificar ]".center(30, "-"))
            for key, value in self.Mod_element.items():
                print(f"{key}: {value}")
            print("-"*30)
            for i in range(len(self.lista_keys)):
                if type(self.lista_keys[i])==tuple:
                    print(f"{i+1}.-", "/".join(self.lista_keys[i]))
                    continue
                print(f"{i+1}.- {self.lista_keys[i]}")
            print(f"{len(self.lista_keys)+1}.- Terminar")

            try:
                opcion=int(input("Eliga el número de la información a modificar: "))-1
                if opcion==len(self.lista_keys):
                    break
                el_key=self.lista_keys[opcion]
            except ValueError:
                print("ADVERTENCIA: Por favor rellene el campo con el tipo de información requerida")
                input("Presione Enter para continuar")
                continue
            except IndexError:
                print("ADVERTENCIA: Por favor ingrese una opción válida")
                input("Presione Enter para continuar")
                continue
            
            if type(el_key)==tuple:
                for i in Cliente.l_TiposIdNumerica:
                    if self.Mod_element.get(i, None)!=None:  
                        old_key=i
                        break
                for i in range(len(Cliente.l_TiposIdNumerica)):
                    print(f"{i+1}.- {Cliente.l_TiposIdNumerica[i]}")
                while True:
                    try:
                        n_key=int(input("Ingrese el número del tipo de identificación numérica: "))-1
                        n_key=Cliente.l_TiposIdNumerica[n_key]
                        break
                    except ValueError:
                        print("ADVERTENCIA: Por favor ingrese el campo con el tipo de información requerida")
                    except IndexError:
                        print("ADVERTENCIA: Por favor ingrese una opción válida")

            if type(l_keys[el_key])==list:
                print(f"Opciones de {el_key}".center(30, "-"))
                for i in range(len(Cliente.l_TiposCliente)):
                    print(f"{i+1}.- {Cliente.l_TiposCliente[i]}")
            
            if type(el_key)==tuple:
                n_value=input(f"Ingrese el nuevo valor de {n_key}: ")
                k, v=zip(*self.Mod_element.items())
                k, v=list(k), list(v)
                index=k.index(old_key)
                k[index]=n_key
                self.Mod_element=dict(zip(k, v))
                self.Mod_element[n_key]=n_value
                continue

            n_value=input(f"Ingrese el nuevo valor de {el_key}: ")
            
            if type(l_keys[el_key])==list:
                try:
                    n_value=int(n_value)-1
                    if n_value in range(len(Cliente.l_TiposCliente)):
                        n_value=Cliente.l_TiposCliente[n_value]
                except ValueError:
                    print("ADVERTENCIA: Por favor rellene el campo con el tipo de información requerida")
                    input("Presione Enter para continuar")
                    continue
                except IndexError:
                    print("ADVERTENCIA: Por favor ingrese una opción válida")
                    input("Presione Enter para continuar")
                    continue
            
            self.Mod_element[el_key]=n_value

    def menu(self):
        print(
            "\n"+"[ Gestión de Clientes ]".center(54, "*")+"\n"
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

    def __init__(self, json_name):
        #El super() establece el nombre del archivo JSON y el nombre del gestor (Productos)
        super().__init__(json_name)
        #Establece los tipos de cliente y los tipos de Identificación numérica
        Cliente.l_TiposCliente=["Natural", "Jurídico"]
        Cliente.l_TiposIdNumerica=("Cédula", "RIF")
        #Establece las llaves que contienen la información de un cliente
        Cliente.l_keys={
            "Nombre":str,
            "Tipo de cliente":Cliente.l_TiposCliente,
            Cliente.l_TiposIdNumerica:str,
            "E-mail":str,
            "Dirección":str,
            "Teléfono":str
        }
        #Establece las llaves y los tipos de valores con los que se puede buscar a un cliente
        Cliente.search_keys={Cliente.l_TiposIdNumerica:"Cédula: 30567501\nRIF: 30567501-5", "E-mail":"tienda.natural@gmail.com"}
        


def main():
    pass

if __name__=="__main__":
    main()
