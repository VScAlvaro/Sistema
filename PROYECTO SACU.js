"use strict";
var __spreadArray = (this && this.__spreadArray) || function (to, from, pack) {
    if (pack || arguments.length === 2) for (var i = 0, l = from.length, ar; i < l; i++) {
        if (ar || !(i in from)) {
            if (!ar) ar = Array.prototype.slice.call(from, 0, i);
            ar[i] = from[i];
        }
    }
    return to.concat(ar || Array.prototype.slice.call(from));
};
Object.defineProperty(exports, "__esModule", { value: true });
var XLSX = require("xlsx");
var readline = require("readline-sync");
/* ===============================
   USUARIOS DEL SISTEMA
================================ */
var USUARIOS = {
    admin: "1234",
    encargado: "senescyt",
};
/* ===============================
   BONIFICACIONES
================================ */
var SEGMENTOS = {
    vulnerabilidad: 15,
    merito: 20,
    pueblos: 10,
    bachiller_actual: 30,
    procesos_anteriores: 20,
    excluidos: 10,
};
var BONIFICACION_MAX = 50;
/* ===============================
   PRIORIDAD DE SEGMENTOS
================================ */
var PRIORIDAD_SEGMENTOS = {
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
var UsuarioSistema = /** @class */ (function () {
    function UsuarioSistema() {
    }
    UsuarioSistema.prototype.iniciarSesion = function () {
        console.log("===== INICIO DE SESIÓN =====");
        for (var i = 0; i < 3; i++) {
            var usuario = readline.question("Usuario: ");
            var clave = readline.question("Contraseña: ", {
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
    };
    return UsuarioSistema;
}());
/* ===============================
   ASPIRANTE
================================ */
var Aspirante = /** @class */ (function () {
    function Aspirante(cedula, nombre, puntaje, segmentos, opciones) {
        this.cedula = cedula;
        this.nombre = nombre;
        this.puntaje = puntaje;
        this.segmentos = segmentos;
        this.opciones = opciones;
        this.carrera = null;
        this.estado = "PENDIENTE";
    }
    Aspirante.prototype.bonificacion = function () {
        var total = this.segmentos.reduce(function (s, seg) { var _a; return s + ((_a = SEGMENTOS[seg]) !== null && _a !== void 0 ? _a : 0); }, 0);
        return Math.min(total, BONIFICACION_MAX);
    };
    Aspirante.prototype.puntajeFinal = function () {
        return this.puntaje + this.bonificacion();
    };
    Aspirante.prototype.prioridadSegmento = function () {
        return Math.max.apply(Math, __spreadArray(__spreadArray([], this.segmentos.map(function (s) { var _a; return (_a = PRIORIDAD_SEGMENTOS[s]) !== null && _a !== void 0 ? _a : 0; }), false), [0], false));
    };
    Aspirante.prototype.mostrar = function () {
        var _a;
        console.log("".concat(this.nombre, " | Base: ").concat(this.puntaje, " | Bonif: ").concat(this.bonificacion(), " | Final: ").concat(this.puntajeFinal(), " | Asignado: ").concat((_a = this.carrera) !== null && _a !== void 0 ? _a : "-", " | Estado: ").concat(this.estado));
    };
    return Aspirante;
}());
/* ===============================
   CARRERA
================================ */
var Carrera = /** @class */ (function () {
    function Carrera(nombre, cupos, puntajeMinimo) {
        this.nombre = nombre;
        this.cupos = cupos;
        this.puntajeMinimo = puntajeMinimo;
    }
    Carrera.prototype.mostrar = function () {
        console.log("".concat(this.nombre, " | Cupos: ").concat(this.cupos, " | Puntaje m\u00EDnimo: ").concat(this.puntajeMinimo));
    };
    return Carrera;
}());
/* ===============================
   CARGA EXCEL
================================ */
function cargarAspirantesExcel(ruta) {
    var wb = XLSX.readFile(ruta);
    var hoja = wb.Sheets[wb.SheetNames[0]];
    var datos = XLSX.utils.sheet_to_json(hoja);
    return datos.map(function (row) {
        var segmentos = [];
        if (row["Vulnerabilidad Socioeconómica"] === "SI")
            segmentos.push("vulnerabilidad");
        if (row["Mérito Académico"] === "SI")
            segmentos.push("merito");
        if (row["Bachiller de Pueblos y Nacionalidades"] === "SI")
            segmentos.push("pueblos");
        if (row["Bachiller Último Año"] === "SI")
            segmentos.push("bachiller_actual");
        return new Aspirante(String(row["Identificación"]), "".concat(row["Nombres"], " ").concat(row["Apellidos"]), Number(row["Nota de Postulación"]), segmentos, [row["Carrera"]]);
    });
}
/* ===============================
   ASIGNACIÓN
================================ */
var AsignacionSenescyt = /** @class */ (function () {
    function AsignacionSenescyt() {
    }
    AsignacionSenescyt.prototype.asignar = function (aspirantes, carreras, historial) {
        var rondas = Math.max.apply(Math, aspirantes.map(function (a) { return a.opciones.length; }));
        var _loop_1 = function (r) {
            console.log("\n===== RONDA ".concat(r + 1, " ====="));
            var _loop_2 = function (carrera) {
                if (carrera.cupos <= 0)
                    return "continue";
                var postulantes = aspirantes
                    .filter(function (a) {
                    return a.estado === "PENDIENTE" &&
                        a.opciones[r] === carrera.nombre &&
                        a.puntajeFinal() >= carrera.puntajeMinimo;
                })
                    .sort(function (a, b) {
                    return b.puntajeFinal() - a.puntajeFinal() ||
                        b.puntaje - a.puntaje ||
                        b.bonificacion() - a.bonificacion() ||
                        b.prioridadSegmento() - a.prioridadSegmento();
                });
                for (var _a = 0, postulantes_1 = postulantes; _a < postulantes_1.length; _a++) {
                    var a = postulantes_1[_a];
                    if (carrera.cupos <= 0)
                        break;
                    carrera.cupos--;
                    a.carrera = carrera.nombre;
                    a.estado = "ASIGNADO";
                    historial.push([a.nombre, carrera.nombre, r + 1]);
                    console.log("".concat(a.nombre, " \u2192 ").concat(carrera.nombre));
                }
            };
            for (var _i = 0, carreras_1 = carreras; _i < carreras_1.length; _i++) {
                var carrera = carreras_1[_i];
                _loop_2(carrera);
            }
        };
        for (var r = 0; r < rondas; r++) {
            _loop_1(r);
        }
    };
    return AsignacionSenescyt;
}());
/* ===============================
   SISTEMA (Singleton)
================================ */
var Sistema = /** @class */ (function () {
    function Sistema() {
        this.historial = [];
        this.strategy = new AsignacionSenescyt();
        this.aspirantes = cargarAspirantesExcel("cupos.xlsx");
        this.carreras = [
            new Carrera("Veterinaria", 30, 750),
            new Carrera("Biología", 40, 711),
            new Carrera("Enfermería", 25, 772),
            new Carrera("Administración de Empresas", 20, 728),
            new Carrera("Agropecuaria", 20, 600),
        ];
    }
    Sistema.getInstance = function () {
        if (!Sistema.instance)
            Sistema.instance = new Sistema();
        return Sistema.instance;
    };
    Sistema.prototype.ejecutar = function () {
        this.strategy.asignar(this.aspirantes, this.carreras, this.historial);
    };
    return Sistema;
}());
/* ===============================
   FACADE
================================ */
var SistemaFacade = /** @class */ (function () {
    function SistemaFacade() {
        this.usuario = new UsuarioSistema();
        this.sistema = Sistema.getInstance();
    }
    SistemaFacade.prototype.menu = function () {
        if (!this.usuario.iniciarSesion())
            return;
        while (true) {
            console.log("\n1. Ver Aspirantes");
            console.log("2. Ver Carreras");
            console.log("3. Ejecutar Asignación");
            console.log("4. Ver Historial");
            console.log("5. Salir");
            var op = readline.question("Opción: ");
            if (op === "1")
                this.sistema.aspirantes.forEach(function (a) { return a.mostrar(); });
            else if (op === "2")
                this.sistema.carreras.forEach(function (c) { return c.mostrar(); });
            else if (op === "3")
                this.sistema.ejecutar();
            else if (op === "4")
                console.log(this.sistema.historial);
            else if (op === "5")
                break;
        }
    };
    return SistemaFacade;
}());
/* ===============================
   MAIN
================================ */
new SistemaFacade().menu();
