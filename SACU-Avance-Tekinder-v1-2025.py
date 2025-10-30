import tkinter as tk
from tkinter import simpledialog, messagebox

# ==============================
# ENTIDAD: ASPIRANTE
# ==============================
class Aspirante:
    """
    Clase que representa a un aspirante universitario.
    Contiene información básica (cédula, nombre, edad),
    la carrera asignada, estado del cupo y categorías a las que pertenece.
    """
    def __init__(self, cedula, nombre, edad):
        self.cedula = cedula
        self.nombre = nombre
        self.edad = edad
        self.carrera_asignada = None
        self.estado_cupo = "PENDIENTE"  # Estados posibles: PENDIENTE, ASIGNADO, ACEPTADO, RECHAZADO

        # Campos booleanos para las distintas categorías
        self.cupo_aceptado_historico_pc = False
        self.cupo_historico_activo = False
        self.vulnerabilidad_socioeconomica = False
        self.merito_academico = False
        self.bachiller_pueblos_nacionalidad = False
        self.bachiller_periodo_academico = False
        self.poblacion_general = False

    def __str__(self):
        """
        Retorna una representación amigable del aspirante.
        """
        return f"{self.nombre} ({self.cedula}) - Estado: {self.estado_cupo}"


# ==============================
# CLASES DE CATEGORIAS
# ==============================
# Cada clase de categoría tiene un método 'asignar' que marca True el atributo correspondiente
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


