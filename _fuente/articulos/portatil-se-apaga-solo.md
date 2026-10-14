---
titulo: El portátil se apaga solo: causas y cómo solucionarlo
titulo_seo: El portátil se apaga solo: 7 causas y soluciones paso a paso
categoria: tecnologia
resumen: Se apaga de golpe, sin aviso ni pantalla azul, normalmente cuando lleva un rato encendido o cuando le exiges algo. En portátiles de más de tres años la causa número uno es el polvo, y se arregla con un destornillador.
descripcion: Por qué el portátil se apaga solo de repente: sobrecalentamiento, polvo, pasta térmica, batería o fuente. Diagnóstico paso a paso y precios de reparación.
fecha: 2026-10-07
actualizado: 2026-10-07
icono: portatil
hero: El portátil se apaga solo
alt_imagen: Ilustración de un portátil apagándose
tags: [portatil, sobrecalentamiento, limpieza]
---

:::claves Lo importante en 30 segundos
- Un apagado de golpe, sin aviso, casi siempre es sobrecalentamiento por polvo en el radiador.
- Limpieza interna con pasta térmica nueva: 50-90 € en taller, y resuelve la mayoría de los casos.
- Si solo se apaga con batería, la batería está agotada aunque marque porcentaje.
:::

Hay una diferencia importante que condiciona todo el diagnóstico: **¿se apaga de golpe, como si le quitaras el enchufe, o se apaga con pantalla azul o un mensaje?**

- **De golpe, sin aviso:** es hardware. Casi siempre temperatura o alimentación.
- **Con pantalla azul o error:** es software o un componente concreto fallando (RAM, disco, controlador).

Esta guía va del primer caso, que es el más común.

## 1. Sobrecalentamiento: la causa número uno

Si tu portátil tiene más de dos o tres años y nunca se ha limpiado, esto es lo que pasa con una probabilidad altísima.

El aire entra por las rejillas inferiores, pasa por un radiador y sale por un lateral. Con el tiempo, entre las láminas del radiador se forma **una manta de polvo compacta**, literalmente un fieltro. El ventilador sigue girando (y suena a avión) pero el aire ya no pasa. Cuando el procesador llega a unos 95-100 °C, el portátil se apaga de inmediato para no destruirse.

Las señales que lo confirman:

- Se apaga **cuando le exiges**: juegos, vídeo, videollamadas, muchas pestañas.
- Antes de apagarse, **el ventilador suena a plena potencia**.
- La zona del teclado o la base **quema**.
- Funciona bien los primeros 10-20 minutos y luego falla.
- **Sale poco aire por la rejilla de salida** aunque el ventilador ruja.

Confírmalo con un monitor de temperaturas (HWMonitor o HWiNFO en Windows, Macs Fan Control en Mac). Si ves picos de 95-100 °C justo antes del apagado, caso cerrado.

### Cómo arreglarlo

**Lo que no funciona:** soplar aire comprimido por las rejillas sin abrir. Compacta el polvo aún más adentro. Puede dar un alivio temporal, pero no resuelve.

**Lo que sí funciona:** abrir la tapa inferior, quitar el ventilador y **retirar a mano la manta de polvo del radiador**. Es sorprendentemente fácil en la mayoría de los portátiles: una docena de tornillos y, muchas veces, sale una lámina de polvo entera.

- Hacerlo tú: 0 € y una hora.
- Limpieza en taller: **30-60 €**.

### La pasta térmica

Si el portátil tiene más de 4-5 años, la pasta térmica entre el procesador y el disipador se ha secado y ya no transmite el calor. Limpiar el polvo ayudará, pero cambiar la pasta es lo que de verdad lo arregla.

- Material: 8-15 € un tubo (te sobrará para varias veces).
- En taller, limpieza + pasta: **50-90 €**.

Es la reparación con mejor relación coste-beneficio que existe en un portátil: por 60 € recuperas un equipo que parecía muerto.

:::truco La prueba de la superficie
Si tu portátil se apaga sobre la cama, el sofá o un cojín pero aguanta sobre la mesa, no tienes una avería: las rejillas de entrada de aire están en la base y la tela las tapa. Usa una base rígida o una peana. Es gratis y resuelve muchísimos casos.
:::

## 2. La batería está agotada o hinchada

Si se apaga **solo cuando va con batería** y aguanta perfectamente enchufado, la batería ya no entrega corriente suficiente. Puede marcar un 60 % y apagarse igualmente: el porcentaje es una estimación que una batería vieja calcula mal.

- Batería nueva: **50-120 €** según modelo.

Y revisa si está **hinchada**: ¿el portátil cojea sobre la mesa?, ¿el touchpad va raro o hace clic solo?, ¿la tapa inferior está abombada? Una batería hinchada empuja el touchpad desde abajo. Es riesgo de incendio y hay que cambiarla ya.

## 3. El cargador o el conector de carga

Si se apaga **enchufado** y la batería estaba baja, puede que no esté cargando de verdad.

