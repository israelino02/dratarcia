# -*- coding: utf-8 -*-
"""Gera o site modelo da Dra. Tarcila: index.html e uma pasta por palavra-chave.

Para trocar telefone, endereço, horário ou textos, edite os blocos abaixo e rode:
    python3 gerar-site.py
Regra do Israel para este site: nenhum hífen ou travessão no texto visível.
"""
import io, json, os, re, html as H
from urllib.parse import quote

BASE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- dados
D = {
    "nome": "Dra. Tarcila Antunes Banagouro",
    "curto": "Dra. Tarcila Banagouro",
    "crm": "CRM/MT 9131",
    "rqe": "RQE 6722",
    "rua": "Av. Magda de C. Pissinatti, 2099",
    "bairro": "Santa Cecília",
    "cidade": "Sinop",
    "uf": "MT",
    "cep": "78555-440",           # só no JSON-LD (texto visível sem hífen)
    "clinica": "Clínica Teor",
    "wa": "5566999134321",
    "tel_txt": "(66) 99913 4321",
    "insta": "dra.tarcila.banagouro",
    "cid": "4104804225488390202",  # Perfil da Empresa no Google
    "lat": -11.834095, "lng": -55.535219,
    "nota": "5,0", "avaliacoes": 2,
    "dominio": "https://www.dratarcilabanagouro.com.br",  # sugestão, ainda não registrado
}
ENDERECO_TXT = f'{D["rua"]}, {D["bairro"]}, {D["cidade"]}, {D["uf"]}'
GOOGLE_PERFIL = f'https://www.google.com/maps?cid={D["cid"]}'
ROTA = "https://www.google.com/maps/dir/?api=1&destination=" + quote(f'{D["nome"]}, {D["rua"]}, {D["cidade"]} {D["uf"]}')
MAPA_EMBED = "https://www.google.com/maps?q=" + quote(f'{D["clinica"]}, {D["rua"]}, {D["bairro"]}, {D["cidade"]} {D["uf"]}') + "&z=16&output=embed"
INSTA = f'https://www.instagram.com/{D["insta"]}/'

def wa(msg="Olá! Vim pelo site e gostaria de agendar uma consulta com a Dra. Tarcila."):
    return f'https://wa.me/{D["wa"]}?text=' + quote(msg)

PAGINAS = [
    ("consulta", "Consulta"),
    ("puericultura", "Puericultura"),
    ("bebe", "Recém nascido"),
    ("alimentacao", "Introdução alimentar"),
]

# ---------------------------------------------------------------- ícones
SPRITE = '''<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <symbol id="i-wa" viewBox="0 0 32 32"><path d="M16 3C8.8 3 3 8.8 3 16c0 2.3.6 4.5 1.8 6.4L3 29l6.8-1.8c1.9 1 4 1.6 6.2 1.6 7.2 0 13-5.8 13-13S23.2 3 16 3zm0 23.6c-2 0-3.9-.5-5.5-1.5l-.4-.2-4 1.1 1.1-3.9-.3-.4a10.5 10.5 0 1 1 9.1 4.9zm5.9-7.9c-.3-.2-1.9-.9-2.2-1-.3-.1-.5-.2-.7.2s-.8 1-1 1.2c-.2.2-.4.2-.7.1a8.6 8.6 0 0 1-4.3-3.7c-.3-.6.3-.5.9-1.7.1-.2 0-.4 0-.6s-.7-1.7-1-2.3c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.6.1-.9.4-.3.4-1.2 1.2-1.2 2.8s1.2 3.2 1.4 3.5c.2.2 2.4 3.7 5.9 5.1 2.2.9 3 1 4.1.8.7-.1 2-.8 2.2-1.6.3-.8.3-1.5.2-1.6-.1-.2-.3-.3-.6-.4z"/></symbol>
  <symbol id="i-star" viewBox="0 0 24 24"><path d="M12 2.8l2.8 5.8 6.3.9-4.6 4.4 1.1 6.3L12 17.2l-5.6 3 1.1-6.3L2.9 9.5l6.3-.9z"/></symbol>
  <symbol id="i-pin" viewBox="0 0 24 24"><path d="M12 21s-7-6.2-7-11a7 7 0 0 1 14 0c0 4.8-7 11-7 11z"/><circle cx="12" cy="10" r="2.6"/></symbol>
  <symbol id="i-route" viewBox="0 0 24 24"><path d="M3.5 11.2l17-7.7-7.7 17-1.9-7.4z"/></symbol>
  <symbol id="i-ig" viewBox="0 0 24 24"><rect x="3.5" y="3.5" width="17" height="17" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.3" cy="6.7" r=".6"/></symbol>
  <symbol id="i-clock" viewBox="0 0 24 24"><circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/></symbol>
  <symbol id="i-arrow" viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></symbol>
  <symbol id="i-check" viewBox="0 0 24 24"><path d="M4.5 12.5l4.5 4.5 10.5-10.5"/></symbol>
  <symbol id="i-review" viewBox="0 0 24 24"><path d="M4 5h16v11H9l-5 4z"/><path d="M12 8.2l.9 1.9 2 .3-1.5 1.4.4 2-1.8-1-1.8 1 .4-2-1.5-1.4 2-.3z"/></symbol>
  <symbol id="i-menu" viewBox="0 0 24 24"><path d="M4 7h16M4 12h16M4 17h16"/></symbol>
  <symbol id="i-steth" viewBox="0 0 24 24"><path d="M6 3.5v5a4 4 0 0 0 8 0v-5"/><path d="M10 12.5v2.5a5 5 0 0 0 10 0v-2"/><circle cx="20" cy="11" r="2"/></symbol>
  <symbol id="i-grow" viewBox="0 0 24 24"><path d="M4 20h16"/><path d="M7 16.5v-3.5M12 16.5V9M17 16.5V5.5"/></symbol>
  <symbol id="i-heart" viewBox="0 0 24 24"><path d="M12 20s-7.5-4.6-7.5-10.2A4.2 4.2 0 0 1 12 7.2a4.2 4.2 0 0 1 7.5 2.6C19.5 15.4 12 20 12 20z"/></symbol>
  <symbol id="i-bowl" viewBox="0 0 24 24"><path d="M3.5 12h17a8.5 8.5 0 0 1-17 0z"/><path d="M15.5 3.5l-3 6"/><path d="M9 20.5h6"/></symbol>
</svg>'''

