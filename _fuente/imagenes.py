#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convierte las cabeceras SVG que genera build.py en JPG de 1200x630.

Las redes sociales (WhatsApp, Facebook, X, Pinterest) no aceptan SVG como
og:image, asi que cada articulo necesita su JPG. Se ejecuta en local, no en la
accion de GitHub: los JPG se generan para todos los articulos (tambien los
programados) y se suben al repositorio.

Requiere Playwright con Chromium. En este equipo esta en el entorno de la skill
de SEO; se puede usar cualquier Python con `pip install playwright` y
`playwright install chromium`.

Uso:
  python _fuente/build.py          (genera los SVG)
  python _fuente/imagenes.py       (renderiza los JPG que falten o esten desfasados)
  python _fuente/imagenes.py --todas
  python _fuente/build.py          (otra vez, para que las paginas usen los JPG)
"""

import os
import sys

from playwright.sync_api import sync_playwright

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR_SVG = os.path.join(RAIZ, "_fuente", ".cache", "svg")
DIR_IMG = os.path.join(RAIZ, "assets", "img")

PAGINA = """<!DOCTYPE html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@600;700;800&display=swap" rel="stylesheet">
<style>html,body{margin:0;padding:0;background:#0f1115;}svg{display:block;}</style>
</head><body>%s</body></html>"""


def main():
    todas = "--todas" in sys.argv
    os.makedirs(DIR_IMG, exist_ok=True)
    pendientes = []
    for nombre in sorted(os.listdir(DIR_SVG)):
        if not nombre.endswith(".svg"):
            continue
        svg = os.path.join(DIR_SVG, nombre)
        jpg = os.path.join(DIR_IMG, nombre[:-4] + ".jpg")
        if todas or not os.path.isfile(jpg) or os.path.getmtime(jpg) < os.path.getmtime(svg) - 1:
            pendientes.append((svg, jpg))

    # build.py reescribe los SVG en cada ejecucion; solo re-renderizamos si cambia el contenido
    cache = os.path.join(DIR_SVG, ".huellas")
    huellas = {}
    if os.path.isfile(cache):
        for linea in open(cache, encoding="utf-8"):
            k, _, v = linea.strip().partition("\t")
            huellas[k] = v
    import hashlib
    reales = []
    for svg, jpg in pendientes:
        h = hashlib.sha1(open(svg, "rb").read()).hexdigest()
        if not todas and os.path.isfile(jpg) and huellas.get(os.path.basename(svg)) == h:
            continue
        reales.append((svg, jpg, h))

    if not reales:
        print("No hay imágenes que renderizar.")
        return

    with sync_playwright() as p:
        nav = p.chromium.launch()
        pag = nav.new_page(viewport={"width": 1200, "height": 630}, device_scale_factor=1)
        for i, (svg, jpg, h) in enumerate(reales, 1):
            contenido = open(svg, encoding="utf-8").read()
            pag.set_content(PAGINA % contenido, wait_until="networkidle")
            pag.evaluate("document.fonts.ready")
            pag.screenshot(path=jpg, type="jpeg", quality=86, clip={"x": 0, "y": 0, "width": 1200, "height": 630})
            huellas[os.path.basename(svg)] = h
            print("[%d/%d] %s" % (i, len(reales), os.path.basename(jpg)))
        nav.close()

    with open(cache, "w", encoding="utf-8") as f:
        for k, v in sorted(huellas.items()):
            f.write("%s\t%s\n" % (k, v))


if __name__ == "__main__":
    main()
