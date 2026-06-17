from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, session
from zoneinfo import ZoneInfo

app = Flask(__name__)



app.secret_key = "TransporteTlalpujahua2026"

USUARIO = "conductor"
PASSWORD = "RutaTlalpujahua2026!"

from google.oauth2.service_account import Credentials
import gspread

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

credenciales = Credentials.from_service_account_file(
    "transportelocaltlalpujahua-0c0bdb0c6d76.json",
    scopes=SCOPES
)

cliente = gspread.authorize(credenciales)

sheet = cliente.open("Transporte Local")

def calcular_minutos_restantes(hora_str):

    try:
        ahora = datetime.now(ZoneInfo("America/Mexico_City"))

        hora_obj = datetime.strptime(hora_str, "%H:%M").time()

        proxima = datetime.combine(ahora.date(), hora_obj)

        # si ya pasó hoy, lo mandamos al día siguiente
        if proxima < ahora:
            proxima += timedelta(days=1)

        minutos = int((proxima - ahora).total_seconds() / 60)

        return minutos

    except:
        return None
    
def cargar_rutas():

    hoja_rutas = sheet.worksheet("Rutas")

    return hoja_rutas.get_all_records()


def cargar_horarios():

    hoja_horarios = sheet.worksheet("Horarios")

    return hoja_horarios.get_all_records()

def buscar_fila_ruta(ruta_id):

    hoja_rutas = sheet.worksheet("Rutas")

    registros = hoja_rutas.get_all_records()

    for i, fila in enumerate(registros, start=2):

        if int(fila["id"]) == ruta_id:
            return hoja_rutas, i

    return None, None

from datetime import time

def convertir_hora(hora):

    try:

        hora_str = str(hora)

        hora_obj = datetime.strptime(
            hora_str,
            "%H:%M"
        )

        return hora_obj.strftime("%I:%M %p")

    except:

        return str(hora)
    
rutas = [

    {
        "id": 1,
        "nombre": "Estanzuela",
        "estado": "Activa",
        "tarifa": "$20",

        "horarios_lv": [
            "07:10 - 08:00",
            "08:30 - 09:00",
            "10:30 - 11:00",
            "12:00 - 13:00",
            "14:30 - 15:00",
            "15:30 - 16:00",
            "17:30 - 18:00"
        ],

        "horarios_sabado": [
            "08:30 - 09:00",
            "10:30 - 11:00",
            "12:30 - 13:00",
            "14:30 - 15:00",
            "15:30 - 16:00",
            "17:30 - 18:00"
        ],

        "horarios_domingo": [
            "08:30 - 09:00",
            "10:30 - 11:00",
            "12:30 - 13:00",
            "13:30 - 14:00",
            "14:30 - 15:00",
            "15:30 - 16:00",
            "16:30 - 17:00"
        ],

        "horarios": [],
        "observacion": "Sale normalmente",
        "actualizacion": "Sin actualizaciones"
    },

    {
        "id": 2,
        "nombre": "San José",
        "estado": "Inactiva",
        "tarifa": "$25",

        "horarios_lv": [
            "Pendiente de información"
        ],

        "horarios_sabado": [
            "Pendiente de información"
        ],

        "horarios_domingo": [
            "Pendiente de información"
        ],

        "horarios": [],
        "observacion": "Pendiente de información",
        "actualizacion": "Sin actualizaciones"
    },

    {
        "id": 3,
        "nombre": "El Gigante",
        "estado": "Inactiva",
        "tarifa": "Pendiente",

        "horarios_lv": [
            "Pendiente de información"
        ],

        "horarios_sabado": [
            "Pendiente de información"
        ],

        "horarios_domingo": [
            "Pendiente de información"
        ],

        "horarios": [],
        "observacion": "Pendiente de información",
        "actualizacion": "Sin actualizaciones"
    },

    {
        "id": 4,
        "nombre": "San Rafael",
        "estado": "Inactiva",
        "tarifa": "Pendiente",

        "horarios_lv": [
            "Pendiente de información"
        ],

        "horarios_sabado": [
            "Pendiente de información"
        ],

        "horarios_domingo": [
            "Pendiente de información"
        ],

        "horarios": [],
        "observacion": "Pendiente de información",
        "actualizacion": "Sin actualizaciones"
    },

    {
        "id": 5,
        "nombre": "San Pedro",
        "estado": "Inactiva",
        "tarifa": "Pendiente",

        "horarios_lv": [
            "Pendiente de información"
        ],

        "horarios_sabado": [
            "Pendiente de información"
        ],

        "horarios_domingo": [
            "Pendiente de información"
        ],

        "horarios": [],
        "observacion": "Pendiente de información",
        "actualizacion": "Sin actualizaciones"
    },

    {
        "id": 6,
        "nombre": "El Puerto",
        "estado": "Inactiva",
        "tarifa": "Pendiente",

        "horarios_lv": [
            "Pendiente de información"
        ],

        "horarios_sabado": [
            "Pendiente de información"
        ],

        "horarios_domingo": [
            "Pendiente de información"
        ],

        "horarios": [],
        "observacion": "Pendiente de información",
        "actualizacion": "Sin actualizaciones"
    },

    {
        "id": 7,
        "nombre": "Remedios",
        "estado": "Inactiva",
        "tarifa": "Pendiente",

        "horarios_lv": [
            "Pendiente de información"
        ],

        "horarios_sabado": [
            "Pendiente de información"
        ],

        "horarios_domingo": [
            "Pendiente de información"
        ],

        "horarios": [],
        "observacion": "Pendiente de información",
        "actualizacion": "Sin actualizaciones"
    }

]


