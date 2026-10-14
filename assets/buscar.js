/* repararovender.es — buscador de guias (todo en el navegador) */
(function () {
  var form = document.getElementById('form-busqueda');
  var input = document.getElementById('campo-busqueda');
  var salida = document.getElementById('resultados-busqueda');
  var estado = document.getElementById('estado-busqueda');
  if (!form || !input || !salida) return;

  var indice = null;

  function normalizar(t) {
    return (t || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');
  }

  function escapar(t) {
    return String(t).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function puntuar(doc, terminos) {
    var titulo = normalizar(doc.t), resto = normalizar(doc.r + ' ' + doc.k + ' ' + doc.c);
    var total = 0;
    for (var i = 0; i < terminos.length; i++) {
      var t = terminos[i];
      if (titulo.indexOf(t) !== -1) total += 5;
      else if (resto.indexOf(t) !== -1) total += 2;
      else return 0;
    }
    return total;
  }

  function buscar(q) {
    var terminos = normalizar(q).split(/\s+/).filter(function (t) { return t.length > 1; });
    if (!terminos.length) {
      salida.innerHTML = '';
      estado.textContent = 'Escribe una avería, un aparato o una pieza.';
      return;
    }
    var res = indice
      .map(function (d) { return { d: d, p: puntuar(d, terminos) }; })
      .filter(function (x) { return x.p > 0; })
      .sort(function (a, b) { return b.p - a.p; });

    estado.textContent = res.length
      ? res.length + (res.length === 1 ? ' guía encontrada' : ' guías encontradas') + ' para «' + q + '»'
      : 'No hay guías para «' + q + '». Prueba con otra palabra o mira todas las guías.';

    salida.innerHTML = res.slice(0, 30).map(function (x) {
      return '<a class="resultado-busqueda" href="' + x.d.u + '">' +
        '<span>' + escapar(x.d.c) + '</span>' +
        '<strong>' + escapar(x.d.t) + '</strong>' +
        '<p>' + escapar(x.d.r) + '</p></a>';
    }).join('');

    if (typeof window.gtag === 'function') window.gtag('event', 'search', { search_term: q });
  }

  function iniciar() {
    var q = new URLSearchParams(location.search).get('q') || '';
    input.value = q;
    if (q) buscar(q);
    else estado.textContent = 'Escribe una avería, un aparato o una pieza.';
  }

  fetch('/assets/busqueda.json')
    .then(function (r) { return r.json(); })
    .then(function (datos) { indice = datos; iniciar(); })
    .catch(function () { estado.textContent = 'No se ha podido cargar el buscador. Prueba a recargar la página.'; });

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (!indice) return;
    var q = input.value.trim();
    history.replaceState(null, '', q ? '?q=' + encodeURIComponent(q) : location.pathname);
    buscar(q);
  });
})();
