---
titulo: Calculadora: ¿merece la pena reparar o es mejor cambiarlo?
titulo_seo: Calculadora: ¿merece la pena reparar o comprar nuevo?
h1: ¿Lo reparo o compro uno nuevo? Calculadora gratuita
descripcion: Calculadora gratuita para saber si compensa reparar tu lavadora, nevera, móvil, portátil o tele según su edad, su vida útil y el presupuesto.
entradilla: Introduce qué aparato es, cuántos años tiene y lo que te piden por arreglarlo. La calculadora compara ese presupuesto con el precio de uno nuevo y con la vida útil que le queda al tuyo.
url: /calculadora-reparar-o-cambiar.html
miga: Calculadora reparar o cambiar
schema: calculadora
clase: calculadora
actualizado: 2026-10-07
scripts: [/assets/calculadora.js]
---

<div class="calc-caja">
<h2>Calcula si te compensa repararlo</h2>
<form id="calc-cambiar" novalidate>
<div class="campo"><label for="cc-tipo">¿Qué aparato es?</label><select id="cc-tipo" required><option value="" disabled selected>Elige el aparato</option></select><span class="ayuda" id="cc-ayuda-vida">La vida útil media cambia mucho de un aparato a otro.</span></div>
<div class="campo-doble">
<div class="campo"><label for="cc-anios">Años que tiene</label><input id="cc-anios" type="number" inputmode="decimal" min="0" max="40" step="0.5" placeholder="Ej.: 7" required></div>
<div class="campo"><label for="cc-estado">Estado general</label><select id="cc-estado"><option value="bueno">Bueno, sin otros problemas</option><option value="normal" selected>Normal</option><option value="malo">Ya venía dando guerra</option></select></div>
</div>
<div class="campo-doble">
<div class="campo"><label for="cc-reparacion">Presupuesto de reparación (€)</label><input id="cc-reparacion" type="number" inputmode="decimal" min="0" step="1" placeholder="Ej.: 150" required><span class="ayuda">Pieza y mano de obra, con desplazamiento.</span></div>
<div class="campo"><label for="cc-nuevo">Precio de uno nuevo equivalente (€)</label><input id="cc-nuevo" type="number" inputmode="decimal" min="0" step="1" placeholder="Ej.: 400" required><span class="ayuda">Se rellena solo; cámbialo si el tuyo es de otra gama.</span></div>
</div>
<button type="submit" class="calc-boton">Calcular</button>
</form>
<div id="cc-resultado" class="resultado" aria-live="polite"></div>
</div>

:::dato Lo que hace la calculadora
Compara lo que cuesta la reparación con lo que cuesta un aparato nuevo equivalente, y ajusta el límite según la edad del tuyo. Un aparato casi nuevo justifica reparaciones caras; uno al final de su vida útil, solo arreglos baratos. No guarda ni envía ningún dato: el cálculo se hace en tu navegador.
:::

## Cómo funciona el cálculo

La regla que usan muchos técnicos y organizaciones de consumidores se resume en una frase: **si el aparato ya ha consumido buena parte de su vida útil y la reparación cuesta más de la mitad de uno nuevo, cámbialo**. La calculadora afina esa regla en cuatro tramos según la edad del aparato respecto a su vida útil media:

| Edad respecto a su vida útil | Gasto máximo razonable en la reparación |
| --- | --- |
| Menos del 40 % (casi nuevo) | Hasta el 55 % del precio de uno nuevo |
| Entre el 40 y el 70 % | Hasta el 40 % |
| Entre el 70 y el 90 % | Hasta el 28 % |
| Más del 90 % (al final de su vida) | Hasta el 20 % |

Ese límite se sube un 10 % si el aparato está en buen estado y se baja un 25 % si ya venía fallando, porque un aparato con varias averías recientes tiene más probabilidades de sufrir la siguiente. Además, cualquier reparación de menos de 120 € que no pase del 25 % de uno nuevo se considera siempre razonable: es dinero que se recupera en poco tiempo de uso.

## La vida útil media de cada aparato

Son medias de uso doméstico normal. Un aparato muy usado (una lavadora con tres lavados diarios) dura menos; uno bien mantenido, más.

