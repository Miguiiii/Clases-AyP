import json

class Busqueda:

    def _KeyValue_search(self, name, search_keys):
        
        print(
            f"[ Buscar {name} ]".center(40, "*")
        )
        while True:
            for i in search_keys.keys():
                index=list(search_keys.keys()).index(i)+1
                print(f"{index}.- {i.capitalize()}")
            try:
                self.Key=int(input("Ingrese el número del tipo de dato a buscar: "))-1
                self.Key=list(search_keys.keys())[self.Key]
                break
            except:
                print("ADVERTENCIA: Por favor ingrese una opción válida")

        if type(search_keys[self.Key])==list:
            self.l_opc=search_keys[self.Key]
            print(f"Opciones de {self.Key}".center(30, "-"))
            for i in range(len(self.l_opc)):
                print(
                    f"{i+1}.- {self.l_opc[i]}"
                )

        while True:
            self.Value=input(f"Ingrese el valor a buscar en la casilla de {self.Key}: ")
            if search_keys[self.Key]!=int and type(search_keys[self.Key])!=list:
                break
            try:
                self.Value=int(self.Value)-1
                if type(search_keys[self.Key])==list:
                    if self.Value not in range(len(search_keys[self.Key])):
                        raise IndexError
                    self.Value=self.l_opc[self.Value]
                break
            except:
                if search_keys[self.Key]==int:
                    print("ADVERTENCIA: Por favor ingrese el campo con el tipo de información requerida")
                elif type(search_keys[self.Key])==list:
                    print("ADVERTENCIA: Por favor ingrese una opción válida")

    def _buscar(self, json_name, name, search_keys):
        self._KeyValue_search(name, search_keys)

        with open(json_name, "r") as BaseDatos:
            self.datos=json.loads(BaseDatos.read())

        return [resul for resul in self.datos if resul[self.Key]==self.Value]

    def display_search(self, json_name, name, search_keys):
        
        self.resultados=self._buscar(json_name, name, search_keys)
        print(
            f"[ {name} con {self.Key}={self.Value} ]".center(40, "*")
        )
        for i in range(len(self.resultados)):
            p=self.resultados[i]
            print(f"{i+1}".center(31, "-"))
            for key, value in p.items():
                print(
                    f"{key}: {value}"
                )
        print("-"*31)

    def __init__(self, json_name):
        Busqueda.json_name=json_name
        Busqueda.Classname=self.json_name.removesuffix(".json")

class Modificar(Busqueda):

    def _identificar(self, search_keys):
        self.display_search(self.json_name, self.Classname, search_keys)
        while True:
            try:
                self.Mod_index=int(input("Ingrese el número del elemento a elegir: "))-1
            except:
                print("ADVERTENCIA: Por favor rellene el campo con el tipo de información requerida")
                continue
            if self.Mod_index not in range(len(self.resultados)):
                print("ADVERTENCIA: Por favor ingrese una opción válida")
                continue
            self.Mod_element=self.resultados[self.Mod_index]
            print("Opción elegida".center(31, "-"))
            for key, value in self.Mod_element.items():
                print(f"{key}: {value}")
            print("-"*31)
                
            while True:
                confirmacion=input("Está seguro de que elige este elemento?    Y/N\n").upper()
                if confirmacion not in ["Y", "N"]:
                    print("ADVERTENCIA: Por favor ingrese una opción válida")
                    continue
                break

            if confirmacion=="Y":
                break 

    def extraer(self, search_keys, eliminar=False):
        self._identificar(search_keys)
        self.Mod_index=self.datos.index(self.Mod_element)
        self.datos.remove(self.Mod_element)
        if eliminar:
            print("El elemento seleccionado ha sido removido con éxito de la base de datos de la tienda.")
            return
    
    def _modificar(self, l_keys, search_keys, ListKey_agregar=False):
        self.extraer(search_keys)
        while True:
            print("[ Elemento a modificar ]".center(30, "-"))
            for key, value in self.Mod_element.items():
                print(f"{key}: {value}")
            print("-"*30)
            for i in range(len(l_keys)):
                print(f"{i+1}.- {l_keys[i].capitalize()}")
            print(f"{len(l_keys)+1}.- Terminar")
            try:
                opcion=int(input("Eliga el número de la información a modificar: "))-1
                if opcion==len(l_keys):
                    return
                el_key=l_keys[opcion]
            except ValueError:
                print("ADVERTENCIA: Por favor rellene el campo con el tipo de información requerida")
                input("Presione Enter para continuar")
                continue
            except IndexError:
                print("ADVERTENCIA: Por favor ingrese una opción válida")
                input("Presione Enter para continuar")
                continue
            if type(self.Mod_element[el_key])==list:
                for i in range(len(search_keys[el_key])):
                    print(f"{i+1}.- {l_keys[i]}")
            n_value=input(f"Ingrese el nuevo valor de {el_key.capitalize()}: ")
            if type(self.Mod_element[el_key])==int:
                try:
                    n_value=int(n_value)
                except:
                    print("ADVERTENCIA: Por favor rellene el campo con el tipo de información requerida")
                    input("Presione Enter para continuar")
                    continue
            self.Mod_element[el_key]=n_value
        
    def reinsertar(self, l_keys, search_keys, ListKey_agregar=False):
        self._modificar(l_keys, search_keys)
        self.datos.insert(self.Mod_index, self.Mod_element)
        with open(self.json_name, "w") as file:
            json.dump(self.datos, file, indent=2)  
        print("[ Elemento modificado con éxito ]".center(30, "*"))
