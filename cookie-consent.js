(function () {
  window.dataLayer = window.dataLayer || [];
  function gtag() { dataLayer.push(arguments); }
  window.gtag = window.gtag || gtag;

  function applyConsent(granted) {
    gtag('consent', 'update', {
      ad_storage: granted ? 'granted' : 'denied',
      ad_user_data: granted ? 'granted' : 'denied',
      ad_personalization: granted ? 'granted' : 'denied',
      analytics_storage: granted ? 'granted' : 'denied'
    });
  }

  function leer(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function guardar(k, v) { try { if (v === null) localStorage.removeItem(k); else localStorage.setItem(k, v); } catch (e) {} }

  var accepted = leer('cookies-accepted');
  var rejected = leer('cookies-rejected');
  if (accepted) applyConsent(true);
  if (rejected) applyConsent(false);
  if (accepted || rejected) return;

  function injectBanner() {
    var style = document.createElement('style');
    style.textContent =
      '.cc-banner{position:fixed;bottom:0;left:0;right:0;background:#ffffff;' +
      'border-top:5px solid #0f2341;padding:1rem 1.25rem;z-index:100;display:flex;' +
      'flex-wrap:wrap;align-items:center;justify-content:space-between;gap:1rem;' +
      'box-shadow:0 -2px 12px rgba(15,35,65,0.18);font-family:"Source Sans 3","Segoe UI",Arial,sans-serif;}' +
      '.cc-text{font-size:0.95rem;color:#14181f;max-width:700px;margin:0;line-height:1.5;}' +
      '.cc-actions-wrap{display:flex;flex-direction:column;gap:0.4rem;align-items:flex-start;flex-shrink:0;}' +
      '.cc-actions{display:flex;gap:0.6rem;flex-wrap:wrap;width:100%;}' +
      '.cc-accept,.cc-reject{flex:1;min-width:130px;min-height:46px;border-radius:3px;' +
      'font-weight:700;font-family:inherit;cursor:pointer;font-size:0.98rem;}' +
      '.cc-accept{background:#0f2341;color:#ffffff;border:2px solid #0f2341;}' +
      '.cc-accept:hover{background:#1a3560;}' +
      '.cc-reject{background:#ffffff;color:#0f2341;border:2px solid #0f2341;}' +
      '.cc-reject:hover{background:#f3f4f6;}' +
      '.cc-info-link{color:#1a52ad;text-decoration:underline;font-size:0.85rem;}' +
      '@media (max-width:520px){.cc-banner{flex-direction:column;align-items:stretch;}' +
      '.cc-actions-wrap{width:100%;align-items:stretch;}}';
    document.head.appendChild(style);

    var banner = document.createElement('div');
    banner.className = 'cc-banner';
    banner.innerHTML =
      '<p class="cc-text">Usamos cookies propias y de terceros (Google Analytics para medir las visitas y Google AdSense para mostrar publicidad). Puedes aceptarlas o rechazarlas; la web funciona igual.</p>' +
      '<div class="cc-actions-wrap">' +
      '<div class="cc-actions">' +
      '<button class="cc-accept" type="button">Aceptar</button>' +
      '<button class="cc-reject" type="button">Rechazar</button>' +
      '</div>' +
      '<a href="/cookies.html" class="cc-info-link">Más info</a>' +
      '</div>';
    document.body.appendChild(banner);

    banner.querySelector('.cc-accept').addEventListener('click', function () {
      guardar('cookies-accepted', '1');
      guardar('cookies-rejected', null);
      applyConsent(true);
      banner.remove();
    });
    banner.querySelector('.cc-reject').addEventListener('click', function () {
      guardar('cookies-rejected', '1');
      guardar('cookies-accepted', null);
      applyConsent(false);
      banner.remove();
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', injectBanner);
  } else {
    injectBanner();
  }
})();
