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



