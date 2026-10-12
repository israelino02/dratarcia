/* ═══════════════════════════════════════════
   DRA. TARCILA · interações do site
   ═══════════════════════════════════════════ */
(function () {
  'use strict';

  var reduzido = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ── ano no rodapé ── */
  var ano = document.getElementById('ano');
  if (ano) ano.textContent = new Date().getFullYear();

  /* ── cabeçalho fixo e barra de progresso ── */
  var header = document.getElementById('header');
  var barra = document.getElementById('progress');
  function aoRolarPagina() {
    var y = window.scrollY || document.documentElement.scrollTop;
    header.classList.toggle('stuck', y > 12);
    if (barra) {
      var max = document.documentElement.scrollHeight - window.innerHeight;
      barra.style.width = (max > 0 ? (y / max) * 100 : 0) + '%';
    }
  }
  window.addEventListener('scroll', aoRolarPagina, { passive: true });
  aoRolarPagina();

  /* ── menu: gaveta no celular, submenu de atendimentos ── */
  var burger = document.getElementById('burger');
  var nav = document.getElementById('nav');
  var fundo = document.getElementById('navBackdrop');
  var gaveta = window.matchMedia('(max-width: 1080px)');

  function fechaMenu() {
    nav.classList.remove('open');
    burger.classList.remove('open');
    fundo.classList.remove('on');
    burger.setAttribute('aria-expanded', 'false');
    burger.setAttribute('aria-label', 'Abrir menu');
    document.body.style.overflow = '';
  }
  burger.addEventListener('click', function () {
    var aberto = nav.classList.toggle('open');
    burger.classList.toggle('open', aberto);
    fundo.classList.toggle('on', aberto);
    burger.setAttribute('aria-expanded', String(aberto));
    burger.setAttribute('aria-label', aberto ? 'Fechar menu' : 'Abrir menu');
    document.body.style.overflow = aberto && gaveta.matches ? 'hidden' : '';
  });
  fundo.addEventListener('click', fechaMenu);
  window.addEventListener('resize', function () {
    if (!gaveta.matches && nav.classList.contains('open')) fechaMenu();
  });
  nav.querySelectorAll('a').forEach(function (a) { a.addEventListener('click', fechaMenu); });

  document.querySelectorAll('.has-sub').forEach(function (item) {
    var botao = item.querySelector('.sub-toggle');
    botao.addEventListener('click', function () {
      var aberto = item.classList.toggle('open');
      botao.setAttribute('aria-expanded', String(aberto));
    });
    item.addEventListener('mouseleave', function () {
      if (gaveta.matches) return;
      item.classList.remove('open');
      botao.setAttribute('aria-expanded', 'false');
    });
  });
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    fechaMenu();
    document.querySelectorAll('.has-sub.open').forEach(function (item) {
      item.classList.remove('open');
      item.querySelector('.sub-toggle').setAttribute('aria-expanded', 'false');
    });
  });

  /* ── animações de entrada ── */
  var revelaveis = document.querySelectorAll('.reveal');
  if (reduzido || !('IntersectionObserver' in window)) {
    revelaveis.forEach(function (el) { el.classList.add('in'); });
  } else {
    var io = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -50px 0px' });
    revelaveis.forEach(function (el) { io.observe(el); });
    /* rede de segurança: o que já está na tela aparece mesmo se o observer falhar */
    window.addEventListener('load', function () {
      setTimeout(function () {
        revelaveis.forEach(function (el) {
          if (el.getBoundingClientRect().top < window.innerHeight) el.classList.add('in');
        });
      }, 1200);
    });
  }

  /* ── vídeo do topo: toca sozinho, em silêncio. Se o navegador bloquear o autoplay
     (economia de bateria no iPhone, por exemplo), tenta de novo no primeiro toque ou rolagem ── */
  var video = document.getElementById('heroVideo');
  if (video) {
    video.muted = true;
    video.defaultMuted = true;
    var toca = function () {
      if (!video.paused) return;
      var p = video.play();
      if (p && p.catch) p.catch(function () {});
    };
    toca();
    video.addEventListener('loadeddata', toca);
    video.addEventListener('canplay', toca);
    document.addEventListener('visibilitychange', function () { if (!document.hidden) toca(); });
    ['touchstart', 'scroll', 'click', 'keydown'].forEach(function (ev) {
      window.addEventListener(ev, function once() { toca(); window.removeEventListener(ev, once); }, { passive: true });
    });
  }

  /* ── contadores ── */
  function conta(el) {
    var alvo = parseInt(el.getAttribute('data-count'), 10) || 0;
    if (reduzido) { el.textContent = alvo; return; }
    var ini = null, dur = 1300;
    function quadro(t) {
      if (ini === null) ini = t;
      var p = Math.min((t - ini) / dur, 1);
      el.textContent = Math.round(alvo * (1 - Math.pow(1 - p, 3)));
      if (p < 1) requestAnimationFrame(quadro);
    }
    el.textContent = '0';
    requestAnimationFrame(quadro);
  }
  var contadores = document.querySelectorAll('[data-count]');
  if ('IntersectionObserver' in window) {
    var co = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (en) {
        if (en.isIntersecting) { conta(en.target); co.unobserve(en.target); }
      });
    }, { threshold: 0.6 });
    contadores.forEach(function (el) { co.observe(el); });
  }

  /* ── esteira infinita da galeria ──
     clona o conjunto antes e depois; quando a rolagem passa do limite, salta a
     largura de um bloco. Como os três blocos são iguais, o salto não aparece. */
  function montaEsteira(cfg) {
    var trilho = cfg.trilho;
    if (!trilho) return null;
    var gap = cfg.gap || 16, limpos = cfg.limpos || 1;
    var originais = Array.prototype.slice.call(trilho.querySelectorAll(cfg.seletor));
    var qtd = originais.length;
    if (!qtd) return null;
    var antes = document.createDocumentFragment(), depois = document.createDocumentFragment();
    originais.forEach(function (card) {
      [antes, depois].forEach(function (destino) {
        var copia = card.cloneNode(true);
        copia.setAttribute('aria-hidden', 'true');
        copia.setAttribute('tabindex', '-1');
        destino.appendChild(copia);
      });
    });
    trilho.insertBefore(antes, trilho.firstChild);
    trilho.appendChild(depois);
    var cards = Array.prototype.slice.call(trilho.querySelectorAll(cfg.seletor));
    var bloco = 0;

    function semSuavizar(fn) {
      var b = trilho.style.scrollBehavior;
      trilho.style.scrollBehavior = 'auto'; fn(); trilho.offsetHeight; trilho.style.scrollBehavior = b;
    }
    function medir() {
      bloco = cards[qtd].offsetLeft - cards[0].offsetLeft;
      if (bloco > 0 && (trilho.scrollLeft < bloco * 0.5 || trilho.scrollLeft > bloco * 1.5)) {
        semSuavizar(function () { trilho.scrollLeft = bloco; });
      }
    }
    function normalizar() {
      if (!bloco) return;
      if (trilho.scrollLeft < bloco * 0.5) semSuavizar(function () { trilho.scrollLeft += bloco; });
      else if (trilho.scrollLeft > bloco * 1.5) semSuavizar(function () { trilho.scrollLeft -= bloco; });
    }
    function vidro() {
      var caixa = trilho.getBoundingClientRect(), centro = caixa.left + caixa.width / 2;
      cards.forEach(function (card) {
        var r = card.getBoundingClientRect();
        if (r.right < caixa.left - r.width || r.left > caixa.right + r.width) return;
        var passo = r.width + gap;
        var livre = (limpos - 1) / 2 * passo + r.width * 0.35;
        var t = Math.min(1, Math.max(0, (Math.abs(r.left + r.width / 2 - centro) - livre) / (passo * 0.85)));
        card.style.setProperty('--vidro', (t * t).toFixed(3));
        card.style.setProperty('--esc', (1 - 0.06 * t).toFixed(3));
      });
    }
    var pendente = false;
    trilho.addEventListener('scroll', function () {
      normalizar();
      if (pendente) return;
      pendente = true;
      requestAnimationFrame(function () { pendente = false; vidro(); });
    }, { passive: true });
    function andar(dir) {
      normalizar();
      trilho.scrollBy({ left: dir * (cards[0].getBoundingClientRect().width + gap), behavior: reduzido ? 'auto' : 'smooth' });
    }
    if (cfg.prev) cfg.prev.addEventListener('click', function () { andar(-1); });
    if (cfg.next) cfg.next.addEventListener('click', function () { andar(1); });
    window.addEventListener('resize', function () { medir(); vidro(); });
    window.addEventListener('load', function () { medir(); vidro(); });
    semSuavizar(function () { trilho.scrollLeft = cards[qtd].offsetLeft - cards[0].offsetLeft; });
    medir(); vidro();
    return { cards: cards };
  }

  /* ── foto ampliada ── */
  var lb = document.getElementById('lightbox');
  var lbImg = document.getElementById('lbImg');
  var lbCap = document.getElementById('lbCap');
  var ultimoFoco = null;
  function abreFoto(src, alt, cap) {
    ultimoFoco = document.activeElement;
    lbImg.src = src; lbImg.alt = alt || ''; lbCap.textContent = cap || '';
    lb.hidden = false;
    document.body.style.overflow = 'hidden';
    document.getElementById('lbClose').focus();
  }
  function fechaFoto() {
    lb.hidden = true; lbImg.src = '';
    document.body.style.overflow = '';
    if (ultimoFoco) ultimoFoco.focus({ preventScroll: true });
  }
  if (lb) {
    document.getElementById('lbClose').addEventListener('click', fechaFoto);
    lb.addEventListener('click', function (e) { if (e.target === lb) fechaFoto(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !lb.hidden) fechaFoto(); });
  }
  var galeria = document.getElementById('galeria');
  if (galeria) {
    var esteira = montaEsteira({
      trilho: galeria, seletor: '.gal-item', gap: 16, limpos: 3,
      prev: document.getElementById('galPrev'), next: document.getElementById('galNext')
    });
    (esteira ? esteira.cards : []).forEach(function (item) {
      item.addEventListener('click', function () {
        var img = item.querySelector('img');
        abreFoto(item.getAttribute('data-src'), img ? img.alt : '', item.getAttribute('data-cap'));
      });
    });
  }

  /* ── atendimentos no celular: cartão compacto que abre ao tocar ── */
  var compacto = window.matchMedia('(max-width: 620px)');
  var cartoes = Array.prototype.slice.call(document.querySelectorAll('.card:not(.card-cta)'));
  function abreCartao(card) {
    if (!compacto.matches) return;
    var aberto = card.classList.toggle('open');
    card.setAttribute('aria-expanded', String(aberto));
  }
  function sincroniza() {
    cartoes.forEach(function (card) {
      if (compacto.matches) {
        card.setAttribute('role', 'button');
        card.setAttribute('tabindex', '0');
        card.setAttribute('aria-expanded', card.classList.contains('open') ? 'true' : 'false');
      } else {
        card.removeAttribute('role'); card.removeAttribute('tabindex'); card.removeAttribute('aria-expanded');
        card.classList.remove('open');
      }
    });
  }
  cartoes.forEach(function (card) {
    card.addEventListener('click', function (e) {
      if (e.target.closest('a')) return;
      abreCartao(card);
    });
    card.addEventListener('keydown', function (e) {
      if (e.target !== card) return;
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); abreCartao(card); }
    });
  });
  sincroniza();
  if (compacto.addEventListener) compacto.addEventListener('change', sincroniza);

  /* ── dúvidas: abre uma por vez ── */
  var accs = document.querySelectorAll('.acc');
  accs.forEach(function (acc) {
    acc.addEventListener('toggle', function () {
      if (!acc.open) return;
      accs.forEach(function (outra) { if (outra !== acc) outra.open = false; });
    });
  });

  /* ── consultório aberto agora? (horário de Sinop, MT) ── */
  var status = document.querySelectorAll('[data-status]');
  if (status.length) {
    var partes = {};
    try {
      new Intl.DateTimeFormat('en-US', { timeZone: 'America/Cuiaba', weekday: 'short', hour: 'numeric', minute: 'numeric', hourCycle: 'h23' })
        .formatToParts(new Date()).forEach(function (p) { partes[p.type] = p.value; });
    } catch (err) { partes = null; }
    if (partes) {
      var dias = { Sun: 0, Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6 };
      var dia = dias[partes.weekday];
      var min = parseInt(partes.hour, 10) * 60 + parseInt(partes.minute, 10);
      var util = dia >= 1 && dia <= 5;
      var aberto = util && min >= 7 * 60 && min < 18 * 60;
      var texto;
      if (aberto) texto = 'Aberto agora · até 18h';
      else if (util && min < 7 * 60) texto = 'Fechado agora · abre hoje às 07h';
      else if (dia >= 0 && dia <= 4) texto = 'Fechado agora · abre amanhã às 07h';
      else texto = 'Fechado agora · abre segunda às 07h';
      status.forEach(function (el) { el.textContent = texto; el.classList.toggle('aberto', aberto); });
      var chave = util ? 'util' : (dia === 6 ? 'sab' : 'dom');
      document.querySelectorAll('[data-dia="' + chave + '"]').forEach(function (li) { li.classList.add('hoje'); });
    }
  }
})();
