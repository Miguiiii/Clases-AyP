import json

class Busqueda:

    def KeyValue_search(self, keys):
        keys=keys
        while True:
            for i in keys.keys():
                index=list(keys.keys()).index(i)+1
                print(f"{index}.- {i.capitalize()}")
            try:
                self.Key=int(input("Ingrese el número del tipo de dato a buscar: "))-1
                self.Key=list(keys.keys())[self.Key]
                break
            except:
                print("ADVERTENCIA: Por favor ingrese una opción válida")         

        while True:
            self.Value=input(f"Ingrese el valor a buscar en la casilla de {self.Key}: ")
            if keys[self.Key]==int:
                try:
                    self.Value=int(self.Value)
                except:
                    print("ADVERTENCIA: Por favor ingrese el campo con el tipo de información requerida")
                    continue
            break
        print(self.Key, self.Value)

    def __init__(self, txt_name, keys):
        self.txt_name=txt_name
        self.KeyValue_search(keys)

class Modificar(Busqueda):

    def __init__(self, txt_name, keys):
        super().__init__(txt_name, keys)

# Busqueda("Productos.txt", {"name":str, "description":str, "price":int, "category":str})



# key="category"
# value="Garden"
# l1=None

# with open("Productos.txt", "r") as P:
#     l1=json.loads(P.read())


# l2=[i for i in l1 if i[key]==value]

# ind=l1.index(l2[0])

# l2=l1.pop(ind)

# l2["description"]="Salchipapas"

# l1.insert(ind, l2)

# with open("Productos.txt", "w") as P:
#     P.write(json.dumps(l1, indent=4))