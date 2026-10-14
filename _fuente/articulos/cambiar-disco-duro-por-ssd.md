---
titulo: ¿Merece la pena cambiar el disco duro por un SSD?
titulo_seo: ¿Merece la pena cambiar el disco duro por un SSD? Precios y guía
categoria: tecnologia
resumen: Es la mejora con más impacto por euro que existe en informática, y no está ni cerca. Por 50 € un ordenador de ocho años que tardaba tres minutos en arrancar pasa a estar listo en quince segundos.
descripcion: Si merece la pena poner un SSD en un ordenador antiguo, qué tipo elegir (SATA, NVMe), cuánto cuesta, cómo clonar el sistema y qué ganancia real esperar.
fecha: 2026-10-07
actualizado: 2026-10-07
icono: disco
hero: Cambiar el disco por un SSD
alt_imagen: Ilustración de un disco duro y una unidad SSD
tags: [ssd, portatil, mejora]
---

:::claves Lo importante en 30 segundos
- Un SSD accede a los datos entre 50 y 100 veces más rápido que un disco duro mecánico.
- Un SSD de 1 TB cuesta 45-90 € y se puede clonar el sistema sin reinstalar nada.
- En uso doméstico la diferencia entre SATA y NVMe es pequeña; el salto grande es dejar el disco mecánico.
:::

La respuesta corta es sí, y con mucha diferencia sobre cualquier otra mejora. Pero conviene entender por qué, porque explica también los casos en los que no aplica.

## Por qué se nota tantísimo

Un disco duro mecánico tiene platos girando y un cabezal que se desplaza físicamente para buscar cada dato. Un SSD no tiene partes móviles: accede a cualquier posición de forma instantánea.

| | Disco duro (HDD) | SSD SATA | SSD NVMe |
| --- | --- | --- | --- |
| Lectura secuencial | 80-160 MB/s | 500-550 MB/s | 2.000-7.000 MB/s |
| Tiempo de acceso | 10-15 ms | 0,1 ms | 0,02 ms |
| Arranque de Windows | 60-180 s | 10-20 s | 8-15 s |
| Ruido | Sí | No | No |
| Resistencia a golpes | Baja | Alta | Alta |

Fíjate en la fila del **tiempo de acceso**: ahí está la clave. Un sistema operativo no lee un archivo enorme de golpe, lee **miles de archivos pequeños dispersos**. En eso, un HDD es entre cincuenta y cien veces más lento. Por eso la sensación de mejora es tan desproporcionada respecto a la cifra de MB/s.

:::dato La comparación que importa
Un ordenador de 2016 con SSD va a sentirse más rápido en el uso diario que un ordenador de 2024 con disco duro mecánico. No es exageración: el disco es el cuello de botella de casi todo lo que hace un sistema operativo.
:::

## ¿Cuál necesito? SATA o NVMe

Esta es la única decisión técnica real, y depende de lo que admita tu equipo.

**SSD SATA de 2,5 pulgadas.** Tiene el mismo formato que un disco duro de portátil y usa el mismo cable. **Funciona en prácticamente cualquier ordenador** de los últimos quince años. Es la opción segura.

**SSD NVMe (M.2).** Es una tarjeta pequeña que se enchufa directamente en la placa. Mucho más rápido en cifras, pero **solo sirve si tu equipo tiene ranura M.2 compatible con NVMe**. Ojo: algunas ranuras M.2 antiguas solo admiten SATA, no NVMe.

Cómo saber qué admites:

- Busca tu modelo exacto de portátil o placa base + "M.2 NVMe".
- O usa el configurador de Crucial o Kingston: detecta tu equipo y te dice exactamente qué encaja.
- En un sobremesa, abre y mira si hay una ranura M.2 en la placa.

**Para uso normal, la diferencia entre SATA y NVMe apenas se nota.** El salto grande es de HDD a SSD; de SATA a NVMe solo se aprecia copiando archivos muy grandes o en trabajo profesional de vídeo. Si tu equipo solo admite SATA, no te sientas limitado.

## Precios en España

| Capacidad | SSD SATA | SSD NVMe |
| --- | --- | --- |
| 500 GB | 30-45 € | 35-55 € |
| 1 TB | 45-75 € | 55-90 € |
| 2 TB | 90-140 € | 100-170 € |

Instalación y clonado en taller: **40-80 €**.

Sobre la capacidad: **no bajes de 500 GB**. La diferencia con 250 GB es de diez euros y te vas a quedar corto. El punto dulce ahora mismo es 1 TB.

Sobre la marca: compra de fabricantes conocidos (Samsung, Crucial, Kingston, WD, SanDisk). Los SSD muy baratos de marcas desconocidas usan memoria de peor calidad y controladores sin caché, y el rendimiento se desploma al llenarlos.

## Cómo hacerlo: clonar o instalar limpio

**Clonar** copia tu sistema tal cual al nuevo disco. Enciendes y todo está donde estaba.