def ico(nome, cls="i"):
    fill = nome in ("wa", "star")
    return f'<svg class="{cls}{" fill" if fill else ""}" aria-hidden="true"><use href="#i-{nome}"></use></svg>'

ESTRELAS = '<span class="stars" aria-hidden="true">' + "".join(ico("star") for _ in range(5)) + "</span>"

# ---------------------------------------------------------------- blocos comuns
def head(p, titulo, desc, url, extra_ld):
    ld_medico = {
        "@context": "https://schema.org", "@type": "Physician",
        "name": D["nome"], "medicalSpecialty": "Pediatric",
        "description": "Pediatra em Sinop, MT. Puericultura, recém nascido, introdução alimentar e consulta pediátrica.",
        "url": D["dominio"] + "/", "image": D["dominio"] + "/assets/img/dratarcila.jpg",
        "telephone": "+" + D["wa"],
        "address": {"@type": "PostalAddress", "streetAddress": D["rua"] + ", " + D["clinica"],
                    "addressLocality": D["cidade"], "addressRegion": D["uf"],
                    "postalCode": D["cep"], "addressCountry": "BR"},
        "geo": {"@type": "GeoCoordinates", "latitude": D["lat"], "longitude": D["lng"]},
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
            "opens": "07:00", "closes": "18:00"}],
        "hasMap": GOOGLE_PERFIL, "sameAs": [INSTA, GOOGLE_PERFIL],
        "isAcceptingNewPatients": True,
    }
    lds = [ld_medico] + extra_ld
    ld_html = "\n".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in lds)
    return f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{H.escape(titulo)}</title>
<meta name="description" content="{H.escape(desc)}">
<meta name="robots" content="noindex, nofollow">
<link rel="canonical" href="{D["dominio"]}{url}">
<meta property="og:type" content="website">
<meta property="og:title" content="{H.escape(titulo)}">
<meta property="og:description" content="{H.escape(desc)}">
<meta property="og:image" content="{D["dominio"]}/assets/img/dratarcila.jpg">
<meta name="theme-color" content="#FBF8F6">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Ccircle cx='32' cy='32' r='32' fill='%23B8456A'/%3E%3Ctext x='32' y='42' font-family='Georgia' font-style='italic' font-size='28' fill='white' text-anchor='middle'%3ETB%3C/text%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Lora:ital,wght@1,500;1,600&display=swap">
<link rel="stylesheet" href="{p}assets/style.css">
<script>document.documentElement.classList.add('js')</script>
{ld_html}
</head>
<body>
<a class="skip" href="#conteudo">Ir para o conteúdo</a>
{SPRITE}'''

def header(p, atual=None):
    marca = ' aria-current="page"'
    links = "".join(
        f'<a href="{p}{slug}/"{marca if slug == atual else ""}>{rot}</a>'
        for slug, rot in PAGINAS)
    links += f'<a href="{p}#sobre">Sobre</a><a href="{p}#consultorio">Consultório</a>'
    return f'''
<header class="header">
  <div class="wrap">
    <a class="brand" href="{p or "./"}" aria-label="{D["curto"]}, página inicial">
      <span class="brand-mark" aria-hidden="true">TB</span>
      <span><span class="brand-name">{D["curto"]}</span><span class="brand-sub">Pediatra · {D["crm"]}</span></span>
    </a>
    <nav class="nav" id="menu" aria-label="Principal">{links}</nav>
    <a class="btn btn-1" href="{wa()}" target="_blank" rel="noopener">{ico("wa")}<span>Agendar</span></a>
    <button class="menu-btn" type="button" aria-controls="menu" aria-expanded="false" aria-label="Abrir menu">{ico("menu")}</button>
  </div>
