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