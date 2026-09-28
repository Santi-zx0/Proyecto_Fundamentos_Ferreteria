# ==============================================================================
# PROYECTO FINAL - FUNDAMENTOS DE PROGRAMACIÓN
# Sistema de Inventario y Ventas para una Ferretería
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# CONSTANTES GLOBALES (valores que no cambian durante la ejecución)
# ------------------------------------------------------------------------------
ARCHIVO_INVENTARIO = "inventario.csv"  # Archivo CSV donde se guarda el inventario
ARCHIVO_VENTAS = "ventas.csv"  # Archivo CSV donde se acumula el historial de ventas
LIMITE_STOCK_BAJO = 5  # Un producto con 5 unidades o menos está en "stock bajo"
ENCABEZADO_INVENTARIO = "nombre,precio,cantidad"  # Primera línea del CSV de inventario
ENCABEZADO_VENTAS = "producto,cantidad,precio_unitario,total"  # Primera línea del CSV de ventas
LINEA_SEPARADORA = "-" * 60  # Línea decorativa para separar secciones en pantalla


# ==============================================================================
# FUNCIONES AUXILIARES PARA LEER DATOS DEL USUARIO (con manejo de excepciones)
# ==============================================================================

def leer_entero(mensaje_pedido, valor_minimo):
    # Función que regresa valor: pide un número entero y no deja avanzar
    # hasta que el usuario escriba un entero válido mayor o igual al mínimo.
    while True:  # Se repite hasta obtener un dato correcto
        try:  # Intentamos convertir lo que escribió el usuario
            numero_leido = int(input(mensaje_pedido))  # Convierte el texto a entero
            if numero_leido >= valor_minimo:  # Revisa que cumpla el mínimo permitido
                return numero_leido  # Dato válido: se regresa y termina la función
            print(f"  El número debe ser mayor o igual a {valor_minimo}.")  # Aviso de rango
        except ValueError:  # Ocurre si el usuario escribe letras o decimales
            print("  Entrada inválida. Escribe un número entero (ejemplo: 10).")  # Mensaje amigable


def leer_decimal_positivo(mensaje_pedido):
    # Función que regresa valor: pide un número decimal que sea MAYOR a 0
    # (regla de negocio: el precio siempre debe ser mayor a 0).
    while True:  # Se repite hasta obtener un precio válido
        try:  # Intentamos convertir el texto a decimal
            numero_decimal = float(input(mensaje_pedido))  # Convierte el texto a float
            if numero_decimal > 0:  # El precio tiene que ser positivo
                return numero_decimal  # Precio válido, se regresa
            print("  El precio debe ser mayor a 0. Intenta de nuevo.")  # Regla de negocio
        except ValueError:  # Ocurre si el usuario escribe texto no numérico
            print("  Entrada inválida. Escribe un número (ejemplo: 25.50).")  # Mensaje amigable


def leer_nombre_producto(mensaje_pedido):
    # Función que regresa valor: pide el nombre de un producto, lo limpia de
    # espacios y lo convierte a minúsculas para que la búsqueda no dependa
    # de mayúsculas ("Martillo" y "martillo" son el mismo producto).
    while True:  # Se repite hasta tener un nombre válido
        nombre_escrito = input(mensaje_pedido).strip().lower()  # Quita espacios y pasa a minúsculas
        if nombre_escrito == "":  # No se permite un nombre vacío
            print("  El nombre no puede estar vacío.")  # Aviso al usuario
        elif "," in nombre_escrito:  # La coma rompería el formato del archivo CSV
            print("  El nombre no puede contener comas (,).")  # Aviso al usuario
        else:  # El nombre es válido
            return nombre_escrito  # Se regresa el nombre ya limpio


def formato_moneda(cantidad_dinero):
    # Función que regresa valor: convierte un número a texto con formato de
    # moneda, por ejemplo 1250 -> "$1,250.00".
    return f"${cantidad_dinero:,.2f}"  # :,.2f agrega comas de miles y 2 decimales


