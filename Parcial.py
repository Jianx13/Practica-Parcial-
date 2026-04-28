#Programa que simula un parcial, el programa se encarga de comprar de boletas, la cantidad y la finalizacion de compra
import os 
import time 

pelicula =[
    ("Avengers: Doomsday", "120 min", "13+"),
    ("Toy Story 5", "90 min", "6+"),
    ("El Rey León 2", "110 min", "6+"),
    ("Dune: Parte 3", "130 min", "16+"),
    ("Michael", "100 min", "13+")
]

# CORRECCIÓN 1: claves de 0 a 4 para coincidir con el índice de la lista pelicula
horarios = {
    0: ["12:00 PM", "3:00 PM", "6:00 PM"],
    1: ["1:00 PM", "4:00 PM", "7:00 PM"],
    2: ["11:00 AM", "2:00 PM", "5:00 PM"],
    3: ["12:30 PM", "3:30 PM", "6:30 PM"],
    4: ["1:30 PM", "4:30 PM", "7:30 PM"]
}

boleteria = {
    "1": ("Estandar", 15_000),
    "2": ("VIP", 25_000),
}

historial_compras: list[dict] = []

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar():
    input("\n Presione Enter para continuar...")

def linea(caracter="─", ancho=52):
    print("  " + caracter * ancho)
    
def titulo(texto: str):
    linea()
    linea("═")
    print(f"  {'🎬  CINECOLOMBIA 🎬':^50}")
    linea("═")
    if texto:
        print(f"  {texto}")
        linea()
        
        
def mostrar_cartelera():
    titulo("CARTELERA DE HOY")
    print(f"  {'#':<4} {'Película':<25}  {'Duración':>10}  {'Clasif.'}")
    linea()
    for i, peli in enumerate(pelicula, 1):
        nombre, duracion, clasif = peli
        print(f"  {i:<4} {nombre:<25}  {duracion:>10}  {clasif}")
    linea()


def seleccionar_pelicula() -> tuple | None:
    mostrar_cartelera()
    print("  [0] Volver al menú principal\n")
    while True:
        try:
            opcion = input("  Elige el número de la película: ").strip()
            if opcion == "0":
                return None
            indice = int(opcion) - 1
            if not (0 <= indice < len(pelicula)):
                raise ValueError
            return (indice, pelicula[indice])
        except ValueError:
            print(f"  ⚠  Ingresa un número entre 1 y {len(pelicula)}.")


def seleccionar_horario(indice_peli: int) -> str | None:
    # CORRECCIÓN 2: variable renombrada a "lista_horarios" para no pisar
    # el diccionario global "horarios" --> antes causaba UnboundLocalError
    lista_horarios = horarios[indice_peli]
    nombre = pelicula[indice_peli][0]
    titulo(f"HORARIOS  —  {nombre}")
    for i, h in enumerate(lista_horarios, 1):
        print(f"  [{i}]  {h}")
    print("  [0]  Volver\n")
    while True:
        try:
            opcion = input("  Elige el horario: ").strip()
            if opcion == "0":
                return None
            idx = int(opcion) - 1
            if not (0 <= idx < len(lista_horarios)):
                raise ValueError
            return lista_horarios[idx]
        except ValueError:
            print(f"  ⚠  Opción inválida. Elige entre 1 y {len(lista_horarios)}.")


def seleccionar_tipo_boleta() -> tuple | None:
    titulo("TIPO DE BOLETA")
    for key, (tipo, precio) in boleteria.items():
        print(f"  [{key}]  {tipo:<15}  ${precio:,}")
    print("  [0]  Volver\n")
    while True:
        opcion = input("  Elige el tipo de boleta: ").strip()
        if opcion == "0":
            return None
        if opcion in boleteria:
            return boleteria[opcion]
        print("  ⚠  Opción no válida.")

        
def pedir_cantidad() -> int | None:
    while True:
        try:
            cantidad = int(input("  ¿Cuántas boletas? (1-10, 0 para volver): ").strip())
            if cantidad == 0:
                return None
            if not (1 <= cantidad <= 10):
                raise ValueError
            return cantidad
        except ValueError:
            print("  ⚠  Ingresa un número entre 1 y 10.")


def confirmar_compra(resumen: dict) -> bool:
    titulo("RESUMEN DE COMPRA")
    peli = resumen["pelicula"]
    # CORRECCIÓN 3: peli[0] es el nombre, peli[1] es la duración
    # antes usaba peli[1] para el nombre, mostrando "120 min" en vez del título
    print(f"  Película   : {peli[0]}")
    print(f"  Duración   : {peli[1]}")
    print(f"  Horario    : {resumen['horario']}")
    print(f"  Tipo       : {resumen['tipo_boleta']}")
    print(f"  Cantidad   : {resumen['cantidad']}")
    print(f"  Precio c/u : ${resumen['precio_unitario']:,}")
    linea()
    print(f"  TOTAL      : ${resumen['total']:,}")
    linea()
    print("  [1] Confirmar y pagar")
    print("  [0] Cancelar\n")
    while True:
        opcion = input("  Tu elección: ").strip()
        if opcion == "1":
            return True
        if opcion == "0":
            return False
        print("  ⚠  Escribe 1 para confirmar o 0 para cancelar.")
        
        
