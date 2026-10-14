---
titulo: Portátil lento: 8 arreglos que funcionan sin gastar dinero
titulo_seo: Portátil lento: 8 soluciones reales (y la que más se nota)
categoria: tecnologia
resumen: Tarda tres minutos en arrancar y el ventilador ruge con dos pestañas abiertas. Siete de estas ocho soluciones son gratis, y la octava cuesta 40 € y es la que de verdad transforma un portátil viejo.
descripcion: Cómo acelerar un portátil lento sin comprar uno nuevo: arranque, disco, RAM, temperatura y limpieza. Ocho soluciones ordenadas por lo que más se nota.
fecha: 2026-10-07
actualizado: 2026-10-07
icono: portatil
hero: Portátil lento
alt_imagen: Ilustración de un portátil funcionando con lentitud
tags: [portatil, rendimiento, ssd]
---

:::claves Lo importante en 30 segundos
- Si tiene disco duro mecánico, poner un SSD (45-75 €) es lo que más se nota con diferencia.
- Vaciar el arranque y dejar un 15-20 % del disco libre es gratis y se nota.
- Con 4 GB de RAM, ampliar a 8 GB cuesta 25-70 € y cambia el uso diario.
:::

Un portátil de hace seis años no es lento porque su procesador sea malo. Un i5 de 2019 sigue siendo perfectamente capaz de mover un navegador, una hoja de cálculo y una videollamada. Es lento por otras razones, y casi todas tienen arreglo.

Van ordenadas por **cuánto se nota el cambio**, no por dificultad.

## 1. Cambia el disco duro por un SSD (el único que paga)

Si tu portátil todavía lleva un **disco duro mecánico** (HDD), esta es la única cosa de la lista que importa de verdad. No es una mejora: es la diferencia entre un equipo inservible y uno perfectamente usable.

Un HDD de portátil lee a unos 80-120 MB/s. Un SSD SATA, a 500 MB/s. Y en tiempos de acceso aleatorio —lo que de verdad nota el usuario— la diferencia es de **cien veces**.

Cómo saber qué tienes: en Windows, abre el Administrador de tareas → pestaña Rendimiento → Disco. Pondrá HDD o SSD.

- SSD SATA de 1 TB: **45-75 €**.
- Instalación en taller con clonado: **40-80 €**.

Tienes el detalle completo en [¿merece la pena cambiar el disco duro por un SSD?](/blog/cambiar-disco-duro-por-ssd.html). Si tu portátil tiene HDD, deja de leer, hazlo, y vuelve.

## 2. Limpia el polvo y cambia la pasta térmica

Un portátil que se calienta **reduce su propia velocidad** (lo llaman *throttling*) para no destruirse. Un equipo con el radiador atascado de polvo puede estar funcionando al 40 % de su capacidad de forma permanente.

Señal: el ventilador ruge constantemente y la base quema, pero sale poco aire por la rejilla.

- Hacerlo tú: 0 € y una hora.
- En taller con pasta térmica nueva: **50-90 €**.

Lo tienes explicado en [el portátil se apaga solo](/blog/portatil-se-apaga-solo.html), que trata la versión extrema del mismo problema.

## 3. Vacía el arranque

Cada programa que se abre con Windows retrasa el arranque y se queda consumiendo memoria todo el día. Después de unos años, un portátil típico tiene veinte cosas arrancando.

**Ctrl + Shift + Esc** → pestaña **Inicio**. Verás cada programa y su "impacto de inicio". Desactiva todo lo que no necesites nada más encender:

- Actualizadores (Adobe, Java, impresoras, fabricantes)
- Clientes de juegos (Steam, Epic, Battle.net)
- Spotify, Discord, Teams, Zoom
- Aplicaciones de nube que no uses a diario
- Software del fabricante que no hace nada útil

Desactivar el arranque **no desinstala nada**: el programa sigue ahí y se abre cuando lo abras tú.

## 4. Deja espacio libre en el disco

Igual que en los móviles: un disco al 97 % ralentiza todo el sistema, y en Windows además impide que funcione bien el archivo de paginación.

- Ejecuta **Liberador de espacio** y marca "Archivos de Windows Update" y "Instalaciones anteriores de Windows" (puede liberar 20-30 GB).
- Revisa la carpeta de Descargas.
- Desinstala programas que no uses: Panel de control → Programas.
- Vacía la papelera (sí, de verdad).

Objetivo: **al menos un 15-20 % libre**.

## 5. Mira si una sola cosa se está comiendo el equipo

Abre el Administrador de tareas y ordena por CPU, luego por Memoria, luego por Disco. Busca lo que esté al 100 % de forma sostenida.

Culpables habituales:

| Lo que ves | Qué suele ser |
| --- | --- |
| Disco al 100 % constante | HDD mecánico, o Windows Update indexando |
| Un antivirus de terceros arriba | Quítalo; Defender basta en la mayoría de casos |
| Navegador con 1,5 GB | Demasiadas pestañas y extensiones |
| "Antimalware Service Executable" | Análisis programado de Defender; se puede reprogramar |
| Un proceso que no reconoces | Búscalo antes de matarlo |

El navegador merece mención aparte: **cada pestaña abierta es un proceso con su propia memoria**. Si tienes 4 GB de RAM y 30 pestañas, el problema no es el portátil.

