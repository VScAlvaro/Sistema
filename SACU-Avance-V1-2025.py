# ==============================
# Sistema de Asignación de Cupos Universitarios
# Con inicio de sesión para estudiantes
# ==============================

class Aspirante:
    def __init__(self, cedula, nombre, edad, carrera, usuario, contrasena):
        self.cedula = cedula
        self.nombre = nombre
        self.edad = edad
        self.carrera_asignada = carrera
        self.usuario = usuario
        self.contrasena = contrasena
        self.estado_cupo = "ASIGNADO"

        # Categorías
        self.cupo_aceptado_historico_pc = False
        self.cupo_historico_activo = False
        self.vulnerabilidad_socioeconomica = False
        self.merito_academico = False
        self.bachiller_pueblos_nacionalidad = False
        self.bachiller_periodo_academico = False
        self.poblacion_general = False

    def __str__(self):
        return f"{self.nombre} ({self.cedula}) - {self.carrera_asignada} - Estado: {self.estado_cupo}"


# ------------------------------
# CLASES DE CATEGORÍAS
# ------------------------------
class MeritoAcademico:
    def asignar(self, aspirante):
        aspirante.merito_academico = True

class VulnerabilidadSocioeconomica:
    def asignar(self, aspirante):
        aspirante.vulnerabilidad_socioeconomica = True

class PoblacionGeneral:
    def asignar(self, aspirante):
        aspirante.poblacion_general = True


# ------------------------------
# SISTEMA DE ASIGNACIÓN
# ------------------------------
class SistemaAsignacion:
    def __init__(self):
        # Aspirantes predefinidos con usuario y contraseña
        self.aspirantes = [
            Aspirante("0102030405", "Ana Torres", 18, "Ingeniería Ambiental", "ana18", "1234"),
            Aspirante("0607080910", "Carlos Mejía", 20, "Medicina", "carlos20", "abcd"),
            Aspirante("1101121314", "Sofía Loor", 19, "Arquitectura", "sofia19", "pass")
        ]

        # Asignar categorías
        MeritoAcademico().asignar(self.aspirantes[0])
        VulnerabilidadSocioeconomica().asignar(self.aspirantes[1])
        PoblacionGeneral().asignar(self.aspirantes[2])

        self.usuario_actual = None  # Para saber quién inició sesión

    # --------------------------
    # INICIO DE SESIÓN
    # --------------------------
    def login(self):
        print("=== INICIO DE SESIÓN ===")
        usuario = input("Usuario: ")
        contrasena = input("Contraseña: ")

        for aspirante in self.aspirantes:
            if aspirante.usuario == usuario and aspirante.contrasena == contrasena:
                self.usuario_actual = aspirante
                print(f"\nBienvenido/a, {aspirante.nombre} ✅")
                return True
        print("\n❌ Usuario o contraseña incorrectos.")
        return False

    # --------------------------
    # OPCIONES DE ESTUDIANTE
    # --------------------------
    def aceptar_cupo(self):
        a = self.usuario_actual
        if a.estado_cupo == "ASIGNADO":
            a.estado_cupo = "ACEPTADO"
            print(f"[✔] {a.nombre} ha aceptado su cupo en {a.carrera_asignada}.")
        else:
            print(f"[!] Ya respondió o no tiene cupo asignado.")

    def rechazar_cupo(self):
        a = self.usuario_actual
        if a.estado_cupo == "ASIGNADO":
            a.estado_cupo = "RECHAZADO"
            print(f"[✖] {a.nombre} ha rechazado su cupo.")
        else:
            print(f"[!] Ya respondió o no tiene cupo asignado.")

    def mostrar_info(self):
        a = self.usuario_actual
        print("\n--- INFORMACIÓN PERSONAL ---")
        print(f"Nombre: {a.nombre}")
        print(f"Cédula: {a.cedula}")
        print(f"Edad: {a.edad}")
        print(f"Carrera: {a.carrera_asignada}")
        print(f"Estado del cupo: {a.estado_cupo}")
        print("Categorías:")
        print(f"  Mérito Académico: {a.merito_academico}")
        print(f"  Vulnerabilidad Socioeconómica: {a.vulnerabilidad_socioeconomica}")
        print(f"  Población General: {a.poblacion_general}")

    # --------------------------
    # MENÚ PRINCIPAL
    # --------------------------
    def menu_estudiante(self):
        while True:
            print("\n=== MENÚ DEL ESTUDIANTE ===")
            print("1. Aceptar cupo")
            print("2. Rechazar cupo")
            print("3. Ver información")
            print("4. Cerrar sesión")
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                self.aceptar_cupo()
            elif opcion == "2":
                self.rechazar_cupo()
            elif opcion == "3":
                self.mostrar_info()
            elif opcion == "4":
                print("Cerrando sesión...")
                self.usuario_actual = None
                break
            else:
                print("Opción inválida. Intente nuevamente.")

    # --------------------------
    # INICIO DEL SISTEMA
    # --------------------------
    def ejecutar(self):
        while True:
            print("\n=== SISTEMA DE CUPOS UNIVERSITARIOS ===")
            print("1. Iniciar sesión")
            print("2. Salir")
            op = input("Seleccione una opción: ")

            if op == "1":
                if self.login():
                    self.menu_estudiante()
            elif op == "2":
                print("Saliendo del sistema...")
                break
            else:
                print("Opción inválida.")


# ------------------------------
# EJECUCIÓN PRINCIPAL
# ------------------------------
if __name__ == "__main__":
    sistema = SistemaAsignacion()
    sistema.ejecutar()
1