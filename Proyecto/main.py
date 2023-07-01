import TiendaApp
#Lo de arriba importa el módulo de la aplicación de la tienda
def main():
    TiendaApp.App()

#Este if solo se ejecuta si este archivo de python se está ejecutando desde sí mismo, pero no se ejecuta si es importado en otro lado
if __name__=="__main__":
    main()

# from gestionProductos import Producto as P

# P("Productos.json").display_search(P.json_name, P.Classname, P.search_keys)


# est={1:30, 2:25, 3:35}

# dias, vals=zip(*est.items())

# print(dias)

# print(vals)

# l=[1, 2, 3, 4]

# i=l.pop(5)
# print("Listo")

# import json
# dicc={"name":"Miguel", "Ciudad":"Caracas"}

# print(" "+json.dumps(dicc, indent=2, separators=("", ": ")))