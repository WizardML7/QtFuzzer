/*!
 * WizardML7 Theme Kit — drop-in dark theme + live color switcher + twinkling starfield.
 * Usage: <script src="wizard-theme.js" defer></script>  (place near the end of <body>)
 *
 * Exposes CSS variables you style your page with:
 *   --accent       e.g. #13C4DC   (also --wz-accent)
 *   --accent-hot   brighter hover shade
 *   --accent-rgb   "19,196,220"   -> use rgba(var(--accent-rgb), .3) for glows
 *
 * The chosen theme is saved to localStorage under "wzml7_theme". Because every
 * page on https://wizardml7.github.io/* shares one origin, a visitor's choice
 * automatically follows them across all of your project pages.
 *
 * Options (set BEFORE this script loads):
 *   window.WizardTheme = { stars: true, switcher: true, default: 'teal' };
 */
(function () {
  if (window.__wizardThemeLoaded) return;
  window.__wizardThemeLoaded = true;

  var OPT = window.WizardTheme || {};
  var SHOW_STARS = OPT.stars !== false;
  var SHOW_SWITCHER = OPT.switcher !== false;
  var DEFAULT = OPT.default || 'teal';
  var KEY = 'wzml7_theme';

  var THEMES = {
    teal:    { label: 'Arcane Teal',       accent: '#13C4DC', hot: '#45E2F3', rgb: '19,196,220' },
    azure:   { label: 'Azure',             accent: '#3D8BFF', hot: '#6BA8FF', rgb: '61,139,255' },
    arcane:  { label: 'Spellbound Violet', accent: '#8A6CFF', hot: '#A98EFF', rgb: '138,108,255' },
    emerald: { label: 'Emerald',           accent: '#1FB46A', hot: '#36D483', rgb: '31,180,106' },
    gold:    { label: 'Gold',              accent: '#E5A52E', hot: '#F4C45A', rgb: '229,165,46' },
    magenta: { label: 'Magenta',           accent: '#FF4D8D', hot: '#FF6FA3', rgb: '255,77,141' }
  };
  var ORDER = ['teal', 'azure', 'arcane', 'emerald', 'gold', 'magenta'];

  function current() {
    try { var t = localStorage.getItem(KEY); return THEMES[t] ? t : DEFAULT; }
    catch (e) { return DEFAULT; }
  }

  function apply(name) {
    var p = THEMES[name] || THEMES[DEFAULT];
    var r = document.documentElement.style;
    r.setProperty('--accent', p.accent);     r.setProperty('--wz-accent', p.accent);
    r.setProperty('--accent-hot', p.hot);     r.setProperty('--wz-accent-hot', p.hot);
    r.setProperty('--accent-rgb', p.rgb);     r.setProperty('--wz-accent-rgb', p.rgb);
    var sws = document.querySelectorAll('.wz-sw');
    for (var i = 0; i < sws.length; i++) {
      sws[i].style.boxShadow = '0 0 0 ' + (sws[i].getAttribute('data-theme') === name ? '2px #fff' : '1px #3a4044');
    }
  }

  function setTheme(name) {
    if (!THEMES[name]) return;
    try { localStorage.setItem(KEY, name); } catch (e) {}
    apply(name);
    reloadStars();
  }
  window.setWizardTheme = setTheme;

  // Apply immediately so there's no color flash.
  apply(current());

  // ---- injected styles ----
  function injectCSS() {
    if (document.getElementById('wz-theme-style')) return;
    var css =
      '@keyframes wzGlow{0%,100%{opacity:.5}50%{opacity:.95}}' +
      '#wz-stars{position:fixed;inset:0;z-index:0;pointer-events:none;}' +
      '#wz-switcher{position:fixed;right:22px;bottom:22px;z-index:2147483000;display:flex;align-items:center;gap:13px;' +
        'background:rgba(17,22,26,.92);-webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px);' +
        'border:1px solid #2a3036;border-radius:999px;padding:10px 16px;box-shadow:0 10px 30px rgba(0,0,0,.5);' +
        'font-family:"Source Code Pro",ui-monospace,monospace;}' +
      '#wz-switcher .wz-lbl{font-size:11px;color:#8a9099;letter-spacing:.08em;}' +
      '#wz-switcher .wz-row{display:flex;align-items:center;gap:9px;}' +
      '.wz-sw{width:22px;height:22px;border-radius:50%;cursor:pointer;padding:0;border:2px solid #0D0D0D;' +
        'box-shadow:0 0 0 1px #3a4044;transition:box-shadow .15s,transform .15s;}' +
      '.wz-sw:hover{transform:scale(1.12);}' +
      /* Mobile: compact pill, no THEME label, tighter so it never overlaps content */
      '@media (max-width:640px){' +
        '#wz-switcher{right:12px;bottom:12px;gap:0;padding:7px 11px;}' +
        '#wz-switcher .wz-lbl{display:none;}' +
        '#wz-switcher .wz-row{gap:11px;}' +    /* a touch more spacing between swatches for fingers */
        '.wz-sw{width:20px;height:20px;}' +
      '}' +
      /* Respect reduced-motion: calm the swatch hover scale */
      '@media (prefers-reduced-motion:reduce){.wz-sw:hover{transform:none;}}';
    var st = document.createElement('style');
    st.id = 'wz-theme-style';
    st.textContent = css;
    document.head.appendChild(st);
  }

  // ---- color switcher widget ----
  function buildSwitcher() {
    if (!SHOW_SWITCHER || document.getElementById('wz-switcher')) return;
    var wrap = document.createElement('div');
    wrap.id = 'wz-switcher';
    var lbl = document.createElement('span');
    lbl.className = 'wz-lbl';
    lbl.textContent = 'THEME';
    var row = document.createElement('div');
    row.className = 'wz-row';
    ORDER.forEach(function (name) {
      var b = document.createElement('button');
      b.className = 'wz-sw';
      b.setAttribute('data-theme', name);
      b.title = THEMES[name].label;
      b.style.background = THEMES[name].accent;
      b.addEventListener('click', function () { setTheme(name); });
      row.appendChild(b);
    });
    wrap.appendChild(lbl);
    wrap.appendChild(row);
    document.body.appendChild(wrap);
    apply(current()); // refresh active ring
  }

  // ---- twinkling starfield (tsParticles, loaded from CDN) ----
  var starsContainer = null;
  function ensureStarsDiv() {
    var el = document.getElementById('wz-stars');
    if (!el) { el = document.createElement('div'); el.id = 'wz-stars'; document.body.insertBefore(el, document.body.firstChild); }
    return el;
  }
  function accentHex() {
    try { return (getComputedStyle(document.documentElement).getPropertyValue('--accent') || '#13C4DC').trim(); }
    catch (e) { return '#13C4DC'; }
  }
  function loadStars() {
    if (!SHOW_STARS || !window.tsParticles) return;
    ensureStarsDiv();
    try { if (starsContainer) { starsContainer.destroy(); starsContainer = null; } } catch (e) {}
    window.tsParticles.load({
      id: 'wz-stars',
      options: {
        fullScreen: { enable: false },
        fpsLimit: 60,
        detectRetina: true,
        particles: {
          number: { value: 70, density: { enable: true, area: 900 } },
          color: { value: ['#ffffff', '#ffffff', '#dfe6ee', accentHex()] },
          shape: { type: 'star', options: { star: { sides: 4, inset: 2 } } },
          opacity: { value: { min: 0.06, max: 0.85 }, animation: { enable: true, speed: 1.5, sync: false, startValue: 'random' } },
          size: { value: { min: 0.5, max: 2.7 } },
          move: { enable: true, speed: 0.22, direction: 'none', random: true, straight: false, outModes: { default: 'out' } },
          rotate: { value: { min: 0, max: 360 }, animation: { enable: true, speed: 2, sync: false } },
          links: { enable: false }
        }
      }
    }).then(function (c) { starsContainer = c; });
  }
  function reloadStars() { if (SHOW_STARS) loadStars(); }

  function loadTsParticles(cb) {
    if (window.tsParticles) return cb();
    var s = document.createElement('script');
    s.src = 'https://cdn.jsdelivr.net/npm/tsparticles@2.12.0/tsparticles.bundle.min.js';
    s.onload = cb;
    document.head.appendChild(s);
  }

  function init() {
    injectCSS();
    buildSwitcher();
    if (SHOW_STARS) loadTsParticles(loadStars);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