# ==============================================================================
# RF10. CARGAR INVENTARIO AL INICIAR (lectura de archivos + excepciones)
# ==============================================================================

def cargar_inventario():
    # Función que regresa valor: lee el archivo CSV y regresa un diccionario
    # con la forma {nombre: [precio, cantidad]}.
    inventario_cargado = {}  # Diccionario vacío donde se guardarán los productos
    try:  # Intentamos abrir el archivo (puede no existir la primera vez)
        with open(ARCHIVO_INVENTARIO, "r", encoding="utf-8") as archivo_lectura:  # Abre en modo lectura
            lineas_archivo = archivo_lectura.readlines()  # Lee todas las líneas en una lista
        for numero_linea in range(1, len(lineas_archivo)):  # Empieza en 1 para saltar el encabezado
            linea_limpia = lineas_archivo[numero_linea].strip()  # Quita el salto de línea
            if linea_limpia == "":  # Si la línea está vacía
                continue  # Se ignora y pasa a la siguiente
            try:  # Cada línea se valida por separado para no perder todo el archivo
                partes_linea = linea_limpia.split(",")  # Separa por comas: nombre, precio, cantidad
                nombre_producto = partes_linea[0].strip().lower()  # Primer dato: nombre
                precio_producto = float(partes_linea[1])  # Segundo dato: precio (decimal)
                cantidad_producto = int(partes_linea[2])  # Tercer dato: cantidad (entero)
                datos_producto = [precio_producto, cantidad_producto]  # Lista [precio, cantidad]
                inventario_cargado[nombre_producto] = datos_producto  # Se agrega al diccionario
            except (ValueError, IndexError):  # Línea con datos incompletos o no numéricos
                print(f"  Aviso: la línea {numero_linea + 1} tiene un error y se omitió.")  # Aviso
        total_cargados = len(inventario_cargado)  # Cuántos productos se cargaron
        print(f"Inventario cargado correctamente: {total_cargados} producto(s).")  # RF10 salida
    except FileNotFoundError:  # Primera vez que se usa el programa: no hay archivo
        print("No se encontró inventario previo. Se inició un inventario nuevo.")  # RF10 salida
    except PermissionError:  # El archivo existe pero no se puede leer (por ejemplo, abierto en Excel)
        print("No se pudo leer el inventario (¿abierto en Excel?). Se inicia vacío.")  # Aviso
    return inventario_cargado  # Regresa el diccionario (con datos o vacío)


# ==============================================================================
# RF9. GUARDAR INVENTARIO AL SALIR (escritura de archivos + excepciones)
# ==============================================================================

def guardar_inventario(inventario_actual):
    # Función que regresa valor: escribe el inventario en el CSV y regresa
    # True si se guardó bien o False si hubo un problema.
    try:  # Intentamos escribir el archivo
        with open(ARCHIVO_INVENTARIO, "w", encoding="utf-8") as archivo_escritura:  # "w" sobrescribe el archivo
            archivo_escritura.write(ENCABEZADO_INVENTARIO + "\n")  # Primero se escribe el encabezado
            for nombre_producto in inventario_actual:  # Recorre cada producto del diccionario
                precio_producto = inventario_actual[nombre_producto][0]  # Obtiene el precio
                cantidad_producto = inventario_actual[nombre_producto][1]  # Obtiene la cantidad
                linea_csv = f"{nombre_producto},{precio_producto},{cantidad_producto}\n"  # Arma la fila
                archivo_escritura.write(linea_csv)  # Escribe la fila en el archivo
        print(f"Inventario guardado correctamente en '{ARCHIVO_INVENTARIO}'.")  # RF9 salida
        return True  # Se guardó sin problemas
    except PermissionError:  # El archivo está abierto en otro programa (por ejemplo, Excel)
        print("ERROR: no se pudo guardar. Cierra el archivo en Excel.")  # Aviso
    except OSError:  # Cualquier otro problema del sistema de archivos
        print("ERROR: ocurrió un problema al escribir el archivo de inventario.")  # Aviso
    return False  # Si llegó aquí, hubo un error


