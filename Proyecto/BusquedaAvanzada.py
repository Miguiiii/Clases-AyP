import json
from InterfazBusqueda import Busqueda as IB
from gestionClientes import Cliente as C

class Avanzada(IB):
    #Esta clase se encuentra en otro módulo para evitar una importación circular (Módulo de gestionCliente e InterfazBusqeuda)

    def identificar(self, search_keys):
        #Misma función que el método identificar de la clase Modificar
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
    
    def _get_stats(self, ind):
        #Obtiene las estadísticas
        with open(Avanzada.stats, "r") as file:
            estadisticas=json.load(file)[Avanzada.Classname]
        self.estadisticas=list(estadisticas.items())[ind]

    def sort_stats_ByKey(self, stats):
        #Una función para ordenar un diccionario de estadísticas en base a la Key
        return dict(sorted(stats.items()))

    def display_totales_año(self, stat_name, name, estats):
        #Se usa para el display del tipo de estadística "Totales" si se decide mostrar en base a los años
        print(f"[ {stat_name} por {name} ]".center(50, "-"))
        print(
            f"{name}".ljust(25, " ")+f"{stat_name}".rjust(25, " ")+"\n"
        )
        for a, t in estats.items():
            print(
                f"{a}".ljust(25, " ")+f"{t}".rjust(25, " ")
            )
        print(50*"-")
        return

    def display_totales(self, stat_name, name, estats):
        #Se usa para lo mismo que la función anterior, pero para el display en base a Meses, semanas y días
        print(f"[ {stat_name} por {name} ]".center(50, "-"))
        for a, k in estats.items():
            print(f" Año {a} ".center(16, "*").center(50, " "))
            print(
                f"{name}".ljust(25, " ")+f"{stat_name}".rjust(25, " ")+"\n"
            )
            for i, j in k.items():
                print(
                    f"{i}".ljust(25, " ")+f"{j}".rjust(25, " ")
                )
            print("")
        print(50*"-")
        return

    def menu_totales(self, stat_name, estats):
        #Para elegir de qué forma se mostrará la estadística del tipo "Totales"
        if len(estats)==0:
            name=stat_name.split(" ")[0].removesuffix("s").lower()
            print(f"[ {stat_name} ]".center(50, "-"))
            print(f"No hay ningún(a) {name} registrado".center(50, " "))
            print(50*"-"+"\n")
            return input("Presione Enter para continuar")

        print(f"{stat_name} por cada: ")
        print(
            "   1.- Año\n"
            "   2.- Mes\n"
            "   3.- Semana\n"
            "   4.- Día"
        )
        while True:
            try:
                eleccion=int(input("Ingrese el número de la elección: "))
                if eleccion not in [1, 2, 3, 4]:
                    raise IndexError
                break
            except ValueError:
                print("ADVERTENCIA: Por favor rellene el campo con el tipo de información requerida")
                input("Presione Enter para continuar")
            except IndexError:
                print("ADVERTENCIA: Por favor ingrese una opción válida")
                input("Presione Enter para continuar")
        
        print("")
        estats=self.sort_stats_ByKey(estats)
        if eleccion==1:
            reg="Año"
            estats={año:sum(dicc["dias"].values()) for año, dicc in estats.items()}
            return self.display_totales_año(stat_name, reg, estats)
        if eleccion==2:
            reg="Mes"
            estats={año:self.sort_stats_ByKey(dicc["meses"]) for año, dicc in estats.items()}

        elif eleccion==3:
            reg="Semana"
            estats={año:self.sort_stats_ByKey(dicc["semanas"]) for año, dicc in estats.items()}

        elif eleccion==4:
            reg="Día"
            estats={año:self.sort_stats_ByKey(dicc["dias"]) for año, dicc in estats.items()}

        return self.display_totales(stat_name, reg, estats)

    def sort_stats_ByValue(self, stats):
        #Una función para ordenar un diccionario de estadísticas en base a los Valores
        stats=stats
        stats=dict(sorted(stats.items(), key=lambda item: item[1], reverse=True))
        return stats

    def display_productos(self, stat_name, estats):
        #Para el display de la estadística del tipo "Productos"
        print(f"[ {stat_name} ]".center(50, "-"))
        stat_name=stat_name.split(" ")
        name=stat_name[0].removesuffix("s").lower()
        stat=" ".join(stat_name[1:]).removesuffix("s")

        if len(estats)==0:
            print(f"No hay ningún {name} {stat}".center(50, " "))
            print(50*"-"+"\n")
            return input("Presione Enter para continuar")
        
        stat=stat_name[-1].removesuffix("s")

        print(
            f"{name}".capitalize().ljust(25, " ")+f"Nº de veces {stat}".rjust(25, " ")+"\n"
        )

        for prod, n in estats.items():
            print(
                f"{prod}".ljust(25, " ")+f"{n}".rjust(25, " ")
            )
        print(50*"-")
        return
        
    def display_frecuentes(self, stat_name, estats):
        #Para el display de la estadística del tipo "Frecuentes" (Habla de los clientes)
        print(f"[ {stat_name} ]".center(58, "-"))

        if len(estats)==0:
            stat=" ".join(stat_name[1:])
            print("No hay ningún cliente que compre frecuentemente".center(58, " "))
            print(58*"-"+"\n")
            return input("Presione Enter para continuar")
    
        print(
            "Cliente".ljust(29, " ")+"Compras Realizadas".rjust(29, " ")+"\n"
        )
        for client, frec in estats.items():
            print(
                f"{client}".ljust(25, " ")+f"{frec}".rjust(25, " ")
            )
        print(50*"-")
        return
        
    def display_pendientes(self, stat_name, estats):
        #Para el display de la estadística del tipo "Pendientes" (Tanto Pagos como Envíos)
        print(f"[ {stat_name} ]".center(50, "-"))
        stat_name=stat_name.split(" ")
        name=stat_name[0].removesuffix("s").lower()

        if len(estats)==0:
            stat=" ".join(stat_name[1:])
            print(f"No hay ningún {name} {stat}".center(50, " "))
            print(50*"-"+"\n")
            return input("Presione Enter para continuar")
        
        stat=" ".join(stat_name[2:])
        
        print(
            f"{name}".capitalize().ljust(25, " ")+f"{stat}".capitalize().rjust(25, " ")+"\n"
        )
        for client, pend in estats.items():
            print(
                f"{client}".ljust(25, " ")+f"{pend}".rjust(25, " ")
            )
        print(50*"-")
        return

    def menu_estad(self, Stat_keys):
        #El menú en el que se elige la estadística a visualizar de la clase que la llamó
        print("\n"+f"[ Estadísticas de {Avanzada.Classname} ]".center(40, "*"))
        for i in range(len(Stat_keys)):
            print(f"{i+1}.- {Stat_keys[i]}")
        print(f"{len(Stat_keys)+1}.- Regresar")
        try:
            eleccion_ind=int(input("Ingrese el número del tipo de estadísticas a mostrar: "))-1
            if eleccion_ind==len(Stat_keys):
                return
            eleccion_stat=Stat_keys[eleccion_ind]
        except ValueError:
            print("ADVERTENCIA: Por favor rellene el campo con el tipo de información requerida")
            input("Presione Enter para continuar")
            return self.menu_estad(Stat_keys)
        except IndexError:
            print("ADVERTENCIA: Por favor ingrese una opción válida")
            input("Presione Enter para continuar")
            return self.menu_estad(Stat_keys)
        self._get_stats(eleccion_ind)
        
        if self.estadisticas[0]=="Totales":
            return self.menu_totales(eleccion_stat, self.estadisticas[1])
        self.sorted_estadisticas=self.sort_stats_ByValue(self.estadisticas[1])
        if self.estadisticas[0]=="Pendientes":
            return self.display_pendientes(eleccion_stat, self.sorted_estadisticas)
        elif self.estadisticas[0]=="Frecuentes":
            return self.display_frecuentes(eleccion_stat, self.sorted_estadisticas)
        elif self.estadisticas[0]=="Productos":
            return self.display_productos(eleccion_stat, self.sorted_estadisticas)
        
    def __init__(self, json_name, stats_json):
        Avanzada.ClientSearchKeys=C("Clientes.json").search_keys
        Avanzada.search_keys={"Cliente":Avanzada.ClientSearchKeys, "Fecha":"27/06/2023\nFormato: dd/mm/aaaa (día/mes/año)"}
        super().__init__(json_name)
        Avanzada.stats=stats_json
        