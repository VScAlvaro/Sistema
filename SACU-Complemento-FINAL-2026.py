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