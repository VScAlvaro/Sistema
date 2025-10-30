#------------------------------
#SISTEMA DE ASIGNACION DE CUPOS
#------------------------------
class SistemaAsignacion:
    def init(self):
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