from datetime import datetime
from google.oauth2.service_account import Credentials
import gspread

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)


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


def cargar_rutas():

    hoja = sheet.worksheet("Rutas")

    return hoja.get_all_records()

def cargar_horarios():

    hoja = sheet.worksheet("Horarios")

    return hoja.get_all_records()

def guardar_reporte(usuario, ruta, reporte):

    hoja = sheet.worksheet("Reportes")

    fecha = datetime.now().strftime(
        "%d/%m/%Y %I:%M %p"
    )

    hoja.append_row([
        fecha,
        usuario,
        ruta,
        reporte
    ])

TOKEN = "8825240316:AAF6etfKUQXseNuPXnv-QGWXHIyhOm34iOE"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "Bienvenido a Transporte Local Tlalpujahua\n\nUsa /rutas para consultar las rutas disponibles."
    )


async def rutas(update: Update, context: ContextTypes.DEFAULT_TYPE):

    datos = cargar_rutas()

    mensaje = "Rutas disponibles\n\n"

    for ruta in datos:

        mensaje += f"• {ruta['nombre']}\n"

    await update.message.reply_text(mensaje)

async def proxima(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:

        await update.message.reply_text(
            "Uso: /proxima NombreRuta"
        )
        return

    nombre_busqueda = " ".join(context.args).lower()

    horarios = cargar_horarios()
    datos_rutas = cargar_rutas()

    ahora = datetime.now()

    dia = ahora.weekday()

    if dia <= 4:
        tipo_dia = "LV"
    elif dia == 5:
        tipo_dia = "SAB"
    else:
        tipo_dia = "DOM"

    horarios_ruta = []

    for h in horarios:

        if (
            h["ruta"].lower() == nombre_busqueda
            and h["tipo_dia"] == tipo_dia
        ):
            horarios_ruta.append(h["hora"])

    if not horarios_ruta:

        await update.message.reply_text(
            "No hay horarios disponibles."
        )
        return

    ahora_minutos = ahora.hour * 60 + ahora.minute

    for hora in horarios_ruta:

        hora_dt = datetime.strptime(
            str(hora),
            "%H:%M"
        )

        salida_minutos = (
            hora_dt.hour * 60 +
            hora_dt.minute
        )

        if salida_minutos >= ahora_minutos:

            faltan = salida_minutos - ahora_minutos

            estado = "Desconocido"

            for r in datos_rutas:

                if r["nombre"].lower() == nombre_busqueda:

                    estado = r["estado"]
                    break

            hora_formateada = datetime.strptime(
                str(hora),
                "%H:%M"
            ).strftime("%I:%M %p")

            mensaje = (
                f"Ruta: {nombre_busqueda.title()}\n"
                f"Próxima salida: {hora_formateada}\n"
                f"Faltan: {faltan} minutos\n"
                f"Estado: {estado}"
            )

            await update.message.reply_text(
                mensaje
            )
            return

    await update.message.reply_text(
        "Ya no hay salidas programadas hoy."
    )



async def estado(update: Update, context: ContextTypes.DEFAULT_TYPE):

    datos = cargar_rutas()

    mensaje = "Estado actual de rutas\n\n"

    for ruta in datos:

        mensaje += (
            f"{ruta['nombre']}: "
            f"{ruta['estado']}\n"
        )

    await update.message.reply_text(mensaje)

async def ruta(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:

        await update.message.reply_text(
            "Uso: /ruta NombreRuta"
        )
        return

    nombre_busqueda = " ".join(context.args).lower()

    datos = cargar_rutas()

    for r in datos:

        if r["nombre"].lower() == nombre_busqueda:

            mensaje = (
                f"Ruta: {r['nombre']}\n"
                f"Estado: {r['estado']}\n"
                f"Tarifa: {r['tarifa']}\n"
                f"Observación: {r['observacion']}\n"
                f"Última actualización: {r['actualizacion']}"
            )

            await update.message.reply_text(mensaje)
            return

    await update.message.reply_text(
        "Ruta no encontrada."
    )

async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):

    mensaje = (
        "Comandos disponibles\n\n"
        "/start - Iniciar bot\n"
        "/ayuda - Ver comandos\n"
        "/rutas - Ver rutas disponibles\n"
        "/estado - Estado de todas las rutas\n"
        "/ruta NombreRuta - Consultar una ruta\n"
        "/proxima NombreRuta - Próxima salida\n"
        "/reportar Ruta Mensaje - Reportar incidencias"
    )

    await update.message.reply_text(mensaje)

async def reportar(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) < 2:

        await update.message.reply_text(
            "Uso:\n/reportar Ruta Mensaje"
        )
        return

    ruta = context.args[0]

    reporte = " ".join(context.args[1:])

    usuario = update.effective_user.username

    if usuario is None:
        usuario = str(update.effective_user.id)

    guardar_reporte(
        usuario,
        ruta,
        reporte
    )

    await update.message.reply_text(
        "Reporte enviado correctamente."
    )

async def mensaje_libre(update: Update, context: ContextTypes.DEFAULT_TYPE):

    texto = update.message.text.lower()

    datos = cargar_rutas()

    for ruta in datos:

        nombre = ruta["nombre"].lower()

        if nombre in texto:

            if "estado" in texto or "activa" in texto:

                await update.message.reply_text(
                    f"{ruta['nombre']} está {ruta['estado']}."
                )
                return

            if "tarifa" in texto or "cuesta" in texto:

                await update.message.reply_text(
                    f"La tarifa de {ruta['nombre']} es {ruta['tarifa']}."
                )
                return

            if "observacion" in texto or "observación" in texto:

                await update.message.reply_text(
                    ruta["observacion"]
                )
                return
            
            if (
                "sale" in texto
                or "salida" in texto
                or "hora" in texto
                or "cuando" in texto
                or "cuándo" in texto
            ):

                horarios = cargar_horarios()

                ahora = datetime.now()

                dia = ahora.weekday()

                if dia <= 4:
                    tipo_dia = "LV"
                elif dia == 5:
                      tipo_dia = "SAB"
                else:
                      tipo_dia = "DOM"

                horarios_ruta = []

                for h in horarios:

                     if (
                            h["ruta"].lower() == nombre
                            and h["tipo_dia"] == tipo_dia
                    ):
                         horarios_ruta.append(h["hora"])

                ahora_minutos = (
                    ahora.hour * 60 +
                    ahora.minute
                )

                for hora in horarios_ruta:

                    hora_dt = datetime.strptime(
                         str(hora),
                         "%H:%M"
                    )

                    salida_minutos = (
                        hora_dt.hour * 60 +
                        hora_dt.minute
                    )

                    if salida_minutos >= ahora_minutos:

                        faltan = salida_minutos - ahora_minutos

                        hora_formateada = datetime.strptime(
                            str(hora),
                            "%H:%M"
                        ).strftime("%I:%M %p")

                        await update.message.reply_text(
                            f"Próxima salida de {ruta['nombre']}:\n"
                            f"{hora_formateada}\n"
                            f"Faltan {faltan} minutos."
                        )

                        return

                await update.message.reply_text(
                    f"Ya no hay salidas programadas hoy para {ruta['nombre']}."
                )

                return

    await update.message.reply_text(
        "No entendí tu consulta. Usa /ayuda para ver los comandos disponibles."
    )

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("rutas", rutas))
app.add_handler(CommandHandler("estado", estado))
app.add_handler(CommandHandler("ruta", ruta))
app.add_handler(CommandHandler("proxima", proxima))
app.add_handler(CommandHandler("ayuda", ayuda))
app.add_handler(
    CommandHandler("reportar", reportar)
)
app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        mensaje_libre
    )
)

print(cargar_rutas())
print("Bot iniciado...")

app.run_polling()
