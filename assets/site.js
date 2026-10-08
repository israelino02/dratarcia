(function(){
  // menu do celular
  var btn = document.querySelector('.menu-btn');
  var nav = document.getElementById('menu');
  if (btn && nav){
    btn.addEventListener('click', function(){
      var aberto = nav.classList.toggle('open');
      btn.setAttribute('aria-expanded', aberto ? 'true' : 'false');
    });
    nav.addEventListener('click', function(e){
      if (e.target.closest('a')){ nav.classList.remove('open'); btn.setAttribute('aria-expanded','false'); }
    });
  }

  // sombra no cabeçalho ao rolar
  var header = document.querySelector('.header');
  function onScroll(){ if (header) header.classList.toggle('scrolled', window.scrollY > 8); }
  window.addEventListener('scroll', onScroll, {passive:true}); onScroll();

  // entrada suave dos blocos
  var itens = document.querySelectorAll('[data-reveal]');
  if ('IntersectionObserver' in window){
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(en){ if (en.isIntersecting){ en.target.classList.add('in'); io.unobserve(en.target); } });
    }, {rootMargin:'0px 0px -8% 0px'});
    itens.forEach(function(el){ io.observe(el); });
  } else {
    itens.forEach(function(el){ el.classList.add('in'); });
  }

  // aberto ou fechado agora, no horário de Sinop (segunda a sexta, 7h às 18h)
  var ABRE = 7, FECHA = 18;
  var DIAS = ['domingo','segunda','terça','quarta','quinta','sexta','sábado'];
  function agoraSinop(){
    try{
      var p = new Intl.DateTimeFormat('en-US',{timeZone:'America/Cuiaba',weekday:'short',hour:'numeric',minute:'numeric',hour12:false}).formatToParts(new Date());
      var m = {}; p.forEach(function(x){ m[x.type] = x.value; });
      var dia = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'].indexOf(m.weekday);
      return {dia:dia, h:(parseInt(m.hour,10) % 24) + parseInt(m.minute,10)/60};
    }catch(e){ var d = new Date(); return {dia:d.getDay(), h:d.getHours() + d.getMinutes()/60}; }
  }
  function util(d){ return d >= 1 && d <= 5; }
  var a = agoraSinop();
  var aberto = util(a.dia) && a.h >= ABRE && a.h < FECHA;
  var texto;
  if (aberto){ texto = 'Aberto agora · fecha às ' + FECHA + 'h'; }
  else if (util(a.dia) && a.h < ABRE){ texto = 'Fechado · abre hoje às ' + ABRE + 'h'; }
  else {
    var prox = (a.dia + 1) % 7; while (!util(prox)) prox = (prox + 1) % 7;
    texto = 'Fechado · abre ' + (prox === (a.dia + 1) % 7 ? 'amanhã' : DIAS[prox]) + ' às ' + ABRE + 'h';
  }
  document.querySelectorAll('[data-status]').forEach(function(el){
    el.textContent = texto;
    el.classList.toggle('open', aberto);
  });
  var linha = util(a.dia) ? 'util' : (a.dia === 6 ? 'sab' : 'dom');
  document.querySelectorAll('.hours li[data-dia="' + linha + '"]').forEach(function(li){ li.classList.add('today'); });

  // galeria com ampliação
  var dlg = document.querySelector('.lightbox');
  if (dlg && typeof dlg.showModal === 'function'){
    var img = dlg.querySelector('img'), leg = dlg.querySelector('p');
    document.querySelectorAll('.gallery button').forEach(function(b){
      b.addEventListener('click', function(){
        var src = b.querySelector('img');
        img.src = src.getAttribute('src'); img.alt = src.alt;
        leg.textContent = b.querySelector('figcaption').textContent;
        dlg.showModal();
      });
    });
    dlg.addEventListener('click', function(e){ if (e.target === dlg || e.target.closest('.close')) dlg.close(); });
  }

  var ano = document.getElementById('ano'); if (ano) ano.textContent = new Date().getFullYear();
})();
