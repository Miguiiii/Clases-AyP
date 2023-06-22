import json

class Busqueda:

    def _KeyValue_search(self, name):
        
        print(
            f"[ Buscar {name} ]".center(40, "*")
        )
        while True:
            for i in self.s_keys.keys():
                index=list(self.s_keys.keys()).index(i)+1
                print(f"{index}.- {i.capitalize()}")
            try:
                self.Key=int(input("Ingrese el número del tipo de dato a buscar: "))-1
                self.Key=list(self.s_keys.keys())[self.Key]
                break
            except:
                print("ADVERTENCIA: Por favor ingrese una opción válida")

        if type(self.s_keys[self.Key])==list:
            self.l_opc=self.s_keys[self.Key]
            print(f"Opciones de {self.Key}".center(30, "-"))
            for i in range(len(self.l_opc)):
                print(
                    f"{i+1}.- {self.l_opc[i]}"
                )

        while True:
            self.Value=input(f"Ingrese el valor a buscar en la casilla de {self.Key}: ")
            if self.s_keys[self.Key]!=int and type(self.s_keys[self.Key])!=list:
                break
            try:
                self.Value=int(self.Value)
                if type(self.s_keys[self.Key])==list:
                    if self.Value not in range(1, len(self.s_keys[self.Key])):
                        raise IndexError
                    self.Value=self.l_opc[self.Value-1]
                break
            except:
                if self.s_keys[self.Key]==int:
                    print("ADVERTENCIA: Por favor ingrese el campo con el tipo de información requerida")
                elif type(self.s_keys[self.Key])==list:
                    print("ADVERTENCIA: Por favor ingrese una opción válida")

    def _buscar(self, json_name, name):
        self._KeyValue_search(name)

        with open(json_name, "r") as BaseDatos:
            self.datos=json.loads(BaseDatos.read())

        return [resul for resul in self.datos if resul[self.Key]==self.Value]

    def display_search(self, json_name, name, search_keys):
        self.s_keys=search_keys
        self.resultados=self._buscar(json_name, name)
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

    def __init__(self, json_name, search_keys):
        self.json_name=json_name
        self.Classname=self.json_name.removesuffix(".json")

        self.display_search(self.json_name, self.Classname, search_keys)


class Modificar(Busqueda):

    def _identificar(self):
        self.display_search(self.json_name, self.s_keys, self.Classname)
        while True:
            try:
                self.Mod_index=int(input("Ingrese el número del producto: "))-1
            except:
                print("ADVERTENCIA: Por favor ingrese el campo con el tipo de información requerida")
                continue
            if self.Mod_index not in range(len(self.resultados)):
                print("ADVERTENCIA: Por favor ingrese una opción válida")
                continue
            self.Mod_element=self.resultados[self.Mod_index]
            print("Opción elegida".center(31, "-")+"\n")
            for key, value in self.Mod_element:
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

    def extraer(self, eliminar=False):
        self._identificar()
        self.datos.remove(self.Mod_element)
        if eliminar:
            print("El elemento seleccionado ha sido removido con éxito de la base de datos de la tienda.")
            return
        self.Mod_index=self.datos.index(self.Mod_element)
    
    def _modificar(self, l_keys):
        self.extraer()
        while True:
            print("-"*30)
            for key, value in self.Mod_element:
                print(f"{key}: {value}")
            print("-"*30)
            for i in range(l_keys):
                print(f"{i+1}.- {l_keys[i]}")
            print(f"{len(l_keys)+1}.- Terminar")


    def reinsertar(self, l_keys):
        self._modificar(l_keys)
        self.datos.insert(self.Mod_index, self.Mod_element)
        with open(self.json_name, "w") as file:
            json.dump(self.datos, file, indent=4)       

    def __init__(self, json_name, search_keys):
        super().__init__(json_name, search_keys)
        self.reinsertar(["name", "description", "price", "category", "disponibilidad"])




# # li=[]

# Modificar("Productos.json",
#           {"name":str, "disponibilidad":int, "price":int,
#            "category":
#            ['Computers', 'Grocery', 'Health', 'Shoes', 'Home',
#             'Beauty', 'Movies', 'Games', 'Baby', 'Jewelery',
#             'Garden', 'Industrial', 'Clothing', 'Music', 'Books', 'Sports'
#             ]
#             }
#         )

# # key="category"
# # value="Garden"
# # l1=None

# # with open("Productos.json", "r") as P:
# #     l1=json.loads(P.read())

# # l2=[i for i in l1 if i[key]==value]


#identificar ind=l1.index(l2[0])

#extraer l2=l1.pop(ind)

#modificar l2["description"]="Salchipapas"

# reinsertar
# l1.insert(ind, l2)

# with open("Productos.txt", "w") as P:
#     P.write(json.dumps(l1, indent=4))