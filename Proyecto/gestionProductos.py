import json
from InterfazBusqueda import Modificar as IB

class Producto(IB):

    def _get_cats(self, json_name):
        with open(json_name, "r") as fh:
            self.l_categorias=list({p["category"] for p in json.load(fh)})

    def info_producto(self):
        self.nombreProducto=input("Ingrese el nombre del nuevo producto: ")
        self.descripcion=input("Ingrese una descripción para el producto: ")
        while True:
            try:
                self.precio=int(input("Ingrese el precio del producto en forma de número entero: "))
                self.disponibilidad=int(input("Ingrese la disponibilidad del producto: "))
                break
            except:
                print("ADVERTENCIA: Por favor ingrese los campo con el tipo de información requerida")
        print("Opciones de categoría".center(30, "-"))
        for i in range(len(self.l_categorias)):
            print(f"{i+1}.- {self.l_categorias[i]}")
        print(f"{len(self.l_categorias)+1}.- Crear una nueva categoría")
        while True:
            try:
                self.categoria=int(input("Ingrese la opción para establecer la categoría del producto: "))
            except:
                print("ADVERTENCIA: Por favor ingrese los campo con el tipo de información requerida")
                continue
            if self.categoria<=(len(self.l_categorias)+1):
                break
            print("ADVERTENCIA: Por favor ingrese una opción válida")

        if self.categoria==(len(self.l_categorias)+1):
            self.categoria=input("Ingrese el nombre de la nueva categoría: ")

        else:
            self.categoria=self.l_categorias[self.categoria-1]

        return dict(zip(self.l_keys, [self.nombreProducto, self.descripcion, self.precio, self.categoria, self.disponibilidad]))

    def registrar(self, json_name):
        self.info=self.info_producto()
        print("-"*30)
        print(
            f"Nombre: {self.nombreProducto}\n"
            f"Descripción: {self.descripcion}\n"
            f"Precio: {self.precio}\n"
            f"Categoría: {self.categoria}\n"
            f"Disponibilidad: {self.disponibilidad}\n"
        )
        print("-"*30)
        
        while True:
            confirmacion=input("Está seguro de que quiere agregar este producto a la tienda?    Y/N\n").upper()
            if confirmacion not in ["Y", "N"]:
                print("ADVERTENCIA: Por favor ingrese una opción válida")
                continue
            break

        if confirmacion=="N":
            return

        with open(json_name, "r") as P:
            lista_productos=json.loads(P.read())
        lista_productos.append(self.info)
        with open(json_name, "w") as P:
            P.write(json.dumps(lista_productos, indent=2))

        print("Nuevo producto registrado".center(35, "-"))

    def menu(self, json_name):
        self._get_cats(self.json_name)
        self.search_keys={"name":str, "disponibilidad":int, "price":int, "category":self.l_categorias}
        print(
            "[ Gestión de Productos ]".center(54, "*")+"\n"
            "1.- Agregar un nuevo producto\n"
            "2.- Buscar productos en la base de datos\n"
            "3.- Modificar información de productos existentes\n"
            "4.- Eliminar productos de la tienda\n"
            "5.- Regresar\n"
            )
        while True:
            opcion=input("Ingrese el número de la acción a realizar: ")
            if opcion not in ["1", "2", "3", "4", "5"]:
                print("ADVERTENCIA: Por favor ingrese un número de acción válido")
                continue
            break
        if opcion=="1":
            self.registrar(json_name)
        
        if opcion=="2":
            self.display_search(self.json_name, self.Classname, self.search_keys)
        
        if opcion=="3":
            self.reinsertar(self.l_keys, self.search_keys)
        
        if opcion=="4":
            self.extraer(self.search_keys)
        
        if opcion=="5":
            return
        
        input("Presione Enter para continuar")
        self.menu(json_name)

    def __init__(self, json_name):
        super().__init__(json_name)
        self.l_keys=["name", "description", "price", "category", "disponibilidad"]
        self.menu(self.json_name)

def main():
    Producto("Productos.json")

if __name__=="__main__":
    main()