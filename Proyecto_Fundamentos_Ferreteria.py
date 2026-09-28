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

