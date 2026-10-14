#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador estatico de repararovender.es

Fuentes (no se publican: Jekyll ignora las carpetas que empiezan por "_"):
  _fuente/articulos/*.md   articulos del blog, con frontmatter
  _fuente/paginas/*.md     paginas sueltas (legales, sobre nosotros, calculadora...)

Salida:
  /blog/                   hub con todas las guias
  /blog/<categoria>/       indice de cada categoria
  /blog/<slug>.html        cada articulo (mismo patron que las URLs ya indexadas)
  /<pagina>.html           paginas sueltas
  /index.html              solo se reescriben los bloques entre marcadores <!-- RV:... -->
  /sitemap.xml /robots.txt /feed.xml /llms.txt /assets/busqueda.json

Publicacion programada: un articulo con "fecha" futura no se publica. La accion
de GitHub (.github/workflows) reconstruye cada manana y publica lo que toque.

Uso:
  python _fuente/build.py                        construye con la fecha de hoy
  BUILD_DATE=2026-11-01 python _fuente/build.py  simula otra fecha
"""

import html
import json
import os
import re
import shutil
import sys
import unicodedata
from datetime import date
from urllib.parse import quote

# ---------------------------------------------------------------------------
# Configuracion
# ---------------------------------------------------------------------------

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FUENTE = os.path.join(RAIZ, "_fuente")
DIR_ARTICULOS = os.path.join(FUENTE, "articulos")
DIR_PAGINAS = os.path.join(FUENTE, "paginas")
DIR_SVG = os.path.join(FUENTE, ".cache", "svg")
DIR_IMG = os.path.join(RAIZ, "assets", "img")

SITIO = "https://repararovender.es"
MARCA = "¿Reparo o Vendo?"
ADSENSE_CLIENTE = "ca-pub-3619241757820313"
GA_ID = "G-8YCHFVX91E"
INDEXNOW_KEY = "20bba4d3296a3309ba135188bb2ccfff"

# Direccion que aparece en las paginas legales y de contacto.
# OJO: "contacto@gmail.com" es la que habia y NO es de Jordi. Cambiar antes de publicar.
CONTACTO_EMAIL = "contacto@gmail.com"

# IDs de bloques de anuncio de AdSense. Vacios = solo Auto Ads (ya activas).
ADSENSE_SLOTS = {"en_articulo": "", "pie_articulo": ""}

HOY = date.fromisoformat(os.environ["BUILD_DATE"]) if os.environ.get("BUILD_DATE") else date.today()

# URLs que ya estaban publicadas e indexadas: el build falla si alguna desaparece.
URLS_PROTEGIDAS = [
    "/blog/reparar-embrague-o-vender-coche.html",
    "/blog/motor-gripado-reparar-o-vender.html",
    "/blog/itv-caducada-reparar-o-vender.html",
    "/blog/correa-distribucion-reparar-o-vender.html",
    "/blog/bateria-coche-reparar-o-vender.html",
    "/blog/tasacion-coche-averiado.html",
]

CATEGORIAS = {
    "coches": {
        "nombre": "Coches",
        "titulo": "Reparar o vender el coche: precios por avería y cuándo compensa",
        "descripcion": "Embrague, motor, correa, caja de cambios, turbo, ITV y tasación: lo que cuesta cada avería en España y cuándo es mejor vender el coche.",
        "intro": "El cálculo de siempre: compara el presupuesto del taller con lo que vale tu coche hoy. Aquí tienes el precio de cada avería, las señales que la delatan y cuándo sale más a cuenta vender.",
        "texto": [
            "La decisión de reparar o vender un coche averiado casi nunca depende solo del presupuesto. Depende de cuánto vale el coche hoy en el mercado, de qué pieza se ha roto y de lo que esa avería dice sobre el estado del resto del vehículo. Un embrague de 900 € en un coche que vale 9.000 € es mantenimiento; el mismo embrague en uno que vale 1.500 € es una decisión seria.",
            "En estas guías encontrarás los precios habituales en talleres españoles para cada avería, cómo distinguir una avería grave de una menor por los síntomas, y la regla que usan talleres y tasadores: por debajo del 20 % del valor del coche, repara; entre el 20 y el 50 %, depende del estado general; por encima del 50 %, vender suele ganar.",
            "Si ya tienes el presupuesto delante, la forma más rápida de decidir es la [calculadora gratuita de la portada](/#calculadora), que cruza el coste de la reparación con una estimación del valor de mercado de tu coche.",
        ],
        "color": "#1d5bbf",
        "tinta": "#1a52ad",
        "pilar": "vender-coche-averiado",
    },
    "electrodomesticos": {
        "nombre": "Electrodomésticos",
        "titulo": "Averías de electrodomésticos: causas, precios y si merece la pena arreglarlos",
        "titulo_seo": "Averías de electrodomésticos: causas y si compensa arreglarlos",
        "descripcion": "Lavadora, lavavajillas, nevera, horno, secadora, microondas, inducción y más: qué falla, qué puedes arreglar tú y cuándo compensa comprar uno nuevo.",
        "intro": "La mayoría de las averías de un electrodoméstico son cuatro o cinco piezas que se repiten una y otra vez. Aquí tienes el diagnóstico de cada síntoma, lo que cuesta cada arreglo en España y el punto exacto en el que deja de merecer la pena.",
        "texto": [
            "Antes de llamar a un técnico conviene saber algo que ahorra mucho dinero: una parte importante de las averías de electrodomésticos no son averías. Son filtros atascados, programas mal elegidos, gomas sucias o ajustes que nadie ha tocado desde que se instaló el aparato. Cada guía empieza por esas causas gratuitas, en el orden en el que conviene revisarlas.",
            "Cuando sí hay una pieza rota, te contamos qué cuesta repararla con mano de obra incluida y comparamos esa cifra con lo que vale un aparato nuevo equivalente y con los años de vida que le quedan al tuyo. Esa comparación es la que decide, y es la que casi nunca te hace el técnico.",
            "Todas las guías siguen el mismo criterio, que puedes aplicar a tu caso con la [calculadora de reparar o cambiar](/calculadora-reparar-o-cambiar.html): cuanto más viejo es el aparato, menor es el porcentaje de su precio que tiene sentido gastar en arreglarlo.",
        ],
        "color": "#e0570f",
        "tinta": "#b8460a",
        "pilar": "cuando-reparar-y-cuando-cambiar",
    },
    "tecnologia": {
        "nombre": "Tecnología",
        "titulo": "Reparar móvil, portátil o tele: qué cuesta y cuándo compensa",
        "descripcion": "Baterías, pantallas, discos SSD, wifi, impresoras y mandos. Qué vale cada reparación, qué puedes hacer tú y cuándo es mejor vender el aparato.",
        "intro": "Un móvil o un portátil se tira muchas veces por un componente de 40 € que aguanta tres años más. Estas guías te dicen qué se puede cambiar, qué cuesta y cuándo el aparato ya no da más de sí.",
        "texto": [
            "La tecnología envejece de una forma engañosa: la sensación de que un móvil o un portátil se ha quedado viejo suele venir de una sola pieza desgastada (la batería, el disco duro, la pasta térmica) o de años de software acumulado, no de que el procesador ya no dé para más.",
            "En estas guías separamos lo que tiene arreglo barato de lo que no. Verás precios de taller y de servicio oficial, lo que puedes hacer tú sin riesgo, y un factor que en tecnología pesa más que el precio: cuántos años de actualizaciones de seguridad le quedan al aparato.",
            "Y si decides cambiarlo, el aparato viejo casi siempre vale algo. En la sección de [vender de segunda mano](/blog/vender/) te explicamos cómo ponerle precio y dónde venderlo.",
        ],
        "color": "#0b8577",
        "tinta": "#0a7568",
        "pilar": "cambiar-bateria-movil-o-comprar-nuevo",
    },
    "hogar": {
        "nombre": "Hogar y bricolaje",
        "titulo": "Arreglos de casa paso a paso: persianas, grifos, cisternas, caldera y más",
        "titulo_seo": "Arreglos de casa paso a paso: persianas, grifos, cisternas",
        "descripcion": "Las averías domésticas más comunes explicadas paso a paso, con precios de material, lo que cobra un profesional y cuándo no debes tocar nada.",
        "intro": "Una persiana, un grifo o una cisterna son arreglos de media hora y menos de 20 € en material. Estas guías te llevan paso a paso y te avisan de los casos en los que hay que llamar a un profesional.",
        "texto": [
            "Hay arreglos de casa que cualquiera puede hacer con un destornillador y una tarde, y que un profesional cobra a 70-120 € porque el desplazamiento y la primera hora se pagan igual. Cambiar la cinta de una persiana, el cartucho de un grifo o el mecanismo de una cisterna entran en ese grupo.",
            "En cada guía tienes la lista de material con su precio, los pasos en orden y los errores típicos que hacen que el arreglo no funcione a la primera. También te decimos con claridad cuándo parar: con el gas y con el cuadro eléctrico no se experimenta, y lo indicamos en cada caso.",
            "Si un arreglo se complica, la regla de siempre sirve también aquí: compara lo que cuesta repararlo con lo que vale cambiarlo entero, contando la instalación.",
        ],
        "color": "#b8285a",
        "tinta": "#a5234f",
        "pilar": "persiana-no-sube",
    },
    "vender": {
        "nombre": "Vender de segunda mano",
        "titulo": "Vender de segunda mano: precio, fotos, plataformas y estafas",
        "descripcion": "Cómo poner precio, hacer fotos que venden, elegir plataforma, enviar con seguridad y detectar las estafas más comunes al vender lo que ya no usas.",
        "intro": "Lo que no vas a arreglar, véndelo bien. Cómo tasar sin regalarlo, qué plataforma conviene para cada tipo de producto, cómo hacer las fotos y las estafas que debes conocer antes de publicar.",
        "texto": [
            "Vender de segunda mano tiene dos formas de salir mal: regalar algo que valía bastante más o pasarte semanas con un anuncio que nadie contesta. Las dos se evitan con lo mismo: mirar lo que se vende de verdad, no lo que se anuncia, y presentar el producto mejor que la competencia.",
            "Estas guías cubren todo el proceso: cómo calcular un precio realista, cómo hacer fotos con el móvil que destaquen en el listado, qué plataforma funciona mejor para cada cosa, cómo enviar sin riesgo y cuáles son las estafas que más se repiten en España.",
            "También tratamos el caso que más nos interesa en este sitio: qué hacer con algo averiado. Un móvil con la pantalla rota, una lavadora que no centrifuga o un coche con el motor tocado siguen teniendo comprador si sabes dónde buscarlo.",
        ],
        "color": "#26803a",
        "tinta": "#22733a",
        "pilar": "poner-precio-segunda-mano",
    },
}

ORDEN_CATEGORIAS = ["coches", "electrodomesticos", "tecnologia", "hogar", "vender"]

MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
         "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
DIAS_RFC = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
MESES_RFC = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# Estado global del build (lo usan los renderizadores de enlaces)
ESTADO = {"publicadas": set(), "todas": set(), "errores": [], "avisos": []}


# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------

def T(plantilla, **kw):
    """Sustituye {{clave}} en una sola pasada. Falla si falta alguna clave."""
    return re.sub(r"\{\{(\w+)\}\}", lambda m: str(kw[m.group(1)]), plantilla)


def esc(texto):
    return html.escape(str(texto), quote=True)


def slugificar(texto):
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    texto = re.sub(r"[^a-zA-Z0-9\s-]", "", texto).strip().lower()
    return re.sub(r"[\s-]+", "-", texto)


def fecha_legible(iso):
    d = date.fromisoformat(iso)
    return "%d de %s de %d" % (d.day, MESES[d.month - 1], d.year)


def fecha_rfc822(iso):
    d = date.fromisoformat(iso)
    return "%s, %02d %s %d 07:00:00 +0200" % (DIAS_RFC[d.weekday()], d.day, MESES_RFC[d.month - 1], d.year)


def jsonld(obj):
    return '<script type="application/ld+json">\n%s\n</script>' % json.dumps(obj, ensure_ascii=False, indent=1)


def escribir(ruta_rel, contenido):
    destino = os.path.join(RAIZ, ruta_rel.lstrip("/"))
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    with open(destino, "w", encoding="utf-8", newline="\n") as f:
        f.write(contenido)


def url_imagen(slug):
    """JPG renderizado si existe; si no, la imagen generica del sitio."""
    if os.path.isfile(os.path.join(DIR_IMG, slug + ".jpg")):
        return "/assets/img/%s.jpg" % slug
    ESTADO["avisos"].append("Sin imagen JPG para '%s' (ejecuta _fuente/imagenes.py)" % slug)
    return "/assets/img/portada.jpg"


# ---------------------------------------------------------------------------
# Markdown -> bloques
# ---------------------------------------------------------------------------

RE_ENLACE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
RE_FUERTE = re.compile(r"\*\*([^*]+)\*\*")
RE_CURSIVA = re.compile(r"(?<![*\w])\*([^*\n]+)\*(?![*\w])")
RE_CODIGO = re.compile(r"`([^`]+)`")


def _enlace(m):
    texto, destino = m.group(1), html.unescape(m.group(2))
    ruta = destino.split("#")[0].split("?")[0]
    if ruta.startswith("/blog/") and ruta.endswith(".html"):
        if ruta not in ESTADO["todas"]:
            ESTADO["errores"].append("Enlace a un artículo que no existe: %s" % destino)
        elif ruta not in ESTADO["publicadas"]:
            return texto  # se enlazara solo cuando el destino se publique
    externo = destino.startswith("http") and "repararovender.es" not in destino
    extra = ' target="_blank" rel="noopener nofollow"' if externo else ""
    return '<a href="%s"%s>%s</a>' % (esc(destino), extra, texto)


def en_linea(texto):
    texto = esc(texto)
    texto = RE_CODIGO.sub(r"<code>\1</code>", texto)
    texto = RE_FUERTE.sub(r"<strong>\1</strong>", texto)
    texto = RE_CURSIVA.sub(r"<em>\1</em>", texto)
    return RE_ENLACE.sub(_enlace, texto)


INICIO_BLOQUE = re.compile(r"^(##|###|-\s|\d+\.\s|\||>\s|:::|<)")


def parsear_bloques(cuerpo):
    bloques = []
    lineas = cuerpo.split("\n")
    i, n = 0, len(lineas)
    while i < n:
        pelada = lineas[i].strip()
        if not pelada:
            i += 1
            continue

        if pelada.startswith(":::"):
            partes = pelada[3:].strip().split(" ", 1)
            clase = partes[0] or "dato"
            titulo = partes[1] if len(partes) > 1 else ""
            dentro = []
            i += 1
            while i < n and lineas[i].strip() != ":::":
                dentro.append(lineas[i])
                i += 1
            i += 1
            bloques.append(("callout", {"clase": clase, "titulo": titulo,
                                        "bloques": parsear_bloques("\n".join(dentro))}))
            continue

        if pelada.startswith("<"):
            crudo = []
            while i < n and lineas[i].strip():
                crudo.append(lineas[i])
                i += 1
            bloques.append(("raw", {"html": "\n".join(crudo)}))
            continue

        if pelada.startswith("## "):
            t = pelada[3:].strip()
            bloques.append(("h2", {"texto": t, "id": slugificar(t)}))
            i += 1
            continue

        if pelada.startswith("### "):
            t = pelada[4:].strip()
            bloques.append(("h3", {"texto": t, "id": slugificar(t)}))
            i += 1
            continue

        if pelada.startswith("|"):
            filas = []
            while i < n and lineas[i].strip().startswith("|"):
                filas.append(lineas[i].strip())
                i += 1
            if len(filas) >= 2 and set(filas[1].replace("|", "").replace(" ", "")) <= set("-:"):
                cab = [c.strip() for c in filas[0].strip("|").split("|")]
                cuerpo_f = [[c.strip() for c in f.strip("|").split("|")] for f in filas[2:]]
                bloques.append(("tabla", {"cabecera": cab, "filas": cuerpo_f}))
            continue

        if pelada.startswith("- "):
            items = []
            while i < n and lineas[i].strip().startswith("- "):
                items.append(lineas[i].strip()[2:].strip())
                i += 1
            bloques.append(("ul", {"items": items}))
            continue

        if re.match(r"^\d+\.\s", pelada):
            items = []
            while i < n and re.match(r"^\d+\.\s", lineas[i].strip()):
                items.append(re.sub(r"^\d+\.\s", "", lineas[i].strip()))
                i += 1
            bloques.append(("ol", {"items": items}))
            continue

        if pelada.startswith("> "):
            partes = []
            while i < n and lineas[i].strip().startswith("> "):
                partes.append(lineas[i].strip()[2:])
                i += 1
            bloques.append(("cita", {"texto": " ".join(partes)}))
            continue

        partes = []
        while i < n and lineas[i].strip() and not INICIO_BLOQUE.match(lineas[i].strip()):
            partes.append(lineas[i].strip())
            i += 1
        if not partes:  # linea que parecia bloque pero no lo era: tratar como texto
            partes.append(lineas[i].strip())
            i += 1
        bloques.append(("p", {"texto": " ".join(partes)}))
    return bloques


def render_bloques(bloques):
    out = []
    for tipo, d in bloques:
        if tipo == "h2":
            out.append('<h2 id="%s">%s</h2>' % (d["id"], en_linea(d["texto"])))
        elif tipo == "h3":
            out.append('<h3 id="%s">%s</h3>' % (d["id"], en_linea(d["texto"])))
        elif tipo == "p":
            out.append("<p>%s</p>" % en_linea(d["texto"]))
        elif tipo in ("ul", "ol"):
            out.append("<%s>%s</%s>" % (tipo, "".join("<li>%s</li>" % en_linea(x) for x in d["items"]), tipo))
        elif tipo == "cita":
            out.append("<blockquote><p>%s</p></blockquote>" % en_linea(d["texto"]))
        elif tipo == "raw":
            out.append(d["html"])
        elif tipo == "tabla":
            th = "".join('<th scope="col">%s</th>' % en_linea(c) for c in d["cabecera"])
            trs = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % en_linea(c) for c in fila)
                          for fila in d["filas"])
            out.append('<div class="tabla-wrap"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % (th, trs))
        elif tipo == "callout":
            titulo = '<p class="callout-titulo">%s</p>' % en_linea(d["titulo"]) if d["titulo"] else ""
            out.append('<aside class="callout callout-%s">%s%s</aside>' % (esc(d["clase"]), titulo, render_bloques(d["bloques"])))
    return "\n".join(out)


def extraer_faq(bloques):
    faq, estado = [], {"dentro": False, "pregunta": None, "resp": []}

    def cerrar():
        if estado["pregunta"] and estado["resp"]:
            texto = RE_ENLACE.sub(r"\1", " ".join(estado["resp"])).replace("**", "").replace("`", "")
            faq.append((estado["pregunta"], texto))

    for tipo, d in bloques:
        if tipo == "h2":
            cerrar()
            estado.update(dentro="preguntas frecuentes" in d["texto"].lower(), pregunta=None, resp=[])
        elif estado["dentro"] and tipo == "h3":
            cerrar()
            estado.update(pregunta=d["texto"], resp=[])
        elif estado["dentro"] and estado["pregunta"] and tipo == "p":
            estado["resp"].append(d["texto"])
        elif estado["dentro"] and estado["pregunta"] and tipo in ("ul", "ol"):
            estado["resp"].append(" ".join(d["items"]))
    cerrar()
    return faq


# ---------------------------------------------------------------------------
# Lectura de fuentes
# ---------------------------------------------------------------------------

def leer_md(ruta):
    with open(ruta, encoding="utf-8") as f:
        texto = f.read().replace("\r\n", "\n")
    if not texto.startswith("---"):
        raise ValueError("Falta el frontmatter en %s" % ruta)
    _, fm, cuerpo = texto.split("---", 2)
    meta = {}
    for linea in fm.strip().split("\n"):
        if ":" not in linea:
            continue
        k, v = linea.split(":", 1)
        v = v.strip()
        if v.startswith("[") and v.endswith("]"):
            v = [x.strip() for x in v[1:-1].split(",") if x.strip()]
        meta[k.strip()] = v
    return meta, cuerpo.strip()


def leer_articulo(ruta):
    meta, cuerpo = leer_md(ruta)
    a = dict(meta)
    a["slug"] = meta.get("slug") or os.path.splitext(os.path.basename(ruta))[0]
    a["url"] = "/blog/%s.html" % a["slug"]
    a["cuerpo_md"] = cuerpo
    a["palabras"] = len(re.findall(r"\w+", cuerpo))
    a["lectura"] = max(3, round(a["palabras"] / 220))
    a.setdefault("actualizado", a.get("fecha"))
    a.setdefault("icono", "herramientas")
    a.setdefault("tags", [])
    if isinstance(a["tags"], str):
        a["tags"] = [a["tags"]]
    if a.get("categoria") not in CATEGORIAS:
        raise ValueError("Categoría desconocida '%s' en %s" % (a.get("categoria"), ruta))
    for campo in ("titulo", "resumen", "descripcion", "fecha"):
        if not a.get(campo):
            raise ValueError("Falta '%s' en %s" % (campo, ruta))
    date.fromisoformat(a["fecha"])
    date.fromisoformat(a["actualizado"])
    if a["actualizado"] < a["fecha"]:
        a["actualizado"] = a["fecha"]
    a["publicado"] = date.fromisoformat(a["fecha"]) <= HOY
    return a


# ---------------------------------------------------------------------------
# Imagenes (SVG fuente; imagenes.py las convierte a JPG)
# ---------------------------------------------------------------------------

ICONOS = {
    "lavadora": '<rect x="26" y="16" width="68" height="88" rx="8"/><circle cx="60" cy="68" r="24"/><circle cx="60" cy="68" r="13"/><line x1="26" y1="40" x2="94" y2="40"/><circle cx="80" cy="28" r="4"/><circle cx="66" cy="28" r="4"/>',
    "secadora": '<rect x="26" y="16" width="68" height="88" rx="8"/><circle cx="60" cy="68" r="24"/><line x1="26" y1="40" x2="94" y2="40"/><circle cx="80" cy="28" r="4"/><path d="M48 62 q6 -8 12 0 q6 8 12 0"/><path d="M48 76 q6 -8 12 0 q6 8 12 0"/>',
    "lavavajillas": '<rect x="26" y="16" width="68" height="88" rx="8"/><line x1="26" y1="38" x2="94" y2="38"/><circle cx="52" cy="66" r="14"/><circle cx="76" cy="78" r="11"/><line x1="36" y1="28" x2="60" y2="28"/>',
    "nevera": '<rect x="32" y="10" width="56" height="100" rx="8"/><line x1="32" y1="46" x2="88" y2="46"/><line x1="76" y1="24" x2="76" y2="38"/><line x1="76" y1="56" x2="76" y2="74"/>',
    "horno": '<rect x="22" y="22" width="76" height="76" rx="8"/><rect x="34" y="46" width="52" height="40" rx="5"/><circle cx="38" cy="34" r="4"/><circle cx="52" cy="34" r="4"/><circle cx="66" cy="34" r="4"/>',
    "induccion": '<rect x="12" y="34" width="96" height="56" rx="8"/><circle cx="40" cy="62" r="16"/><circle cx="40" cy="62" r="8"/><circle cx="82" cy="62" r="12"/><circle cx="82" cy="62" r="5"/>',
    "microondas": '<rect x="14" y="32" width="92" height="56" rx="7"/><rect x="24" y="42" width="52" height="36" rx="4"/><circle cx="90" cy="48" r="3.5"/><circle cx="90" cy="60" r="3.5"/><circle cx="90" cy="72" r="3.5"/>',
    "cafetera": '<path d="M30 30 h52 v14 h-52 Z"/><path d="M34 44 v44 q0 10 10 10 h24 q10 0 10 -10 v-44"/><path d="M78 56 h8 q10 0 10 12 q0 12 -10 12 h-8"/><line x1="24" y1="104" x2="92" y2="104"/>',
    "aspiradora": '<circle cx="60" cy="60" r="40"/><circle cx="60" cy="60" r="26"/><circle cx="60" cy="38" r="5"/><line x1="40" y1="84" x2="80" y2="84"/>',
    "campana": '<path d="M48 14 h24 v34 h-24 Z"/><path d="M48 48 l-34 30 h92 l-34 -30"/><line x1="14" y1="88" x2="106" y2="88"/><path d="M40 100 q6 -6 12 0 q6 6 12 0 q6 -6 12 0"/>',
    "movil": '<rect x="38" y="10" width="44" height="100" rx="9"/><line x1="52" y1="20" x2="68" y2="20"/><line x1="50" y1="100" x2="70" y2="100"/>',
    "bateria": '<rect x="18" y="40" width="78" height="42" rx="7"/><rect x="96" y="52" width="8" height="18" rx="3"/><line x1="30" y1="52" x2="30" y2="70"/><line x1="44" y1="52" x2="44" y2="70"/><line x1="58" y1="52" x2="58" y2="70"/>',
    "pantalla": '<rect x="38" y="10" width="44" height="100" rx="9"/><path d="M44 34 l14 18 l-9 14 l16 16"/><path d="M70 30 l-8 22 l12 8"/>',
    "portatil": '<rect x="26" y="26" width="68" height="46" rx="5"/><path d="M16 84 h88 l-8 -12 H24 Z"/><line x1="50" y1="78" x2="70" y2="78"/>',
    "disco": '<circle cx="60" cy="60" r="38"/><circle cx="60" cy="60" r="9"/><line x1="60" y1="60" x2="86" y2="78"/>',
    "tv": '<rect x="14" y="24" width="92" height="60" rx="6"/><line x1="44" y1="98" x2="76" y2="98"/><line x1="60" y1="84" x2="60" y2="98"/>',
    "mando": '<path d="M30 46 h60 q16 0 16 18 q0 18 -14 18 q-10 0 -14 -8 h-36 q-4 8 -14 8 q-14 0 -14 -18 q0 -18 16 -18 Z"/><circle cx="44" cy="64" r="7"/><circle cx="78" cy="64" r="7"/>',
    "wifi": '<path d="M16 50 q44 -40 88 0"/><path d="M30 64 q30 -26 60 0"/><path d="M44 78 q16 -14 32 0"/><circle cx="60" cy="92" r="5"/>',
    "impresora": '<rect x="34" y="14" width="52" height="28" rx="3"/><rect x="16" y="42" width="88" height="40" rx="7"/><rect x="34" y="68" width="52" height="38" rx="3"/><circle cx="90" cy="54" r="3.5"/>',
    "auriculares": '<path d="M24 74 v-14 q0 -36 36 -36 q36 0 36 36 v14"/><rect x="16" y="66" width="20" height="32" rx="8"/><rect x="84" y="66" width="20" height="32" rx="8"/>',
    "ordenador": '<rect x="14" y="16" width="92" height="62" rx="6"/><line x1="46" y1="100" x2="74" y2="100"/><line x1="60" y1="78" x2="60" y2="100"/><circle cx="60" cy="47" r="12"/><line x1="60" y1="35" x2="60" y2="47"/>',
    "grifo": '<path d="M34 78 v-22 q0 -16 16 -16 h18"/><rect x="26" y="78" width="30" height="10" rx="3"/><line x1="68" y1="30" x2="68" y2="50"/><line x1="58" y1="40" x2="78" y2="40"/><path d="M86 58 q8 12 0 18 q-8 -6 0 -18 Z"/>',
    "cisterna": '<rect x="30" y="18" width="60" height="32" rx="5"/><path d="M38 50 v18 q0 24 22 24 q22 0 22 -24 v-18"/><circle cx="78" cy="34" r="4"/>',
    "persiana": '<rect x="20" y="18" width="80" height="84" rx="5"/><line x1="20" y1="36" x2="100" y2="36"/><line x1="20" y1="52" x2="100" y2="52"/><line x1="20" y1="68" x2="100" y2="68"/><line x1="20" y1="84" x2="100" y2="84"/>',
    "caldera": '<rect x="28" y="18" width="64" height="66" rx="6"/><line x1="42" y1="84" x2="42" y2="102"/><line x1="78" y1="84" x2="78" y2="102"/><path d="M60 38 q10 10 0 22 q-10 -12 0 -22 Z"/>',
    "termo": '<rect x="36" y="10" width="48" height="90" rx="22"/><line x1="48" y1="100" x2="48" y2="112"/><line x1="72" y1="100" x2="72" y2="112"/><path d="M60 40 q9 9 0 20 q-9 -11 0 -20 Z"/>',
    "aire": '<rect x="14" y="26" width="92" height="34" rx="7"/><line x1="26" y1="50" x2="94" y2="50"/><path d="M34 72 q8 -8 16 0 q8 8 16 0"/><path d="M54 90 q8 -8 16 0 q8 8 16 0"/>',
    "humedad": '<path d="M60 14 q30 38 30 58 q0 30 -30 30 q-30 0 -30 -30 q0 -20 30 -58 Z"/><path d="M46 74 q0 12 12 14"/>',
    "enchufe": '<rect x="24" y="24" width="72" height="72" rx="14"/><circle cx="60" cy="60" r="22"/><circle cx="51" cy="60" r="3.5"/><circle cx="69" cy="60" r="3.5"/>',
    "puerta": '<rect x="32" y="12" width="56" height="98" rx="3"/><circle cx="78" cy="62" r="4"/><line x1="20" y1="110" x2="100" y2="110"/>',
    "fregadero": '<path d="M14 46 h92"/><path d="M22 46 v18 q0 18 18 18 h40 q18 0 18 -18 v-18"/><path d="M60 82 v22"/><path d="M52 30 v-12 h16 v8"/>',
    "mueble": '<rect x="20" y="20" width="80" height="80" rx="5"/><line x1="20" y1="48" x2="100" y2="48"/><line x1="20" y1="74" x2="100" y2="74"/><line x1="60" y1="74" x2="60" y2="100"/>',
    "bici": '<circle cx="32" cy="76" r="20"/><circle cx="92" cy="76" r="20"/><path d="M32 76 l20 -30 h26 l14 30"/><line x1="52" y1="46" x2="74" y2="76"/><line x1="72" y1="40" x2="86" y2="40"/>',
    "etiqueta": '<path d="M60 14 h44 v44 l-50 50 L14 64 Z"/><circle cx="86" cy="36" r="7"/>',
    "camara": '<rect x="14" y="32" width="92" height="60" rx="8"/><circle cx="60" cy="62" r="19"/><circle cx="60" cy="62" r="8"/><rect x="44" y="20" width="32" height="12" rx="4"/>',
    "euro": '<circle cx="60" cy="60" r="40"/><path d="M74 44 q-22 -10 -22 16 q0 26 22 16"/><line x1="40" y1="54" x2="66" y2="54"/><line x1="40" y1="66" x2="66" y2="66"/>',
    "aviso": '<path d="M60 16 L106 98 H14 Z"/><line x1="60" y1="46" x2="60" y2="70"/><circle cx="60" cy="84" r="4"/>',
    "reciclar": '<path d="M60 18 l18 30 h-36 Z"/><path d="M96 76 l-18 -30 l-16 10"/><path d="M24 76 l18 -30 l16 10"/><path d="M30 80 h60"/>',
    "balanza": '<line x1="60" y1="18" x2="60" y2="94"/><line x1="34" y1="94" x2="86" y2="94"/><line x1="22" y1="36" x2="98" y2="36"/><path d="M22 36 l-10 24 h20 Z"/><path d="M98 36 l-10 24 h20 Z"/>',
    "tienda": '<path d="M20 44 h80 v56 H20 Z"/><path d="M14 44 l10 -24 h72 l10 24"/><line x1="48" y1="44" x2="48" y2="100"/><line x1="72" y1="44" x2="72" y2="100"/>',
    "ropa": '<path d="M42 16 l-28 16 l10 20 l10 -6 v56 h52 v-56 l10 6 l10 -20 l-28 -16 q-8 10 -18 10 q-10 0 -18 -10 Z"/>',
    "caja": '<path d="M16 38 l44 -20 l44 20 v48 l-44 20 l-44 -20 Z"/><path d="M16 38 l44 20 l44 -20"/><line x1="60" y1="58" x2="60" y2="106"/>',
    "coche": '<path d="M18 72 l8 -24 q2 -8 12 -8 h44 q10 0 14 8 l10 24"/><rect x="14" y="70" width="92" height="18" rx="6"/><circle cx="36" cy="92" r="9"/><circle cx="84" cy="92" r="9"/>',
    "motor": '<path d="M24 56 h14 v-12 h26 v12 h18 l14 14 v22 H24 Z"/><line x1="92" y1="62" x2="104" y2="62"/><line x1="44" y1="32" x2="44" y2="44"/>',
    "correa": '<circle cx="42" cy="56" r="22"/><circle cx="90" cy="78" r="14"/><path d="M42 34 q40 -6 54 30"/><path d="M24 68 q24 32 54 22"/>',
    "itv": '<rect x="24" y="14" width="72" height="92" rx="7"/><line x1="38" y1="40" x2="82" y2="40"/><line x1="38" y1="56" x2="82" y2="56"/><path d="M38 76 l10 10 l20 -20"/>',
    "engranaje": '<circle cx="60" cy="60" r="31"/><circle cx="60" cy="60" r="11"/><path stroke-width="12" d="M60 14 v14 M60 92 v14 M14 60 h14 M92 60 h14 M27.5 27.5 l10 10 M82.5 82.5 l10 10 M27.5 92.5 l10 -10 M82.5 37.5 l10 -10"/>',
    "turbo": '<circle cx="56" cy="60" r="34"/><circle cx="56" cy="60" r="10"/><path d="M56 26 q20 14 0 34 M90 60 q-14 20 -34 0 M56 94 q-20 -14 0 -34 M22 60 q14 -20 34 0"/><path d="M90 40 h20"/>',
    "llave": '<path d="M22 92 l40 -40"/><path d="M62 52 q-6 -22 14 -32 q12 -6 24 0 l-16 16 l4 12 l12 4 l16 -16 q6 12 0 24 q-10 20 -32 14"/>',
    "herramientas": '<path d="M22 92 l34 -34"/><path d="M66 42 l28 28"/><path d="M88 30 l14 14 l-10 10 l-14 -14 Z"/><path d="M18 76 q-8 -16 6 -24 q10 -6 18 2 l-10 10 l12 12 l10 -10 q8 8 2 18 q-8 14 -24 6 Z"/>',
    "documento": '<path d="M30 12 h44 l18 18 v78 h-62 Z"/><path d="M74 12 v18 h18"/><line x1="42" y1="54" x2="80" y2="54"/><line x1="42" y1="70" x2="80" y2="70"/><line x1="42" y1="86" x2="66" y2="86"/>',
    "calculadora": '<rect x="28" y="12" width="64" height="96" rx="8"/><rect x="38" y="22" width="44" height="20" rx="3"/><circle cx="44" cy="58" r="4"/><circle cx="60" cy="58" r="4"/><circle cx="76" cy="58" r="4"/><circle cx="44" cy="76" r="4"/><circle cx="60" cy="76" r="4"/><circle cx="76" cy="76" r="4"/><circle cx="44" cy="94" r="4"/><circle cx="60" cy="94" r="4"/><circle cx="76" cy="94" r="4"/>',
}


def partir_titulo(titulo, max_linea):
    palabras = titulo.split()
    lineas, actual = [], ""
    for p in palabras:
        prueba = (actual + " " + p).strip()
        if len(prueba) <= max_linea or not actual:
            actual = prueba
        else:
            lineas.append(actual)
            actual = p
    if actual:
        lineas.append(actual)
    return lineas


def svg_hero(titulo_corto, categoria, icono, color=None, etiqueta=None):
    """Cartel 1200x630: color solido de la categoria, titular en blanco y franja de marca."""
    cat = CATEGORIAS.get(categoria)
    color = color or cat["color"]
    etiqueta = etiqueta or cat["nombre"]
    for max_linea, cuerpo, interlinea in ((18, 68, 78), (22, 58, 66), (26, 50, 58)):
        lineas = partir_titulo(titulo_corto, max_linea)
        if len(lineas) <= 3:
            break
    else:
        lineas = lineas[:3]
        lineas[2] = lineas[2].rstrip(".,:;") + "…"
    alto = 34 + 28 + len(lineas) * interlinea
    y0 = int((540 - alto) / 2) + 26
    textos = "".join('<text x="70" y="%d" font-size="%d" font-weight="800" fill="#ffffff">%s</text>'
                     % (y0 + 28 + cuerpo + i * interlinea - 6, cuerpo, esc(l)) for i, l in enumerate(lineas))
    return T("""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" width="1200" height="630">
<rect width="1200" height="630" fill="{{color}}"/>
<rect x="830" y="0" width="370" height="540" fill="#000000" fill-opacity="0.14"/>
<g transform="translate(871 126) scale(2.4)" fill="none" stroke="#ffffff" stroke-width="5.5" stroke-linecap="square" stroke-linejoin="miter">{{icono}}</g>
<g font-family="'Archivo','Helvetica Neue',Arial,sans-serif">
 <rect x="70" y="{{ykick}}" width="44" height="8" fill="#ffffff"/>
 <text x="130" y="{{ykicktxt}}" font-size="24" font-weight="800" fill="#ffffff" letter-spacing="3">{{cat}}</text>
 {{textos}}
 <rect x="0" y="540" width="1200" height="90" fill="#ffffff"/>
 <rect x="0" y="540" width="1200" height="6" fill="#0f2341"/>
 <text x="70" y="600" font-size="34" font-weight="800" fill="#0f2341">¿Reparo<tspan fill="#d9480f"> o Vendo</tspan>?</text>
 <text x="1130" y="598" font-size="24" font-weight="700" fill="#5f6675" text-anchor="end">repararovender.es</text>
</g>
</svg>
""", color=color, icono=ICONOS.get(icono, ICONOS["herramientas"]), cat=esc(etiqueta.upper()),
             ykick=y0 - 4, ykicktxt=y0 + 6, textos=textos)


# ---------------------------------------------------------------------------
# Plantillas comunes
# ---------------------------------------------------------------------------

def cabecera_comun():
    return T("""<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script>
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('consent', 'default', {
  ad_storage: 'denied',
  ad_user_data: 'denied',
  ad_personalization: 'denied',
  analytics_storage: 'denied',
  wait_for_update: 500
});
</script>
<script async src="https://www.googletagmanager.com/gtag/js?id={{ga}}"></script>
<script>gtag('js', new Date()); gtag('config', '{{ga}}');</script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={{cliente}}" crossorigin="anonymous"></script>
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="icon" type="image/png" sizes="96x96" href="/favicon-96.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="alternate" type="application/rss+xml" title="{{marca}} — guías" href="/feed.xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@600;700;800&family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/estilos.css">""", ga=GA_ID, cliente=ADSENSE_CLIENTE, marca=esc(MARCA))


def nav(activa=""):
    cortos = {"coches": "Coches", "electrodomesticos": "Electrodomésticos", "tecnologia": "Tecnología",
              "hogar": "Hogar", "vender": "Vender"}
    enlaces = [("/blog/", "Guías", "hub")] + [("/blog/%s/" % c, cortos[c], c) for c in ORDEN_CATEGORIAS]
    items = "".join('<a href="%s"%s>%s</a>' % (u, ' aria-current="page"' if k == activa else "", esc(t)) for u, t, k in enlaces)
    return T("""<a class="saltar" href="#contenido">Saltar al contenido</a>
<header class="sitio-header">
  <div class="header-inner">
    <a href="/" class="logo">¿Reparo<span> o Vendo</span>?</a>
    <nav class="nav-principal" aria-label="Principal">{{items}}<a href="/buscar.html" class="nav-buscar">Buscar</a><a href="/calculadora-reparar-o-cambiar.html" class="nav-cta">Calculadora</a></nav>
  </div>
</header>""", items=items)


def pie():
    cats = "".join('<a href="/blog/%s/">%s</a>' % (c, esc(CATEGORIAS[c]["nombre"])) for c in ORDEN_CATEGORIAS)
    return T("""<footer class="sitio-footer">
  <div class="container">
    <div class="footer-cols">
      <div>
        <p class="footer-marca">¿Reparo<span> o Vendo</span>?</p>
        <p class="footer-texto">Guías para decidir si algo se arregla, se cambia o se vende. Con precios orientativos para España y sin rodeos.</p>
      </div>
      <div><p class="footer-titulo">Categorías</p>{{cats}}</div>
      <div>
        <p class="footer-titulo">Herramientas</p>
        <a href="/#calculadora">Calculadora: ¿reparo o vendo mi coche?</a>
        <a href="/calculadora-reparar-o-cambiar.html">Calculadora: ¿reparar o cambiar?</a>
        <a href="/blog/">Todas las guías</a>
        <a href="/buscar.html">Buscar</a>
        <a href="/feed.xml">RSS</a>
      </div>
      <div>
        <p class="footer-titulo">El sitio</p>
        <a href="/sobre-nosotros.html">Sobre nosotros</a>
        <a href="/contacto.html">Contacto</a>
        <a href="/aviso-legal.html">Aviso legal</a>
        <a href="/privacidad.html">Privacidad</a>
        <a href="/cookies.html">Cookies</a>
      </div>
    </div>
    <p class="footer-legal">&copy; {{anio}} ¿Reparo o Vendo? · Los precios son estimaciones orientativas para España y varían según zona, marca y taller. La información de este sitio no sustituye el diagnóstico de un profesional.</p>
  </div>
</footer>
<script src="/assets/sitio.js" defer></script>
<script src="/cookie-consent.js" defer></script>""", cats=cats, anio=HOY.year)


def pagina(titulo, descripcion, ruta, contenido, imagen=None, og_tipo="website",
           robots="index, follow, max-image-preview:large, max-snippet:-1",
           ld=None, extra_head="", activa="", clase="", scripts=""):
    img = SITIO + (imagen or "/assets/img/portada.jpg")
    return T("""<!DOCTYPE html>
<html lang="es">
<head>
{{comun}}
<title>{{titulo}}</title>
<meta name="description" content="{{desc}}">
<meta name="robots" content="{{robots}}">
<link rel="canonical" href="{{canonica}}">
<meta property="og:type" content="{{ogtipo}}">
<meta property="og:site_name" content="{{marca}}">
<meta property="og:locale" content="es_ES">
<meta property="og:title" content="{{titulo}}">
<meta property="og:description" content="{{desc}}">
<meta property="og:url" content="{{canonica}}">
<meta property="og:image" content="{{img}}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{{titulo}}">
<meta name="twitter:description" content="{{desc}}">
<meta name="twitter:image" content="{{img}}">
{{extra}}
</head>
<body class="{{clase}}">
{{nav}}
{{contenido}}
{{pie}}
{{ld}}
{{scripts}}
</body>
</html>
""", comun=cabecera_comun(), titulo=esc(titulo), desc=esc(descripcion), robots=robots,
             canonica=SITIO + ruta, ogtipo=og_tipo, marca=esc(MARCA), img=img, extra=extra_head,
             clase=clase, nav=nav(activa), contenido=contenido, pie=pie(),
             ld="\n".join(jsonld(x) for x in (ld or [])), scripts=scripts)


def org_ld():
    return {"@type": "Organization", "name": MARCA, "url": SITIO + "/",
            "logo": {"@type": "ImageObject", "url": SITIO + "/apple-touch-icon.png", "width": 180, "height": 180}}


def migas_ld(items):
    lista = []
    for i, (n, u) in enumerate(items):
        el = {"@type": "ListItem", "position": i + 1, "name": n}
        if u:
            el["item"] = SITIO + u
        lista.append(el)
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": lista}


def migas_html(items):
    partes = []
    for n, u in items:
        partes.append('<a href="%s">%s</a>' % (u, esc(n)) if u else '<span aria-current="page">%s</span>' % esc(n))
    return '<nav class="miga" aria-label="Ruta de navegación">%s</nav>' % ' <span class="sep">/</span> '.join(partes)


def bloque_anuncio(clave):
    slot = ADSENSE_SLOTS.get(clave, "")
    if not slot:
        return ""
    return T("""<div class="anuncio"><span class="anuncio-etiqueta">Publicidad</span>
<ins class="adsbygoogle" style="display:block" data-ad-client="{{c}}" data-ad-slot="{{s}}" data-ad-format="auto" data-full-width-responsive="true"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({});</script></div>""", c=ADSENSE_CLIENTE, s=slot)


def tarjeta(a, nivel="h3"):
    cat = CATEGORIAS[a["categoria"]]
    return T("""<a class="tarjeta" href="{{url}}">
  <div class="tarjeta-img"><img src="{{img}}" alt="" width="1200" height="630" loading="lazy" decoding="async"></div>
  <div class="tarjeta-cuerpo">
    <span class="kicker" style="--pc:{{color}};--pt:{{tinta}}">{{cat}}</span>
    <{{n}}>{{titulo}}</{{n}}>
    <p>{{resumen}}</p>
    <span class="tarjeta-meta">{{lectura}} min de lectura</span>
  </div>
</a>""", url=a["url"], img=a["imagen"], color=cat["color"], tinta=cat["tinta"], cat=esc(cat["nombre"]), n=nivel,
             titulo=esc(a["titulo"]), resumen=esc(a["resumen"]), lectura=a["lectura"])


def compartir(a):
    url = SITIO + a["url"]
    t = a["titulo"]

    def u(red):
        return quote(url + "?utm_source=%s&utm_medium=social&utm_campaign=compartir" % red, safe="")

    redes = [
        ("whatsapp", "WhatsApp", "https://wa.me/?text=" + quote(t + " ", safe="") + u("whatsapp")),
        ("facebook", "Facebook", "https://www.facebook.com/sharer/sharer.php?u=" + u("facebook")),
        ("x", "X", "https://twitter.com/intent/tweet?text=" + quote(t, safe="") + "&url=" + u("x")),
        ("telegram", "Telegram", "https://t.me/share/url?url=" + u("telegram") + "&text=" + quote(t, safe="")),
        ("pinterest", "Pinterest", "https://pinterest.com/pin/create/button/?url=" + u("pinterest")
         + "&media=" + quote(SITIO + a["imagen"], safe="") + "&description=" + quote(t, safe="")),
    ]
    enlaces = "".join('<a class="red red-%s" href="%s" target="_blank" rel="noopener" data-red="%s">%s</a>' % (k, esc(h), k, n)
                      for k, n, h in redes)
    return ('<div class="compartir"><span class="compartir-titulo">Compártelo</span>%s'
            '<button type="button" class="red red-copiar" data-copiar="%s">Copiar enlace</button></div>') % (enlaces, esc(url))


# ---------------------------------------------------------------------------
# Articulos
# ---------------------------------------------------------------------------

def render_articulo(a, pubs):
    cat = CATEGORIAS[a["categoria"]]
    bloques = parsear_bloques(a["cuerpo_md"])

    h2s = [d for t, d in bloques if t == "h2"]
    sumario = ""
    if len(h2s) >= 3:
        sumario = '<nav class="sumario" aria-label="Contenido de la guía"><p class="sumario-titulo">En esta guía</p><ol>%s</ol></nav>' % "".join(
            '<li><a href="#%s">%s</a></li>' % (d["id"], esc(re.sub(r"^\d+\.\s+", "", d["texto"]))) for d in h2s)

    claves = ""
    if bloques and bloques[0][0] == "callout" and bloques[0][1]["clase"] == "claves":
        claves = render_bloques([bloques[0]])
        bloques = bloques[1:]

    partes, vistos, anuncio = [], 0, bloque_anuncio("en_articulo")
    for tipo, d in bloques:
        if tipo == "h2":
            vistos += 1
            if vistos == 3 and anuncio:
                partes.append(anuncio)
        partes.append(render_bloques([(tipo, d)]))

    tags = set(a["tags"])

    def afinidad(x):
        return (len(tags & set(x["tags"])), x["fecha"])

    misma = sorted([x for x in pubs if x["categoria"] == a["categoria"] and x["slug"] != a["slug"]], key=afinidad, reverse=True)[:5]
    otras = sorted([x for x in pubs if x["categoria"] != a["categoria"]], key=afinidad, reverse=True)[:3]

    def lista(xs):
        return "".join('<a href="%s"><span>%s</span>%s</a>' % (x["url"], esc(CATEGORIAS[x["categoria"]]["nombre"]), esc(x["titulo"])) for x in xs)

    fechas = "Publicado el %s" % fecha_legible(a["fecha"])
    if a["actualizado"] != a["fecha"]:
        fechas += " · Actualizado el %s" % fecha_legible(a["actualizado"])

    migas = [("Inicio", "/"), ("Guías", "/blog/"), (cat["nombre"], "/blog/%s/" % a["categoria"]), (a["titulo"], None)]
    es_coche = a["categoria"] == "coches"

    contenido = T("""<main id="contenido" class="articulo-main">
  <div class="container">
    {{migas}}
    <article>
      <header class="articulo-cab">
        <a class="kicker kicker-grande" href="/blog/{{cat_slug}}/" style="--pc:{{color}};--pt:{{tinta}}">{{cat}}</a>
        <h1>{{h1}}</h1>
        <p class="entradilla">{{entradilla}}</p>
        <p class="meta-articulo">{{fechas}} · {{lectura}} min de lectura · Por <a href="/sobre-nosotros.html">la redacción de ¿Reparo o Vendo?</a></p>
      </header>
      <figure class="hero-figura">
        <img src="{{img}}" alt="{{alt}}" width="1200" height="630" fetchpriority="high" decoding="async">
      </figure>
      {{compartir}}
      <div class="prosa">{{claves}}</div>
      {{sumario}}
      <div class="prosa">
{{cuerpo}}
      </div>
      {{anuncio_pie}}
      <aside class="caja-cta">
        <p class="caja-cta-titulo">{{cta_titulo}}</p>
        <p>{{cta_texto}}</p>
        <a href="{{cta_url}}">{{cta_boton}}</a>
      </aside>
      {{compartir}}
    </article>
    <section class="relacionados">
      <h2>Más guías de {{cat_min}}</h2>
      <div class="relacionados-lista">{{misma}}</div>
      {{otras_bloque}}
      <p class="ver-todas"><a href="/blog/{{cat_slug}}/">Ver todas las guías de {{cat_min}} →</a></p>
    </section>
  </div>
</main>""",
        migas=migas_html(migas), color=cat["color"], tinta=cat["tinta"], cat=esc(cat["nombre"]), h1=esc(a.get("h1") or a["titulo"]),
        entradilla=esc(a["resumen"]), fechas=fechas, lectura=a["lectura"], img=a["imagen"],
        alt=esc(a.get("alt_imagen") or a["titulo"]), compartir=compartir(a), sumario=sumario, claves=claves,
        cuerpo="\n".join(partes), anuncio_pie=bloque_anuncio("pie_articulo"),
        cta_titulo="¿Lo reparas o lo vendes?" if es_coche else "¿Lo arreglas o lo cambias?",
        cta_texto=("La calculadora cruza el presupuesto del taller con el valor de mercado estimado de tu coche. Tarda diez segundos y es gratis."
                   if es_coche else
                   "La calculadora cruza el presupuesto con lo que cuesta uno nuevo y los años que le quedan al tuyo. Tarda diez segundos y es gratis."),
        cta_url="/#calculadora" if es_coche else "/calculadora-reparar-o-cambiar.html",
        cta_boton="Calcular si reparo o vendo mi coche" if es_coche else "Calcular si merece la pena repararlo",
        cat_min=esc(cat["nombre"].lower()), misma=lista(misma),
        otras_bloque=('<h2 class="relacionados-sub">También te puede interesar</h2><div class="relacionados-lista">%s</div>' % lista(otras)) if otras else "",
        cat_slug=a["categoria"])

    ld = [{
        "@context": "https://schema.org", "@type": "Article",
        "headline": a["titulo"], "description": a["descripcion"],
        "image": {"@type": "ImageObject", "url": SITIO + a["imagen"], "width": 1200, "height": 630},
        "articleSection": cat["nombre"], "keywords": ", ".join(a["tags"]), "inLanguage": "es-ES",
        "wordCount": a["palabras"],
        "author": {"@type": "Organization", "name": MARCA, "url": SITIO + "/sobre-nosotros.html"},
        "publisher": org_ld(),
        "datePublished": a["fecha"], "dateModified": a["actualizado"],
        "mainEntityOfPage": {"@type": "WebPage", "@id": SITIO + a["url"]},
    }, migas_ld(migas)]
    faq = extraer_faq(bloques)
    if faq:
        ld.append({"@context": "https://schema.org", "@type": "FAQPage",
                   "mainEntity": [{"@type": "Question", "name": p, "acceptedAnswer": {"@type": "Answer", "text": r}} for p, r in faq]})

    extra = T("""<meta property="article:published_time" content="{{p}}">
<meta property="article:modified_time" content="{{m}}">
<meta property="article:section" content="{{s}}">
<meta property="og:image:alt" content="{{alt}}">""", p=a["fecha"], m=a["actualizado"], s=esc(cat["nombre"]),
               alt=esc(a.get("alt_imagen") or a["titulo"]))

    return pagina(a.get("titulo_seo") or a["titulo"], a["descripcion"], a["url"], contenido, imagen=a["imagen"],
                  og_tipo="article", ld=ld, extra_head=extra, activa=a["categoria"], clase="pagina-articulo")


# ---------------------------------------------------------------------------
# Hub, categorias, paginas
# ---------------------------------------------------------------------------

def render_hub(pubs):
    destacados = [a for a in pubs if str(a.get("destacado", "")).lower() == "si"][:6]
    ultimos = sorted(pubs, key=lambda a: (a["fecha"], a["slug"]), reverse=True)[:6]
    secciones, indice = [], []
    for c in ORDEN_CATEGORIAS:
        cat = CATEGORIAS[c]
        lista = [a for a in pubs if a["categoria"] == c]
        if not lista:
            continue
        secciones.append(T("""<section class="seccion-cat" aria-labelledby="cat-{{c}}" style="--pc:{{color}};--pt:{{tinta}}">
  <div class="seccion-cab"><h2 id="cat-{{c}}">{{nombre}}</h2><a href="/blog/{{c}}/">Ver las {{n}} guías →</a></div>
  <p class="seccion-intro">{{intro}}</p>
  <div class="rejilla">{{tarjetas}}</div>
</section>""", c=c, color=cat["color"], tinta=cat["tinta"], nombre=esc(cat["nombre"]), n=len(lista), intro=esc(cat["intro"]),
                           tarjetas="".join(tarjeta(a) for a in lista[:6])))
        indice.append('<div class="indice-col" style="--pc:%s"><h3><a href="/blog/%s/">%s</a></h3><ul>%s</ul></div>' % (
            cat["color"], c, esc(cat["nombre"]), "".join('<li><a href="%s">%s</a></li>' % (a["url"], esc(a["titulo"])) for a in lista)))

    contenido = T("""<main id="contenido">
  <section class="hub-hero">
    <div class="container">
      {{migas}}
      <h1>Antes de tirarlo, mira si se arregla</h1>
      <p class="hub-lead">{{n}} guías con el diagnóstico de las averías más comunes del coche y de la casa, lo que cuesta cada arreglo en España y cuándo sale más a cuenta comprar uno nuevo. Y si no merece la pena arreglarlo, cómo venderlo bien.</p>
      <form class="buscador" action="/buscar.html" method="get" role="search">
        <label for="q" class="oculto">Buscar en las guías</label>
        <input id="q" name="q" type="search" placeholder="Busca una avería: lavadora, embrague, persiana…" autocomplete="off">
        <button type="submit">Buscar</button>
      </form>
      <div class="hub-acciones">
        <a class="boton" href="/calculadora-reparar-o-cambiar.html">Calculadora: ¿reparar o cambiar?</a>
        <a class="boton boton-fantasma" href="/#calculadora">Calculadora del coche</a>
      </div>
      <nav class="cat-bloques" aria-label="Categorías">{{chips}}</nav>
    </div>
  </section>
  <div class="container">
    <section class="destacados"><h2 class="titulo-seccion">Las más consultadas</h2><div class="rejilla">{{dest}}</div></section>
    <section><h2 class="titulo-seccion">Últimas guías</h2><div class="rejilla">{{ult}}</div></section>
    {{secciones}}
    <section class="indice-completo" aria-labelledby="indice"><h2 id="indice" class="titulo-seccion">Índice completo de guías</h2><div class="indice-cols">{{indice}}</div></section>
  </div>
</main>""", migas=migas_html([("Inicio", "/"), ("Guías", None)]), n=len(pubs),
                  chips="".join('<a href="/blog/%s/" class="cat-bloque" style="--pc:%s"><strong>%s</strong><span>%d guías</span></a>' % (
                      c, CATEGORIAS[c]["color"], esc(CATEGORIAS[c]["nombre"]), len([a for a in pubs if a["categoria"] == c])) for c in ORDEN_CATEGORIAS),
                  dest="".join(tarjeta(a) for a in (destacados or ultimos)), ult="".join(tarjeta(a) for a in ultimos),
                  secciones="\n".join(secciones), indice="".join(indice))

    ld = [{"@context": "https://schema.org", "@type": "CollectionPage", "name": "Guías de ¿Reparo o Vendo?",
           "url": SITIO + "/blog/", "inLanguage": "es-ES", "isPartOf": {"@type": "WebSite", "name": MARCA, "url": SITIO + "/"},
           "mainEntity": {"@type": "ItemList", "numberOfItems": len(pubs),
                          "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": SITIO + a["url"]} for i, a in enumerate(pubs)]}},
          migas_ld([("Inicio", "/"), ("Guías", None)])]
    return pagina("Guías para reparar, cambiar o vender: %d guías prácticas" % len(pubs),
                  "%d guías sobre las averías más comunes del coche, los electrodomésticos y la casa: síntomas, precios en España y cuándo compensa reparar o vender." % len(pubs),
                  "/blog/", contenido, ld=ld, activa="hub", clase="pagina-hub")


def render_categoria(c, pubs):
    cat = CATEGORIAS[c]
    lista = [a for a in pubs if a["categoria"] == c]
    pilar = next((a for a in lista if a["slug"] == cat.get("pilar")), None)
    empieza = ""
    if pilar:
        empieza = '<aside class="empieza" style="--pc:' + cat["color"] + '"><p class="empieza-titulo">Si no sabes por dónde empezar</p><a href="%s">%s →</a></aside>' % (pilar["url"], esc(pilar["titulo"]))
    texto = "".join("<p>%s</p>" % en_linea(p) for p in cat["texto"])
    otras = "".join('<a href="/blog/%s/" class="chip" style="--pc:%s">%s</a>' % (x, CATEGORIAS[x]["color"], esc(CATEGORIAS[x]["nombre"]))
                    for x in ORDEN_CATEGORIAS if x != c)
    migas = [("Inicio", "/"), ("Guías", "/blog/"), (cat["nombre"], None)]
    contenido = T("""<main id="contenido">
  <section class="cat-hero" style="--pc:{{color}}">
    <div class="container">
      {{migas}}
      <h1>{{h1}}</h1>
      <p class="hub-lead">{{intro}}</p>
      <p class="cat-contador">{{n}} guías en esta categoría</p>
    </div>
  </section>
  <div class="container">
    {{empieza}}
    <div class="rejilla">{{tarjetas}}</div>
    <section class="cat-texto prosa">{{texto}}</section>
    <section class="otras-cats"><h2 class="titulo-seccion">Otras categorías</h2><div class="chips">{{otras}}</div></section>
  </div>
</main>""", color=cat["color"], migas=migas_html(migas), h1=esc(cat["titulo"]), intro=esc(cat["intro"]), n=len(lista),
                  empieza=empieza, tarjetas="".join(tarjeta(a, "h2") for a in lista), texto=texto, otras=otras)
    ld = [{"@context": "https://schema.org", "@type": "CollectionPage", "name": cat["nombre"], "description": cat["descripcion"],
           "url": "%s/blog/%s/" % (SITIO, c), "inLanguage": "es-ES",
           "mainEntity": {"@type": "ItemList", "numberOfItems": len(lista),
                          "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": SITIO + a["url"]} for i, a in enumerate(lista)]}},
          migas_ld(migas)]
    return pagina(cat.get("titulo_seo", cat["titulo"]), cat["descripcion"], "/blog/%s/" % c, contenido, ld=ld, activa=c, clase="pagina-categoria")


def render_pagina(meta, cuerpo):
    cuerpo = cuerpo.replace("{{EMAIL}}", CONTACTO_EMAIL)
    bloques = parsear_bloques(cuerpo)
    ruta = meta["url"]
    migas = [("Inicio", "/"), (meta.get("miga") or meta["titulo"], None)]
    actualizado = meta.get("actualizado")
    pie_fecha = '<p class="meta-articulo">Última actualización: %s</p>' % fecha_legible(actualizado) if actualizado else ""
    contenido = T("""<main id="contenido" class="articulo-main pagina-simple">
  <div class="container">
    {{migas}}
    <h1>{{h1}}</h1>
    {{entradilla}}
    <div class="prosa">
{{cuerpo}}
    </div>
    {{pie_fecha}}
  </div>
</main>""", migas=migas_html(migas), h1=esc(meta.get("h1") or meta["titulo"]),
                  entradilla=('<p class="entradilla">%s</p>' % esc(meta["entradilla"])) if meta.get("entradilla") else "",
                  cuerpo=render_bloques(bloques), pie_fecha=pie_fecha)
    ld = [migas_ld(migas)]
    if meta.get("schema") == "calculadora":
        ld.append({"@context": "https://schema.org", "@type": "WebApplication", "name": meta["titulo"], "url": SITIO + ruta,
                   "description": meta["descripcion"], "applicationCategory": "UtilityApplication", "operatingSystem": "Web",
                   "inLanguage": "es-ES", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"}})
    if meta.get("schema") == "about":
        about = {"@context": "https://schema.org", "@type": "AboutPage", "url": SITIO + ruta, "inLanguage": "es-ES",
                 "about": org_ld()}
        ld.append(about)
    faq = extraer_faq(bloques)
    if faq:
        ld.append({"@context": "https://schema.org", "@type": "FAQPage",
                   "mainEntity": [{"@type": "Question", "name": p, "acceptedAnswer": {"@type": "Answer", "text": r}} for p, r in faq]})
    scripts = "".join('<script src="%s" defer></script>' % s for s in (meta.get("scripts") or []))
    robots = "noindex, follow" if meta.get("indexar") == "no" else "index, follow, max-image-preview:large, max-snippet:-1"
    return pagina(meta.get("titulo_seo") or meta["titulo"], meta["descripcion"], ruta, contenido,
                  imagen=meta.get("imagen"), robots=robots, ld=ld, scripts=scripts, clase="pagina-" + meta.get("clase", "simple"))


# ---------------------------------------------------------------------------
# Portada (solo bloques entre marcadores)
# ---------------------------------------------------------------------------

def reemplazar_bloque(texto, nombre, nuevo):
    patron = re.compile(r"(<!-- RV:%s:INICIO -->)(.*?)(<!-- RV:%s:FIN -->)" % (nombre, nombre), re.S)
    if not patron.search(texto):
        raise SystemExit("Falta el marcador RV:%s en index.html" % nombre)
    return patron.sub(lambda m: m.group(1) + "\n" + nuevo + "\n" + m.group(3), texto, count=1)


def actualizar_portada(pubs):
    ruta = os.path.join(RAIZ, "index.html")
    with open(ruta, encoding="utf-8") as f:
        texto = f.read()

    head = T("""<script async src="https://www.googletagmanager.com/gtag/js?id={{ga}}"></script>
<script>gtag('js', new Date()); gtag('config', '{{ga}}');</script>
<link rel="alternate" type="application/rss+xml" title="{{marca}} — guías" href="/feed.xml">
{{ld}}""", ga=GA_ID, marca=esc(MARCA), ld=jsonld({"@context": "https://schema.org", "@graph": [
        {"@type": "WebSite", "@id": SITIO + "/#web", "name": MARCA, "url": SITIO + "/", "inLanguage": "es-ES",
         "publisher": {"@id": SITIO + "/#org"},
         "potentialAction": {"@type": "SearchAction", "target": SITIO + "/buscar.html?q={q}", "query-input": "required name=q"}},
        dict({"@id": SITIO + "/#org"}, **org_ld())]}))

    navh = """      <a href="#calculadora">Calculadora</a>
      <a href="/blog/">Guías</a>
      <a href="/blog/coches/">Coches</a>
      <a href="#guias">Casa y tecnología</a>
      <a href="#faq">FAQ</a>"""

    coches = [a for a in pubs if a["categoria"] == "coches"]
    lista_coche = "\n".join('          <li><a href="%s">%s</a></li>' % (a["url"], esc(a["titulo"])) for a in coches)
    lista_coche += '\n          <li><a href="/blog/coches/"><strong>Ver todas las guías de coches →</strong></a></li>'

    ultimos = [a for a in sorted(pubs, key=lambda a: (a["fecha"], a["slug"]), reverse=True) if a["categoria"] != "coches"][:6]
    tiles = "".join(T('<a class="rv-cat" href="/blog/{{c}}/" style="--pc:{{color}}"><strong>{{nombre}}</strong><span>{{n}} guías</span></a>',
                      c=c, color=CATEGORIAS[c]["color"], nombre=esc(CATEGORIAS[c]["nombre"]),
                      n=len([a for a in pubs if a["categoria"] == c])) for c in ORDEN_CATEGORIAS)
    cards = "".join(T('<a class="rv-card" href="{{url}}"><img src="{{img}}" alt="" width="1200" height="630" loading="lazy" decoding="async"><span class="rv-card-cat" style="--pt:{{tinta}}">{{cat}}</span><strong>{{t}}</strong></a>',
                      url=a["url"], img=a["imagen"], tinta=CATEGORIAS[a["categoria"]]["tinta"],
                      cat=esc(CATEGORIAS[a["categoria"]]["nombre"]), t=esc(a["titulo"])) for a in ultimos)
    seccion = T("""<section class="rv-guias" id="guias" aria-labelledby="rv-guias-titulo">
<style>
.rv-guias{padding:3rem 0 3.4rem;background:#f3f4f6;border-top:1px solid #dde1e7;}
.rv-guias h2{font-family:'Archivo',Arial,sans-serif;font-weight:800;font-size:clamp(1.5rem,3.6vw,2rem);line-height:1.15;margin:0 0 .6rem;color:#14181f;}
.rv-guias .rv-lead{color:#3b4250;font-size:1.08rem;margin:0 0 1.6rem;max-width:68ch;}
.rv-cats{display:grid;grid-template-columns:repeat(5,1fr);gap:.6rem;margin-bottom:2.2rem;}
.rv-cat{display:flex;flex-direction:column;justify-content:space-between;min-height:104px;text-decoration:none;background:var(--pc);color:#fff;border-radius:3px;padding:.9rem 1rem;}
.rv-cat strong{font-family:'Archivo',Arial,sans-serif;font-weight:800;font-size:1.08rem;line-height:1.15;}
.rv-cat span{font-size:.88rem;display:flex;justify-content:space-between;}
.rv-cat span::after{content:"→";font-weight:700;}
.rv-cat:hover{filter:brightness(.9);}
.rv-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1.2rem;}
.rv-card{display:flex;flex-direction:column;gap:.4rem;text-decoration:none;background:#fff;border:1px solid #dde1e7;border-radius:3px;overflow:hidden;padding-bottom:1rem;}
.rv-card img{width:100%;height:auto;aspect-ratio:1200/630;object-fit:cover;display:block;margin:0;border-radius:0;}
.rv-card-cat{margin:.5rem 1rem 0;color:var(--pt);font-family:'Archivo',Arial,sans-serif;font-size:.75rem;font-weight:800;text-transform:uppercase;letter-spacing:.08em;}
.rv-card strong{margin:0 1rem;color:#14181f;font-family:'Archivo',Arial,sans-serif;font-size:1.05rem;line-height:1.3;}
.rv-card:hover strong{color:#c94108;text-decoration:underline;}
.rv-btn{display:inline-block;margin-top:1.8rem;background:#c94108;color:#fff;font-weight:700;text-decoration:none;padding:.85rem 1.4rem;border-radius:3px;}
.rv-btn:hover{background:#a83606;}
@media (max-width:900px){.rv-cats{grid-template-columns:repeat(3,1fr);}.rv-grid{grid-template-columns:1fr 1fr;}}
@media (max-width:560px){.rv-cats{grid-template-columns:1fr 1fr;}.rv-grid{grid-template-columns:1fr;}}
</style>
<div class="container">
  <h2 id="rv-guias-titulo">No solo coches: guías para todo lo que se arregla o se vende</h2>
  <p class="rv-lead">Lavadoras, neveras, móviles, portátiles, persianas, grifos… El mismo criterio de la calculadora aplicado a todo lo que tienes en casa: qué falla, qué cuesta arreglarlo y cuándo compensa cambiarlo o venderlo.</p>
  <div class="rv-cats">{{tiles}}</div>
  <div class="rv-grid">{{cards}}</div>
  <a class="rv-btn" href="/blog/">Ver las {{n}} guías</a>
</div>
</section>""", tiles=tiles, cards=cards, n=len(pubs))

    piep = """      <a href="/blog/">Guías</a>
      <a href="/calculadora-reparar-o-cambiar.html">Calculadora reparar o cambiar</a>
      <a href="/sobre-nosotros.html">Sobre nosotros</a>
      <a href="/contacto.html">Contacto</a>
      <a href="/aviso-legal.html">Aviso Legal</a>
      <a href="/privacidad.html">Política de Privacidad</a>
      <a href="/cookies.html">Política de Cookies</a>"""

    texto = reemplazar_bloque(texto, "HEAD", head)
    texto = reemplazar_bloque(texto, "NAV", navh)
    texto = reemplazar_bloque(texto, "GUIAS-COCHE", lista_coche)
    texto = reemplazar_bloque(texto, "SECCION", seccion)
    texto = reemplazar_bloque(texto, "FOOTER", piep)
    with open(ruta, "w", encoding="utf-8", newline="\n") as f:
        f.write(texto)


# ---------------------------------------------------------------------------
# Ficheros de descubrimiento
# ---------------------------------------------------------------------------

def generar_sitemap(pubs, paginas):
    ultima = max(a["actualizado"] for a in pubs)
    entradas = [("/", ultima, "/assets/img/portada.jpg"), ("/blog/", ultima, None)]
    for c in ORDEN_CATEGORIAS:
        lista = [a for a in pubs if a["categoria"] == c]
        if lista:
            entradas.append(("/blog/%s/" % c, max(a["actualizado"] for a in lista), None))
    for a in pubs:
        entradas.append((a["url"], a["actualizado"], a["imagen"]))
    for m in paginas:
        if m.get("indexar") != "no":
            entradas.append((m["url"], m.get("actualizado") or ultima, None))
    xml = []
    for u, lm, img in entradas:
        im = "\n    <image:image><image:loc>%s%s</image:loc></image:image>" % (SITIO, img) if img else ""
        xml.append("  <url>\n    <loc>%s%s</loc>\n    <lastmod>%s</lastmod>%s\n  </url>" % (SITIO, u, lm, im))
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'
            + "\n".join(xml) + "\n</urlset>\n")


def generar_feed(pubs):
    recientes = sorted(pubs, key=lambda a: (a["fecha"], a["slug"]), reverse=True)[:30]
    items = []
    for a in recientes:
        ruta_img = os.path.join(RAIZ, a["imagen"].lstrip("/"))
        tam = os.path.getsize(ruta_img) if os.path.isfile(ruta_img) else 0
        tipo = "image/jpeg" if a["imagen"].endswith(".jpg") else "image/png"
        items.append(T("""  <item>
    <title>{{t}}</title>
    <link>{{u}}</link>
    <guid isPermaLink="true">{{u}}</guid>
    <pubDate>{{d}}</pubDate>
    <category>{{c}}</category>
    <description>{{r}}</description>
    <enclosure url="{{img}}" length="{{tam}}" type="{{tipo}}"/>
  </item>""", t=esc(a["titulo"]), u=SITIO + a["url"], d=fecha_rfc822(a["fecha"]), c=esc(CATEGORIAS[a["categoria"]]["nombre"]),
                       r=esc(a["resumen"]), img=SITIO + a["imagen"], tam=tam, tipo=tipo))
    return T("""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>{{marca}} — guías para reparar, cambiar o vender</title>
  <link>{{sitio}}/blog/</link>
  <atom:link href="{{sitio}}/feed.xml" rel="self" type="application/rss+xml"/>
  <description>Averías del coche y de la casa: síntomas, precios en España y cuándo compensa reparar, cambiar o vender.</description>
  <language>es-es</language>
  <lastBuildDate>{{d}}</lastBuildDate>
{{items}}
</channel>
</rss>
""", marca=esc(MARCA), sitio=SITIO, d=fecha_rfc822(recientes[0]["fecha"]), items="\n".join(items))


def generar_llms(pubs):
    lineas = ["# %s" % MARCA, "",
              "> Guías en español para decidir si reparar, cambiar o vender coches, electrodomésticos, aparatos de tecnología y elementos de la casa. Incluye precios orientativos de reparación en España y dos calculadoras gratuitas.", "",
              "## Herramientas", "",
              "- [Calculadora: ¿reparo o vendo mi coche?](%s/): compara el coste de la reparación con el valor de mercado estimado del coche." % SITIO,
              "- [Calculadora: ¿reparar o cambiar?](%s/calculadora-reparar-o-cambiar.html): para electrodomésticos y tecnología, según edad, vida útil y presupuesto." % SITIO, ""]
    for c in ORDEN_CATEGORIAS:
        lista = [a for a in pubs if a["categoria"] == c]
        if not lista:
            continue
        lineas += ["## %s" % CATEGORIAS[c]["nombre"], ""]
        lineas += ["- [%s](%s%s): %s" % (a["titulo"], SITIO, a["url"], a["resumen"]) for a in lista]
        lineas.append("")
    return "\n".join(lineas)


def generar_robots():
    return """User-agent: Mediapartners-Google
Disallow:

User-agent: *
Allow: /
Disallow: /buscar.html

Sitemap: %s/sitemap.xml
""" % SITIO


# ---------------------------------------------------------------------------
# Verificacion del resultado
# ---------------------------------------------------------------------------

def verificar(rutas_html):
    errores = []
    titulos = {}
    for ruta in rutas_html:
        with open(ruta, encoding="utf-8") as f:
            h = f.read()
        rel = os.path.relpath(ruta, RAIZ).replace("\\", "/")
        for destino in re.findall(r'(?:href|src)="(/[^"#?]*)', h):
            if destino.startswith("//"):
                continue
            objetivo = destino.lstrip("/")
            if objetivo == "" or objetivo.endswith("/"):
                objetivo += "index.html"
            if not os.path.exists(os.path.join(RAIZ, objetivo)):
                errores.append("%s -> enlace roto %s" % (rel, destino))
        for bloque in re.findall(r'<script type="application/ld\+json">\n(.*?)\n</script>', h, re.S):
            try:
                json.loads(bloque)
            except ValueError as e:
                errores.append("%s -> JSON-LD inválido: %s" % (rel, e))
        t = re.search(r"<title>(.*?)</title>", h, re.S)
        if t and '"noindex' not in h[:4000]:
            titulos.setdefault(t.group(1), []).append(rel)
        if len(re.findall(r"<h1[\s>]", h)) != 1:
            errores.append("%s -> tiene %d H1" % (rel, len(re.findall(r"<h1[\s>]", h))))
    for t, rs in titulos.items():
        if len(rs) > 1:
            errores.append("Título duplicado '%s' en %s" % (t, ", ".join(rs)))
    return errores


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    todos = [leer_articulo(os.path.join(DIR_ARTICULOS, n)) for n in sorted(os.listdir(DIR_ARTICULOS)) if n.endswith(".md")]
    slugs = [a["slug"] for a in todos]
    if len(slugs) != len(set(slugs)):
        raise SystemExit("Hay slugs duplicados")

    pubs = sorted([a for a in todos if a["publicado"]],
                  key=lambda a: (ORDEN_CATEGORIAS.index(a["categoria"]), a["fecha"], a["slug"]))
    ESTADO["todas"] = {a["url"] for a in todos}
    ESTADO["publicadas"] = {a["url"] for a in pubs}

    faltan = [u for u in URLS_PROTEGIDAS if u not in ESTADO["publicadas"]]
    if faltan:
        raise SystemExit("ERROR: desaparecerían URLs ya indexadas: %s" % ", ".join(faltan))

    # SVG fuente para todos (tambien los programados, asi su JPG ya existe al publicarse)
    os.makedirs(DIR_SVG, exist_ok=True)
    for a in todos:
        with open(os.path.join(DIR_SVG, a["slug"] + ".svg"), "w", encoding="utf-8") as f:
            f.write(svg_hero(a.get("hero") or a["titulo"], a["categoria"], a["icono"]))
    with open(os.path.join(DIR_SVG, "calculadora-reparar-o-cambiar.svg"), "w", encoding="utf-8") as f:
        f.write(svg_hero("¿Lo reparo o compro uno nuevo?", "electrodomesticos", "calculadora", etiqueta="Calculadora gratuita"))
    with open(os.path.join(DIR_SVG, "portada.svg"), "w", encoding="utf-8") as f:
        f.write(svg_hero("¿Reparo o vendo mi coche?", "coches", "coche", color="#0f2341", etiqueta="Calculadora gratuita"))
    for a in todos:
        a["imagen"] = url_imagen(a["slug"])

    # /blog/ se regenera entero desde las fuentes
    dir_blog = os.path.join(RAIZ, "blog")
    if os.path.isdir(dir_blog):
        shutil.rmtree(dir_blog)
    if os.path.isdir(os.path.join(RAIZ, "guias")):
        shutil.rmtree(os.path.join(RAIZ, "guias"))

    escritos = []

    def w(ruta, contenido):
        escribir(ruta, contenido)
        escritos.append(os.path.join(RAIZ, ruta.lstrip("/")))

    for a in pubs:
        w(a["url"], render_articulo(a, pubs))
    w("/blog/index.html", render_hub(pubs))
    for c in ORDEN_CATEGORIAS:
        if any(a["categoria"] == c for a in pubs):
            w("/blog/%s/index.html" % c, render_categoria(c, pubs))

    paginas = []
    for n in sorted(os.listdir(DIR_PAGINAS)):
        if n.endswith(".md"):
            meta, cuerpo = leer_md(os.path.join(DIR_PAGINAS, n))
            if meta.get("url") == "/calculadora-reparar-o-cambiar.html":
                meta["imagen"] = url_imagen("calculadora-reparar-o-cambiar")
            paginas.append(meta)
            w(meta["url"], render_pagina(meta, cuerpo))

    actualizar_portada(pubs)
    escritos.append(os.path.join(RAIZ, "index.html"))

    escribir("/sitemap.xml", generar_sitemap(pubs, paginas))
    escribir("/feed.xml", generar_feed(pubs))
    escribir("/llms.txt", generar_llms(pubs))
    escribir("/robots.txt", generar_robots())
    escribir("/%s.txt" % INDEXNOW_KEY, INDEXNOW_KEY)
    escribir("/assets/busqueda.json", json.dumps(
        [{"t": a["titulo"], "u": a["url"], "r": a["resumen"], "c": CATEGORIAS[a["categoria"]]["nombre"],
          "k": " ".join(a["tags"]), "i": a["imagen"]} for a in pubs], ensure_ascii=False))

    errores = ESTADO["errores"] + verificar(escritos)

    programadas = sorted([a for a in todos if not a["publicado"]], key=lambda a: a["fecha"])
    print("Fecha del build: %s" % HOY.isoformat())
    print("Publicados %d artículos (%d programados para más adelante)." % (len(pubs), len(programadas)))
    for c in ORDEN_CATEGORIAS:
        print("  %-18s %2d publicados / %2d en total" % (c, len([a for a in pubs if a["categoria"] == c]),
                                                       len([a for a in todos if a["categoria"] == c])))
    print("Palabras publicadas: %s" % format(sum(a["palabras"] for a in pubs), ",d").replace(",", "."))
    if programadas:
        print("Próximo programado: %s (%s); último: %s" % (programadas[0]["fecha"], programadas[0]["slug"], programadas[-1]["fecha"]))
    if CONTACTO_EMAIL == "contacto@gmail.com":
        print("AVISO: CONTACTO_EMAIL sigue siendo contacto@gmail.com, que no es una dirección propia.")
    for av in sorted(set(ESTADO["avisos"])):
        print("AVISO: " + av)
    if errores:
        print("\n%d ERRORES:" % len(errores))
        for e in errores:
            print("  - " + e)
        sys.exit(1)
    print("Verificación: 0 enlaces rotos, JSON-LD válido, un H1 por página, sin títulos duplicados.")


if __name__ == "__main__":
    main()