</header>
<main id="conteudo">'''

def proof():
    return f'''<div class="proof">
        <a href="{GOOGLE_PERFIL}" target="_blank" rel="noopener">{ESTRELAS}<span><b>{D["nota"]}</b> no Google · {D["avaliacoes"]} avaliações</span></a>
        <span>{D["crm"]} · {D["rqe"]}</span>
      </div>'''

def consultorio(p):
    return f'''
<section id="consultorio" class="on-plum">
  <div class="wrap loc">
    <div class="loc-text" data-reveal>
      <p class="kicker">Consultório</p>
      <h2 class="sec-title">{D["bairro"]}, no norte de {D["cidade"]}</h2>
      <p>Atendimento com hora marcada na {D["clinica"]}. Estacionamento em frente à clínica e acesso para cadeira de rodas.</p>
      <span class="status" data-status>Segunda a sexta, 07h às 18h</span>
      <div class="hours">
        <h3>Horário de atendimento</h3>
        <ul>
          <li data-dia="util"><span>Segunda a sexta</span><span>07h às 18h</span></li>
          <li data-dia="sab"><span>Sábado</span><span>Fechado</span></li>
          <li data-dia="dom"><span>Domingo</span><span>Fechado</span></li>
        </ul>
      </div>
      <div class="hero-actions">
        <a class="btn btn-1" href="{wa()}" target="_blank" rel="noopener">{ico("wa")}Agendar pelo WhatsApp</a>
        <a class="btn btn-2" href="{ROTA}" target="_blank" rel="noopener">{ico("route")}Ver rota no Maps</a>
      </div>
      <p class="loc-note">Em caso de urgência, como dificuldade para respirar, convulsão ou criança muito abatida, procure o pronto atendimento mais próximo.</p>
    </div>
    <div data-reveal>
      <article class="gcard" aria-label="Perfil no Google">
        <div class="gcard-map"><iframe src="{MAPA_EMBED}" title="Mapa da {D["clinica"]} em {D["cidade"]}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></div>
        <div class="gcard-body">
          <h3>{D["nome"]}</h3>
          <div class="gcard-rating"><b>{D["nota"]}</b>{ESTRELAS}<span>({D["avaliacoes"]})</span><span>· Pediatra</span></div>
        </div>
        <div class="gcard-actions">
          <a href="{ROTA}" target="_blank" rel="noopener"><span class="c">{ico("route")}</span>Rotas</a>
          <a href="{wa()}" target="_blank" rel="noopener"><span class="c">{ico("wa")}</span>WhatsApp</a>
          <a href="{INSTA}" target="_blank" rel="noopener"><span class="c">{ico("ig")}</span>Instagram</a>
          <a href="{GOOGLE_PERFIL}" target="_blank" rel="noopener"><span class="c">{ico("review")}</span>Avaliações</a>
        </div>
        <ul class="gcard-rows">
          <li>{ico("pin")}<a href="{ROTA}" target="_blank" rel="noopener">{D["clinica"]}, {D["rua"]}, {D["bairro"]}, {D["cidade"]}, {D["uf"]}</a></li>
          <li>{ico("clock")}<span><span class="st" data-status>Segunda a sexta, 07h às 18h</span></span></li>
          <li>{ico("wa")}<a href="{wa()}" target="_blank" rel="noopener">{D["tel_txt"]}</a></li>
          <li>{ico("ig")}<a href="{INSTA}" target="_blank" rel="noopener">@{D["insta"]}</a></li>
        </ul>
      </article>
    </div>
  </div>
</section>'''

def faq(itens, titulo="Dúvidas frequentes"):
    blocos = "\n".join(f'      <details><summary>{q}</summary><p>{a}</p></details>' for q, a in itens)
    return f'''
<section class="sec-alt" id="duvidas">
  <div class="wrap">
    <div class="sec-head" data-reveal><p class="kicker">Perguntas</p><h2>{titulo}</h2></div>
    <div class="faq" data-reveal>
{blocos}
    </div>
  </div>
</section>'''

def faq_ld(itens):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", a)}} for q, a in itens]}

def cta(titulo="Agende a consulta do seu filho", texto=None, msg=None, botao="Agendar pelo WhatsApp"):
    texto = texto or f"Atendimento com hora marcada na {D['clinica']}, bairro {D['bairro']}, {D['cidade']}."
    return f'''
<section class="cta">
  <div class="wrap" data-reveal>
    <h2>{titulo}</h2>
    <p>{texto}</p>
    <a class="btn btn-1" href="{wa(msg) if msg else wa()}" target="_blank" rel="noopener">{ico("wa")}{botao}</a>
  </div>
