# Cómo funciona la web por dentro

Todo el blog se genera desde esta carpeta. GitHub Pages no publica `_fuente/` (Jekyll ignora las carpetas que empiezan por `_`), así que aquí puedes tener borradores y scripts sin que se vean.

## Añadir un artículo

1. Copia cualquier fichero de `_fuente/articulos/` y renómbralo con la URL que quieras: `mi-nueva-guia.md` se publicará en `/blog/mi-nueva-guia.html`.
2. Cambia el frontmatter (lo que va entre los `---`):

| Campo | Para qué sirve |
| --- | --- |
| `titulo` | Titular del artículo (H1) |
| `titulo_seo` | Título para Google, máximo unos 62 caracteres |
| `categoria` | `coches`, `electrodomesticos`, `tecnologia`, `hogar` o `vender` |
| `resumen` | Entradilla y texto de las tarjetas |
| `descripcion` | Meta descripción para Google, 120-158 caracteres |
| `fecha` | Día de publicación. **Si es futura, el artículo no sale hasta ese día** |
| `actualizado` | Fecha de la última revisión |
| `icono` | Icono de la imagen (ver la lista `ICONOS` en `build.py`) |
| `hero` | Texto corto para la imagen de cabecera |
| `tags` | Etiquetas, sirven para enlazar artículos relacionados |
| `destacado: si` | Aparece en "Las más consultadas" |

3. Escribe el texto en Markdown. Extras disponibles:
   - `:::claves Lo importante en 30 segundos` … `:::` → caja de puntos clave (ponla la primera).
   - `:::aviso Título`, `:::truco Título`, `:::dato Título`, `:::precio Título` → recuadros de color.
   - Una sección `## Preguntas frecuentes` con preguntas en `###` genera el schema FAQ automáticamente.
   - Enlaza a otros artículos con `[texto](/blog/slug.html)`. Si el destino está programado, el enlace aparece solo cuando se publique.

4. Genera y revisa:

```
python _fuente/build.py
```

El build se para con error si hay un enlace roto, un JSON-LD inválido, un título duplicado o si desaparecería una URL ya indexada.

## Imágenes

`build.py` crea la imagen de cada artículo en SVG; para convertirlas a JPG (lo que usan las redes sociales) hace falta Playwright:

```
python _fuente/imagenes.py
python _fuente/build.py
```

Si tienes una foto real para un artículo, la mejor opción para el clic en redes, guárdala como `assets/img/<slug>.jpg` (1200×630) y no vuelvas a ejecutar `imagenes.py` sobre ese slug, o bórrale su SVG de `_fuente/.cache/svg/` antes.

## Publicación automática

La acción `.github/workflows/publicar-programados.yml` se ejecuta cada mañana: reconstruye la web con la fecha de Madrid y, si toca publicar algún artículo, hace commit y push, y avisa a Bing y compañía por IndexNow.

**Importante:** como la acción hace commits en `main`, antes de tocar nada en local haz siempre:

```
git pull
```

## Configuración

Al principio de `build.py`:

- `CONTACTO_EMAIL`: el correo que aparece en las páginas legales y de contacto.
- `GA_ID`: Google Analytics 4.
- `ADSENSE_SLOTS`: si creas bloques de anuncio manuales en AdSense, pon aquí sus IDs. Vacío = solo Auto Ads.
