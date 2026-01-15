/* ===============================
   ASIGNACIÓN
================================ */
class AsignacionSenescyt {
  asignar(aspirantes: Aspirante[], carreras: Carrera[], historial: any[]) {
    const rondas = Math.max(...aspirantes.map((a) => a.opciones.length));

    for (let r = 0; r < rondas; r++) {
      console.log(\n===== RONDA ${r + 1} =====);

      for (const carrera of carreras) {
        if (carrera.cupos <= 0) continue;

        const postulantes = aspirantes
          .filter(
            (a) =>
              a.estado === "PENDIENTE" &&
              a.opciones[r] === carrera.nombre &&
              a.puntajeFinal() >= carrera.puntajeMinimo
          )
          .sort(
            (a, b) =>
              b.puntajeFinal() - a.puntajeFinal() ||
              b.puntaje - a.puntaje ||
              b.bonificacion() - a.bonificacion() ||
              b.prioridadSegmento() - a.prioridadSegmento()
          );

        for (const a of postulantes) {
          if (carrera.cupos <= 0) break;

          carrera.cupos--;
          a.carrera = carrera.nombre;
          a.estado = "ASIGNADO";
          historial.push([a.nombre, carrera.nombre, r + 1]);

          console.log(${a.nombre} → ${carrera.nombre});
        }
      }
    }
  }
}

/* ===============================
   SISTEMA (Singleton)
================================ */
class Sistema {
  private static instance: Sistema;

  aspirantes: Aspirante[];
  carreras: Carrera[];
  historial: any[] = [];
  strategy = new AsignacionSenescyt();

  private constructor() {
    this.aspirantes = cargarAspirantesExcel("cupos.xlsx");
    this.carreras = [
      new Carrera("Veterinaria", 30, 750),
      new Carrera("Biología", 40, 711),
      new Carrera("Enfermería", 25, 772),
      new Carrera("Administración de Empresas", 20, 728),
      new Carrera("Agropecuaria", 20, 600),
    ];
  }

  static getInstance(): Sistema {
    if (!Sistema.instance) Sistema.instance = new Sistema();
    return Sistema.instance;
  }

  ejecutar() {
    this.strategy.asignar(this.aspirantes, this.carreras, this.historial);
  }
}

/* ===============================
   FACADE
================================ */
class SistemaFacade {
  usuario = new UsuarioSistema();
  sistema = Sistema.getInstance();

  menu() {
    if (!this.usuario.iniciarSesion()) return;

    while (true) {
      console.log("\n1. Ver Aspirantes");
      console.log("2. Ver Carreras");
      console.log("3. Ejecutar Asignación");
      console.log("4. Ver Historial");
      console.log("5. Salir");

      const op = readline.question("Opción: ");

      if (op === "1") this.sistema.aspirantes.forEach((a) => a.mostrar());
      else if (op === "2") this.sistema.carreras.forEach((c) => c.mostrar());
      else if (op === "3") this.sistema.ejecutar();
      else if (op === "4") console.log(this.sistema.historial);
      else if (op === "5") break;
    }
  }
}

/* ===============================
   MAIN
================================ */
new SistemaFacade().menu();