</section>'''

def footer(p):
    links = "".join(f'<li><a href="{p}{slug}/">{rot}</a></li>' for slug, rot in PAGINAS)
    return f'''
</main>
<footer class="footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <a class="brand" href="{p or "./"}"><span class="brand-mark" aria-hidden="true">TB</span><span><span class="brand-name">{D["curto"]}</span><span class="brand-sub">Pediatra em {D["cidade"]}, {D["uf"]}</span></span></a>
        <p>{D["crm"]} · {D["rqe"]}<br>Residência em Pediatria pela UFMT.</p>
      </div>
      <div>
        <h4>Atendimentos</h4>
        <ul>{links}</ul>
      </div>
      <div>
        <h4>Contato</h4>
        <ul>
          <li><a href="{wa()}" target="_blank" rel="noopener">WhatsApp {D["tel_txt"]}</a></li>
          <li><a href="{INSTA}" target="_blank" rel="noopener">@{D["insta"]}</a></li>
          <li><a href="{ROTA}" target="_blank" rel="noopener">{D["clinica"]}, {D["rua"]}<br>{D["bairro"]}, {D["cidade"]}, {D["uf"]}</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© <span id="ano">2026</span> {D["nome"]}. Diretor técnico médico: {D["nome"]}, {D["crm"]}, {D["rqe"]}.</span>
      <span>Versão de apresentação</span>
    </div>
  </div>
</footer>
<a class="float-wa" href="{wa()}" target="_blank" rel="noopener" aria-label="Agendar pelo WhatsApp">{ico("wa")}</a>
<dialog class="lightbox" aria-label="Foto ampliada"><button class="close" type="button" aria-label="Fechar">×</button><img src="" alt=""><p></p></dialog>
<script src="{p}assets/site.js" defer></script>
</body>
</html>
'''

# ---------------------------------------------------------------- home
CARDS = [
    ("consulta", "steth", "Consulta pediátrica", "Consulta de rotina ou quando algo preocupa: febre, tosse, alimentação, sono e comportamento."),
    ("puericultura", "grow", "Puericultura", "Acompanhamento do crescimento, do desenvolvimento e das vacinas, mesmo quando está tudo bem."),
    ("bebe", "heart", "Recém nascido", "Primeira consulta depois da maternidade: amamentação, icterícia, umbigo, sono e cuidados em casa."),
    ("alimentacao", "bowl", "Introdução alimentar", "Quando começar, como oferecer e como montar o prato do bebê, dentro da rotina da família."),
]
TEMAS = [
    ("Febre, gripes e viroses", "Avaliação e orientação para cuidar em casa com segurança.", "febre, gripes e viroses"),
    ("Crescimento e desenvolvimento", "Marcos esperados para cada idade, acompanhados de perto.", "crescimento e desenvolvimento"),
    ("Sono do bebê e da criança", "Rotina e hábitos que ajudam a família inteira a dormir.", "sono do bebê"),
    ("Orientação sobre vacinas", "Caderneta em dia, com explicação de cada dose.", "vacinas"),
    ("Consulta do adolescente", "Puberdade, alimentação, telas e saúde emocional.", "consulta do adolescente"),
    ("Consulta com gestantes", "Conhecer a pediatra antes do bebê chegar.", "consulta com gestante"),
]
GALERIA = [
    ("fachada.jpg", "Fachada da Clínica Teor", 880, 1100),
    ("entrada.jpg", "Entrada", 825, 1100),
    ("recepcao.jpg", "Recepção", 890, 1100),
    ("espera.jpg", "Sala de espera", 825, 1100),
    ("sala.jpg", "Consultório", 855, 840),
]
FAQ_HOME = [
    ("Com quantos dias levar o bebê na primeira consulta?", "O ideal é nos primeiros dias depois da alta da maternidade, de preferência ainda na primeira semana de vida. Leve a Caderneta da Criança, o resumo de alta e os resultados dos testes do pezinho, da orelhinha, do olhinho e do coraçãozinho."),
    ("Até que idade a Dra. Tarcila atende?", "Do recém nascido à adolescência. O intervalo entre as consultas muda com a idade, e a Dra. Tarcila combina com a família quando será o próximo retorno."),
    ("Com que frequência a criança precisa ir ao pediatra?", "No primeiro ano de vida as consultas são mais frequentes, porque o bebê muda muito de um mês para o outro. A partir do segundo ano os retornos ficam mais espaçados."),
    ("Como faço para agendar?", f"Pelo WhatsApp {D['tel_txt']}. O atendimento é com hora marcada, para que cada consulta tenha o tempo de que precisa."),
    ("Onde fica o consultório?", f"Na {D['clinica']}, {D['rua']}, bairro {D['bairro']}, em {D['cidade']}. Há estacionamento em frente à clínica."),
]

def pagina_home():
    p = ""
    cards = "\n".join(f'''      <a class="card" href="{slug}/" data-reveal>
        <span class="ico">{ico(i)}</span>
        <h3>{t}</h3>
        <p>{d}</p>
        <span class="more">Ver detalhes {ico("arrow")}</span>
      </a>''' for slug, i, t, d in CARDS)
    temas = "\n".join(f'''      <div class="topic" data-reveal>
        <h3>{t}</h3>
        <p>{d}</p>
        <a href="{wa("Olá! Vim pelo site e gostaria de saber mais sobre " + m + " com a Dra. Tarcila.")}" target="_blank" rel="noopener">Saber mais {ico("arrow")}</a>
      </div>''' for t, d, m in TEMAS)
    galeria = "\n".join(f'''      <button type="button" aria-label="Ampliar foto: {leg}"><figure style="margin:0;height:100%"><img src="assets/img/{arq}" alt="{leg}, {D["clinica"]}, {D["cidade"]}" loading="lazy" width="{w}" height="{h}"><figcaption>{leg}</figcaption></figure></button>''' for arq, leg, w, h in GALERIA)

    corpo = f'''
