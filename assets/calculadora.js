/* repararovender.es — calculadora "¿reparar o cambiar?"
 *
 * Criterio (el mismo que explican las guias): cuanto mas cerca esta el aparato
 * del final de su vida util media, menor es el porcentaje de su precio que
 * merece la pena gastar en repararlo.
 */
(function () {
  // vida util media (anos) y precio orientativo de uno nuevo equivalente (EUR)
  var APARATOS = {
    lavadora: { n: 'Lavadora', vida: 11, precio: 400 },
    lavavajillas: { n: 'Lavavajillas', vida: 10, precio: 450 },
    frigorifico: { n: 'Frigorífico', vida: 13, precio: 600 },
    secadora: { n: 'Secadora', vida: 11, precio: 450 },
    horno: { n: 'Horno', vida: 15, precio: 380 },
    induccion: { n: 'Placa de inducción o vitrocerámica', vida: 12, precio: 400 },
    microondas: { n: 'Microondas', vida: 9, precio: 110 },
    campana: { n: 'Campana extractora', vida: 12, precio: 250 },
    cafetera: { n: 'Cafetera superautomática', vida: 8, precio: 450 },
    aspiradora: { n: 'Aspiradora o robot aspirador', vida: 6, precio: 280 },
    termo: { n: 'Termo eléctrico', vida: 10, precio: 300 },
    caldera: { n: 'Caldera de gas (instalada)', vida: 15, precio: 1900 },
    aire: { n: 'Aire acondicionado split (instalado)', vida: 12, precio: 750 },
    televisor: { n: 'Televisor', vida: 9, precio: 500 },
    portatil: { n: 'Portátil', vida: 6, precio: 700 },
    sobremesa: { n: 'Ordenador de sobremesa', vida: 7, precio: 800 },
    movil: { n: 'Móvil', vida: 4, precio: 400 },
    tablet: { n: 'Tablet', vida: 5, precio: 350 },
    consola: { n: 'Consola', vida: 7, precio: 450 },
    otro: { n: 'Otro aparato', vida: 10, precio: 300 }
  };

  var form = document.getElementById('calc-cambiar');
  if (!form) return;
  var selTipo = document.getElementById('cc-tipo');
  var inAnios = document.getElementById('cc-anios');
  var inRep = document.getElementById('cc-reparacion');
  var inNuevo = document.getElementById('cc-nuevo');
  var selEstado = document.getElementById('cc-estado');
  var caja = document.getElementById('cc-resultado');
  var ayudaVida = document.getElementById('cc-ayuda-vida');

  Object.keys(APARATOS).forEach(function (k) {
    var o = document.createElement('option');
    o.value = k;
    o.textContent = APARATOS[k].n;
    selTipo.appendChild(o);
  });

  var precioTocado = false;
  inNuevo.addEventListener('input', function () { precioTocado = true; });

  function alCambiarTipo() {
    var a = APARATOS[selTipo.value];
    if (!a) return;
    if (!precioTocado || !inNuevo.value) inNuevo.value = a.precio;
    ayudaVida.textContent = 'Vida útil media: unos ' + a.vida + ' años.';
  }
  selTipo.addEventListener('change', alCambiarTipo);

  function eur(x) {
    return Math.round(x).toLocaleString('es-ES') + ' €';
  }

  function umbral(fraccionVida) {
    if (fraccionVida < 0.4) return 0.55;
    if (fraccionVida < 0.7) return 0.40;
    if (fraccionVida < 0.9) return 0.28;
    return 0.20;
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var a = APARATOS[selTipo.value];
    var anios = parseFloat(inAnios.value);
    var rep = parseFloat(inRep.value);
    var nuevo = parseFloat(inNuevo.value);
    if (!a || !(anios >= 0) || !(rep > 0) || !(nuevo > 0)) {
      caja.className = 'resultado visible duda';
      caja.innerHTML = '<p class="resultado-veredicto">Faltan datos</p><p>Rellena el tipo de aparato, los años que tiene, el presupuesto de reparación y el precio de uno nuevo.</p>';
      return;
    }

    var ajusteEstado = { bueno: 1.1, normal: 1, malo: 0.75 }[selEstado.value] || 1;
    var frac = anios / a.vida;
    var limite = umbral(frac) * ajusteEstado;
    var pct = rep / nuevo;
    var restante = Math.max(0, a.vida - anios);

    var clase, titulo, texto;
    if (pct <= 0.25 && rep <= 120) {
      clase = 'reparar';
      titulo = 'Repáralo';
      texto = 'Es una reparación barata: ' + eur(rep) + ' es el ' + Math.round(pct * 100) + ' % de uno nuevo. Aunque el aparato tenga sus años, por ese dinero compensa alargarle la vida.';
    } else if (pct <= limite * 0.75) {
      clase = 'reparar';
      titulo = 'Repáralo';
      texto = 'La reparación cuesta el ' + Math.round(pct * 100) + ' % de uno nuevo, por debajo del límite razonable para un aparato de su edad (' + Math.round(limite * 100) + ' %).';
    } else if (pct <= limite * 1.15) {
      clase = 'duda';
      titulo = 'Depende de su estado';
      texto = 'Estás en la zona gris: el ' + Math.round(pct * 100) + ' % del precio de uno nuevo, cerca del límite para su edad (' + Math.round(limite * 100) + ' %). Si no ha dado más guerra, repara. Si ya venía fallando, cambia.';
    } else {
      clase = 'cambiar';
      titulo = 'Mejor cámbialo';
      texto = 'La reparación supone el ' + Math.round(pct * 100) + ' % del precio de uno nuevo, por encima de lo que compensa en un aparato de su edad (' + Math.round(limite * 100) + ' %). Ese dinero rinde más como parte de uno nuevo.';
    }

    var garantia = anios < 3
      ? '<p><strong>Ojo:</strong> si lo compraste a partir de 2022 y tiene menos de 3 años, puede estar cubierto por la garantía legal. Busca la factura antes de pagar nada.</p>'
      : '';

    var ancho = Math.min(100, Math.round(pct / (limite * 1.6) * 100));
    caja.className = 'resultado visible ' + clase;
    caja.innerHTML =
      '<p class="resultado-veredicto">' + titulo + '</p>' +
      '<p>' + texto + '</p>' +
      '<div class="barra" role="img" aria-label="La reparación supone el ' + Math.round(pct * 100) + ' por ciento del precio de uno nuevo"><i style="width:' + ancho + '%"></i></div>' +
      '<div class="barra-leyenda"><span>Reparar</span><span>Depende</span><span>Cambiar</span></div>' +
      garantia +
      '<div class="resultado-detalle">' +
      '<div><span>Reparación / nuevo</span><strong>' + Math.round(pct * 100) + ' %</strong></div>' +
      '<div><span>Límite a su edad</span><strong>' + Math.round(limite * 100) + ' %</strong></div>' +
      '<div><span>Vida útil restante</span><strong>' + (restante > 0 ? '~' + Math.round(restante) + ' años' : 'agotada') + '</strong></div>' +
      '<div><span>Coste por año extra</span><strong>' + eur(rep / Math.max(1, restante)) + '</strong></div>' +
      '</div>';

    if (typeof window.gtag === 'function') {
      window.gtag('event', 'calculadora_resultado', { aparato: selTipo.value, veredicto: clase, porcentaje: Math.round(pct * 100) });
    }
    caja.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  });
})();
