---
titulo: Política de cookies
titulo_seo: Política de cookies · ¿Reparo o Vendo?
descripcion: Qué cookies utiliza repararovender.es, para qué sirven, cuánto duran y cómo aceptarlas, rechazarlas o retirar el consentimiento.
url: /cookies.html
actualizado: 2026-10-07
---

Este sitio web utiliza cookies propias y de terceros. A continuación te explicamos qué son, para qué las usamos y cómo puedes gestionarlas.

## ¿Qué son las cookies?

Las cookies son pequeños archivos de texto que se almacenan en tu navegador cuando visitas una web. Permiten recordar tus preferencias y recoger información sobre cómo usas el sitio.

## Cookies que utilizamos

| Cookie | Tipo | Finalidad | Duración |
| --- | --- | --- | --- |
| cookies-accepted / cookies-rejected | Propia (almacenamiento local) | Recordar si has aceptado o rechazado el aviso de cookies | Hasta que la borres |
| _ga, _ga_* (Google Analytics) | Terceros, analítica | Contar visitas y saber qué páginas se consultan, de forma agregada | Hasta 2 años |
| __gads, __gpi, IDE y similares (Google AdSense) | Terceros, publicidad | Mostrar anuncios, limitar su repetición y, si lo aceptas, personalizarlos | Hasta 13 meses |

Las cookies de analítica y de publicidad **solo se instalan si las aceptas**. Si las rechazas, el sitio funciona igual y Google recibe únicamente señales sin cookies, sin identificarte, conforme al modo de consentimiento de Google.

## Cookies de terceros

Google AdSense y Google Analytics son servicios de Google LLC. Las cookies de AdSense pueden utilizarse para mostrar anuncios basados en tus visitas anteriores a este y otros sitios web. Puedes consultar la política de privacidad de Google en policies.google.com y gestionar tus preferencias publicitarias en adssettings.google.com.

## Cómo gestionar o retirar el consentimiento

Puedes retirar o cambiar tu consentimiento en cualquier momento con el botón de abajo: se borrará tu elección y volverá a aparecer el aviso. También puedes configurar tu navegador para bloquear o eliminar cookies, aunque esto puede afectar al funcionamiento de algunas partes del sitio.

<p><button type="button" class="boton boton-fantasma" id="btn-retirar">Retirar o cambiar el consentimiento de cookies</button></p>
<script>
document.getElementById('btn-retirar').addEventListener('click', function () {
  try { localStorage.removeItem('cookies-accepted'); localStorage.removeItem('cookies-rejected'); } catch (e) {}
  location.reload();
});
</script>