def registrar_venta_en_archivo(venta_realizada):
    # Función que no regresa valor: agrega (modo "a") una venta al historial
    # ventas.csv para que quede un respaldo permanente de cada venta.
    try:  # Intentamos revisar si el archivo ya existe
        with open(ARCHIVO_VENTAS, "r", encoding="utf-8"):  # Solo lo abrimos para comprobar que existe
            archivo_existe = True  # Si se pudo abrir, ya existe
    except FileNotFoundError:  # No existe todavía
        archivo_existe = False  # Habrá que escribir el encabezado
    try:  # Intentamos agregar la venta al final del archivo
        with open(ARCHIVO_VENTAS, "a", encoding="utf-8") as archivo_ventas:  # "a" agrega sin borrar
            if not archivo_existe:  # Si es un archivo nuevo
                archivo_ventas.write(ENCABEZADO_VENTAS + "\n")  # Escribe el encabezado
            producto, cantidad, precio_unitario, total_venta = venta_realizada  # Desempaqueta la tupla
            linea_csv = f"{producto},{cantidad},{precio_unitario},{total_venta}\n"  # Arma la fila
            archivo_ventas.write(linea_csv)  # Escribe la venta
    except OSError:  # Error al escribir (permisos, archivo abierto, etc.)
        print("  Aviso: la venta se registró, pero no se respaldó en ventas.csv.")  # Aviso sin detener


# ==============================================================================
# RF1. MENÚ PRINCIPAL (función que no regresa valor)
# ==============================================================================

def mostrar_menu():
    # Imprime las 8 opciones del sistema.
    opciones_menu = ("Agregar producto", "Consultar inventario",  # Tupla: las opciones
                     "Buscar producto", "Vender producto",  # no cambian durante
                     "Reporte de stock bajo", "Ver ventas del día",  # la ejecución
                     "Ver total vendido en el día", "Salir")  # Opción 8: Salir
    print("\n" + LINEA_SEPARADORA)  # Línea superior
    print("        FERRETERÍA - SISTEMA DE INVENTARIO Y VENTAS")  # Título del menú
    print(LINEA_SEPARADORA)  # Línea inferior del título
    for numero_opcion in range(len(opciones_menu)):  # Recorre la tupla por posición
        print(f"  {numero_opcion + 1}. {opciones_menu[numero_opcion]}")  # Muestra "1. Agregar producto", etc.
    print(LINEA_SEPARADORA)  # Línea de cierre del menú


# ==============================================================================
# RF2. AGREGAR PRODUCTO NUEVO
# ==============================================================================

def agregar_producto(inventario_actual):
    # Función que no regresa valor: agrega un producto al diccionario
    # (los diccionarios se modifican directamente dentro de la función).
    print("\n--- AGREGAR PRODUCTO ---")  # Título de la sección
    nombre_producto = leer_nombre_producto("Nombre del producto: ")  # Pide el nombre
    if nombre_producto in inventario_actual:  # Revisa si ya existe (no se duplica)
        print(f"El producto '{nombre_producto.title()}' ya existe. No se agregó.")  # Aviso
        return  # Termina la función sin agregar
    precio_producto = leer_decimal_positivo("Precio unitario: $")  # Pide precio (> 0)
    cantidad_producto = leer_entero("Cantidad inicial en stock: ", 0)  # Pide cantidad (>= 0)
    inventario_actual[nombre_producto] = [precio_producto, cantidad_producto]  # Guarda el producto
    print(f"Producto agregado: {nombre_producto.title()}")  # Confirmación: nombre
    print(f"  Precio: {formato_moneda(precio_producto)}")  # Confirmación: precio
    print(f"  Cantidad: {cantidad_producto}")  # Confirmación: cantidad


# ==============================================================================
# RF3. CONSULTAR INVENTARIO COMPLETO
# ==============================================================================

