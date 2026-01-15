# ==========================================
# SIMULACIÓN SENESCYT - CON IF Y SEGMENTOS
# ==========================================

SEGMENTOS = {
    "vulnerabilidad": 0.20,
    "merito": 0.20,
    "pueblos": 0.10,
    "bachiller_actual": 0.30,
    "procesos_anteriores": 0.20,
    "excluidos": 0.10,
}


# ===============================
# ASPIRANTE
# ===============================
class Aspirante:
    def __init__(self, cedula, nombre, puntaje, segmentos, opciones):
        self.cedula = cedula
        self.nombre = nombre
        self.puntaje = puntaje
        self.segmentos = segmentos
        self.opciones = opciones
        self.carrera_asignada = None
        self.estado = "PENDIENTE"

    def porcentaje_total(self):
        total = 0
        for s in self.segmentos:
            if s in SEGMENTOS:
                total += SEGMENTOS[s]
        return total

    def mostrar(self):
        print(
            f"{self.nombre} | Puntaje: {self.puntaje} | "
            f"Segmentos: {self.segmentos} | "
            f"% Total: {self.porcentaje_total():.2f} | "
            f"Opción: {self.opciones} | "
            f"Asignado: {self.carrera_asignada or '-'}"
        )


# ===============================
# CARRERA
# ===============================
class Carrera:
    def __init__(self, nombre, cupos, puntaje_minimo):
        self.nombre = nombre
        self.cupos = cupos
        self.puntaje_minimo = puntaje_minimo

    def mostrar(self):
        print(
            f"{self.nombre} | Cupos: {self.cupos} | "
            f"Puntaje mínimo: {self.puntaje_minimo}"
        )


# ===============================
# ASIGNACIÓN (COMPARACIÓN CON IF)
# ===============================
class AsignacionSenescyt:
    def asignar(self, aspirantes, carreras, historial):
        print("\n=== PROCESO DE ASIGNACIÓN ===")

        for carrera in carreras:
            if carrera.cupos <= 0:
                continue

            candidatos = []

            for a in aspirantes:
                if a.estado == "PENDIENTE":
                    if carrera.nombre in a.opciones:
                        if a.puntaje >= carrera.puntaje_minimo:
                            candidatos.append(a)

            if len(candidatos) == 0:
                continue

            ganador = candidatos[0]

            for aspirante in candidatos[1:]:
                if aspirante.porcentaje_total() > ganador.porcentaje_total():
                    ganador = aspirante
                elif aspirante.porcentaje_total() == ganador.porcentaje_total():
                    if aspirante.puntaje > ganador.puntaje:
                        ganador = aspirante

            ganador.estado = "ASIGNADO"
            ganador.carrera_asignada = carrera.nombre
            carrera.cupos -= 1
            historial.append(ganador.nombre)

            print(
                f"Cupo asignado a {ganador.nombre} | "
                f"%={ganador.porcentaje_total():.2f} | "
                f"Puntaje={ganador.puntaje}"
            )


# ===============================
# SISTEMA (SINGLETON)
# ===============================
class Sistema:
    _instance = None

    def __init__(self):
        self.aspirantes = [
            Aspirante(
                "01", "Luis", 850,
                ["bachiller_actual"],
                ["Veterinaria"]
            ),
            Aspirante(
                "02", "Ana", 850,
                ["vulnerabilidad", "merito"],
                ["Veterinaria"]
            ),
        ]

        self.carreras = [
            Carrera("Veterinaria", 1, 800),
        ]

        self.historial = []
        self.asignador = AsignacionSenescyt()

    @staticmethod
    def get_instance():
        if Sistema._instance is None:
            Sistema._instance = Sistema()
        return Sistema._instance

    def ejecutar(self):
        self.asignador.asignar(self.aspirantes, self.carreras, self.historial)

    def ver_aspirantes(self):
        print("\n--- ASPIRANTES ---")
        for a in self.aspirantes:
            a.mostrar()

    def ver_carreras(self):
        print("\n--- CARRERAS ---")
        for c in self.carreras:
            c.mostrar()


# ===============================
# FACADE + MENÚ
# ===============================
class SistemaFacade:
    def __init__(self):
        self.sistema = Sistema.get_instance()

    def menu(self):
        while True:
            print("\n1. Ver aspirantes")
            print("2. Ver carreras")
            print("3. Ejecutar asignación")
            print("4. Salir")

            opcion = input("Opción: ")

            if opcion == "1":
                self.sistema.ver_aspirantes()
            elif opcion == "2":
                self.sistema.ver_carreras()
            elif opcion == "3":
                self.sistema.ejecutar()
            elif opcion == "4":
                break


# ===============================
# MAIN
# ===============================
if __name__ == "__main__":
    SistemaFacade().menu()