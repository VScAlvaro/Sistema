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