def consultar_inventario(inventario_actual):
    # Función que no regresa valor: muestra todos los productos en forma de tabla.
    print("\n--- INVENTARIO COMPLETO ---")  # Título de la sección
    if len(inventario_actual) == 0:  # Si no hay productos registrados
        print("El inventario está vacío.")  # Mensaje informativo
        return  # Termina la función
    nombres_ordenados = list(inventario_actual.keys())  # Lista con los nombres de los productos
    nombres_ordenados.sort()  # Ordena alfabéticamente para que sea más legible
    print(f"{'PRODUCTO':<25}{'PRECIO':>15}{'CANTIDAD':>12}")  # Encabezado de la tabla
    print(LINEA_SEPARADORA)  # Separador
    for nombre_producto in nombres_ordenados:  # Recorre cada producto en orden
        precio_producto = inventario_actual[nombre_producto][0]  # Precio del producto
        cantidad_producto = inventario_actual[nombre_producto][1]  # Cantidad del producto
        texto_precio = formato_moneda(precio_producto)  # Precio con formato $
        print(f"{nombre_producto.title():<25}{texto_precio:>15}{cantidad_producto:>12}")  # Fila
    print(LINEA_SEPARADORA)  # Separador final
    print(f"Total de productos registrados: {len(inventario_actual)}")  # Resumen


# ==============================================================================
# RF5. BUSCAR PRODUCTO
# ==============================================================================

def buscar_producto(inventario_actual):
    # Función que no regresa valor: busca un producto por nombre y muestra sus datos.
    print("\n--- BUSCAR PRODUCTO ---")  # Título de la sección
    nombre_buscado = leer_nombre_producto("Nombre del producto a buscar: ")  # Pide el nombre
    try:  # Intentamos acceder directamente a la llave del diccionario
        datos_producto = inventario_actual[nombre_buscado]  # Si no existe, lanza KeyError
        print(f"Producto encontrado: {nombre_buscado.title()}")  # Nombre
        print(f"  Precio unitario: {formato_moneda(datos_producto[0])}")  # Precio
        print(f"  Existencia: {datos_producto[1]} unidad(es)")  # Cantidad
        if datos_producto[1] <= LIMITE_STOCK_BAJO:  # Aviso adicional si está en stock bajo
            print("  ¡Atención! Este producto está en STOCK BAJO.")  # Alerta
    except KeyError:  # El producto no está en el inventario
        print(f"No se encontró ningún producto llamado '{nombre_buscado.title()}'.")  # Mensaje amigable


# ==============================================================================
# RF4. VENDER PRODUCTO
# ==============================================================================

def vender_producto(inventario_actual, ventas_del_dia):
    # Función que no regresa valor: descuenta del inventario y agrega la venta
    # (como tupla) a la lista de ventas del día.
    print("\n--- VENDER PRODUCTO ---")  # Título de la sección
    nombre_producto = leer_nombre_producto("Nombre del producto a vender: ")  # Pide el nombre
    if nombre_producto not in inventario_actual:  # Verifica que el producto exista
        print(f"ERROR: '{nombre_producto.title()}' no existe. Venta cancelada.")  # Mensaje de error
        return  # Termina sin vender
    cantidad_vender = leer_entero("Cantidad a vender: ", 1)  # Pide cantidad (> 0, o sea >= 1)
    precio_unitario = inventario_actual[nombre_producto][0]  # Obtiene el precio actual
    stock_disponible = inventario_actual[nombre_producto][1]  # Obtiene el stock actual
    if cantidad_vender > stock_disponible:  # Regla de negocio: no vender más de lo que hay
        print(f"ERROR: stock insuficiente. Solo hay {stock_disponible} unidad(es).")  # Mensaje claro
        print("Venta cancelada.")  # El programa sigue funcionando
        return  # Termina sin vender
    inventario_actual[nombre_producto][1] = stock_disponible - cantidad_vender  # Descuenta del inventario
    total_venta = round(precio_unitario * cantidad_vender, 2)  # Calcula el total (precio × cantidad) redondeado a 2 decimales
    venta_realizada = (nombre_producto, cantidad_vender,  # Tupla de la venta:
                       precio_unitario, total_venta)  # (producto, cantidad, precio, total)
    ventas_del_dia.append(venta_realizada)  # Agrega la venta al registro del día
    registrar_venta_en_archivo(venta_realizada)  # Respaldo en ventas.csv
    print("Venta registrada con éxito:")  # Confirmación
    print(f"  Producto: {nombre_producto.title()}")  # Producto vendido
    print(f"  Cantidad: {cantidad_vender}")  # Cantidad vendida
    print(f"  Precio unitario: {formato_moneda(precio_unitario)}")  # Precio unitario
    print(f"  Total: {formato_moneda(total_venta)}")  # Total de la venta
    stock_restante = inventario_actual[nombre_producto][1]  # Stock después de la venta
    if stock_restante <= LIMITE_STOCK_BAJO:  # Aviso si quedó en stock bajo
        print(f"  Aviso: quedan {stock_restante} unidad(es) (stock bajo).")  # Alerta


