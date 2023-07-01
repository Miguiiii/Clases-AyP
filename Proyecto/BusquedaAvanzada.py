import json
from InterfazBusqueda import Busqueda as IB
from gestionClientes import Cliente as C

class Avanzada(IB):

    def identificar(self, search_keys):
        encontrado=self.display_search(Avanzada.Classname, search_keys)
        if encontrado==False:
            return encontrado
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
                if type(value)==dict:
                    print(f"{key}:")
                    for k, v in value.items():
                        print(f"   {k}: {v}")
                    continue
                print(f"{key}: {value}")
            print("-"*31)
                
            while True:
                confirmacion=input("Está seguro de que elige este elemento?    Y/N\n").upper()
                if confirmacion not in ["Y", "N"]:
                    print("ADVERTENCIA: Por favor ingrese una opción válida")
                    continue
                break

            if confirmacion=="Y":
                return self.Mod_element
            
            else:
                return self.identificar(search_keys)
        
    def __init__(self, json_name, stats_json):
        Avanzada.ClientSearchKeys=C("Clientes.json").search_keys
        Avanzada.search_keys={"Cliente":Avanzada.ClientSearchKeys, "Fecha":"27/06/2023\nFormato: dd/mm/aaaa (día/mes/año)"}
        super().__init__(json_name)
        Avanzada.stats=stats_json
        