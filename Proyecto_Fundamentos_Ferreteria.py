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

