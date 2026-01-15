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
        console.log(" Acceso concedido\n");
        return true;
      }
      console.log("Credenciales incorrectas");
    }

    console.log(" Acceso bloqueado");
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