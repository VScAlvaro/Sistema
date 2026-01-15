import * as XLSX from "xlsx";
import * as readline from "readline-sync";

/* ===============================
   USUARIOS DEL SISTEMA
================================ */
const USUARIOS: Record<string, string> = {
  admin: "1234",
  encargado: "senescyt",
};

/* ===============================
   BONIFICACIONES
================================ */
const SEGMENTOS: Record<string, number> = {
  vulnerabilidad: 15,
  merito: 20,
  pueblos: 10,
  bachiller_actual: 30,
  procesos_anteriores: 20,
  excluidos: 10,
};

const BONIFICACION_MAX = 50;

/* ===============================
   PRIORIDAD DE SEGMENTOS
================================ */
const PRIORIDAD_SEGMENTOS: Record<string, number> = {
  pueblos: 4,
  vulnerabilidad: 3,
  bachiller_actual: 2,
  merito: 1,
  procesos_anteriores: 0,
  excluidos: 0,
};

/* ===============================
   LOGIN
================================ */
class UsuarioSistema {
  iniciarSesion(): boolean {
    console.log("===== INICIO DE SESIÓN =====");

    for (let i = 0; i < 3; i++) {
      const usuario = readline.question("Usuario: ");
      const clave = readline.question("Contraseña: ", {
        hideEchoBack: true,
      });

      if (USUARIOS[usuario] === clave) {
        console.log("✅ Acceso concedido\n");
        return true;
      }
      console.log("❌ Credenciales incorrectas");
    }

    console.log("🚫 Acceso bloqueado");
    return false;
  }
}

/* ===============================
   ASPIRANTE
================================ */
class Aspirante {
  carrera: string | null = null;
  estado = "PENDIENTE";

  constructor(
    public cedula: string,
    public nombre: string,
    public puntaje: number,
    public segmentos: string[],
    public opciones: string[]
  ) {}

  bonificacion(): number {
    const total = this.segmentos.reduce(
      (s, seg) => s + (SEGMENTOS[seg] ?? 0),
      0
    );
    return Math.min(total, BONIFICACION_MAX);
  }

  puntajeFinal(): number {
    return this.puntaje + this.bonificacion();
  }

  prioridadSegmento(): number {
    return Math.max(
      ...this.segmentos.map((s) => PRIORIDAD_SEGMENTOS[s] ?? 0),
      0
    );
  }

  mostrar() {
    console.log(
      `${this.nombre} | Base: ${this.puntaje} | Bonif: ${this.bonificacion()} | Final: ${this.puntajeFinal()} | Asignado: ${this.carrera ?? "-"} | Estado: ${this.estado}`
    );
  }
}

/* ===============================
   CARRERA
================================ */
class Carrera {
  constructor(
    public nombre: string,
    public cupos: number,
    public puntajeMinimo: number
  ) {}

  mostrar() {
    console.log(
      `${this.nombre} | Cupos: ${this.cupos} | Puntaje mínimo: ${this.puntajeMinimo}`
    );
  }
}

/* ===============================
   CARGA EXCEL
================================ */
function cargarAspirantesExcel(ruta: string): Aspirante[] {
  const wb = XLSX.readFile(ruta);
  const hoja = wb.Sheets[wb.SheetNames[0]];
  const datos: any[] = XLSX.utils.sheet_to_json(hoja);

  return datos.map((row) => {
    const segmentos: string[] = [];

    if (row["Vulnerabilidad Socioeconómica"] === "SI")
      segmentos.push("vulnerabilidad");
    if (row["Mérito Académico"] === "SI") segmentos.push("merito");
    if (row["Bachiller de Pueblos y Nacionalidades"] === "SI")
      segmentos.push("pueblos");
    if (row["Bachiller Último Año"] === "SI")
      segmentos.push("bachiller_actual");

    return new Aspirante(
      String(row["Identificación"]),
      `${row["Nombres"]} ${row["Apellidos"]}`,
      Number(row["Nota de Postulación"]),
      segmentos,
      [row["Carrera"]]
    );
  });
}

/* ===============================
   ASIGNACIÓN
================================ */
class AsignacionSenescyt {
  asignar(aspirantes: Aspirante[], carreras: Carrera[], historial: any[]) {
    const rondas = Math.max(...aspirantes.map((a) => a.opciones.length));

    for (let r = 0; r < rondas; r++) {
      console.log(`\n===== RONDA ${r + 1} =====`);

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

          console.log(`${a.nombre} → ${carrera.nombre}`);
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