def obtener_datos_generales():

    ahora = datetime.now(ZoneInfo("America/Mexico_City"))

    fecha_actual = ahora.strftime("%d/%m/%Y")
    hora_actual = ahora.strftime("%I:%M %p")

    dia_semana = ahora.weekday()

    if dia_semana <= 4:
        tipo_horario = "Lunes a Viernes"

    elif dia_semana == 5:
        tipo_horario = "Sábado"

    else:
        tipo_horario = "Domingo"

    for ruta in rutas:

        if dia_semana <= 4:
            ruta["horarios"] = ruta["horarios_lv"]

        elif dia_semana == 5:
            ruta["horarios"] = ruta["horarios_sabado"]

        else:
            ruta["horarios"] = ruta["horarios_domingo"]

        ruta["tipo_horario"] = tipo_horario

    return fecha_actual, hora_actual

def obtener_horarios_por_ruta():

    horarios = cargar_horarios()

    ahora = datetime.now(
        ZoneInfo("America/Mexico_City")
    )

    dia = ahora.weekday()

    if dia <= 4:
        tipo_actual = "LV"

    elif dia == 5:
        tipo_actual = "SAB"

    else:
        tipo_actual = "DOM"

    resultado = {}

    for fila in horarios:

        if fila["tipo_dia"] != tipo_actual:
            continue

        ruta_id = int(fila["ruta_id"])

        if ruta_id not in resultado:
            resultado[ruta_id] = []

        resultado[ruta_id].append(
            convertir_hora(
                str(fila["hora"])
            )
        )

    return resultado

def obtener_proximas_salidas():

    horarios = cargar_horarios()

    ahora = datetime.now(
        ZoneInfo("America/Mexico_City")
    )

    dia = ahora.weekday()

    if dia <= 4:
        tipo_actual = "LV"

    elif dia == 5:
        tipo_actual = "SAB"

    else:
        tipo_actual = "DOM"

    resultado = {}

    for fila in horarios:

        if fila["tipo_dia"] != tipo_actual:
            continue

        try:

            ruta_id = int(fila["ruta_id"])

            hora_str = str(fila["hora"])

            hora_horario = datetime.strptime(
                hora_str,
                "%H:%M"
            ).time()

            if hora_horario > ahora.time():

                if ruta_id not in resultado:

                    resultado[ruta_id] = convertir_hora(
                        hora_str
                    )

        except:

            continue

    return resultado