# ==============================
# SISTEMA DE ASIGNACION DE CUPOS
# ==============================
class SistemaAsignacionGUI:
    """
    Clase principal que controla la interfaz gráfica y la lógica del sistema de asignación.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Asignación de Cupos")
        self.aspirantes = []  # Lista para almacenar todos los aspirantes registrados

        # Crear el frame principal para los botones
        self.frame = tk.Frame(root)
        self.frame.pack(pady=20)

        # Botones principales del sistema
        tk.Button(self.frame, text="Registrar Aspirante", width=30, command=self.registrar_aspirante).pack(pady=5)
        tk.Button(self.frame, text="Asignar Carrera y Categoria", width=30, command=self.asignar_cupo_categoria).pack(pady=5)
        tk.Button(self.frame, text="Aceptar Cupo", width=30, command=self.aceptar_cupo).pack(pady=5)
        tk.Button(self.frame, text="Rechazar Cupo", width=30, command=self.rechazar_cupo).pack(pady=5)
        tk.Button(self.frame, text="Mostrar Registros", width=30, command=self.mostrar_registros).pack(pady=5)
        tk.Button(self.frame, text="Salir", width=30, command=root.quit).pack(pady=5)

    # ------------------------------
    # FUNCIONES DEL SISTEMA
    # ------------------------------

    def registrar_aspirante(self):
        """
        Solicita al usuario los datos del aspirante mediante cuadros de diálogo.
        Crea un objeto Aspirante y lo añade a la lista de aspirantes.
        """
        cedula = simpledialog.askstring("Registrar", "Cédula:")
        nombre = simpledialog.askstring("Registrar", "Nombre:")
        try:
            edad = int(simpledialog.askstring("Registrar", "Edad:"))
        except:
            messagebox.showerror("Error", "Edad inválida")
            return

        # Crear y guardar el aspirante
        aspirante = Aspirante(cedula, nombre, edad)
        self.aspirantes.append(aspirante)
        messagebox.showinfo("Éxito", f"Aspirante {nombre} registrado correctamente.")

    def seleccionar_aspirante(self):
        """
        Muestra una lista de aspirantes registrados y solicita al usuario seleccionar uno.
        Retorna el aspirante seleccionado o None si la selección es inválida.
        """
        if not self.aspirantes:
            messagebox.showwarning("Aviso", "No hay aspirantes registrados")
            return None

        # Crear texto con las opciones disponibles
        opciones = "\n".join([f"{i+1}. {a.nombre} ({a.cedula}) - Estado: {a.estado_cupo}" for i, a in enumerate(self.aspirantes)])
        sel = simpledialog.askinteger("Seleccionar Aspirante", f"Seleccione un aspirante:\n{opciones}")
        if not sel or sel < 1 or sel > len(self.aspirantes):
            messagebox.showerror("Error", "Selección inválida")
            return None

        return self.aspirantes[sel-1]

    def asignar_cupo_categoria(self):
        """
        Asigna una carrera y una categoría a un aspirante seleccionado.
        Actualiza el estado del cupo a "ASIGNADO".
        """
        aspirante = self.seleccionar_aspirante()
        if not aspirante: return

        # Pedir carrera
        carrera = simpledialog.askstring("Asignar Carrera", "Ingrese nombre de la carrera:")
        if not carrera: return
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
        opciones_cat = "\n".join([f"{i+1}. {nombre}" for i, (nombre, _) in enumerate(categorias)])
        sel_cat = simpledialog.askinteger("Seleccionar Categoria", f"Seleccione una categoría:\n{opciones_cat}")
        if not sel_cat or sel_cat < 1 or sel_cat > len(categorias):
            messagebox.showerror("Error", "Categoría inválida")
            return

        # Asignar la categoría seleccionada
        categoria_obj = categorias[sel_cat-1][1]()
        categoria_obj.asignar(aspirante)
        messagebox.showinfo("Éxito", f"{aspirante.nombre} asignado a {carrera} en categoría {categorias[sel_cat-1][0]}")

    def aceptar_cupo(self):
        """
        Cambia el estado del cupo a "ACEPTADO" para el aspirante seleccionado.
        """
        aspirante = self.seleccionar_aspirante()
        if not aspirante: return
        if aspirante.estado_cupo == "ASIGNADO":
            aspirante.estado_cupo = "ACEPTADO"
            messagebox.showinfo("Éxito", f"{aspirante.nombre} ha aceptado su cupo en {aspirante.carrera_asignada}")
        else:
            messagebox.showwarning("Aviso", f"{aspirante.nombre} no tiene un cupo asignado")

    def rechazar_cupo(self):
        """
        Cambia el estado del cupo a "RECHAZADO" para el aspirante seleccionado y elimina la carrera asignada.
        """
        aspirante = self.seleccionar_aspirante()
        if not aspirante: return
        if aspirante.estado_cupo == "ASIGNADO":
            aspirante.estado_cupo = "RECHAZADO"
            aspirante.carrera_asignada = None
            messagebox.showinfo("Éxito", f"{aspirante.nombre} ha rechazado su cupo")
        else:
            messagebox.showwarning("Aviso", f"{aspirante.nombre} no tiene un cupo asignado")

    def mostrar_registros(self):
        """
        Muestra en una ventana nueva todos los aspirantes registrados,
        sus carreras asignadas, estado del cupo y categorías.
        """
        if not self.aspirantes:
            messagebox.showinfo("Registros", "No hay aspirantes registrados")
            return

        texto = ""
        for a in self.aspirantes:
            texto += f"\n{a}\n"
            texto += f"  Carrera asignada: {a.carrera_asignada}\n"
            texto += f"  Historico PC: {a.cupo_aceptado_historico_pc}\n"
            texto += f"  Historico Activo: {a.cupo_historico_activo}\n"
            texto += f"  Vulnerabilidad Socioeconomica: {a.vulnerabilidad_socioeconomica}\n"
            texto += f"  Merito Academico: {a.merito_academico}\n"
            texto += f"  Bachiller Pueblos/Nacionalidad: {a.bachiller_pueblos_nacionalidad}\n"
            texto += f"  Bachiller Periodo Academico: {a.bachiller_periodo_academico}\n"
            texto += f"  Poblacion General: {a.poblacion_general}\n"

        # Mostrar los registros en una ventana aparte
        ventana_registro = tk.Toplevel(self.root)
        ventana_registro.title("Registros de Aspirantes")
        txt = tk.Text(ventana_registro, width=70, height=25)
        txt.pack()
        txt.insert(tk.END, texto)
        txt.config(state=tk.DISABLED)


# ==============================
# EJECUCION DEL PROGRAMA
# ==============================
if __name__ == "__main__":
    root = tk.Tk()                  # Crear ventana principal
    app = SistemaAsignacionGUI(root) # Inicializar sistema con interfaz
    root.mainloop()                  # Ejecutar bucle principal de Tkinter
