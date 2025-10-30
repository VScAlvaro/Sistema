# ------------------------------
# ENTIDAD: ASPIRANTE
# ------------------------------
class Aspirante:
    def _init_(self, cedula, nombre, edad):
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
    def _str_(self):
        return f"{self.nombre} ({self.cedula}) - Estado: {self.estado_cupo}"