<section class="hero">
  <div class="wrap">
    <div class="hero-inner">
      <p class="hero-chip">{ico("pin")}{D["clinica"]} · {D["bairro"]}, {D["cidade"]}</p>
      <h1>Os primeiros meses são cheios de dúvidas. Você não precisa passar por eles sozinha <span class="h1-sub">Pediatra em {D["cidade"]}, {D["uf"]}, no bairro {D["bairro"]}</span></h1>
      <p class="hero-lead">Uma pediatra que acompanha seu bebê de perto, examina com calma, ouve o que você percebe em casa e explica cada orientação com clareza. Da primeira semana de vida à adolescência, com hora marcada na {D["clinica"]}.</p>
      <div class="hero-actions">
        <a class="btn btn-1" href="{wa()}" target="_blank" rel="noopener">{ico("wa")}Agendar pelo WhatsApp</a>
        <a class="btn btn-2" href="#atendimentos">Ver atendimentos</a>
      </div>
      {proof()}
    </div>
  </div>
</section>

<section id="atendimentos" class="sec-alt">
  <div class="wrap">
    <div class="sec-head" data-reveal>
      <p class="kicker">Atendimentos</p>
      <h2>Do primeiro dia de vida à adolescência</h2>
      <p>Cada fase com o mesmo cuidado: entender a rotina da família, examinar com calma e deixar claro o próximo passo.</p>
    </div>
    <div class="cards">
{cards}
    </div>
  </div>
</section>

<section id="sobre" class="sec-tint">
  <div class="wrap split">
    <figure class="split-figure" data-reveal><img src="assets/img/consultorio.jpg" alt="{D["nome"]} no consultório da {D["clinica"]}" loading="lazy" width="825" height="1100"></figure>
    <div class="split-text" data-reveal>
      <p class="kicker">Sobre</p>
      <h2 class="sec-title">Pediatra, mãe e defensora da consulta sem pressa</h2>
      <p style="margin-top:18px">Sou pediatra em {D["cidade"]} e acredito que cada consulta precisa de tempo. Tempo para ouvir o que a família percebe em casa, examinar a criança por inteiro e explicar o porquê de cada orientação, sem pressa e sem termos difíceis.</p>
      <p>Meu trabalho vai além do peso e da medida: acompanho crescimento, desenvolvimento, alimentação, sono e comportamento, para que os pais saiam da consulta seguros sobre o próximo passo.</p>
      <div class="creds">
        <div class="cred"><b>UNIC</b><span>Graduação em Medicina</span></div>
        <div class="cred"><b>UFMT</b><span>Residência em Pediatria</span></div>
        <div class="cred"><b>Lisboa, Portugal</b><span>Doutorado</span></div>
        <div class="cred"><b>{D["crm"]} · {D["rqe"]}</b><span>Registro de especialista em Pediatria</span></div>
      </div>
    </div>
  </div>
</section>

<section class="sec-alt">
  <div class="wrap">
    <div class="sec-head" data-reveal>
      <p class="kicker">Na consulta</p>
      <h2>O que também faz parte do acompanhamento</h2>
    </div>
    <div class="topics">
{temas}
    </div>
    <p class="fineprint">A indicação de qualquer conduta depende de consulta médica e avaliação individual.</p>
  </div>
</section>

<section id="espaco" class="sec-tint">
  <div class="wrap">
    <div class="sec-head" data-reveal>
      <p class="kicker">O espaço</p>
      <h2>Um consultório pensado para receber a família</h2>
      <p>Recepção ampla, sala de espera confortável e estacionamento em frente, no bairro {D["bairro"]}.</p>
    </div>
    <div class="gallery" data-reveal>
{galeria}
    </div>
  </div>
