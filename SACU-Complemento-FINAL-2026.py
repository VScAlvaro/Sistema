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
