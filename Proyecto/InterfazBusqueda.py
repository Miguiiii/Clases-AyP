import json
#Todos los gestores son hijos de una de estas dos clases, pues en todos se debe poder buscar información
class Busqueda:

    def _KeyValue_search(self, name, search_keys):
        
        print(
            f"[ Buscar {name} ]".center(40, "*")
        )
        while True:
            #Imprime las opciones de Keys de búsqueda que tiene el gestor que la llamó
            for i in search_keys.keys():
                index=list(search_keys.keys()).index(i)+1
                if type(i)==tuple:
                    print(f"{index}.-", "/".join(i))
                    continue
                print(f"{index}.- {i.capitalize()}")
            try:
                self.s_Key=int(input("Ingrese el número del tipo de dato a buscar: "))-1
                self.s_Key=list(search_keys.keys())[self.s_Key]
                break
            except IndexError:
                print("ADVERTENCIA: Por favor ingrese una opción válida")
            except ValueError:
                print("ADVERTENCIA: Por favor rellene el campo con el tipo de información requerida")
        self.Key=self.s_Key
        #Si la key es una tupla, significa que en su posición en el elemento puede haber varias keys diferentes, mutuamente excluyentes
        if type(self.s_Key)==tuple:
            #Este segmento IF establece cuál de los elementos de la tupla es la Key que se está buscando
            while True:
                for i in range(len(self.s_Key)):
                    print(f"{i+1}.- {self.s_Key[i]}")
                try:
                    self.Key=int(input("Ingrese el número del tipo de dato a buscar: "))-1
                    self.Key=self.s_Key[self.Key]
                    break
                except IndexError:
                    print("ADVERTENCIA: Por favor ingrese una opción válida")
                except ValueError:
                    print("ADVERTENCIA: Por favor rellene el campo con el tipo de información requerida")
        if type(search_keys.get(self.Key))==list:
            #En el caso de que el Valor a buscar es predeterminado, se guarda en una lista, y se muestra aquí
            self.l_opc=search_keys[self.Key]
            print(f"Opciones de {self.Key}".center(30, "-"))
            for i in range(len(self.l_opc)):
                print(
                    f"{i+1}.- {self.l_opc[i]}"
                )
        #Esto es principalmente para los gestores que tienen como elemento a un Cliente, el cual es un diccionario de valores
        elif type(search_keys[self.s_Key])==dict:
            #Permite buscar en el gestor un elemento cuyo cliente cumpla con las condiciones de búsqueda de un cliente normal, pero aplicadas en otro elemento
            self.out_key=self.s_Key
            self._KeyValue_search("Cliente", search_keys[self.s_Key])
            return

        while True:
            if type(search_keys[self.s_Key])==str:
                #Esto ayuda a no tener que verificar cada vez que se busca una string, pues solo se pone un ejemplo del tipo de dato que se está buscando
                print("Ejemplo de dato seleccionado:")
                print(search_keys[self.s_Key])
            self.Value=input(f"Ingrese el valor a buscar en la casilla de {self.Key}: ")
            if search_keys[self.s_Key] not in [int, float] and type(search_keys[self.s_Key])!=list:
                #Si el Valor a buscar es una string, esta función se detiene aquí
                return
            try:
                #Dependiendo de si el valor se supone que sea un Float o Int, comprueba uno u otro
                if search_keys[self.s_Key]==float:
                    self.Value=float(self.Value)
                else:
                    self.Value=int(self.Value)
                if not self.Value>0:
                    raise Exception
                if type(search_keys[self.s_Key])==list:
                    #En este caso, como las opciones son predeterminadas, al ingresar un valor Int, se está seleccionando uno de los indices de la lista de opciones
                    self.Value-=1
                    if self.Value not in range(len(search_keys[self.s_Key])):
                        raise IndexError
                    self.Value=self.l_opc[self.Value]
                break
            except:
                if search_keys[self.s_Key] in [int, float]:
                    print("ADVERTENCIA: Por favor rellene el campo con el tipo de información requerida")
                elif type(search_keys[self.s_Key])==list:
                    print("ADVERTENCIA: Por favor ingrese una opción válida")

    def _buscar(self, name, search_keys):
        #Llama a la función de ingresar los valores de la Key y el Valor a buscar
        self._KeyValue_search(name, search_keys)
        #Abre el archivo en el que se buscará el elemento y saca los datos
        with open(Busqueda.json_name, "r") as BaseDatos:
            self.datos=json.load(BaseDatos)
        #Out_key es un valor que no es None solo cuando el Valor a buscar es un diccionario, por lo que se debe de buscar una Key interna dentro de otra Key externa
        if self.out_key!=None:
            return [resul for resul in self.datos if resul[self.out_key][self.Key]==self.Value]
        #De lo contrario busca en la base de datos como si fuera un diccionario de valores normales
        return [resul for resul in self.datos if resul.get(self.Key, None)==self.Value]

    def display_search(self, name, search_keys):
        self.out_key=None
        #Llama a la función de buscar y obtiene los resultados de la búsqueda
        self.resultados=self._buscar(name, search_keys)
        #Esto es simplemente para el display
        if self.out_key!=None:
            self.Key=f"{self.Key} de {self.out_key}"

        #Si la función anterior devuelve una lista de resultados vacía, esta función lo indica y se detiene aquí
        if len(self.resultados)==0:
            print(f"[ No se han encontrado {name} con {self.Key}={self.Value} ]".center(40, "*"))
            return False
        
        print(
            f"[ {name} con {self.Key}={self.Value} ]".center(50, "*")
        )
        #De lo contrario, imprime de forma normal los pares Key:Value de cada resultado enumerado
        for i in range(len(self.resultados)):
            p=self.resultados[i]
            print(f"{i+1}".center(31, "-"))
            for key, value in p.items():
                #Si el valor es un diccionario, esto lo imprime de forma más presentable
                if type(value)==dict:
                    print(f"{key}:")
                    for k, v in value.items():
                        print(
                            f"   {k}: {v}"
                        )
                    continue
                print(
                    f"{key}: {value}"
                )
        print("-"*31)

    def __init__(self, json_name):
        #Establece el nombre del archivo JSON y el nombre del gestor
        Busqueda.json_name=json_name
        Busqueda.Classname=self.json_name.removesuffix(".json")