</section>
{consultorio(p)}
{faq(FAQ_HOME)}
{cta()}'''
    titulo = f"Pediatra em Sinop MT | {D['nome']}"
    desc = f"Pediatra em Sinop, MT, no bairro Santa Cecília. Consulta com tempo para a família: puericultura, recém nascido, introdução alimentar e acompanhamento do desenvolvimento. {D['crm']} · {D['rqe']}."
    return head(p, titulo, desc, "/", [faq_ld(FAQ_HOME)]) + header(p) + corpo + footer(p)

# ---------------------------------------------------------------- páginas por palavra-chave
SUB = {
"consulta": dict(
    titulo="Consulta com Pediatra em Sinop MT | " + D["nome"],
    desc="Consulta pediátrica em Sinop, MT, no bairro Santa Cecília. Febre, tosse, alimentação, sono e desenvolvimento avaliados com tempo para a família. CRM/MT 9131 · RQE 6722.",
    rot="Consulta pediátrica",
    h1="Procurando pediatra em Sinop?", sub="Consulta pediátrica no bairro Santa Cecília, Sinop, MT",
    lead="Na consulta, a criança é vista por inteiro e a família tem espaço para perguntar. A Dra. Tarcila examina com calma, explica o que encontrou e deixa claro o que fazer em casa e quando voltar.",
    cta="Agendar consulta pediátrica", msg="Olá! Vim pelo site e gostaria de agendar uma consulta pediátrica com a Dra. Tarcila.",
    ev_t="O que é avaliado na consulta", ev_p="Queixas parecidas podem ter causas diferentes. A consulta serve para entender o que está acontecendo antes de qualquer conduta.",
    ev=[("Febre e infecções comuns", "Gripes, resfriados, viroses, dor de ouvido e dor de garganta."),
        ("Tosse e chiado", "Avaliação da respiração e orientação sobre quando é preciso investigar."),
        ("Alimentação", "Apetite, seletividade, ganho de peso e hábitos à mesa."),
        ("Sono", "Despertares noturnos, rotina e horário de dormir."),
        ("Pele", "Assaduras, manchas, dermatite e alergias de pele."),
        ("Comportamento", "Birras, adaptação escolar, uso de telas e rotina da família.")],
    ck_t="Quando marcar uma consulta", ck_p="Não precisa esperar a criança ficar doente para ir ao pediatra.",
    ck=["Consulta de rotina, mesmo com a criança bem",
        "Febre, tosse ou dor que não melhora",
        "Mudança no apetite, no sono ou no comportamento",
        "Dúvidas sobre vacinas, alimentação ou desenvolvimento",
        "Avaliação antes de começar a escola ou um esporte"],
    alerta=True,
    faq=[("Preciso marcar horário?", "Sim. O atendimento é com hora marcada pelo WhatsApp, para que cada consulta tenha o tempo necessário."),
         ("O que levar na consulta?", "Caderneta da Criança, exames recentes, receitas em uso e uma lista com as dúvidas da família."),
         ("A consulta serve para criança que está bem?", "Serve. A consulta de rotina acompanha crescimento, desenvolvimento e vacinas e ajuda a prevenir problemas.")]),
"puericultura": dict(
    titulo="Puericultura em Sinop MT | Acompanhamento do Bebê e da Criança | Dra. Tarcila",
    desc="Puericultura em Sinop, MT: acompanhamento de rotina do bebê e da criança, com peso, altura, desenvolvimento, alimentação, sono e vacinas. Pediatra no bairro Santa Cecília.",
    rot="Puericultura",
    h1="Seu filho está crescendo bem?", sub="Puericultura em Sinop, MT",
    lead="Puericultura é o acompanhamento de rotina da criança, mesmo quando está tudo bem. É nessas consultas que a pediatra percebe cedo o que precisa de atenção e responde as dúvidas antes que virem preocupação.",
    cta="Agendar puericultura", msg="Olá! Vim pelo site e gostaria de agendar uma consulta de puericultura com a Dra. Tarcila.",
    ev_t="O que é acompanhado", ev_p="Cada consulta registra a evolução da criança e compara com o esperado para a idade.",
    ev=[("Peso, altura e cabeça", "Medidas registradas nas curvas de crescimento da Caderneta da Criança."),
        ("Desenvolvimento", "Marcos motores, de linguagem e sociais esperados para cada idade."),
        ("Alimentação", "Amamentação, fórmula, introdução alimentar e hábitos da família."),
        ("Sono", "Rotina, despertares e ambiente seguro para dormir."),
        ("Vacinas", "Calendário em dia, com explicação de cada dose."),
        ("Prevenção", "Orientação sobre acidentes, telas, dentes e higiene.")],
    ck_t="Quando fazer as consultas", ck_p="Calendário de referência do Ministério da Saúde. A Dra. Tarcila ajusta para cada criança.",
    ck=["Primeira consulta na primeira semana de vida",
        "Várias consultas ao longo do primeiro ano",
        "Duas consultas no segundo ano",
        "Uma consulta por ano a partir dos 2 anos",
        "Sempre que a família notar algo diferente"],
    alerta=False,
    faq=[("Puericultura é só para bebê?", "Não. O acompanhamento vai do recém nascido à adolescência; o que muda é o intervalo entre as consultas."),
         ("Se meu filho está bem, preciso levar?", "Sim. A puericultura existe justamente para acompanhar a criança saudável e perceber cedo qualquer mudança."),
         ("O que levar?", "A Caderneta da Criança, para registrar medidas e vacinas, e as dúvidas da família.")]),
"bebe": dict(
    titulo="Pediatra para Recém Nascido em Sinop MT | " + D["nome"],
    desc="Pediatra para recém nascido e bebê em Sinop, MT. Primeira consulta depois da maternidade: amamentação, icterícia, umbigo, sono e cuidados em casa. Bairro Santa Cecília.",
    rot="Recém nascido",
    h1="O bebê chegou. E agora?", sub="Pediatra para recém nascido em Sinop, MT",
    lead="Os primeiros dias em casa trazem muitas dúvidas. A primeira consulta com a pediatra serve para avaliar o bebê com calma, apoiar a amamentação e deixar os pais seguros com a rotina nova.",
    cta="Agendar a primeira consulta", msg="Olá! Vim pelo site e gostaria de agendar a primeira consulta do meu bebê com a Dra. Tarcila.",
    ev_t="O que é avaliado na primeira consulta", ev_p="Um exame completo do bebê e uma conversa sem pressa sobre os primeiros dias.",
    ev=[("Exame completo", "Da cabeça aos pés, com atenção aos reflexos e ao tônus."),
        ("Amamentação", "Pega, posição, frequência das mamadas e ganho de peso."),
        ("Icterícia", "Avaliação da pele amarelada, comum nos primeiros dias."),
        ("Coto umbilical", "Limpeza e o que é esperado até a queda."),
        ("Xixi, cocô e cólicas", "O que é normal e quando prestar atenção."),
        ("Sono seguro", "Posição para dormir, berço e ambiente do quarto.")],
    ck_t="O que levar na primeira consulta", ck_p="Ter esses documentos em mãos deixa a consulta mais completa.",
    ck=["Caderneta da Criança",
        "Resumo de alta da maternidade",
        "Resultados dos testes do pezinho, da orelhinha, do olhinho e do coraçãozinho",
        "Anotações sobre mamadas, xixi e cocô",
        "Lista com as dúvidas da família"],
    alerta=False,
    faq=[("Quando fazer a primeira consulta?", "Nos primeiros dias depois da alta, de preferência ainda na primeira semana de vida."),
         ("Dá para conhecer a pediatra antes do parto?", "Sim. A consulta com gestantes serve para tirar dúvidas sobre os primeiros dias do bebê antes do nascimento. Pergunte pelo WhatsApp."),
         ("Icterícia é grave?", "Na maioria das vezes é passageira, mas precisa ser avaliada. Se a pele amarelada aumentar ou o bebê ficar muito sonolento, procure atendimento.")]),
"alimentacao": dict(
    titulo="Introdução Alimentar em Sinop MT | Pediatra " + D["nome"],
    desc="Orientação de introdução alimentar em Sinop, MT: quando começar, sinais de prontidão, como oferecer e como montar o prato do bebê. Pediatra no bairro Santa Cecília.",
    rot="Introdução alimentar",
    h1="Hora de começar a comer?", sub="Introdução alimentar em Sinop, MT",
    lead="A introdução alimentar costuma começar por volta dos 6 meses e traz muitas dúvidas. A consulta ajuda a família a começar com segurança e a montar um plano que caiba na rotina da casa.",
    cta="Agendar orientação alimentar", msg="Olá! Vim pelo site e gostaria de agendar uma orientação de introdução alimentar com a Dra. Tarcila.",
    ev_t="O que é orientado", ev_p="Um plano prático, adaptado à idade do bebê e à rotina da família.",
    ev=[("Sinais de prontidão", "Sustentar a cabeça, sentar com apoio e mostrar interesse pela comida."),
        ("Como oferecer", "Comida amassada, em pedaços ou os dois, de acordo com cada bebê."),
        ("Montagem do prato", "Grupos de alimentos e quantidades para cada idade."),
        ("Alimentos alergênicos", "Quando e como oferecer ovo, amendoim e outros."),
        ("Engasgo e segurança", "Diferença entre engasgo e reflexo de proteção, e cortes seguros."),
        ("Água e bebidas", "O que oferecer e o que evitar no primeiro ano.")],
    ck_t="Quando procurar orientação", ck_p="Quanto antes a família planeja, mais tranquila fica essa fase.",
    ck=["Antes de começar, por volta dos 6 meses",
        "Bebê que recusa a comida ou come muito pouco",
        "Dúvidas sobre alergia alimentar",
        "Bebê prematuro ou com ganho de peso abaixo do esperado",
        "Rotina corrida e pouco tempo para cozinhar"],
    alerta=False,
    faq=[("Com quantos meses começar?", "Por volta dos 6 meses, quando o bebê mostra sinais de prontidão. A idade certa para cada bebê é combinada na consulta."),
         ("Pode dar mel e açúcar?", "Mel não deve ser oferecido antes de 1 ano, e o açúcar deve ser evitado até os 2 anos."),
         ("Precisa de uma consulta só para isso?", "Pode ser parte da consulta de rotina ou uma consulta dedicada, quando a família quer um plano mais detalhado.")]),
}

def pagina_sub(slug):
    s = SUB[slug]; p = "../"
    evals = "\n".join(f'      <div class="eval" data-reveal><h3>{t}</h3><p>{d}</p></div>' for t, d in s["ev"])
    checks = "\n".join(f'      <li>{ico("check")}<span>{c}</span></li>' for c in s["ck"])
    alerta = ('<p class="alert"><b>Urgência:</b> dificuldade para respirar, convulsão, criança muito abatida ou febre em bebê com menos de 3 meses pedem atendimento imediato no pronto atendimento mais próximo.</p>'
              if s["alerta"] else "")
    outros = "\n".join(f'''      <a class="card" href="../{o}/" data-reveal>
        <span class="ico">{ico(i)}</span><h3>{t}</h3><p>{d}</p><span class="more">Ver detalhes {ico("arrow")}</span>
      </a>''' for o, i, t, d in CARDS if o != slug)
    corpo = f'''
