#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Avisa a los buscadores que usan IndexNow (Bing, Yandex, Seznam, Naver...) de
las URLs nuevas o cambiadas. Google no usa IndexNow: para Google basta el
sitemap, que Search Console relee solo.

Uso:
  python _fuente/indexnow.py --desde HEAD~1   URLs de los ficheros cambiados en el último commit
  python _fuente/indexnow.py --todas          todas las URLs del sitemap
"""

import json
import os
import re
import subprocess
import sys
import urllib.request

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITIO = "https://repararovender.es"
HOST = "repararovender.es"
CLAVE = "20bba4d3296a3309ba135188bb2ccfff"


def urls_del_sitemap():
    with open(os.path.join(RAIZ, "sitemap.xml"), encoding="utf-8") as f:
        return re.findall(r"<loc>(.*?)</loc>", f.read())


def urls_cambiadas(desde):
    salida = subprocess.run(["git", "diff", "--name-only", desde, "HEAD"], cwd=RAIZ,
                            capture_output=True, text=True, check=True).stdout.split()
    urls = set()
    for ruta in salida:
        if not ruta.endswith(".html") or ruta.startswith("_") or ruta == "404.html" or ruta == "buscar.html":
            continue
        if ruta == "index.html":
            urls.add(SITIO + "/")
        elif ruta.endswith("/index.html"):
            urls.add("%s/%s" % (SITIO, ruta[:-len("index.html")]))
        else:
            urls.add("%s/%s" % (SITIO, ruta))
    return sorted(urls)


def enviar(urls):
    if not urls:
        print("No hay URLs que enviar.")
        return
    cuerpo = json.dumps({"host": HOST, "key": CLAVE, "keyLocation": "%s/%s.txt" % (SITIO, CLAVE),
                         "urlList": urls[:10000]}).encode("utf-8")
    peticion = urllib.request.Request("https://api.indexnow.org/indexnow", data=cuerpo,
                                      headers={"Content-Type": "application/json; charset=utf-8"})
    with urllib.request.urlopen(peticion, timeout=30) as r:
        print("IndexNow respondió %s para %d URLs." % (r.status, len(urls)))


def main():
    if "--todas" in sys.argv:
        urls = urls_del_sitemap()
    elif "--desde" in sys.argv:
        urls = urls_cambiadas(sys.argv[sys.argv.index("--desde") + 1])
    else:
        print(__doc__)
        return
    for u in urls:
        print("  " + u)
    enviar(urls)


if __name__ == "__main__":
    main()