- Necesitas un **adaptador USB a SATA** (8-15 €) para conectar el SSD mientras clonas.
- Software gratuito: Macrium Reflect Free, Clonezilla, o el que incluyen Samsung (Data Migration) y Crucial (Acronis).
- Requisito: los **datos usados** del disco viejo tienen que caber en el nuevo. Si tienes 700 GB usados y el SSD es de 500 GB, limpia antes.

**Instalación limpia** es reinstalar Windows desde cero en el SSD. Más trabajo, pero el resultado es aún mejor porque te deshaces de años de acumulación. Si tu equipo ya iba lento por software además de por disco, esta es la opción.

:::truco Aprovecha el disco viejo
No tires el HDD. En un portátil con hueco para dos unidades, déjalo como almacén de archivos. Si solo hay una bahía, cómprate una **caja USB para disco de 2,5"** (8-15 €) y conviértelo en un disco externo. Te sirve de copia de seguridad, que es justo lo que casi nadie tiene.
:::

## Después de instalarlo

Dos ajustes que importan:

- **Comprueba que TRIM está activo** (en Windows lo está por defecto). Abre una consola como administrador y escribe `fsutil behavior query DisableDeleteNotify`. Si devuelve 0, está activo.
- **No desfragmentes el SSD.** No sirve de nada y consume ciclos de escritura. Windows ya distingue el tipo de unidad y hace lo correcto solo; no instales herramientas de desfragmentación de terceros.
- **Deja un 10-15 % libre.** Los SSD necesitan espacio sin ocupar para gestionar la escritura. Uno lleno hasta arriba pierde rendimiento.

## ¿Cuánto duran?

Es la duda más repetida y la respuesta tranquiliza: un SSD doméstico actual tiene una resistencia de escritura (TBW) de entre 150 y 600 terabytes según capacidad. Un usuario normal escribe en torno a 10-30 GB al día. Eso da, tirando por lo bajo, **más de veinte años**.

En la práctica, el SSD sobrevivirá al ordenador. Lo que sí conviene saber: cuando un SSD falla, suele hacerlo de golpe y sin los ruidos de aviso de un disco mecánico. **Ten copia de seguridad**, igual que con cualquier disco.

## Cuándo NO compensa

Por honestidad, los casos en los que no lo haría:

- **El equipo ya tiene SSD.** Pasar de SATA a NVMe apenas se nota en uso doméstico.
- **El portátil tiene otros problemas serios**: pantalla rota, bisagra partida, 4 GB de RAM soldada. Suma todo antes de invertir.
- **El procesador es muy antiguo** (más de doce años) y no vas a poder instalar un sistema con soporte de seguridad.

Fuera de esos casos, es la mejor compra que puedes hacer para un ordenador. Mira también [portátil lento: 8 arreglos](/blog/portatil-lento-soluciones.html) para combinarlo con el resto.

## Preguntas frecuentes

### ¿Cuánto mejora un ordenador al poner un SSD?

Muchísimo en la sensación de uso: el arranque de Windows pasa de uno a tres minutos a diez o veinte segundos, y los programas abren casi al instante. La clave no es la velocidad de transferencia sino el tiempo de acceso, donde un SSD es entre cincuenta y cien veces más rápido que un disco mecánico, y eso es lo que hace un sistema operativo todo el rato.

### ¿Qué SSD compro, SATA o NVMe?

SATA si tu equipo no tiene ranura M.2 compatible con NVMe, que es el caso de muchos portátiles anteriores a 2016. Para uso doméstico la diferencia real entre ambos es pequeña: el salto grande es pasar de disco mecánico a SSD. Comprueba la compatibilidad con el configurador de Crucial o Kingston, que detectan tu modelo exacto.

### ¿Puedo poner un SSD sin reinstalar Windows?

Sí, clonando el disco actual al nuevo con un adaptador USB a SATA (8-15 €) y un programa gratuito como Macrium Reflect, Clonezilla o el que incluye el propio fabricante del SSD. El único requisito es que los datos realmente usados quepan en la capacidad del nuevo disco. Al terminar, el ordenador arranca exactamente igual que antes, pero mucho más rápido.

### ¿Cuánto dura un SSD?

Más que el ordenador en el que lo pongas. Los SSD domésticos actuales soportan entre 150 y 600 terabytes de escritura según capacidad, y un usuario normal escribe 10-30 GB al día, lo que da más de veinte años. Eso sí, cuando fallan suelen hacerlo de golpe y sin ruidos de aviso, así que conviene tener copia de seguridad igual que con cualquier disco.

### ¿Hay que desfragmentar un SSD?

No, nunca. La desfragmentación tiene sentido en discos mecánicos, donde el cabezal se mueve físicamente, pero en un SSD no aporta nada y consume ciclos de escritura innecesarios. Windows detecta automáticamente el tipo de unidad y aplica el mantenimiento correcto (TRIM), así que no instales herramientas de desfragmentación de terceros.
