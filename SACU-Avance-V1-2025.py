# ==============================
# Sistema de Asignación de Cupos Universitarios (Consola)
# ==============================

# ------------------------------
# ENTIDAD: ASPIRANTE
# ------------------------------
class Aspirante:
    def __init__(self, cedula, nombre, edad):
        self.cedula = cedula
        self.nombre = nombre
        self.edad = edad
        self.carrera_asignada = None
        self.estado_cupo = "PENDIENTE"  # PENDIENTE, ASIGNADO, ACEPTADO, RECHAZADO

        # Categorías
        self.cupo_aceptado_historico_pc = False
        self.cupo_historico_activo = False
        self.vulnerabilidad_socioeconomica = False
        self.merito_academico = False
        self.bachiller_pueblos_nacionalidad = False
        self.bachiller_periodo_academico = False
        self.poblacion_general = False

    # Método que define cómo se muestra el objeto como texto
    def __str__(self):
        return f"{self.nombre} ({self.cedula}) - Estado: {self.estado_cupo}"

# ------------------------------
# CLASES DE CATEGORIAS
# ------------------------------
class CupoAceptadoHistoricoPC:
    def asignar(self, aspirante):
        aspirante.cupo_aceptado_historico_pc = True

class CupoHistoricoActivo:
    def asignar(self, aspirante):
        aspirante.cupo_historico_activo = True

class VulnerabilidadSocioeconomica:
    def asignar(self, aspirante):
        aspirante.vulnerabilidad_socioeconomica = True

class MeritoAcademico:
    def asignar(self, aspirante):
        aspirante.merito_academico = True

class BachillerPueblosNacionalidad:
    def asignar(self, aspirante):
        aspirante.bachiller_pueblos_nacionalidad = True

class BachillerPeriodoAcademico:
    def asignar(self, aspirante):
        aspirante.bachiller_periodo_academico = True

class PoblacionGeneral:
    def asignar(self, aspirante):
        aspirante.poblacion_general = True

# ------------------------------
# SISTEMA DE ASIGNACION DE CUPOS
# ------------------------------
class SistemaAsignacion:
    def __init__(self):
        self.aspirantes = []

    # Registrar un nuevo aspirante
    def registrar_aspirante(self):
        print("\n--- Registrar Aspirante ---")
        cedula = input("Cédula: ")
        nombre = input("Nombre: ")
        try:
            edad = int(input("Edad: "))
        except ValueError:
            print("Edad inválida")
            return
        aspirante = Aspirante(cedula, nombre, edad)
        self.aspirantes.append(aspirante)
        print(f"[OK] Aspirante {nombre} registrado correctamente.")

    # Seleccionar un aspirante de la lista
    def seleccionar_aspirante(self):
        if not self.aspirantes:
            print("No hay aspirantes registrados")
            return None
        for i, a in enumerate(self.aspirantes):
            print(f"{i+1}. {a}")
        try:
            sel = int(input("Seleccione un aspirante: ")) - 1
            if sel < 0 or sel >= len(self.aspirantes):
                print("Selección inválida")
                return None
            return self.aspirantes[sel]
        except ValueError:
            print("Entrada inválida")
            return None

    # Asignar carrera y categoría a un aspirante
    def asignar_cupo_categoria(self):
        aspirante = self.seleccionar_aspirante()
        if not aspirante:
            return

        # Pedir carrera
        carrera = input("Ingrese el nombre de la carrera: ")
        if not carrera:
            print("Carrera inválida")
            return
        aspirante.carrera_asignada = carrera
        aspirante.estado_cupo = "ASIGNADO"

        # Pedir categoría
        categorias = [
            ("Cupo Aceptado Historico PC", CupoAceptadoHistoricoPC),
            ("Cupo Historico Activo", CupoHistoricoActivo),
            ("Vulnerabilidad Socioeconomica", VulnerabilidadSocioeconomica),
            ("Merito Academico", MeritoAcademico),
            ("Bachiller Pueblos/Nacionalidad", BachillerPueblosNacionalidad),
            ("Bachiller Periodo Academico", BachillerPeriodoAcademico),
            ("Poblacion General", PoblacionGeneral)
        ]
        for i, (nombre, _) in enumerate(categorias):
            print(f"{i+1}. {nombre}")
        try:
            sel_cat = int(input("Seleccione una categoría: ")) - 1
            if sel_cat < 0 or sel_cat >= len(categorias):
                print("Categoría inválida")
                return
            categoria_obj = categorias[sel_cat][1]()
            categoria_obj.asignar(aspirante)
            print(f"[OK] {aspirante.nombre} asignado a {carrera} en categoría {categorias[sel_cat][0]}")
        except ValueError:
            print("Entrada inválida")

    # Aceptar un cupo
    def aceptar_cupo(self):
        aspirante = self.seleccionar_aspirante()
        if not aspirante:
            return
        if aspirante.estado_cupo == "ASIGNADO":
            aspirante.estado_cupo = "ACEPTADO"
            print(f"{aspirante.nombre} ha aceptado su cupo en {aspirante.carrera_asignada}")
        else:
            print(f"{aspirante.nombre} no tiene un cupo asignado")

    # Rechazar un cupo
    def rechazar_cupo(self):
        aspirante = self.seleccionar_aspirante()
        if not aspirante:
            return
        if aspirante.estado_cupo == "ASIGNADO":
            aspirante.estado_cupo = "RECHAZADO"
            aspirante.carrera_asignada = None
            print(f"{aspirante.nombre} ha rechazado su cupo")
        else:
            print(f"{aspirante.nombre} no tiene un cupo asignado")

    # Mostrar todos los registros
    def mostrar_registros(self):
        if not self.aspirantes:
            print("No hay aspirantes registrados")
            return
        print("\n--- LISTA DE ASPIRANTES ---")
        for a in self.aspirantes:
            print(a)
            print(f"  Carrera asignada: {a.carrera_asignada}")
            print(f"  Historico PC: {a.cupo_aceptado_historico_pc}")
            print(f"  Historico Activo: {a.cupo_historico_activo}")
            print(f"  Vulnerabilidad Socioeconomica: {a.vulnerabilidad_socioeconomica}")
            print(f"  Merito Academico: {a.merito_academico}")
            print(f"  Bachiller Pueblos/Nacionalidad: {a.bachiller_pueblos_nacionalidad}")
            print(f"  Bachiller Periodo Academico: {a.bachiller_periodo_academico}")
            print(f"  Poblacion General: {a.poblacion_general}")
            print("------------------------------")

    # Menú principal
    def menu(self):
        while True:
            print("\n=== SISTEMA DE ASIGNACIÓN DE CUPOS ===")
            print("1. Registrar Aspirante")
            print("2. Asignar Carrera y Categoría")
            print("3. Aceptar Cupo")
            print("4. Rechazar Cupo")
            print("5. Mostrar Registros")
            print("6. Salir")
            opcion = input("Seleccione una opción: ")
            if opcion == "1":
                self.registrar_aspirante()
            elif opcion == "2":
                self.asignar_cupo_categoria()
            elif opcion == "3":
                self.aceptar_cupo()
            elif opcion == "4":
                self.rechazar_cupo()
            elif opcion == "5":
                self.mostrar_registros()
            elif opcion == "6":
                print("Saliendo del sistema... ")
                break
            else:
                print("Opción inválida")

# ------------------------------
# EJECUCIÓN
# ------------------------------
if __name__ == "__main__":
    sistema = SistemaAsignacion()
    sistema.menu()