@app.route("/")
def inicio():
    proxima_global = None
    minutos_global = None
    fecha_actual, hora_actual = obtener_datos_generales()

    rutas_sheets = cargar_rutas()

    horarios_por_ruta = obtener_horarios_por_ruta()
    proximas_salidas = obtener_proximas_salidas()

    ahora = datetime.now(ZoneInfo("America/Mexico_City"))

    dia = ahora.weekday()

    if dia <= 4:
        tipo_horario = "Lunes a Viernes"
    elif dia == 5:
        tipo_horario = "Sábado"
    else:
        tipo_horario = "Domingo"

    # =========================
    # TARJETA GLOBAL
    # =========================
    proxima_global = obtener_proxima_salida_global()

    if proxima_global:
        minutos_global = calcular_minutos_restantes(proxima_global["hora_str"])
    else:
        minutos_global = None

    # =========================
    # RUTAS NORMALES
    # =========================
    for ruta in rutas_sheets:

        ruta_id = int(ruta["id"])

        ruta["horarios"] = horarios_por_ruta.get(
            ruta_id,
            ["Pendiente de información"]
        )

        ruta["tipo_horario"] = tipo_horario

        proxima = proximas_salidas.get(ruta_id)

        ruta["proxima_salida"] = proxima if proxima else "Sin próximas salidas"

    proxima_global = obtener_proxima_salida_global()

    if proxima_global:
        minutos_global = calcular_minutos_restantes(proxima_global["hora_str"])
    else:
        minutos_global = None

    return render_template(
        "index.html",
        rutas=rutas_sheets,
        fecha_actual=fecha_actual,
        hora_actual=hora_actual,
        proxima_global=proxima_global,
        minutos_global=minutos_global
    )


@app.route("/login", methods=["GET", "POST"])
def login():

    error = None

    if request.method == "POST":

        usuario = request.form["usuario"]
        password = request.form["password"]

        if usuario == USUARIO and password == PASSWORD:

            session["logueado"] = True

            return redirect(url_for("admin"))

        else:

            error = "Usuario o contraseña incorrectos"

    return render_template(
        "login.html",
        error=error
    )


@app.route("/cambiar_estado/<int:ruta_id>/<nuevo_estado>")
def cambiar_estado(ruta_id, nuevo_estado):

    if not session.get("logueado"):
        return redirect(url_for("login"))

    hoja_rutas, fila = buscar_fila_ruta(ruta_id)

    if fila:

        hoja_rutas.update_cell(fila, 3, nuevo_estado)

        hoja_rutas.update_cell(
            fila,
            6,
            datetime.now(
                ZoneInfo("America/Mexico_City")
            ).strftime("%d/%m/%Y %I:%M %p")
        )

    return redirect(url_for("admin"))

@app.route("/actualizar_observacion/<int:ruta_id>", methods=["POST"])
def actualizar_observacion(ruta_id):

    if not session.get("logueado"):
        return redirect(url_for("login"))

    nueva_observacion = request.form.get(
        "observacion",
        ""
    ).strip()

    hoja_rutas, fila = buscar_fila_ruta(ruta_id)

    if fila:

        hoja_rutas.update_cell(
            fila,
            5,
            nueva_observacion
        )

        hoja_rutas.update_cell(
            fila,
            6,
            datetime.now(
                ZoneInfo("America/Mexico_City")
            ).strftime("%d/%m/%Y %I:%M %p")
        )

    return redirect(url_for("admin"))

@app.route("/admin")
def admin():

    if not session.get("logueado"):
        return redirect(url_for("login"))

    fecha_actual, hora_actual = obtener_datos_generales()

    rutas_sheets = cargar_rutas()

    return render_template(
        "admin.html",
        rutas=rutas_sheets,
        fecha_actual=fecha_actual,
        hora_actual=hora_actual
    )


def obtener_proxima_salida_global():
    horarios = cargar_horarios()
    ahora = datetime.now(ZoneInfo("America/Mexico_City"))
    dia = ahora.weekday()

    if dia <= 4:
        tipo_actual = "LV"
    elif dia == 5:
        tipo_actual = "SAB"
    else:
        tipo_actual = "DOM"

    mejor = None

    for fila in horarios:
        if fila["tipo_dia"] != tipo_actual:
            continue

        try:
            ruta_id = int(fila["ruta_id"])
            hora_str = str(fila["hora"])

            hora_obj = datetime.strptime(hora_str, "%H:%M").time()
            hora_dt = datetime.combine(ahora.date(), hora_obj)

            # SOLUCIÓN: Si ya pasó hoy, lo mandamos a mañana para evaluarlo
            if hora_dt <= ahora:
                hora_dt += timedelta(days=1)

            if mejor is None or hora_dt < mejor["hora_dt"]:
                mejor = {
                    "ruta_id": ruta_id,
                    "hora": hora_dt,
                    "hora_str": hora_str,
                    "hora_dt": hora_dt
                }

        except:
            continue

    return mejor

if __name__ == "__main__":
    app.run(debug=True)