<section class="hero">
  <div class="wrap">
    <div class="hero-inner">
      <nav class="crumbs" aria-label="Você está em"><a href="../">Início</a><span aria-hidden="true">/</span><span>{s["rot"]}</span></nav>
      <h1>{s["h1"]} <span class="h1-sub">{s["sub"]}</span></h1>
      <p class="hero-lead">{s["lead"]}</p>
      <div class="hero-actions">
        <a class="btn btn-1" href="{wa(s["msg"])}" target="_blank" rel="noopener">{ico("wa")}{s["cta"]}</a>
        <a class="btn btn-2" href="#consultorio">Ver endereço</a>
      </div>
      {proof()}
    </div>
  </div>
</section>

<section class="sec-alt">
  <div class="wrap">
    <div class="sec-head" data-reveal><p class="kicker">{s["rot"]}</p><h2>{s["ev_t"]}</h2><p>{s["ev_p"]}</p></div>
    <div class="evals">
{evals}
    </div>
  </div>
</section>

<section class="sec-tint">
  <div class="wrap">
    <div class="sec-head" data-reveal><h2>{s["ck_t"]}</h2><p>{s["ck_p"]}</p></div>
    <ul class="checks" data-reveal>
{checks}
    </ul>
    {alerta}
    <a class="btn btn-1" href="{wa(s["msg"])}" target="_blank" rel="noopener">{ico("wa")}Agendar pelo WhatsApp</a>
  </div>
