import json
from InterfazBusqueda import Modificar as IB

class Producto(IB):

    def _get_cats(self, json_name):
        with open(json_name, "r") as fh:
            Producto.l_categorias=list({p["category"] for p in json.load(fh)})

    def info_producto(self):
        self.nombreProducto=input("Ingrese el nombre del nuevo producto: ")
        self.descripcion=input("Ingrese una descripción para el producto: ")
        while True:
            try:
                self.precio=int(input("Ingrese el precio del producto en forma de número entero: "))
                self.quantity=int(input("Ingrese la cantidad disponible de este producto: "))
                break
            except:
                print("ADVERTENCIA: Por favor ingrese los campo con el tipo de información requerida")
        print("Opciones de categoría".center(30, "-"))
        for i in range(len(Producto.l_categorias)):
            print(f"{i+1}.- {Producto.l_categorias[i]}")
        print(f"{len(Producto.l_categorias)+1}.- Crear una nueva categoría")
        while True:
            try:
                self.categoria=int(input("Ingrese la opción para establecer la categoría del producto: "))-1
            except:
                print("ADVERTENCIA: Por favor ingrese los campo con el tipo de información requerida")
                continue
            if self.categoria in range(len(Producto.l_categorias)):
                self.categoria=Producto.l_categorias[self.categoria]
                break
            elif self.categoria==(len(Producto.l_categorias)):
                self.categoria=input("Ingrese el nombre de la nueva categoría: ").lower().capitalize()
                if self.categoria in Producto.l_categorias:
                    print("ADVERTENCIA: Esta categoría ya exsiste")
                    continue
                break
            print("ADVERTENCIA: Por favor ingrese una opción válida")

        return dict(zip(Producto.l_keys, [self.nombreProducto, self.descripcion, self.precio, self.categoria, self.quantity]))

    def registrar(self, json_name):
        self.info=self.info_producto()
        print("-"*30)
        print(
            f"Nombre: {self.nombreProducto}\n"
            f"Descripción: {self.descripcion}\n"
            f"Precio: {self.precio}\n"
            f"Categoría: {self.categoria}\n"
            f"Cantidad disponible: {self.quantity}"
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
            json.dump(lista_productos, P, indent=2)
        Producto.l_categorias.append(self.categoria)

        print("Nuevo producto registrado".center(35, "-"))

    def menu(self, json_name):
        Producto.search_keys={"name":str, "quantity":int, "price":int, "category":Producto.l_categorias}
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
            self.display_search(Producto.json_name, Producto.Classname, Producto.search_keys)
        
        if opcion=="3":
            self.reinsertar(Producto.l_keys, Producto.search_keys)
        
        if opcion=="4":
            self.extraer(Producto.search_keys, True)
        
        if opcion=="5":
            return
        
        input("Presione Enter para continuar")
        self.menu(json_name)

    def __init__(self, json_name):
        super().__init__(json_name)
        Producto.l_keys={"name":str, "description":str, "price":int, "category":Producto.l_categorias, "quantity":int}
        self._get_cats(Producto.json_name)
        self.menu(Producto.json_name)

def main():
    Producto("Productos.json")

if __name__=="__main__":
    main()