import json

class Busqueda:

    def KeyValue_search(self, search_keys, name):
        self.s_keys=search_keys
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
                    self.Value=self.l_opc[self.Value-1]
                break
            except:
                if self.s_keys[self.Key]==int:
                    print("ADVERTENCIA: Por favor ingrese el campo con el tipo de información requerida")
                elif type(self.s_keys[self.Key])==list:
                    print("ADVERTENCIA: Por favor ingrese una opción válida")
                continue



    def buscar(self, txt_name, search_keys, name):
        self.KeyValue_search(search_keys, name)

        with open(txt_name, "r") as BaseDatos:
            self.datos=json.loads(BaseDatos.read())

        self.resultados=[resul for resul in self.datos if resul[self.Key]==self.Value]

    def display_search(self, txt_name, search_keys, name, keys):
        self.buscar(txt_name, search_keys, name)
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
            

    def __init__(self, txt_name, search_keys, keys):
        self.txt_name=txt_name
        self.name=self.txt_name.removesuffix(".txt")
        self.l_keys=keys

        self.display_search(self.txt_name, search_keys, self.name, self.l_keys)


class Modificar(Busqueda):

    def extraer(self):
        pass

    def __init__(self, txt_name, keys):
        super().__init__(txt_name, keys)





# # Busqueda("Productos.txt", {"name":str, "disponibilidad":int, "price":int, "category":['Computers', 'Grocery', 'Health', 'Shoes', 'Home',
# #                'Beauty', 'Movies', 'Games', 'Baby', 'Jewelery',
# #                'Garden', 'Industrial', 'Clothing', 'Music', 'Books', 'Sports'
# #                ]}, ["name", "description", "price", "category"])

# # key="category"
# # value="Garden"
# # l1=None

# # with open("Productos.txt", "r") as P:
# #     l1=json.loads(P.read())

# # l2=[i for i in l1 if i[key]==value]


#identificar ind=l1.index(l2[0])

#extraer l2=l1.pop(ind)

#modificar l2["description"]="Salchipapas"

# reinsertar
# l1.insert(ind, l2)

# with open("Productos.txt", "w") as P:
#     P.write(json.dumps(l1, indent=4))