#Solo Producto y Cliente son hijos de Modificar, pues solo esos gestores permiten modificar información de la base de datos
class Modificar(Busqueda):

    def identificar(self, search_keys):
        #Esto llama a la función de mostrar los resultados de una búsqueda
        encontrado=self.display_search(Modificar.Classname, search_keys)
        #Si no se encuentra nada, empieza una reacción en cadena que termina devolviendo False
        if encontrado==False:
            return encontrado
        #Si se encuentra algo, este display sirve para identificar cuál de los elementos encontrados quieres seleccionar
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

    def extraer(self, search_keys, eliminar=False):
        #Llama a la función de identificar
        encontrado=self.identificar(search_keys)
        #Esta función extrae el elemento seleccionado de la base de datos y almacena su índice en la misma
        if encontrado==False:
            return False
        self.Mod_index=self.datos.index(self.Mod_element)
        self.datos.remove(self.Mod_element)
        if eliminar:
            #Si se llama a esta función para eliminar el elemento seleccionado, este código se ejecuta
            with open(Modificar.json_name, "w") as file:
                json.dump(self.datos, file, indent=2)
            print("El elemento seleccionado ha sido removido con éxito de la base de datos de la tienda.")
            return
    
    def _modificar(self, l_keys, search_keys, venta):
        encontrado=self.extraer(search_keys)
        if encontrado==False:
            #si no se encuentra nada, devuelve False
            return False
        if venta:
            #Si se llama esta función para comprar, se ejecuta este bloque para elegir la cantidad del producto a extraer, para así modificarlo en la base de datos
            while True:
                print("-"*31)
                for key, value in self.Mod_element.items():
                    print(f"{key}: {value}")
                print("-"*31)
                try:
                    cant=int(input("Ingrese la cantidad de {} que agregar al carrito de compra: ".format(self.Mod_element["name"])))
                    if cant<=0:
                        raise ValueError
                except ValueError:
                    print("ADVERTENCIA: Por favor ingrese los campo con el tipo de información requerida")
                    continue
                if cant>self.Mod_element["quantity"]:
                    print("ADVERTENCIA: La cantidad ingresada supera a la disponible en el inventario")
                    continue
                cant=cant
                break
            self.Prod_comprado=self.Mod_element.copy()
            self.Mod_element["quantity"]-=cant
            self.Prod_comprado["quantity"]=cant
            return

        self.lista_keys=list(l_keys.keys())
        
    def reinsertar(self, l_keys, search_keys, venta=False, cancelar=False, P_Cancelado=None):
        #Si no se está llamando esta función para cancelar una venta, se ejecuta este bloque
        if not cancelar:
            encontrado=self._modificar(l_keys, search_keys, venta)
            if encontrado==False:
                return False

        else:
            #De lo contrario, al llamarse esta función en Cancelar=True, el elemento indicado es devuelto a su índice en la base de datos            
            self.Mod_index=P_Cancelado[0]
            self.Prod_cantidad=P_Cancelado[1]
            with open(Modificar.json_name, "r") as file:
                self.datos=json.load(file)
            self.Mod_element=self.datos.pop(self.Mod_index)
            self.Mod_element["quantity"]+=self.Prod_cantidad
        
        #El resto de este bloque reinserta el elemento encontrado/indicado de vuelta en los datos del archivo externo
        self.datos.insert(self.Mod_index, self.Mod_element)
        with open(Modificar.json_name, "w") as file:
            json.dump(self.datos, file, indent=2)

        if venta:
            return self.Mod_index, self.Prod_comprado
        
        if not cancelar:
            print("[ Elemento modificado con éxito ]".center(30, "*"))
