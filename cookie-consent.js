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

  var accepted = localStorage.getItem('cookies-accepted');
  var rejected = localStorage.getItem('cookies-rejected');
  if (accepted) applyConsent(true);
  if (rejected) applyConsent(false);
  if (accepted || rejected) return;

  function injectBanner() {
    var style = document.createElement('style');
    style.textContent =
      '.cc-banner{position:fixed;bottom:0;left:0;right:0;background:#171a21;' +
      'border-top:1px solid #2a2f3a;padding:1.1rem 1.25rem;z-index:100;display:flex;' +
      'flex-wrap:wrap;align-items:center;justify-content:space-between;gap:1rem;' +
      'box-shadow:0 -4px 20px rgba(0,0,0,0.4);font-family:"Inter",sans-serif;}' +
      '.cc-text{font-size:0.88rem;color:#9aa3b2;max-width:680px;margin:0;}' +
      '.cc-actions-wrap{display:flex;flex-direction:column;gap:0.5rem;align-items:flex-start;flex-shrink:0;}' +
      '.cc-actions{display:flex;gap:0.75rem;flex-wrap:wrap;width:100%;}' +
      '.cc-accept,.cc-reject{flex:1;min-width:120px;min-height:46px;border-radius:8px;' +
      'font-weight:700;font-family:inherit;cursor:pointer;font-size:0.9rem;border:none;}' +
      '.cc-accept{background:#ff7a45;color:#1a1206;}' +
      '.cc-reject{background:transparent;color:#eef0f3;border:1px solid #2a2f3a;}' +
      '.cc-info-link{color:#9aa3b2;text-decoration:underline;font-size:0.8rem;}' +
      '@media (max-width:480px){.cc-banner{flex-direction:column;align-items:stretch;}' +
      '.cc-actions-wrap{width:100%;align-items:stretch;}}';
    document.head.appendChild(style);

    var banner = document.createElement('div');
    banner.className = 'cc-banner';
    banner.innerHTML =
      '<p class="cc-text">Usamos cookies propias y de terceros (Google AdSense) para mejorar tu experiencia y mostrarte publicidad relevante. Puedes aceptar o rechazar su uso.</p>' +
      '<div class="cc-actions-wrap">' +
      '<div class="cc-actions">' +
      '<button class="cc-accept" type="button">Aceptar</button>' +
      '<button class="cc-reject" type="button">Rechazar</button>' +
      '</div>' +
      '<a href="/cookies.html" class="cc-info-link">Más info</a>' +
      '</div>';
    document.body.appendChild(banner);

    banner.querySelector('.cc-accept').addEventListener('click', function () {
      localStorage.setItem('cookies-accepted', '1');
      localStorage.removeItem('cookies-rejected');
      applyConsent(true);
      banner.remove();
    });
    banner.querySelector('.cc-reject').addEventListener('click', function () {
      localStorage.setItem('cookies-rejected', '1');
      localStorage.removeItem('cookies-accepted');
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