## 6. Quita extensiones del navegador

Para mucha gente, "el portátil va lento" significa en realidad "el navegador va lento". Entra en la gestión de extensiones y quita todo lo que no uses cada día. Las barras de herramientas, los gestores de cupones y los "optimizadores" son especialmente dañinos.

## 7. Añade RAM si tienes 4 GB

Con 4 GB de memoria, Windows 11 y un navegador ya están al límite y el sistema empieza a usar el disco como memoria, que es lentísimo.

- Pasar de 4 a 8 GB (o de 8 a 16): **25-70 €**.
- Comprueba cuánta tienes y si hay ranura libre: Administrador de tareas → Rendimiento → Memoria. Verás "Ranuras usadas: 1 de 2".

Importante: hay que comprar el **tipo correcto** (DDR3, DDR4, DDR5) y a ser posible igual que la que ya tienes. Busca tu modelo exacto o usa el configurador de la web de Crucial o Kingston, que lo detectan solo.

## 8. Reinstala Windows (la opción nuclear que sí funciona)

Si el portátil lleva seis años con el mismo sistema, acumula capas de software, drivers viejos y restos de programas desinstalados. Una instalación limpia de Windows deja un equipo **notablemente** más rápido.

Windows 11 lo tiene integrado: Configuración → Sistema → Recuperación → **Restablecer este equipo**, con la opción de conservar archivos personales.

:::aviso Antes de reinstalar
Copia tus archivos a un disco externo o a la nube (y comprueba que la copia está bien **abriendo** algunos archivos, no solo mirando que existen). Apunta las licencias de los programas que uses y comprueba que tienes a mano las contraseñas. Y descarga antes los drivers de la web del fabricante de tu modelo, sobre todo el de red: si reinstalas y te quedas sin wifi, estás atrapado.
:::

## Lo que no funciona

Por ahorrarte tiempo y dinero:

- **Los programas "aceleradores" y limpiadores de registro.** No hacen nada medible y muchos son software no deseado.
- **Desfragmentar un SSD.** No hace falta y desgasta la unidad. Windows ya lo gestiona.
- **Los antivirus de pago** frente a Windows Defender, si solo navegas con cabeza.
- **Aumentar la memoria virtual** manualmente. Windows lo gestiona mejor que tú.

## ¿Y si nada funciona?

Un portátil es razonable sustituirlo cuando:

- Tiene **menos de 8 GB de RAM sin posibilidad de ampliar** (soldada).
- Su procesador no soporta Windows 11 y Windows 10 ya no recibe actualizaciones de seguridad (desde octubre de 2025).
- La bisagra, el teclado o la pantalla están rotos además de todo lo demás.

Fuera de eso, **un portátil con SSD, 8 GB de RAM y limpieza interna aguanta tranquilamente tres o cuatro años más** haciendo ofimática, navegación y videollamadas. La inversión total ronda los 100-150 €, frente a los 600-900 € de uno nuevo.

Si decides cambiarlo, el viejo con SSD puesto vale bastante más en segunda mano: mira [cómo poner precio a algo de segunda mano](/blog/poner-precio-segunda-mano.html).

## Preguntas frecuentes

### ¿Qué es lo que más acelera un portátil lento?

Cambiar el disco duro mecánico por un SSD, sin ninguna duda. Es la única mejora que transforma la sensación de uso de un equipo antiguo: los tiempos de acceso mejoran unas cien veces y el arranque pasa de minutos a segundos. Cuesta entre 45 y 75 € el disco, más 40-80 € si lo instala un taller con clonado del sistema.

### ¿Por qué mi portátil tarda tanto en arrancar?

Por dos razones que suelen darse juntas: tener un disco duro mecánico en lugar de un SSD, y tener demasiados programas configurados para abrirse con el sistema. Lo segundo se arregla gratis en el Administrador de tareas, pestaña Inicio, desactivando actualizadores, clientes de juegos y aplicaciones de nube que no necesitas nada más encender.

### ¿Cuánta RAM necesita un portátil hoy?

8 GB es el mínimo razonable para navegar y hacer ofimática con comodidad, y 16 GB si trabajas con muchas pestañas, edición o máquinas virtuales. Con 4 GB, Windows 11 y un navegador ya saturan la memoria y el sistema empieza a usar el disco como sustituto, lo que ralentiza todo enormemente. Ampliar de 4 a 8 GB cuesta entre 25 y 70 €.

### ¿Sirven los programas que prometen acelerar el PC?

No de forma medible, y bastantes son software no deseado que empeora el problema que dicen resolver. Lo mismo vale para los limpiadores de registro. Lo que sí funciona es vaciar el arranque, liberar espacio en disco, quitar extensiones del navegador, limpiar el polvo interno y, sobre todo, poner un SSD.

### ¿Merece la pena arreglar un portátil de seis años?

Normalmente sí, si el gasto se queda en torno a 100-150 € entre SSD, RAM y limpieza con pasta térmica. Eso devuelve a un equipo de seis años tres o cuatro años más de uso cómodo para ofimática y navegación, frente a los 600-900 € de uno nuevo. Solo deja de compensar si la RAM está soldada en 4 GB o si el procesador no admite un sistema con soporte de seguridad.
