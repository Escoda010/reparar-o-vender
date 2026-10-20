#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Manda un aviso a Telegram cuando se publica un articulo o cuando algo falla.

Lee el token y el chat_id de las variables de entorno TELEGRAM_BOT_TOKEN y
TELEGRAM_CHAT_ID (que en GitHub Actions llegan desde los secrets, nunca
del repo).

Modos:
  python _fuente/telegram_aviso.py --publicacion   detecta articulos nuevos
                                                    en el ultimo commit y
                                                    los anuncia
  python _fuente/telegram_aviso.py --fallo "..."   avisa de un error
  python _fuente/telegram_aviso.py --prueba        manda un ping
"""

import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITIO = "https://repararovender.es"


def enviar(texto):
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    chat = os.environ.get("TELEGRAM_CHAT_ID", "")
    if not token or not chat:
        print("Faltan TELEGRAM_BOT_TOKEN o TELEGRAM_CHAT_ID; no mando nada.")
        return
    datos = urllib.parse.urlencode({
        "chat_id": chat,
        "text": texto,
        "parse_mode": "HTML",
        "disable_web_page_preview": "false",
    }).encode("utf-8")
    peticion = urllib.request.Request("https://api.telegram.org/bot%s/sendMessage" % token, data=datos)
    with urllib.request.urlopen(peticion, timeout=15) as r:
        print("Telegram respondio %s" % r.status)


def leer_meta_articulo(ruta_html):
    """Saca el <title> y la URL de un fichero HTML ya construido."""
    try:
        with open(ruta_html, encoding="utf-8") as f:
            html = f.read()
        titulo = re.search(r"<title>(.*?)</title>", html, re.S)
        titulo = titulo.group(1).strip() if titulo else ruta_html
        titulo = re.sub(r"\s*[-|·]\s*¿Reparo o Vendo\?.*$", "", titulo)
        return titulo
    except OSError:
        return ruta_html


def articulos_nuevos_en_commit(ref="HEAD"):
    """Devuelve lista de rutas .html de blog/ anadidas en ese commit."""
    salida = subprocess.run(
        ["git", "show", "--name-status", "--pretty=format:", ref],
        cwd=RAIZ, capture_output=True, text=True, check=True,
    ).stdout
    nuevos = []
    for linea in salida.splitlines():
        linea = linea.strip()
        if not linea or not linea.startswith("A\t"):
            continue
        ruta = linea[2:].strip()
        if ruta.startswith("blog/") and ruta.endswith(".html") and "/" not in ruta[5:]:
            nuevos.append(ruta)
    return nuevos


def publicacion():
    rutas = articulos_nuevos_en_commit()
    if not rutas:
        print("El ultimo commit no anade articulos nuevos; no aviso.")
        return
    lineas = ["📝 <b>Publicado hoy en repararovender.es</b>", ""]
    for ruta in rutas:
        titulo = leer_meta_articulo(os.path.join(RAIZ, ruta))
        url = "%s/%s" % (SITIO, ruta)
        lineas.append('• <a href="%s">%s</a>' % (url, titulo))
    enviar("\n".join(lineas))


def fallo(mensaje):
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    run_id = os.environ.get("GITHUB_RUN_ID", "")
    enlace = ""
    if repo and run_id:
        enlace = '\n\n<a href="https://github.com/%s/actions/runs/%s">Ver el log</a>' % (repo, run_id)
    enviar("❌ <b>Algo ha fallado publicando repararovender.es</b>\n\n%s%s" % (mensaje, enlace))


def prueba():
    enviar("✅ Hola. Soy el bot de repararovender.es. A partir de ahora te aviso cuando se publique algo nuevo o cuando algo se rompa.")


def main():
    args = sys.argv[1:]
    if "--publicacion" in args:
        publicacion()
    elif "--fallo" in args:
        i = args.index("--fallo")
        mensaje = args[i + 1] if i + 1 < len(args) else "Sin detalles."
        fallo(mensaje)
    elif "--prueba" in args:
        prueba()
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