# ==============================================================================
# RF6. REPORTE DE STOCK BAJO
# ==============================================================================

def obtener_stock_bajo(inventario_actual):
    # Función que regresa valor: filtra el inventario y regresa una lista de
    # listas (matriz) con [nombre, cantidad] de productos con stock <= 5.
    matriz_stock_bajo = []  # Lista vacía que se llenará con los productos filtrados
    for nombre_producto in inventario_actual:  # Recorre todo el inventario
        cantidad_producto = inventario_actual[nombre_producto][1]  # Cantidad del producto
        if cantidad_producto <= LIMITE_STOCK_BAJO:  # Condición de stock bajo
            matriz_stock_bajo.append([nombre_producto, cantidad_producto])  # Agrega una fila a la matriz
    return matriz_stock_bajo  # Regresa la matriz resultante


def reporte_stock_bajo(inventario_actual):
    # Función que no regresa valor: imprime el reporte usando la matriz filtrada.
    print(f"\n--- REPORTE DE STOCK BAJO ({LIMITE_STOCK_BAJO} unidades o menos) ---")  # Título
    matriz_stock_bajo = obtener_stock_bajo(inventario_actual)  # Obtiene la lista filtrada
    if len(matriz_stock_bajo) == 0:  # Si ningún producto cumple la condición
        print("No hay productos en stock bajo. ¡Todo en orden!")  # Mensaje informativo
        return  # Termina la función
    print(f"{'PRODUCTO':<25}{'CANTIDAD':>12}")  # Encabezado de la tabla
    print(LINEA_SEPARADORA)  # Separador
    for fila_producto in matriz_stock_bajo:  # Recorre cada fila de la matriz
        print(f"{fila_producto[0].title():<25}{fila_producto[1]:>12}")  # Columna 0: nombre, columna 1: cantidad
    print(f"Productos por reabastecer: {len(matriz_stock_bajo)}")  # Resumen


# ==============================================================================
# RF7. VER VENTAS DEL DÍA
# ==============================================================================

def ver_ventas_del_dia(ventas_del_dia):
    # Función que no regresa valor: muestra las ventas en el orden en que ocurrieron.
    print("\n--- VENTAS DEL DÍA ---")  # Título de la sección
    if len(ventas_del_dia) == 0:  # Si todavía no hay ventas
        print("Aún no se ha registrado ninguna venta en esta sesión.")  # Mensaje informativo
        return  # Termina la función
    print(f"{'#':<4}{'PRODUCTO':<22}{'CANT.':>7}{'P. UNIT.':>13}{'TOTAL':>14}")  # Encabezado
    print(LINEA_SEPARADORA)  # Separador
    numero_venta = 1  # Contador para numerar las ventas
    for venta_realizada in ventas_del_dia:  # Recorre la lista de tuplas en orden
        producto, cantidad, precio_unitario, total_venta = venta_realizada  # Desempaqueta la tupla
        texto_precio = formato_moneda(precio_unitario)  # Precio unitario con formato $
        texto_total = formato_moneda(total_venta)  # Total con formato $
        print(f"{numero_venta:<4}{producto.title():<22}{cantidad:>7}"
              f"{texto_precio:>13}{texto_total:>14}")  # Fila de la tabla
        numero_venta += 1  # Incrementa el contador


