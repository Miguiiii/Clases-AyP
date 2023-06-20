import json

class Busqueda:

    def KeyValue_search(self, keys, name):
        self.l_keys=keys
        print(
            f"[ Buscar {name} ]".center(40, "*")
        )
        while True:
            for i in self.l_keys.keys():
                index=list(self.l_keys.keys()).index(i)+1
                print(f"{index}.- {i.capitalize()}")
            try:
                self.Key=int(input("Ingrese el número del tipo de dato a buscar: "))-1
                self.Key=list(self.l_keys.keys())[self.Key]
                break
            except:
                print("ADVERTENCIA: Por favor ingrese una opción válida")         

        while True:
            self.Value=input(f"Ingrese el valor a buscar en la casilla de {self.Key}: ")
            if self.l_keys[self.Key]==int:
                try:
                    self.Value=int(self.Value)
                except:
                    print("ADVERTENCIA: Por favor ingrese el campo con el tipo de información requerida")
                    continue
            break

    def buscar(self, txt_name):
        
        with open(txt_name, "r") as BaseDatos:
            self.datos=json.loads(BaseDatos.read())

        self.resultados=[resul for resul in self.datos if resul[self.Key]==self.Value]

    def display_search(self, name):
        print(
            f"[ {name} con {self.Key}={self.Value} ]".center(40, "*")
        )
        for i in range(len(self.resultados)):
            p=self.resultados[i]
            k=list(self.l_keys.keys())
            print(
                f"{i+1}.-", p[k[0]]
            )

    def __init__(self, txt_name, keys):
        self.txt_name=txt_name
        self.KeyValue_search(keys, self.txt_name.removesuffix(".txt"))
        self.buscar(self.txt_name)
        self.display_search(self.txt_name.removesuffix(".txt"))


class Modificar(Busqueda):

    def extraer(self):
        pass

    def __init__(self, txt_name, keys):
        super().__init__(txt_name, keys)





# # Busqueda("Productos.txt", {"name":str, "description":str, "price":int, "category":str})

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