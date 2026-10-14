/* repararovender.es — comportamiento comun de las paginas del blog */
(function () {
  function evento(nombre, datos) {
    if (typeof window.gtag === 'function') {
      window.gtag('event', nombre, datos || {});
    }
  }

  // Botones de compartir: se mide que red se usa para saber de donde viene el trafico
  document.addEventListener('click', function (e) {
    var red = e.target.closest ? e.target.closest('.red') : null;
    if (!red) return;

    if (red.hasAttribute('data-copiar')) {
      var url = red.getAttribute('data-copiar');
      var hecho = function () {
        var original = red.textContent;
        red.textContent = '¡Copiado!';
        setTimeout(function () { red.textContent = original; }, 1800);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(url).then(hecho, function () { window.prompt('Copia el enlace:', url); });
      } else {
        window.prompt('Copia el enlace:', url);
      }
      evento('share', { method: 'copiar', content_type: 'articulo', item_id: location.pathname });
      return;
    }

    evento('share', { method: red.getAttribute('data-red'), content_type: 'articulo', item_id: location.pathname });
  });
})();