def procesar_pago(total: int):
    titulo("PAGO EN EFECTIVO")
    print(f"  Total a pagar: ${total:,}\n")
    while True:
        try:
            pago = int(input("  Monto entregado por el cliente: $").replace(",", "").strip())
            if pago <= 0:
                raise ValueError("El monto debe ser positivo.")
            if pago < total:
                faltante = total - pago
                print(f"  ⚠  Monto insuficiente. Faltan ${faltante:,}.")
            else:
                cambio = pago - total
                print("\n  Pago recibido correctamente.")
                if cambio > 0:
                    print(f"  Cambio al cliente: ${cambio:,}")
                return
        except ValueError as e:
            if "positivo" in str(e):
                print(f"  ⚠  {e}")
            else:
                print("  ⚠  Solo se aceptan números enteros.")


def generar_ticket(compra: dict):
    titulo("  TU TICKET  ")
    peli = compra["pelicula"]
    print(f"  {'CINECOLOMBIA — Comprobante de compra':^50}")
    linea("· ")
    # CORRECCIÓN 4: la tupla tiene solo 3 elementos (índices 0, 1, 2)
    # antes peli[3] causaba IndexError porque no existe ese índice
    print(f"  Película      : {peli[0]}")
    print(f"  Duración      : {peli[1]}")
    print(f"  Clasificación : {peli[2]}")
    print(f"  Horario       : {compra['horario']}")
    print(f"  Tipo boleta   : {compra['tipo_boleta']}")
    print(f"  Cantidad      : {compra['cantidad']}")
    linea("· ")
    print(f"  TOTAL PAGADO: ${compra['total']:,}")
    linea("═")
    print("  ¡Que disfrutes la función!")
    linea("═")


def ver_historial():
    titulo("HISTORIAL DE COMPRAS")
    if not historial_compras:
        print("  Aún no se ha realizado ninguna compra en esta sesión.")
        pausar()
        return
    total_sesion = 0
    for i, compra in enumerate(historial_compras, 1):
        peli = compra["pelicula"]
        print(f"  Compra #{i}")
        print(f"    {peli[0]}  |  {compra['horario']}  |  "
              f"{compra['tipo_boleta']}  x{compra['cantidad']}  =  ${compra['total']:,}")
        total_sesion += compra["total"]
    linea()
    print(f"  Total recaudado en la sesión: ${total_sesion:,}")
    pausar()


def flujo_compra():
    # 1. Elegir película
    resultado = seleccionar_pelicula()
    if resultado is None:
        return
    # CORRECCIÓN 5: variable renombrada a "peli_elegida" para no pisar
    # la lista global "pelicula" --> antes rompía seleccionar_horario y generar_ticket
    indice_peli, peli_elegida = resultado

    # 2. Elegir horario
    horario = seleccionar_horario(indice_peli)
    if horario is None:
        return

    # 3. Tipo de boleta
    resultado_boleta = seleccionar_tipo_boleta()
    if resultado_boleta is None:
        return
    tipo_nombre, precio_unitario = resultado_boleta

    # 4. Cantidad
    titulo(f"CANTIDAD  —  {peli_elegida[0]}")
    cantidad = pedir_cantidad()
    if cantidad is None:
        return

    # 5. Construir resumen
    total = precio_unitario * cantidad
    resumen = {
        "pelicula":        peli_elegida,
        "horario":         horario,
        "tipo_boleta":     tipo_nombre,
        "cantidad":        cantidad,
        "precio_unitario": precio_unitario,
        "total":           total,
    }

    # 6. Confirmar
    if not confirmar_compra(resumen):
        print("\n  Compra cancelada.")
        pausar()
        return

    # 7. Pago
    procesar_pago(total)

    # 8. Guardar en historial y mostrar ticket
    historial_compras.append(resumen)
    time.sleep(0.8)
    generar_ticket(resumen)
    pausar()


def menu_principal():
    while True:
        titulo("")
        print("  [1]  Ver cartelera")
        print("  [2]  Comprar boletas")
        print("  [3]  Ver historial de compras")
        print("  [0]  Salir\n")
        opcion = input("  ¿Qué deseas hacer? ").strip()

        if opcion == "1":
            mostrar_cartelera()
            pausar()
        elif opcion == "2":
            flujo_compra()
        elif opcion == "3":
            ver_historial()
        elif opcion == "0":
            limpiar_pantalla()
            print("\n  ¡Hasta la próxima! \n")
            break
        else:
            print("  ⚠  Opción no válida.")
            time.sleep(1)
            
if __name__ == "__main__":
    menu_principal()