from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)

app.secret_key = "TransporteTlalpujahua2026"

usuario = request.form["usuario"]
password = request.form["password"]


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

    ahora = datetime.now()

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


@app.route("/")
def inicio():

    fecha_actual, hora_actual = obtener_datos_generales()

    return render_template(
        "index.html",
        rutas=rutas,
        fecha_actual=fecha_actual,
        hora_actual=hora_actual
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

    for ruta in rutas:

        if ruta["id"] == ruta_id:

            ruta["estado"] = nuevo_estado

            ruta["actualizacion"] = datetime.now().strftime(
                "%d/%m/%Y %I:%M %p"
            )

            break

    return redirect(url_for("admin"))

@app.route("/actualizar_observacion/<int:ruta_id>", methods=["POST"])
def actualizar_observacion(ruta_id):

    if not session.get("logueado"):
        return redirect(url_for("login"))

    nueva_observacion = request.form.get("observacion", "").strip()

    for ruta in rutas:

        if ruta["id"] == ruta_id:

            ruta["observacion"] = nueva_observacion

            ruta["actualizacion"] = datetime.now().strftime(
                "%d/%m/%Y %I:%M %p"
            )

            break

    return redirect(url_for("admin"))

@app.route("/admin")
def admin():

    if not session.get("logueado"):
        return redirect(url_for("login"))

    fecha_actual, hora_actual = obtener_datos_generales()

    return render_template(
        "admin.html",
        rutas=rutas,
        fecha_actual=fecha_actual,
        hora_actual=hora_actual
    )


if __name__ == "__main__":
    app.run(debug=True)