- Comprueba que el **LED de carga** se enciende y que el sistema dice "cargando".
- Mueve el cable cerca del conector: si el LED parpadea, hay un cable roto por dentro.
- Mira el **conector del portátil**: si está flojo o se mueve, la soldadura puede estar fracturada (reparación de 60-130 €).
- Si usas un cargador USB-C genérico, comprueba que da **suficientes vatios**. Un cargador de 45 W en un portátil que pide 90 W no mantiene la carga bajo exigencia.

## 4. La RAM

Un módulo de memoria mal asentado o defectuoso provoca apagados y reinicios aparentemente aleatorios.

Prueba gratuita: ejecuta **Windows Memory Diagnostic** (escribe "memoria" en el menú inicio) o MemTest86 desde un USB. Si da errores, prueba a quitar y volver a poner los módulos, o a funcionar con uno solo para identificar cuál falla.

- Módulo nuevo: **25-70 €**.

## 5. La fuente de alimentación o la placa

Si has descartado todo lo anterior, puede ser un fallo de alimentación en la propia placa base.

- Reparación de placa: **120-300 €**, y no siempre con garantías.

Aquí es donde hay que parar y hacer cuentas.

## 6. Software: drivers y actualizaciones

Menos frecuente en apagados súbitos, pero posible:

- Drivers de tarjeta gráfica corruptos: desinstálalos con DDU y reinstala los oficiales.
- Windows: desactiva el **inicio rápido** (Panel de control → Opciones de energía → Comportamiento de los botones). Provoca apagados y arranques erráticos en algunos equipos.
- Comprueba el visor de eventos (Kernel-Power, evento 41) para ver si el sistema registró algo.

## 7. El botón de encendido o un sensor

Raro, pero existe: un botón de encendido con el muelle vencido puede hacer "doble pulsación". Si el portátil se apaga al moverlo o al apoyar la mano en cierta zona, sospecha de esto.

## ¿Compensa repararlo?

Un portátil nuevo de gama media cuesta **500-900 €** y la vida útil razonable está entre **6 y 8 años**.

| Reparación | Precio | ¿Compensa? |
| --- | --- | --- |
| Limpieza + pasta térmica | 50-90 € | **Casi siempre.** La mejor inversión posible |
| Batería | 50-120 € | Sí, hasta los 6-7 años |
| Cargador | 25-60 € | Siempre |
| Conector de carga | 60-130 € | Sí, si el portátil es decente |
| RAM | 25-70 € | Siempre |
| Placa base | 120-300 € | Solo en portátiles de gama alta y menos de 4 años |

La conclusión práctica: **antes de dar por muerto un portátil que se apaga solo, gasta 60 € en una limpieza con cambio de pasta térmica**. Resuelve una mayoría abrumadora de los casos y, si no lo resuelve, al menos has descartado la causa más probable por poco dinero.

Si además va lento, mira [portátil lento: 8 arreglos sin gastar](/blog/portatil-lento-soluciones.html) y [si merece la pena cambiar el disco duro por un SSD](/blog/cambiar-disco-duro-por-ssd.html).

## Preguntas frecuentes

### ¿Por qué se apaga el portátil de repente sin avisar?

Un apagado instantáneo, sin pantalla azul ni mensaje, es casi siempre hardware, y la causa número uno es el sobrecalentamiento: el polvo acumulado en el radiador impide que salga el aire y, al llegar a 95-100 °C, el equipo se corta para protegerse. Las otras causas frecuentes son una batería agotada, un cargador que no entrega potencia suficiente o un módulo de RAM defectuoso.

### ¿Cómo sé si mi portátil se apaga por calor?

Instala un monitor de temperaturas como HWMonitor o HWiNFO y mira los grados justo antes de que se apague: si ves picos de 95-100 °C, está confirmado. Las otras señales son que el ventilador suena a plena potencia antes del apagado, que la base quema, que sale poco aire por la rejilla de salida y que solo falla cuando le exiges trabajo.

### ¿Sirve soplar aire comprimido en las rejillas del portátil?

Poco, y a veces es contraproducente, porque compacta el polvo aún más contra el radiador en lugar de sacarlo. Lo que funciona es abrir la tapa inferior, desmontar el ventilador y retirar a mano la capa de polvo acumulada entre las láminas del radiador. En la mayoría de portátiles sale una lámina de polvo entera.

### ¿Cuánto cuesta limpiar un portátil por dentro?

Entre 30 y 60 € solo la limpieza, y entre 50 y 90 € si incluye cambiar la pasta térmica, que es lo recomendable en equipos de más de cuatro años. Es la reparación con mejor relación coste-beneficio de un portátil: por ese dinero se recupera un equipo que parecía inservible.

### ¿Es peligrosa una batería de portátil hinchada?

Sí, tiene riesgo de incendio y hay que sustituirla cuanto antes. Se detecta porque el portátil cojea sobre la mesa, porque la tapa inferior está abombada o porque el touchpad hace clics solo o deja de responder, al estar empujado desde abajo por la batería. No la perfores ni la presiones.