# ==============================================================================
# RF8. TOTAL VENDIDO EN EL DÍA
# ==============================================================================

def calcular_total_vendido(ventas_del_dia):
    # Función que regresa valor: suma el total de todas las ventas (acumulador).
    total_acumulado = 0.0  # Acumulador que inicia en cero
    for venta_realizada in ventas_del_dia:  # Recorre cada venta
        total_acumulado += venta_realizada[3]  # La posición 3 de la tupla es el total
    return total_acumulado  # Regresa la suma


def mostrar_total_vendido(ventas_del_dia):
    # Función que no regresa valor: muestra el total en formato de moneda.
    print("\n--- TOTAL VENDIDO EN EL DÍA ---")  # Título de la sección
    total_del_dia = calcular_total_vendido(ventas_del_dia)  # Calcula el total
    print(f"Total acumulado: {formato_moneda(total_del_dia)}")  # Ejemplo: $1,250.00
    print(f"Número de ventas: {len(ventas_del_dia)}")  # Dato adicional


# ==============================================================================
# PROGRAMA PRINCIPAL
# ==============================================================================

def main():
    # Función principal: carga el inventario, muestra el menú en ciclo y
    # guarda al salir.
    print("Iniciando sistema de la ferretería...")  # Mensaje de bienvenida
    inventario = cargar_inventario()  # RF10: carga el inventario desde el CSV
    ventas_del_dia = []  # Lista vacía para las ventas de esta sesión (tuplas)
    programa_activo = True  # Bandera booleana que controla el ciclo del menú
    try:  # Protege el ciclo por si el usuario presiona Ctrl+C
        while programa_activo:  # RF1: el menú se repite hasta elegir "Salir"
            mostrar_menu()  # Muestra las 8 opciones
            try:  # Intenta convertir la opción a entero
                opcion_elegida = int(input("Elige una opción (1-8): "))  # Lee la opción
            except ValueError:  # Si escribió letras o símbolos
                print("Opción inválida. Debes escribir un número del 1 al 8.")  # Mensaje
                continue  # Vuelve a mostrar el menú
            if opcion_elegida == 1:  # Opción 1
                agregar_producto(inventario)  # RF2
            elif opcion_elegida == 2:  # Opción 2
                consultar_inventario(inventario)  # RF3
            elif opcion_elegida == 3:  # Opción 3
                buscar_producto(inventario)  # RF5
            elif opcion_elegida == 4:  # Opción 4
                vender_producto(inventario, ventas_del_dia)  # RF4
            elif opcion_elegida == 5:  # Opción 5
                reporte_stock_bajo(inventario)  # RF6
            elif opcion_elegida == 6:  # Opción 6
                ver_ventas_del_dia(ventas_del_dia)  # RF7
            elif opcion_elegida == 7:  # Opción 7
                mostrar_total_vendido(ventas_del_dia)  # RF8
            elif opcion_elegida == 8:  # Opción 8: Salir
                guardar_inventario(inventario)  # RF9: guarda antes de terminar
                programa_activo = False  # Cambia la bandera para romper el ciclo
            else:  # Número fuera del rango 1-8
                print("Esa opción no existe. Elige un número del 1 al 8.")  # Mensaje
    except (KeyboardInterrupt, EOFError):  # El usuario cerró con Ctrl+C / Ctrl+D
        print("\nSalida inesperada detectada. Guardando inventario...")  # Aviso
        guardar_inventario(inventario)  # Guarda para no perder información
    print("¡Gracias por usar el sistema de la ferretería! Hasta pronto.")  # Despedida


main()  # Llamada a la función principal para iniciar el programa