| Aparato | Vida útil media | Precio orientativo nuevo |
| --- | --- | --- |
| Frigorífico | 13 años | 600 € |
| Horno | 15 años | 380 € |
| Caldera de gas | 15 años | 1.900 € instalada |
| Placa de inducción | 12 años | 400 € |
| Aire acondicionado split | 12 años | 750 € instalado |
| Lavadora | 11 años | 400 € |
| Secadora | 11 años | 450 € |
| Lavavajillas | 10 años | 450 € |
| Termo eléctrico | 10 años | 300 € |
| Televisor | 9 años | 500 € |
| Microondas | 9 años | 110 € |
| Cafetera superautomática | 8 años | 450 € |
| Ordenador de sobremesa | 7 años | 800 € |
| Portátil | 6 años | 700 € |
| Aspiradora o robot | 6 años | 280 € |
| Tablet | 5 años | 350 € |
| Móvil | 4 años | 400 € |

## Tres cosas que la calculadora no sabe (y tú sí)

**La garantía.** En España, los productos comprados a partir de enero de 2022 tienen tres años de garantía legal (el mínimo en la Unión Europea son dos). Si tu aparato está dentro de ese plazo y el fallo no es por mal uso, la reparación debería salirte gratis. Busca la factura antes de aceptar cualquier presupuesto.

**El coste de instalar uno nuevo.** En aparatos empotrados (horno, placa, lavavajillas integrable, campana) o con instalación (caldera, aire acondicionado), cambiar no es solo comprar: hay que sumar instalación, a veces adaptar el mueble y retirar el viejo. Si el precio que pones como "nuevo" no incluye eso, la calculadora se inclinará hacia cambiar más de lo que debería.

**El consumo.** Un frigorífico o un aire acondicionado de hace quince años gasta bastante más que uno actual. No es motivo para cambiar un aparato que funciona, pero sí para inclinar la balanza cuando la reparación está en la zona gris.

## Guías para cada aparato

Si quieres entender qué le pasa a tu aparato antes de pagar nada, estas guías explican las causas más comunes de cada avería, empezando por las que se arreglan gratis:

- [¿Merece la pena reparar una lavadora?](/blog/merece-la-pena-reparar-lavadora.html)
- [Cuándo reparar y cuándo cambiar: la guía completa](/blog/cuando-reparar-y-cuando-cambiar.html)
- [La nevera no enfría pero el congelador sí](/blog/nevera-no-enfria-congelador-si.html)
- [¿Cambiar la batería del móvil o comprar uno nuevo?](/blog/cambiar-bateria-movil-o-comprar-nuevo.html)
- [Qué hacer con un electrodoméstico que ya no sirve](/blog/que-hacer-electrodomestico-viejo.html)

Y si lo que tienes averiado es el coche, usa la [calculadora de reparar o vender el coche](/#calculadora), que tiene en cuenta el valor de mercado del vehículo en lugar de la vida útil.

## Preguntas frecuentes

### ¿Cuándo no merece la pena reparar un electrodoméstico?

Cuando la reparación supera el 50 % del precio de uno nuevo equivalente, y ese límite baja al 20-30 % si el aparato ya está cerca del final de su vida útil media. También conviene pensárselo más si el aparato ya había tenido otras averías recientes, porque suelen venir seguidas.

### ¿Qué es la regla del 50 %?

Es un criterio práctico muy extendido: si un aparato ha superado la mitad de su vida útil y la reparación cuesta más de la mitad de lo que vale uno nuevo, es mejor cambiarlo. Esta calculadora usa una versión más fina de esa regla, con cuatro tramos según la edad del aparato.

### ¿La calculadora guarda mis datos?

No. El cálculo se hace por completo en tu navegador y no se envía nada a ningún servidor. Si has aceptado las cookies de analítica, solo se registra de forma anónima qué tipo de aparato se ha calculado y el veredicto, para saber qué guías conviene ampliar.

### ¿Qué precio pongo como "uno nuevo"?

El de un aparato equivalente al tuyo, no el más barato del mercado: misma capacidad, prestaciones parecidas y, si es empotrado o necesita instalación, con la instalación incluida. La calculadora propone un precio orientativo de gama media que puedes cambiar.