</section>
{consultorio(p)}
{faq(s["faq"])}

<section class="sec-alt">
  <div class="wrap">
    <div class="sec-head" data-reveal><p class="kicker">Outros atendimentos</p><h2>Também na consulta com a Dra. Tarcila</h2></div>
    <div class="cards cards-3">
{outros}
    </div>
  </div>
</section>
{cta(msg=s["msg"])}'''
    crumbs_ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Início", "item": D["dominio"] + "/"},
        {"@type": "ListItem", "position": 2, "name": s["rot"], "item": f'{D["dominio"]}/{slug}/'}]}
    return head(p, s["titulo"], s["desc"], f"/{slug}/", [faq_ld(s["faq"]), crumbs_ld]) + header(p, slug) + corpo + footer(p)

# ---------------------------------------------------------------- gravar e conferir
def gravar(caminho, conteudo):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    io.open(caminho, "w", encoding="utf-8").write(conteudo)

def texto_visivel(doc):
    doc = re.sub(r"(?s)<(script|style|svg)\b.*?</\1>", " ", doc)
    doc = re.sub(r"(?s)<head>.*?</head>", " ", doc)
    attrs = " ".join(re.findall(r'(?:alt|aria-label|title)="([^"]*)"', doc))
    return H.unescape(re.sub(r"<[^>]+>", " ", doc) + " " + attrs)

if __name__ == "__main__":
    saidas = {os.path.join(BASE, "index.html"): pagina_home()}
    for slug, _ in PAGINAS:
        saidas[os.path.join(BASE, slug, "index.html")] = pagina_sub(slug)
    problemas = 0
    for caminho, conteudo in saidas.items():
        gravar(caminho, conteudo)
        vis = texto_visivel(conteudo)
        for m in re.finditer(r"[\-‐-―]", vis):
            problemas += 1
            print("HÍFEN em", os.path.relpath(caminho, BASE), "→", vis[max(0, m.start()-30):m.end()+30].replace("\n", " "))
    print(f"{len(saidas)} páginas geradas. Hífens no texto visível: {problemas}")
