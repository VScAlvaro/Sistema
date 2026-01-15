# ==========================================
# SIMULACIÓN REALISTA PROCESO SENESCYT
# ==========================================

SEGMENTOS = {
    "vulnerabilidad": 20,
    "merito": 20,
    "pueblos": 10,
    "bachiller_actual": 30,
    "procesos_anteriores": 20,
    "excluidos": 10,
}

BONIFICACION_MAX = 50


# ===============================
# ASPIRANTE
# ===============================
class Aspirante:
    def __init__(self, cedula, nombre, puntaje, segmentos, opciones):
        self.cedula = cedula
        self.nombre = nombre
        self.puntaje = puntaje
        self.segmentos = segmentos  # lista de segmentos
        self.opciones = opciones
        self.carrera = None
        self.estado = "PENDIENTE"

    def bonificacion(self):
        total = sum(SEGMENTOS[s] for s in self.segmentos)
        return min(total, BONIFICACION_MAX)

    def puntaje_final(self):
        return self.puntaje + self.bonificacion()

    def mostrar(self):
        print(
            f"{self.nombre} | Puntaje: {self.puntaje} | "
            f"Bonificación: {self.bonificacion()} | "
            f"Puntaje Final: {self.puntaje_final()} | "
            f"Opciones: {self.opciones} | "
            f"Asignado: {self.carrera or '-'} | Estado: {self.estado}"
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
            f"{self.nombre} | Cupos: {self.cupos} | Puntaje mínimo: {self.puntaje_minimo}"
        )


# ===============================
# ASIGNACIÓN SENESCYT
# ===============================
class AsignacionSenescyt:
    def asignar(self, aspirantes, carreras, historial):
        rondas = max(len(a.opciones) for a in aspirantes)

        for ronda in range(rondas):
            print(f"\n===== RONDA {ronda + 1} =====")

            for carrera in carreras:
                if carrera.cupos <= 0:
                    continue

                postulantes = [
                    a for a in aspirantes
                    if a.estado == "PENDIENTE"
                    and ronda < len(a.opciones)
                    and a.opciones[ronda] == carrera.nombre
                    and a.puntaje >= carrera.puntaje_minimo
                ]

                if not postulantes:
                    continue

                # Comparación REALISTA
                postulantes.sort(
                    key=lambda a: a.puntaje_final(),
                    reverse=True
                )

                ganador = postulantes[0]

                carrera.cupos -= 1
                ganador.carrera = carrera.nombre
                ganador.estado = "ASIGNADO"
                historial.append(
                    (ganador.nombre, carrera.nombre, ronda + 1)
                )

                print(
                    f"{ganador.nombre} → {carrera.nombre} | "
                    f"Puntaje: {ganador.puntaje} | "
                    f"Bonificación: {ganador.bonificacion()} | "
                    f"FINAL: {ganador.puntaje_final()}"
                )


# ===============================
# SISTEMA (Singleton)
# ===============================
class Sistema:
    _instance = None

    def __init__(self):
        self.aspirantes = [
            # MISMO PUNTAJE, GANA QUIEN TIENE 2 SEGMENTOS
            Aspirante("01", "María", 850,
                      ["merito", "bachiller_actual"],
                      ["Veterinaria"]),

            Aspirante("02", "Luis", 850,
                      ["bachiller_actual"],
                      ["Veterinaria"]),

            # PUNTAJE MUY ALTO, GANA SIEMPRE
            Aspirante("03", "Ana", 950,
                      ["vulnerabilidad"],
                      ["Ingeniería"]),

            Aspirante("04", "Carlos", 820,
                      ["bachiller_actual"],
                      ["Ingeniería"]),
        ]

        self.carreras = [
            Carrera("Veterinaria", 1, 800),
            Carrera("Ingeniería", 1, 850),
        ]

        self.historial = []
        self.strategy = AsignacionSenescyt()

    @staticmethod
    def get_instance():
        if Sistema._instance is None:
            Sistema._instance = Sistema()
        return Sistema._instance

    def ejecutar(self):
        self.strategy.asignar(self.aspirantes, self.carreras, self.historial)
        print("\nPROCESO FINALIZADO")

    def mostrar_aspirantes(self):
        print("\n--- ASPIRANTES ---")
        for a in self.aspirantes:
            a.mostrar()

    def mostrar_carreras(self):
        print("\n--- CARRERAS ---")
        for c in self.carreras:
            c.mostrar()

    def mostrar_historial(self):
        print("\n--- HISTORIAL ---")
        for i, h in enumerate(self.historial):
            print(f"{i + 1}. {h[0]} → {h[1]} (opción {h[2]})")


# ===============================
# FACADE
# ===============================
class SistemaFacade:
    def __init__(self):
        self.sistema = Sistema.get_instance()

    def menu(self):
        while True:
            print("\n1. Ver Aspirantes")
            print("2. Ver Carreras")
            print("3. Ejecutar Asignación")
            print("4. Ver Historial")
            print("5. Salir")

            opcion = input("Opción: ")

            if opcion == "1":
                self.sistema.mostrar_aspirantes()
            elif opcion == "2":
                self.sistema.mostrar_carreras()
            elif opcion == "3":
                self.sistema.ejecutar()
            elif opcion == "4":
                self.sistema.mostrar_historial()
            elif opcion == "5":
                break


# ===============================
# MAIN
# ===============================
if __name__ == "__main__":
    SistemaFacade().menu()