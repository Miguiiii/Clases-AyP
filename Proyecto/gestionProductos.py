import json, InterfazBusqueda

class Producto:
    keys={"name":str, "description":str, "price":int, "category":str}
    def info_producto(self):
        self.nombreProducto=input("Ingrese el nombre del nuevo producto: ")
        self.descripcion=input("Ingrese una descripción para el producto: ")
        while True:
            try:
                self.precio=int(input("Ingrese el precio del producto en forma de número entero: "))
                break
            except:
                print("ADVERTENCIA: Por favor ingrese el campo con el tipo de información requerida")
        self.categoria=input("Ingrese la categoría del producto: ")
        self.disponibilidad=input("Ingrese la disponibilidad del producto: ")
        return dict(zip(Producto.keys, [self.nombreProducto, self.descripcion, self.precio, self.categoria]))

    def registrar(self, txt_name):
        self.info=self.info_producto()
        print(
            "   Nombre: {}".format(self.info["name"])+"\n"
            "   Descripción: {}".format(self.info["description"])+"\n"
            "   Precio: {}".format(self.info["price"])+"\n"
            "   Categoría: {}".format(self.info["category"]+"\n")
        )
        
        while True:
            confirmacion=input("Está seguro de que quiere agregar este producto a la tienda?    Y/N\n").upper()
            if confirmacion not in ["Y", "N"]:
                print("ADVERTENCIA: Por favor ingrese una opción válida")
                continue
            break

        if confirmacion=="N":
            return

        with open(txt_name, "r") as P:
            lista_productos=json.loads(P.read())
        lista_productos.append(self.info)
        with open(txt_name, "w") as P:
            P.write(json.dumps(lista_productos, indent=2))

        print("Nuevo producto registrado".center(35, "-"))


    def menu(self, txt_name):
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
            self.registrar(txt_name)
        
        if opcion=="2":
            return
        
        if opcion=="3":
            return
        
        if opcion=="4":
            return
        
        if opcion=="5":
            return

    def __init__(self, txt_name):
        self.txt_name=txt_name
        self.menu(self.txt_name)

def main():
    Producto("Productos.txt")

if __name__=="__main__":
    main()