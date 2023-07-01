import TiendaApp
#Lo de arriba importa el módulo de la aplicación de la tienda
def main():
    TiendaApp.App()

#Este if solo se ejecuta si este archivo de python se está ejecutando desde sí mismo, pero no se ejecuta si es importado en otro lado
if __name__=="__main__":
    main()