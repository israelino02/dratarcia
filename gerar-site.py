# -*- coding: utf-8 -*-
"""Gera o site da Dra. Tarcila Antunes Banagouro, pediatra em Sinop, MT.

Tudo sai daqui: dados de contato, textos da home e das páginas por palavra chave.
Depois de editar, rode:
    python3 gerar-site.py
Regra do site: nenhum hífen ou travessão no texto visível. O script confere no final.
"""
import io, json, os, re, html as H
from urllib.parse import quote

BASE = os.path.dirname(os.path.abspath(__file__))

# Enquanto o domínio próprio não estiver ligado, o site fica fora do Google (noindex).
# Ao publicar no domínio: PUBLICAR = True, conferir D["dominio"] e rodar de novo.
PUBLICAR = True

# ---------------------------------------------------------------- dados
D = {
    "nome": "Dra. Tarcila Antunes Banagouro",
    "curto": "Dra. Tarcila",
    "crm": "CRM/MT 9131",
    "rqe": "RQE 6722",
    "rua": "Av. Magda de C. Pissinatti, 2099",
    "bairro": "Santa Cecília",
    "cidade": "Sinop",
    "uf": "MT",
    "cep": "78555-440",            # só no JSON-LD (texto visível sem hífen)
    "clinica": "Clínica Teor",
    "hospital": "Hospital Santo Antônio",
    "wa": "5566999134321",
    "tel_txt": "(66) 99913 4321",
    "insta": "dra.tarcila.banagouro",
    "cid": "4104804225488390202",   # Perfil da Empresa no Google
    "lat": -11.834095, "lng": -55.535219,
    "nota": "5,0",
    "dominio": "https://www.dratarcilapediatra.com.br",  # registrado em 13/10/2026 no CPF dela (Registro.br)
}
GOOGLE_PERFIL = f'https://www.google.com/maps?cid={D["cid"]}'
ROTA = "https://www.google.com/maps/dir/?api=1&destination=" + quote(f'{D["clinica"]}, {D["rua"]}, {D["bairro"]}, {D["cidade"]} {D["uf"]}')
MAPA_EMBED = "https://www.google.com/maps?q=" + quote(f'{D["clinica"]}, {D["rua"]}, {D["bairro"]}, {D["cidade"]} {D["uf"]}') + "&z=16&hl=pt-BR&output=embed"
INSTA = f'https://www.instagram.com/{D["insta"]}/'
ID_MEDICA = D["dominio"] + "/#dra-tarcila"

def wa(msg="Olá! Vim pelo site e gostaria de agendar uma consulta com a Dra. Tarcila."):
    return f'https://wa.me/{D["wa"]}?text=' + quote(msg)

def e(t):
    return H.escape(t, quote=True)

def versao(arq):
    """Muda a cada edição do arquivo, para o navegador não ficar com o CSS ou JS antigo."""
    import hashlib
    return hashlib.md5(open(os.path.join(BASE, "assets", arq), "rb").read()).hexdigest()[:8]

# ---------------------------------------------------------------- atendimentos
# slug, rótulo no menu, ícone, título do cartão, texto curto, texto completo (o dela, quando existe)
ATEND = [
    ("consulta", "Consulta pediátrica", "steth", "Consulta Pediátrica",
     "Consulta de rotina ou quando algo preocupa: febre, tosse, alimentação, sono e comportamento.",
     "Acompanhamento individualizado da criança, com avaliação do crescimento, desenvolvimento, alimentação, sono, vacinação e suplementação, além das necessidades específicas de cada fase da infância."),
    ("bebe", "Recém nascido", "heart", "Consulta do Recém Nascido",
     "Primeira consulta depois da maternidade: amamentação, icterícia, umbigo, sono e cuidados em casa.",
     "Avaliação completa dos primeiros dias de vida, incluindo peso, amamentação, icterícia, eliminações, coto umbilical, sono seguro, testes neonatais, vacinação e adaptação do bebê em casa."),
    ("prenatal", "Consulta pré natal", "prenatal", "Consulta Pediátrica Pré Natal",
     "Conhecer a pediatra ainda na gestação e chegar ao nascimento com as dúvidas respondidas.",
     "Consulta realizada ainda durante a gestação para preparar a família para a chegada do bebê. Falamos sobre sala de parto, primeiros cuidados, amamentação, vacinas, testes neonatais, suplementação e as principais dúvidas sobre os primeiros dias de vida."),
    ("parto", "Sala de parto", "assist", "Assistência em Sala de Parto",
     "A pediatra que a família já conhece recebendo o bebê no nascimento.",
     "Acompanhamento pediátrico desde o nascimento, com avaliação e assistência imediata ao recém nascido e realização das intervenções necessárias para uma adaptação segura à vida extrauterina."),
    ("domiciliar", "Atendimento domiciliar", "home", "Atendimento Pediátrico Domiciliar",
     "Consulta completa na casa da família, ideal para recém nascidos e bebês pequenos.",
     "Consulta completa no conforto da casa da família, especialmente conveniente para recém nascidos, bebês pequenos e situações em que o deslocamento pode ser mais difícil."),
    ("telemedicina", "Telemedicina", "video", "Telemedicina",
     "Orientação e acompanhamento por vídeo, com consulta presencial sempre que necessário.",
     "Atendimento pediátrico à distância para situações adequadas a essa modalidade, orientações, acompanhamento e esclarecimento de dúvidas, com indicação de avaliação presencial sempre que necessário."),
    ("puericultura", "Puericultura", "grow", "Puericultura",
     "Acompanhamento do crescimento, do desenvolvimento e das vacinas, mesmo quando está tudo bem.",
     "Acompanhamento de rotina do crescimento, do desenvolvimento e das vacinas, mesmo quando está tudo bem. É nessas consultas que a pediatra percebe cedo o que precisa de atenção."),
    ("alimentacao", "Introdução alimentar", "bowl", "Introdução Alimentar",
     "Quando começar, como oferecer e como montar o prato do bebê, dentro da rotina da família.",
     "Quando começar, como oferecer e como montar o prato do bebê, com um plano prático que caiba na rotina da família e respeite o tempo de cada criança."),
]
ATEND_POR_SLUG = {a[0]: a for a in ATEND}

TEMAS = [
    ("Febre, gripes e viroses", "Avaliação e orientação para cuidar em casa com segurança.", "febre, gripes e viroses"),
    ("Crescimento e desenvolvimento", "Marcos esperados para cada idade, acompanhados de perto.", "crescimento e desenvolvimento"),
    ("Sono do bebê e da criança", "Rotina e hábitos que ajudam a família inteira a dormir.", "sono do bebê"),
    ("Orientação sobre vacinas", "Caderneta em dia, com explicação de cada dose.", "vacinas"),
    ("Consulta do adolescente", "Puberdade, alimentação, telas e saúde emocional.", "consulta do adolescente"),
    ("Amamentação e desmame", "Orientação sobre amamentação, desmame e introdução de novos hábitos alimentares.", "amamentação e desmame"),
]

PILARES = [
    ("Acolhimento", "Um espaço seguro, onde a criança e a família se sentem ouvidas e respeitadas."),
    ("Ciência", "Conhecimento e prática baseados em evidências."),
    ("Desenvolvimento", "Um olhar para a criança de forma integral."),
    ("Prevenção", "Antecipar necessidades e promover saúde."),
    ("Vínculo", "Uma relação de confiança com a criança e com a família."),
]

FORMACAO_BR = [
    ("UNIC", "Graduação em Medicina"),
    ("UFMT", "Residência em Pediatria"),
    (f'{D["crm"]} · {D["rqe"]}', "Registro de especialista em Pediatria"),
    ("Pronto atendimento e sala de parto", "10 anos como médica de pronto atendimento e 7 anos de sala de parto humanizada de médio e alto risco"),
    (D["hospital"], "Atuação na maternidade, em Sinop"),
]
FORMACAO_PT = [
    ("Universidade Católica Portuguesa", "Pós graduação em Neonatologia"),
    ("Sociedade Portuguesa de Infectologia Pediátrica", "Pós graduação em Infectologia Pediátrica"),
    ("Lisboa", "Doutorado em Ciência da Cognição, Linguagem e Neurociência, com investigação voltada ao desenvolvimento infantil"),
    ("Pediatria pública e privada", "Diploma revalidado e atuação nos dois sistemas de saúde em Portugal"),
]

GALERIA = [
    ("clinica-teor-fachada.jpg", "Fachada da Clínica Teor", 880, 1100),
    ("clinica-teor-entrada.jpg", "Entrada", 825, 1100),
    ("clinica-teor-recepcao.jpg", "Recepção", 880, 1100),
    ("clinica-teor-sala-de-espera.jpg", "Sala de espera", 880, 1100),
    ("clinica-teor-corredor.jpg", "Corredor dos consultórios", 825, 1100),
    ("clinica-teor-consultorio.jpg", "Consultório", 855, 840),
]

LOCAIS = [
    ("pin", "Consultório", f'{D["clinica"]}, com hora marcada.'),
    ("assist", "Maternidade", f'Sala de parto e acompanhamento do recém nascido no {D["hospital"]}.'),
    ("home", "Em casa", "Atendimento domiciliar em Sinop, para recém nascidos e bebês pequenos."),
    ("video", "Telemedicina", "Para famílias de Sinop e de outras cidades de Mato Grosso, quando o caso permite."),
]

FAQ_HOME = [
    ("Com quantos dias levar o bebê na primeira consulta?", "O ideal é nos primeiros dias depois da alta da maternidade, de preferência ainda na primeira semana de vida. Leve a Caderneta da Criança, o resumo de alta e os resultados dos testes do pezinho, da orelhinha, do olhinho e do coraçãozinho."),
    ("Até que idade a Dra. Tarcila atende?", "Do recém nascido à adolescência. O intervalo entre as consultas muda com a idade, e a Dra. Tarcila combina com a família quando será o próximo retorno."),
    ("Posso conhecer a pediatra antes do bebê nascer?", 'Pode e deve. A <a href="/prenatal/">consulta pediátrica pré natal</a> acontece ainda na gestação, de preferência no terceiro trimestre, e é nela que se combina a <a href="/parto/">assistência em sala de parto</a>.'),
    ("A Dra. Tarcila atende em casa?", 'Sim. O <a href="/domiciliar/">atendimento domiciliar</a> é feito em Sinop e é especialmente indicado para recém nascidos e bebês pequenos.'),
    ("O atendimento é por convênio?", "O atendimento é particular. É essa escolha que permite consultas com hora marcada e tempo de verdade para cada família. As formas de pagamento são informadas pelo WhatsApp."),
    ("Com que frequência a criança precisa ir ao pediatra?", "No primeiro ano de vida as consultas são mais frequentes, porque o bebê muda muito de um mês para o outro. A partir do segundo ano os retornos ficam mais espaçados."),
    ("Como faço para agendar?", f"Pelo WhatsApp {D['tel_txt']}. O atendimento é com hora marcada, para que cada consulta tenha o tempo de que precisa."),
    ("Onde fica o consultório?", f"Na {D['clinica']}, {D['rua']}, bairro {D['bairro']}, em {D['cidade']}. Há estacionamento em frente à clínica."),
]

# ---------------------------------------------------------------- ícones
SPRITE = '''<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">
  <symbol id="i-wa" viewBox="0 0 32 32"><path d="M16 3C8.8 3 3 8.8 3 16c0 2.3.6 4.5 1.8 6.4L3 29l6.8-1.8c1.9 1 4 1.6 6.2 1.6 7.2 0 13-5.8 13-13S23.2 3 16 3zm0 23.6c-2 0-3.9-.5-5.5-1.5l-.4-.2-4 1.1 1.1-3.9-.3-.4a10.5 10.5 0 1 1 9.1 4.9zm5.9-7.9c-.3-.2-1.9-.9-2.2-1-.3-.1-.5-.2-.7.2s-.8 1-1 1.2c-.2.2-.4.2-.7.1a8.6 8.6 0 0 1-4.3-3.7c-.3-.6.3-.5.9-1.7.1-.2 0-.4 0-.6s-.7-1.7-1-2.3c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.6.1-.9.4-.3.4-1.2 1.2-1.2 2.8s1.2 3.2 1.4 3.5c.2.2 2.4 3.7 5.9 5.1 2.2.9 3 1 4.1.8.7-.1 2-.8 2.2-1.6.3-.8.3-1.5.2-1.6-.1-.2-.3-.3-.6-.4z"/></symbol>
  <symbol id="i-star" viewBox="0 0 24 24"><path d="M12 2.8l2.8 5.8 6.3.9-4.6 4.4 1.1 6.3L12 17.2l-5.6 3 1.1-6.3L2.9 9.5l6.3-.9z"/></symbol>
  <symbol id="i-pin" viewBox="0 0 24 24"><path d="M12 21s-7-6.2-7-11a7 7 0 0 1 14 0c0 4.8-7 11-7 11z"/><circle cx="12" cy="10" r="2.6"/></symbol>
  <symbol id="i-route" viewBox="0 0 24 24"><path d="M3.5 11.2l17-7.7-7.7 17-1.9-7.4z"/></symbol>
  <symbol id="i-ig" viewBox="0 0 24 24"><rect x="3.5" y="3.5" width="17" height="17" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.3" cy="6.7" r=".6"/></symbol>
  <symbol id="i-clock" viewBox="0 0 24 24"><circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/></symbol>
  <symbol id="i-arrow" viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></symbol>
  <symbol id="i-check" viewBox="0 0 24 24"><path d="M4.5 12.5l4.5 4.5 10.5-10.5"/></symbol>
  <symbol id="i-chev" viewBox="0 0 24 24"><path d="M6 9.5l6 6 6-6"/></symbol>
  <symbol id="i-review" viewBox="0 0 24 24"><path d="M4 5h16v11H9l-5 4z"/><path d="M12 8.2l.9 1.9 2 .3-1.5 1.4.4 2-1.8-1-1.8 1 .4-2-1.5-1.4 2-.3z"/></symbol>
  <symbol id="i-prenatal" viewBox="0 0 24 24"><circle cx="12" cy="12" r="8.2"/><path d="M12 9.6c-.9-1.1-2.6-1.1-3.3.1-.6 1.1.2 2.1 3.3 4.4 3.1-2.3 3.9-3.3 3.3-4.4-.7-1.2-2.4-1.2-3.3-.1z"/></symbol>
  <symbol id="i-assist" viewBox="0 0 24 24"><path d="M12 3.5l7.5 3v5.2c0 4.4-3.1 7.6-7.5 8.8-4.4-1.2-7.5-4.4-7.5-8.8V6.5z"/><path d="M12 8.6v6.4M8.8 11.8h6.4"/></symbol>
  <symbol id="i-home" viewBox="0 0 24 24"><path d="M4 11.5L12 4l8 7.5"/><path d="M6.5 10v9.3h11V10"/><path d="M10 19.3v-5h4v5"/></symbol>
  <symbol id="i-video" viewBox="0 0 24 24"><rect x="3.3" y="6.5" width="12" height="11" rx="2.2"/><path d="M15.3 10.3l5.2-3v9.4l-5.2-3z"/></symbol>
  <symbol id="i-steth" viewBox="0 0 24 24"><path d="M6 3.5v5a4 4 0 0 0 8 0v-5"/><path d="M10 12.5v2.5a5 5 0 0 0 10 0v-2"/><circle cx="20" cy="11" r="2"/></symbol>
  <symbol id="i-grow" viewBox="0 0 24 24"><path d="M4 20h16"/><path d="M7 16.5v-3.5M12 16.5V9M17 16.5V5.5"/></symbol>
  <symbol id="i-heart" viewBox="0 0 24 24"><path d="M12 20s-7.5-4.6-7.5-10.2A4.2 4.2 0 0 1 12 7.2a4.2 4.2 0 0 1 7.5 2.6C19.5 15.4 12 20 12 20z"/></symbol>
  <symbol id="i-bowl" viewBox="0 0 24 24"><path d="M3.5 12h17a8.5 8.5 0 0 1-17 0z"/><path d="M15.5 3.5l-3 6"/><path d="M9 20.5h6"/></symbol>
  <symbol id="i-cap" viewBox="0 0 24 24"><path d="M2.5 9.5L12 5l9.5 4.5L12 14z"/><path d="M6.5 11.5v4.2c0 1.6 2.5 3 5.5 3s5.5-1.4 5.5-3v-4.2"/><path d="M21.5 9.5v5"/></symbol>
  <symbol id="i-phone" viewBox="0 0 24 24"><path d="M6.5 4h3l1.5 4-2 1.5a11 11 0 0 0 5.5 5.5L16 13l4 1.5v3a2 2 0 0 1-2.2 2A15.5 15.5 0 0 1 4 6.2 2 2 0 0 1 6.5 4z"/></symbol>
</svg>'''

def ico(nome, cls="ic"):
    fill = nome in ("wa", "star")
    return f'<svg class="{cls}{" fill" if fill else ""}" aria-hidden="true" focusable="false"><use href="#i-{nome}"></use></svg>'

ESTRELAS = '<span class="stars" aria-hidden="true">' + "".join(ico("star") for _ in range(5)) + "</span>"
CORACAO = '<svg class="mq-heart" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 20s-7.5-4.6-7.5-10.2A4.2 4.2 0 0 1 12 7.2a4.2 4.2 0 0 1 7.5 2.6C19.5 15.4 12 20 12 20z"/></svg>'

# ---------------------------------------------------------------- dados estruturados
def ld_medica():
    return {
        "@context": "https://schema.org", "@type": "Physician", "@id": ID_MEDICA,
        "name": D["nome"], "medicalSpecialty": "Pediatric",
        "description": "Pediatra em Sinop, MT. Consulta pediátrica, recém nascido, puericultura, consulta pré natal, sala de parto, atendimento domiciliar e telemedicina.",
        "url": D["dominio"] + "/", "image": D["dominio"] + "/assets/img/dra-tarcila-pediatra-sinop.jpg",
        "logo": D["dominio"] + "/assets/img/logo-simbolo.png",
        "telephone": "+" + D["wa"],
        "priceRange": "$$$",
        "address": {"@type": "PostalAddress", "streetAddress": D["rua"] + ", " + D["clinica"],
                    "addressLocality": D["cidade"], "addressRegion": D["uf"],
                    "postalCode": D["cep"], "addressCountry": "BR"},
        "geo": {"@type": "GeoCoordinates", "latitude": D["lat"], "longitude": D["lng"]},
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
            "opens": "07:00", "closes": "18:00"}],
        "areaServed": [{"@type": "City", "name": "Sinop"}, {"@type": "State", "name": "Mato Grosso"}],
        "hospitalAffiliation": {"@type": "Hospital", "name": D["hospital"],
                                "address": {"@type": "PostalAddress", "addressLocality": D["cidade"], "addressRegion": D["uf"], "addressCountry": "BR"}},
        "alumniOf": [{"@type": "CollegeOrUniversity", "name": "UNIC"},
                     {"@type": "CollegeOrUniversity", "name": "Universidade Federal de Mato Grosso"},
                     {"@type": "CollegeOrUniversity", "name": "Universidade Católica Portuguesa"}],
        "availableService": [{"@type": "MedicalProcedure", "name": a[3]} for a in ATEND],
        "hasMap": GOOGLE_PERFIL, "sameAs": [INSTA, GOOGLE_PERFIL],
        "isAcceptingNewPatients": True, "paymentAccepted": "Particular",
    }

def faq_ld(itens):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", a)}} for q, a in itens]}

# Google Tag Manager (contêiner da Dra. Tarcila). Fora de f-string por causa das chaves do JS.
GTM_ID = "GTM-T77Z8QKZ"
GTM_HEAD = """<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','""" + GTM_ID + """');</script>
<!-- End Google Tag Manager -->"""
GTM_BODY = """<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=""" + GTM_ID + """"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->"""

# ---------------------------------------------------------------- blocos comuns
def head(titulo, desc, url, extra_ld, img_preload=None):
    lds = [ld_medica()] + extra_ld
    ld_html = "\n".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in lds)
    robots = "index, follow, max-image-preview:large" if PUBLICAR else "noindex, nofollow"
    preload = f'<link rel="preload" as="image" href="{img_preload}" fetchpriority="high">\n' if img_preload else ""
    return f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{GTM_HEAD}
<title>{e(titulo)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{D["dominio"]}{url}">
<meta name="geo.region" content="BR-MT">
<meta name="geo.placename" content="Sinop">
<meta name="geo.position" content="{D["lat"]};{D["lng"]}">
<meta property="og:type" content="website">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="{e(D["nome"])}">
<meta property="og:title" content="{e(titulo)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{D["dominio"]}{url}">
<meta property="og:image" content="{D["dominio"]}/assets/img/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#FAF6F2">
<link rel="icon" type="image/png" href="/assets/img/favicon-64.png">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Nunito+Sans:opsz,wght@6..12,400;6..12,600;6..12,700;6..12,800&display=swap">
{preload}<link rel="stylesheet" href="/assets/style.css?v={versao("style.css")}">
<script>document.documentElement.classList.add('js')</script>
{ld_html}
</head>
<body>
{GTM_BODY}
<a class="skip" href="#conteudo">Ir para o conteúdo</a>
<div class="progress" aria-hidden="true"><span id="progress"></span></div>
{SPRITE}'''

def header(atual=None):
    marca = ' aria-current="page"'
    sub = "".join(
        f'<a href="/{slug}/"{marca if slug == atual else ""}>{ico(i)}<span>{rot}</span></a>'
        for slug, rot, i, *_ in ATEND)
    return f'''
<div class="topbar">
  <div class="wrap topbar-in">
    <span class="tb-item">{ico("pin")}{D["cidade"]}, {D["uf"]}</span>
    <span class="tb-item tb-hide">Atendimento particular com hora marcada</span>
    <a class="tb-link" href="{wa()}" target="_blank" rel="noopener">{ico("wa")}{D["tel_txt"]}</a>
  </div>
</div>
<div class="nav-backdrop" id="navBackdrop" aria-hidden="true"></div>
<header class="header" id="header">
  <div class="wrap header-in">
    <a class="brand" href="/" aria-label="{D["nome"]}, pediatra em Sinop. Página inicial">
      <img src="/assets/img/logo-horizontal.png" alt="" width="303" height="66">
    </a>
    <nav class="nav" id="nav" aria-label="Principal">
      <div class="nav-item has-sub">
        <a class="nav-link" href="/#atendimentos">Atendimentos</a>
        <button class="sub-toggle" type="button" aria-expanded="false" aria-controls="sub-atend" aria-label="Mostrar todos os atendimentos">{ico("chev")}</button>
        <div class="sub" id="sub-atend">{sub}</div>
      </div>
      <a class="nav-link" href="/#acompanhamento">Acompanhamento</a>
      <a class="nav-link" href="/#sobre">Sobre</a>
      <a class="nav-link" href="/#espaco">Consultório</a>
      <a class="nav-link" href="/#contato">Contato</a>
      <a class="nav-link" href="/#duvidas">Dúvidas</a>
      <a class="btn btn-1 nav-cta" href="{wa()}" target="_blank" rel="noopener">{ico("wa")}Agendar consulta</a>
    </nav>
    <button class="burger" id="burger" type="button" aria-label="Abrir menu" aria-expanded="false" aria-controls="nav"><span></span><span></span><span></span></button>
  </div>
</header>
<main id="conteudo">'''

def prova():
    return f'''<div class="proof">
        <a href="{GOOGLE_PERFIL}" target="_blank" rel="noopener">{ESTRELAS}<span><b>{D["nota"]}</b> no Google</span></a>
        <span class="proof-sep" aria-hidden="true"></span>
        <span>{D["crm"]} · {D["rqe"]}</span>
      </div>'''

def sec_head(kicker, titulo, texto=None, claro=False, extra=""):
    p = f'<p class="sec-sub reveal d2">{texto}</p>' if texto else ""
    return f'''<header class="sec-head{" sec-head-light" if claro else ""}{extra}">
      <p class="kicker reveal">{kicker}</p>
      <h2 class="reveal d1">{titulo}</h2>
      {p}
    </header>'''

def contato():
    locais = "\n".join(f'''      <div class="local reveal d{n % 4}">
        <span class="local-ic">{ico(i)}</span>
        <h3>{t}</h3>
        <p>{d}</p>
      </div>''' for n, (i, t, d) in enumerate(LOCAIS))
    return f'''
<section class="section contato" id="contato">
  <div class="wrap">
    {sec_head("Consultório e contato", "Pediatra em <em>Sinop, Mato Grosso</em>", f"Consultório com hora marcada na {D['clinica']}. E também na maternidade, em casa e por telemedicina.", claro=True)}
    <div class="locais">
{locais}
    </div>
    <div class="agende-in">
      <div class="mapa reveal">
        <iframe src="{MAPA_EMBED}" title="Mapa da {D["clinica"]}, em {D["cidade"]}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
      </div>
      <div class="agende-info">
        <div class="info-bloco reveal d1">
          <h3>{ico("pin")}Endereço</h3>
          <p>{D["clinica"]}<br>{D["rua"]}<br>{D["bairro"]}, {D["cidade"]}, {D["uf"]}</p>
          <a class="btn btn-line" href="{ROTA}" target="_blank" rel="noopener">{ico("route")}Traçar rota até a clínica</a>
        </div>
        <div class="info-bloco reveal d2">
          <h3>{ico("clock")}Horário do consultório</h3>
          <p class="status" data-status>Segunda a sexta, 07h às 18h</p>
          <ul class="horarios">
            <li data-dia="util"><span>Segunda a sexta</span><b>07h às 18h</b></li>
            <li data-dia="sab"><span>Sábado</span><b>Fechado</b></li>
            <li data-dia="dom"><span>Domingo</span><b>Fechado</b></li>
          </ul>
        </div>
        <div class="info-bloco reveal d3">
          <h3>{ico("wa")}Agendamento</h3>
          <a class="telefone" href="{wa()}" target="_blank" rel="noopener">{D["tel_txt"]}</a>
          <div class="agende-botoes">
            <a class="btn btn-2" href="{wa()}" target="_blank" rel="noopener">{ico("wa")}Chamar no WhatsApp</a>
            <a class="btn btn-line" href="{INSTA}" target="_blank" rel="noopener">{ico("ig")}Instagram</a>
          </div>
        </div>
      </div>
    </div>
    <p class="urgencia reveal"><b>Urgência?</b> Dificuldade para respirar, convulsão, criança muito abatida ou febre em bebê com menos de 3 meses pedem atendimento imediato no pronto atendimento mais próximo.</p>
  </div>
</section>'''

def faq(itens, titulo="Antes de <em>marcar</em>", texto="Ficou alguma pergunta que não está aqui? Chame no WhatsApp e tire a sua dúvida antes de agendar.", msg="Olá! Vim pelo site e tenho uma dúvida sobre o atendimento da Dra. Tarcila."):
    blocos = "\n".join(
        f'        <details class="acc reveal d{min(n, 4)}"{" open" if n == 0 else ""}><summary>{q}</summary><div class="acc-body"><p>{a}</p></div></details>'
        for n, (q, a) in enumerate(itens))
    return f'''
<section class="section faq" id="duvidas">
  <div class="wrap faq-in">
    <div class="faq-side">
      <p class="kicker reveal">Dúvidas frequentes</p>
      <h2 class="reveal d1">{titulo}</h2>
      <p class="reveal d2">{texto}</p>
      <a class="btn btn-1 reveal d3" href="{wa(msg)}" target="_blank" rel="noopener">{ico("wa")}Tirar minha dúvida</a>
    </div>
    <div class="faq-list">
{blocos}
    </div>
  </div>
</section>'''

def footer():
    links = "".join(f'<li><a href="/{slug}/">{rot}</a></li>' for slug, rot, *_ in ATEND)
    return f'''
</main>
<footer class="footer">
  <div class="wrap footer-in">
    <div class="foot-brand">
      <a href="/" aria-label="{D["nome"]}, página inicial"><img src="/assets/img/logo-horizontal.png" alt="{D["nome"]}, pediatra" width="303" height="66" loading="lazy"></a>
      <p>Pediatra em {D["cidade"]}, {D["uf"]}. Do recém nascido à adolescência, do consultório à sala de parto.</p>
      <p class="foot-crm">{D["crm"]} · {D["rqe"]}</p>
      <div class="socials">
        <a href="{INSTA}" target="_blank" rel="noopener" aria-label="Instagram">{ico("ig")}</a>
        <a href="{wa()}" target="_blank" rel="noopener" aria-label="WhatsApp">{ico("wa")}</a>
        <a href="{GOOGLE_PERFIL}" target="_blank" rel="noopener" aria-label="Perfil no Google">{ico("review")}</a>
      </div>
    </div>
    <div class="foot-col">
      <h4>Atendimentos em {D["cidade"]}</h4>
      <ul>{links}</ul>
    </div>
    <div class="foot-col">
      <h4>Contato</h4>
      <ul>
        <li><a href="{wa()}" target="_blank" rel="noopener">WhatsApp <span class="nw">{D["tel_txt"]}</span></a></li>
        <li><a href="{INSTA}" target="_blank" rel="noopener">@{D["insta"]}</a></li>
        <li><a href="{ROTA}" target="_blank" rel="noopener">{D["clinica"]}<br>{D["rua"]}<br>{D["bairro"]}, {D["cidade"]}, {D["uf"]}</a></li>
      </ul>
    </div>
    <div class="foot-col">
      <h4>Consultório</h4>
      <ul class="hours">
        <li><span>Segunda a sexta</span><b>07h às 18h</b></li>
        <li><span>Sábado e domingo</span><b>Fechado</b></li>
      </ul>
      <p class="foot-note">Sala de parto, atendimento domiciliar e telemedicina com horário combinado.</p>
    </div>
  </div>
  <div class="wrap foot-bottom">
    <span>© <span id="ano">2026</span> {D["nome"]} · Pediatra em {D["cidade"]}, {D["uf"]}</span>
    <span>Médica responsável: {D["nome"]}, {D["crm"]}, {D["rqe"]}</span>
  </div>
</footer>
<a class="wa-float" href="{wa()}" target="_blank" rel="noopener" aria-label="Agendar pelo WhatsApp">{ico("wa")}<span class="wa-pulse" aria-hidden="true"></span></a>
<div class="lightbox" id="lightbox" role="dialog" aria-modal="true" aria-label="Foto ampliada" hidden>
  <button class="lb-close" id="lbClose" type="button" aria-label="Fechar">×</button>
  <figure><img id="lbImg" src="" alt=""><figcaption id="lbCap"></figcaption></figure>
</div>
<script src="/assets/site.js?v={versao("site.js")}" defer></script>
</body>
</html>
'''

def card(slug, featured=False, longo=True):
    s, rot, i, titulo, curto, completo = ATEND_POR_SLUG[slug]
    tag = '<span class="card-tag">Do recém nascido à adolescência</span>' if featured else ""
    return f'''      <article class="card{" card-featured" if featured else ""} reveal">
        {tag}<span class="card-ic">{ico(i)}</span>
        <h3>{titulo}</h3>
        <p>{completo if longo else curto}</p>
        <a class="card-link" href="/{s}/">Ver detalhes {ico("arrow")}</a>
      </article>'''

# ---------------------------------------------------------------- home
def pagina_home():
    cards = "\n".join(card(a[0], featured=(n == 0)) for n, a in enumerate(ATEND))
    marquee_itens = [a[1] for a in ATEND] + ["Pediatria além do peso e da medida"]
    marquee = "".join(f"<span>{t}</span>{CORACAO}" for t in marquee_itens) * 2
    temas = "\n".join(f'''      <div class="tema reveal d{n % 3}">
        <span class="tema-n">{n + 1:02d}</span>
        <h3>{t}</h3>
        <p>{d}</p>
        <a href="{wa("Olá! Vim pelo site e gostaria de saber mais sobre " + m + " com a Dra. Tarcila.")}" target="_blank" rel="noopener">Perguntar sobre isso {ico("arrow")}</a>
      </div>''' for n, (t, d, m) in enumerate(TEMAS))
    pilares = "\n".join(f'          <li>{ico("heart")}<span><b>{t}</b> {d}</span></li>' for t, d in PILARES)
    form_br = "\n".join(f'          <li><b>{t}</b><span>{d}</span></li>' for t, d in FORMACAO_BR)
    form_pt = "\n".join(f'          <li><b>{t}</b><span>{d}</span></li>' for t, d in FORMACAO_PT)
    galeria = "\n".join(f'''      <button class="gal-item" type="button" data-src="/assets/img/{arq}" data-cap="{leg}" aria-label="Ampliar foto: {leg}"><img src="/assets/img/{arq}" alt="{leg}, {D["clinica"]}, {D["cidade"]}" loading="lazy" width="{w}" height="{h}"><span class="gal-cap">{leg}</span></button>''' for arq, leg, w, h in GALERIA)
    msg_gest = "Olá! Vim pelo site e gostaria de entender como funciona o acompanhamento da Dra. Tarcila."

    corpo = f'''
<section class="hero">
  <div class="hero-pattern" aria-hidden="true"></div>
  <div class="wrap hero-in">
    <div class="hero-copy">
      <div class="hero-id reveal"><img src="/assets/img/dra-tarcila-pediatra-sinop.jpg" alt="" width="780" height="975"><span><b>{D["nome"]}</b><small>Pediatra · {D["crm"]} · {D["rqe"]}</small></span></div>
      <h1 class="reveal"><span class="h1-kw">Pediatra em {D["cidade"]}, {D["uf"]}<span class="sr">. </span></span>Pediatria <em>Além do Peso e da Medida.</em></h1>
      <p class="hero-promise reveal d1">Do nascimento à adolescência, um acompanhamento que olha para seu filho por inteiro.</p>
      <p class="lede reveal d2">Crescimento, alimentação, sono, desenvolvimento, comportamento e tudo o que faz parte da vida do seu filho também têm espaço na minha consulta.</p>
      <div class="hero-cta reveal d3">
        <a class="btn btn-1 btn-lg" href="{wa()}" target="_blank" rel="noopener">{ico("wa")}Agende uma consulta</a>
        <a class="btn btn-ghost btn-lg" href="#consulta-alem">Como é a consulta</a>
      </div>
      <ul class="hero-badges reveal d4">
        <li>{ico("check")}Atendimento particular</li>
        <li>{ico("check")}Consulta com hora marcada</li>
        <li>{ico("check")}Consultório, domicílio e telemedicina</li>
      </ul>
      <div class="reveal d4">{prova()}</div>
    </div>
    <div class="hero-media reveal d2">
      <figure class="hero-video" id="heroFig">
        <img class="hero-still" src="/assets/img/bebe-hero-poster.jpg" alt="Bebê sorrindo durante a consulta com a pediatra" width="832" height="464" fetchpriority="high">
        <video autoplay muted loop playsinline webkit-playsinline disablepictureinpicture disableremoteplayback preload="auto" tabindex="-1" aria-hidden="true" width="832" height="464" id="heroVideo">
          <source src="/assets/video/bebe-hero.mp4" type="video/mp4">
        </video>
        <img class="hero-anim" data-src="/assets/img/bebe-hero-animado.webp" alt="" aria-hidden="true" width="640" height="358">
      </figure>
    </div>
  </div>
</section>

<div class="marquee" aria-hidden="true"><div class="marquee-track">{marquee}</div></div>

<section class="section consulta-alem" id="consulta-alem">
  <div class="wrap">
    <div class="alem-in">
      <div class="alem-copy">
        <p class="kicker reveal">A consulta</p>
        <h2 class="reveal d1">Na minha consulta, seu filho não vem só para <em>pesar e medir.</em></h2>
        <p class="reveal d2">Claro que eu acompanho o crescimento, examino, avalio o desenvolvimento e vejo se está tudo bem com a saúde dele.</p>
        <p class="reveal d2">Mas também quero saber como ele dorme, como come, do que gosta de brincar, o que mudou na rotina e o que você tem observado em casa.</p>
        <p class="reveal d3">Porque muitas coisas importantes sobre seu filho acontecem longe do consultório.</p>
        <p class="alem-fecho reveal d3">É assim que eu pratico a Pediatria Além do Peso e da Medida.</p>
      </div>
      <div class="alem-lados">
        <div class="lado reveal">
          <span class="lado-tag">No consultório</span>
          <h3>O que eu acompanho</h3>
          <ul>
            <li>{ico("check")}O crescimento</li>
            <li>{ico("check")}O exame</li>
            <li>{ico("check")}O desenvolvimento</li>
            <li>{ico("check")}A saúde dele</li>
          </ul>
        </div>
        <div class="lado lado-2 reveal d1">
          <span class="lado-tag">Além dos números</span>
          <h3>O que eu também quero saber</h3>
          <ul>
            <li>{ico("heart")}Como ele dorme</li>
            <li>{ico("heart")}Como ele come</li>
            <li>{ico("heart")}Do que gosta de brincar</li>
            <li>{ico("heart")}O que mudou na rotina</li>
            <li>{ico("heart")}O que você tem observado em casa</li>
          </ul>
        </div>
      </div>
    </div>
    <div class="alem-temas">
      {sec_head("Na consulta", "O que também faz parte do <em>acompanhamento</em>", "Além do exame, cada consulta abre espaço para o que a família vive em casa.")}
      <div class="temas">
{temas}
      </div>
      <p class="fineprint">A indicação de qualquer conduta depende de consulta médica e avaliação individual.</p>
    </div>
  </div>
</section>

<section class="section gestantes" id="acompanhamento">
  <div class="wrap gest-in">
    <div class="gest-copy">
      <p class="kicker reveal">Acompanhamento</p>
      <h2 class="reveal d1">Você pode conhecer a pediatra do seu bebê <em>antes mesmo de ele nascer.</em></h2>
      <p class="reveal d2">E continuar contando com ela enquanto seu filho cresce.</p>
      <blockquote class="quote reveal d3">
        <p>A Pediatria acompanha seu filho enquanto ele cresce. E a nossa relação pode começar ainda na gestação.</p>
      </blockquote>
      <a class="btn btn-1 reveal d4" href="{wa(msg_gest)}" target="_blank" rel="noopener">{ico("wa")}Conversar pelo WhatsApp</a>
    </div>
    <ol class="jornada">
      <li class="etapa reveal">
        <span class="etapa-n">1</span>
        <h3>Na gestação</h3>
        <p>Podemos conversar sobre a chegada do bebê, os primeiros cuidados, amamentação e as dúvidas que já aparecem antes do nascimento.</p>
        <div class="etapa-links"><a href="/prenatal/">Consulta pré natal {ico("arrow")}</a></div>
      </li>
      <li class="etapa reveal d1">
        <span class="etapa-n">2</span>
        <h3>No nascimento e nos primeiros dias</h3>
        <p>Acompanhamos essa fase de adaptação, a alimentação, o ganho de peso, o sono e os cuidados que começam quando o bebê chega em casa.</p>
        <div class="etapa-links"><a href="/bebe/">Recém nascido {ico("arrow")}</a><a href="/parto/">Sala de parto {ico("arrow")}</a></div>
      </li>
      <li class="etapa reveal d2">
        <span class="etapa-n">3</span>
        <h3>Durante a infância e a adolescência</h3>
        <p>O acompanhamento continua com o crescimento, desenvolvimento, vacinação, alimentação, comportamento e as mudanças de cada idade.</p>
        <div class="etapa-links"><a href="/consulta/">Consulta pediátrica {ico("arrow")}</a></div>
      </li>
    </ol>
  </div>
</section>

<section class="section atend" id="atendimentos">
  <div class="wrap">
    {sec_head("Atendimentos", "Pediatria que acompanha cada fase, <em>do&nbsp;nascimento à adolescência</em>", "Com ciência, cuidado e atenção individualizada, do consultório à sala de parto.")}
    <div class="cards">
{cards}
      <article class="card card-cta reveal">
        <h3>Não sabe por onde começar?</h3>
        <p>Conte pelo WhatsApp a idade do seu filho e o que você precisa. Você recebe a orientação do melhor caminho.</p>
        <a class="btn btn-1" href="{wa("Olá! Vim pelo site e gostaria de entender qual atendimento é o ideal para o meu filho.")}" target="_blank" rel="noopener">{ico("wa")}Conversar no WhatsApp</a>
      </article>
    </div>
  </div>
</section>

<section class="section sobre" id="sobre">
  <div class="wrap sobre-in">
    <div class="sobre-media reveal">
      <span class="shape shape-c" aria-hidden="true"></span>
      <figure class="sobre-photo"><img src="/assets/img/dra-tarcila-consultorio-sinop.jpg" alt="{D["nome"]} no consultório da {D["clinica"]}, em {D["cidade"]}" loading="lazy" width="975" height="1300"></figure>
      <div class="sobre-stamp"><span class="stamp-top">Desde</span><span class="stamp-num">2017</span><span class="stamp-lbl">na pediatria</span></div>
    </div>
    <div class="sobre-copy">
      <p class="kicker reveal">Sobre a Dra. Tarcila</p>
      <h2 class="reveal d1">Pediatra, mãe e defensora da <em>consulta sem pressa</em></h2>
      <p class="reveal d2">Sou pediatra em {D["cidade"]} e acredito que cada consulta precisa de tempo. Tempo para ouvir o que a família percebe em casa, examinar a criança por inteiro e explicar o porquê de cada orientação, sem pressa e sem termos difíceis.</p>
      <p class="reveal d2">Meu trabalho vai além do peso e da medida: acompanho crescimento, desenvolvimento, alimentação, sono e comportamento, para que os pais saiam da consulta seguros sobre o próximo passo.</p>
      <p class="reveal d2">Atuo há 10 anos como médica de pronto atendimento e tenho 7 anos de experiência em sala de parto humanizada de médio e alto risco. Revalidei meu diploma em Portugal, onde trabalhei na pediatria dos sistemas público e privado, e voltei ao Brasil com um olhar ainda mais amplo sobre a infância.</p>
      <ul class="pilares reveal d3">
{pilares}
      </ul>
      <div class="stats reveal d4">
        <div class="stat"><strong><span data-count="10">10</span></strong><span>anos como médica<br>de pronto atendimento</span></div>
        <div class="stat"><strong><span data-count="7">7</span></strong><span>anos em sala de parto<br>de médio e alto risco</span></div>
        <div class="stat"><strong><span data-count="2">2</span></strong><span>países de prática<br>pediátrica</span></div>
      </div>
    </div>
  </div>
</section>

<section class="section formacao" id="formacao">
  <div class="wrap">
    {sec_head("Formação", "Uma trajetória entre o <em>Brasil e Portugal</em>", "Experiências clínicas e acadêmicas nos dois países, que ampliam o olhar sobre a infância.", claro=True)}
    <div class="trilhas">
      <div class="trilha reveal">
        <h3><span>01</span>No Brasil</h3>
        <ol>
{form_br}
        </ol>
      </div>
      <div class="trilha reveal d1">
        <h3><span>02</span>Em Portugal</h3>
        <ol>
{form_pt}
        </ol>
      </div>
    </div>
  </div>
</section>

<section class="section espaco" id="espaco">
  <div class="wrap">
    {sec_head("O espaço", "Um consultório pensado para <em>receber a família</em>", f"Recepção ampla, sala de espera confortável e estacionamento em frente, na {D['clinica']}.")}
  </div>
  <div class="gal-wrap reveal">
    <div class="gallery" id="galeria">
{galeria}
    </div>
  </div>
  <div class="wrap">
    <div class="sl-nav">
      <button class="sl-btn" id="galPrev" type="button" aria-label="Fotos anteriores">{ico("arrow", "ic flip")}</button>
      <button class="sl-btn" id="galNext" type="button" aria-label="Próximas fotos">{ico("arrow")}</button>
    </div>
  </div>
</section>
<section class="section convite" id="convite">
  <div class="wrap">
    <p class="kicker reveal">Agende sua consulta</p>
    <h2 class="reveal d1">Seu filho está crescendo. <em>E eu quero acompanhar muito mais do que os números da curva.</em></h2>
    <p class="convite-texto reveal d2">Seja para começar o acompanhamento ainda na gestação, conhecer uma pediatra para seu bebê ou continuar cuidando da saúde do seu filho em outra fase da infância, podemos conversar.</p>
    <p class="convite-nota reveal d2">Consultas pediátricas particulares em Sinop, MT.</p>
    <a class="btn btn-1 btn-lg reveal d3" href="{wa()}" target="_blank" rel="noopener">{ico("wa")}Agende sua consulta</a>
  </div>
</section>
{contato()}
{faq(FAQ_HOME)}'''
    titulo = f"Pediatra em Sinop MT | {D['nome']}"
    desc = f"Pediatra em Sinop, MT. Pediatria além do peso e da medida, do nascimento à adolescência. Consulta, pré natal, sala de parto, atendimento em casa e telemedicina. {D['crm']}."
    site_ld = {"@context": "https://schema.org", "@type": "WebSite", "name": D["nome"], "url": D["dominio"] + "/", "inLanguage": "pt-BR"}
    return head(titulo, desc, "/", [faq_ld(FAQ_HOME), site_ld], "/assets/img/bebe-hero-poster.jpg") + header() + corpo + footer()

# ---------------------------------------------------------------- páginas por palavra chave
SUB = {
"consulta": dict(
    titulo="Consulta com Pediatra em Sinop MT | " + D["nome"],
    desc="Consulta pediátrica em Sinop, MT. Febre, tosse, alimentação, sono e desenvolvimento avaliados com tempo para a família. CRM/MT 9131 · RQE 6722.",
    h1="Procurando pediatra em Sinop?", sub="Consulta pediátrica em Sinop, MT",
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
    citacao="Meu trabalho vai além do peso e da medida: acompanho crescimento, desenvolvimento, alimentação, sono e comportamento.",
    faq=[("Preciso marcar horário?", "Sim. O atendimento é com hora marcada pelo WhatsApp, para que cada consulta tenha o tempo necessário."),
         ("O que levar na consulta?", "Caderneta da Criança, exames recentes, receitas em uso e uma lista com as dúvidas da família."),
         ("A consulta serve para criança que está bem?", "Serve. A consulta de rotina acompanha crescimento, desenvolvimento e vacinas e ajuda a prevenir problemas."),
         ("O atendimento é por convênio?", "O atendimento é particular. As formas de pagamento são informadas pelo WhatsApp.")]),
"bebe": dict(
    titulo="Pediatra para Recém Nascido em Sinop MT | " + D["nome"],
    desc="Pediatra para recém nascido e bebê em Sinop, MT. Primeira consulta depois da maternidade: amamentação, icterícia, umbigo, sono e cuidados em casa. Também em domicílio.",
    h1="O bebê chegou. E agora?", sub="Pediatra para recém nascido em Sinop, MT",
    lead="Os primeiros dias em casa trazem muitas dúvidas. A primeira consulta com a pediatra serve para avaliar o bebê com calma, apoiar a amamentação e deixar os pais seguros com a rotina nova. No consultório ou em casa.",
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
    citacao="Sigo acompanhando durante a internação, os primeiros cuidados, a amamentação e orientando os próximos passos depois da alta.",
    faq=[("Quando fazer a primeira consulta?", "Nos primeiros dias depois da alta, de preferência ainda na primeira semana de vida."),
         ("A primeira consulta pode ser em casa?", 'Pode. O <a href="/domiciliar/">atendimento domiciliar</a> evita levar o recém nascido para a rua nos primeiros dias.'),
         ("Dá para conhecer a pediatra antes do parto?", 'Sim. A <a href="/prenatal/">consulta pediátrica pré natal</a> serve para tirar dúvidas sobre os primeiros dias do bebê antes do nascimento.'),
         ("Icterícia é grave?", "Na maioria das vezes é passageira, mas precisa ser avaliada. Se a pele amarelada aumentar ou o bebê ficar muito sonolento, procure atendimento.")]),
"prenatal": dict(
    titulo="Consulta Pediátrica Pré Natal em Sinop MT | " + D["nome"],
    desc="Consulta pediátrica pré natal em Sinop, MT: conheça a pediatra do seu bebê ainda na gestação. Sala de parto, amamentação, primeiros cuidados, vacinas e testes neonatais.",
    h1="Conheça a pediatra do seu bebê antes de ele nascer", sub="Consulta pediátrica pré natal em Sinop, MT",
    lead="A consulta pré natal com a pediatra acontece ainda na gestação. É o momento de conhecer quem vai cuidar do seu bebê, entender o que acontece na sala de parto e chegar ao nascimento com as principais dúvidas respondidas.",
    cta="Agendar consulta pré natal", msg="Olá! Vim pelo site e gostaria de agendar uma consulta pediátrica pré natal com a Dra. Tarcila.",
    ev_t="O que conversamos na consulta", ev_p="Uma conversa sem pressa, com a família, sobre a chegada do bebê e os primeiros dias em casa.",
    ev=[("Sala de parto", "O que acontece nos primeiros minutos de vida e como a pediatra acompanha o nascimento."),
        ("Primeiros cuidados", "Banho, coto umbilical, sono seguro e a rotina das primeiras semanas."),
        ("Amamentação", "Pega, frequência das mamadas e como se preparar antes de o bebê chegar."),
        ("Vacinas", "As primeiras doses, ainda na maternidade, e o calendário dos primeiros meses."),
        ("Testes neonatais", "Pezinho, orelhinha, olhinho e coraçãozinho: quando e por que são feitos."),
        ("Suplementação", "Vitaminas indicadas para o bebê e quando começar.")],
    ck_t="Quando marcar", ck_p="De preferência no terceiro trimestre, com tempo para organizar tudo antes do parto.",
    ck=["No terceiro trimestre da gestação",
        "Quando a família quer conhecer a pediatra antes do parto",
        "Para combinar a assistência pediátrica na sala de parto",
        "Gestação de risco ou bebê com algum diagnóstico já no pré natal",
        "Primeiro filho, ou muito tempo desde o último"],
    alerta=False,
    citacao="O nascimento do seu bebê não precisa ser o primeiro encontro com a pediatra que estará ali com vocês. Para mim, esse acompanhamento começa antes.",
    faq=[("Em que fase da gestação marcar?", "De preferência no terceiro trimestre. Assim dá tempo de conversar com calma e combinar a assistência no parto, se a família quiser."),
         ("O pai ou outro acompanhante pode participar?", "Sim. A consulta é pensada para a família inteira que vai receber o bebê."),
         ("A Dra. Tarcila acompanha o parto?", f'Ela faz <a href="/parto/">assistência pediátrica em sala de parto</a> e atua na maternidade do {D["hospital"]}, em Sinop. A consulta pré natal é o primeiro passo para combinar esse acompanhamento.')]),
"parto": dict(
    titulo="Pediatra na Sala de Parto em Sinop MT | " + D["nome"],
    desc="Assistência pediátrica em sala de parto em Sinop, MT, com a pediatra que a família já conhece. Maternidade do Hospital Santo Antônio. 7 anos de sala de parto humanizada de médio e alto risco.",
    h1="Você já pensou em quem vai receber o seu bebê?", sub="Pediatra em sala de parto em Sinop, MT",
    lead="Na hora do nascimento, é a pediatra quem recebe o bebê, faz a primeira avaliação e cuida da adaptação dele à vida fora do útero. Com a Dra. Tarcila, quem chega à sala de parto é alguém que a família já conhece da consulta pré natal.",
    cta="Conversar sobre o parto", msg="Olá! Vim pelo site e gostaria de saber como funciona a assistência da Dra. Tarcila na sala de parto.",
    ev_t="Como é o acompanhamento", ev_p="Do pré natal à alta da maternidade, com a mesma pediatra.",
    ev=[("Antes do parto", "Consulta pré natal para conhecer a família, a gestação e o que importa para vocês nesse nascimento."),
        ("Nos primeiros minutos", "Avaliação e assistência imediata ao recém nascido, com as intervenções necessárias para uma adaptação segura."),
        ("Respeito ao vínculo", "Contato da família com o bebê preservado sempre que as condições do nascimento permitem."),
        ("Durante a internação", "Acompanhamento do bebê na maternidade e orientação sobre os primeiros cuidados."),
        ("Amamentação", "Apoio desde as primeiras mamadas, ainda no hospital."),
        ("Depois da alta", "Orientação dos próximos passos e a primeira consulta do recém nascido.")],
    ck_t="Experiência em sala de parto", ck_p="Uma trajetória construída em nascimentos de todos os tipos.",
    ck=["7 anos de sala de parto humanizada de médio e alto risco",
        "Pós graduação em Neonatologia pela Universidade Católica Portuguesa",
        "10 anos como médica de pronto atendimento",
        f'Atuação na maternidade do {D["hospital"]}, em Sinop',
        "Experiência na pediatria pública e privada em Portugal"],
    alerta=False,
    citacao="Porque nascer é um momento. Cuidar começa antes, e continua depois.",
    faq=[("Em qual hospital a Dra. Tarcila atende o parto?", f'Ela atua na maternidade do {D["hospital"]}, em Sinop. Para outros hospitais, pergunte pelo WhatsApp.'),
         ("Como combinar a presença da pediatra no parto?", 'O primeiro passo é a <a href="/prenatal/">consulta pediátrica pré natal</a>, de preferência no terceiro trimestre. Nela são combinados os detalhes do acompanhamento.'),
         ("A Dra. Tarcila acompanha parto de risco?", "Ela tem 7 anos de experiência em sala de parto humanizada de médio e alto risco. Cada caso é conversado na consulta pré natal.")]),
"domiciliar": dict(
    titulo="Pediatra Domiciliar em Sinop MT | Consulta em Casa | Dra. Tarcila",
    desc="Atendimento pediátrico domiciliar em Sinop, MT: consulta completa no conforto de casa, ideal para recém nascidos e bebês pequenos. Dra. Tarcila Antunes Banagouro, CRM/MT 9131 · RQE 6722.",
    h1="A consulta vai até vocês", sub="Pediatra domiciliar em Sinop, MT",
    lead="Nas primeiras semanas de vida, sair de casa com o bebê nem sempre é simples. No atendimento domiciliar, a Dra. Tarcila faz a consulta completa na casa da família, com o mesmo cuidado e o mesmo tempo da consulta no consultório.",
    cta="Agendar consulta em casa", msg="Olá! Vim pelo site e gostaria de agendar um atendimento pediátrico domiciliar com a Dra. Tarcila.",
    ev_t="Para quem é", ev_p="Especialmente conveniente quando o deslocamento pode ser mais difícil.",
    ev=[("Recém nascidos", "Primeira consulta depois da maternidade, sem expor o bebê ao trânsito e à sala de espera."),
        ("Bebês pequenos", "Acompanhamento dos primeiros meses dentro da rotina da casa."),
        ("Mães no pós parto", "Recuperação de cesárea ou de um parto difícil, quando sair de casa pesa."),
        ("Amamentação em casa", "Orientação da mamada no ambiente onde ela acontece de verdade."),
        ("Rotina do bebê", "Sono, banho e cuidados avaliados no próprio ambiente da criança."),
        ("Deslocamento difícil", "Situações em que levar a criança até o consultório é complicado.")],
    ck_t="O que acontece na visita", ck_p="O cuidado é o mesmo do consultório. Muda só o lugar.",
    ck=["Exame completo do bebê ou da criança",
        "Avaliação do crescimento e do desenvolvimento",
        "Orientação sobre amamentação, sono e cuidados",
        "Revisão da caderneta, das vacinas e dos testes neonatais",
        "Plano claro para os próximos dias e o próximo retorno"],
    alerta=False,
    citacao="Uma consulta completa no conforto da casa da família, especialmente conveniente para recém nascidos e bebês pequenos.",
    faq=[("Em quais regiões a Dra. Tarcila atende em casa?", "Em Sinop. Para endereços mais afastados, consulte pelo WhatsApp."),
         ("Como agendar a consulta em casa?", f"Pelo WhatsApp {D['tel_txt']}, combinando dia, horário e endereço."),
         ("A consulta em casa é diferente da consulta no consultório?", "O cuidado é o mesmo: exame completo, tempo para as perguntas da família e orientação clara do próximo passo.")]),
"telemedicina": dict(
    titulo="Pediatra Online | Telemedicina Pediátrica | Dra. Tarcila, Sinop MT",
    desc="Telemedicina pediátrica com a Dra. Tarcila Antunes Banagouro: orientação, acompanhamento e dúvidas por vídeo, para famílias de Sinop e de Mato Grosso, com avaliação presencial sempre que necessário.",
    h1="Quando a dúvida não pode esperar a próxima consulta", sub="Telemedicina pediátrica em Sinop, MT",
    lead="Nem toda situação precisa de deslocamento. Na teleconsulta, a Dra. Tarcila orienta, acompanha e esclarece dúvidas por vídeo, e indica a avaliação presencial sempre que o caso pede exame físico.",
    cta="Agendar teleconsulta", msg="Olá! Vim pelo site e gostaria de agendar uma teleconsulta pediátrica com a Dra. Tarcila.",
    ev_t="Quando a telemedicina ajuda", ev_p="Para situações adequadas ao atendimento à distância.",
    ev=[("Retornos e acompanhamento", "Revisão da evolução depois de uma consulta presencial."),
        ("Resultados de exames", "Explicação dos resultados e definição do próximo passo."),
        ("Alimentação e sono", "Orientações de rotina, introdução alimentar e hábitos."),
        ("Amamentação", "Dúvidas do dia a dia nas primeiras semanas."),
        ("Família em viagem", "Orientação quando a família está fora de Sinop."),
        ("Dúvidas pontuais", "Perguntas que surgem entre uma consulta e outra.")],
    ck_t="Quando não usar a telemedicina", ck_p="Algumas situações pedem exame presencial ou atendimento de urgência.",
    ck=["Dificuldade para respirar",
        "Febre em bebê com menos de 3 meses",
        "Convulsão ou criança muito abatida",
        "Sinais de desidratação: pouco xixi, boca seca, choro sem lágrimas",
        "Qualquer piora rápida do estado geral"],
    alerta=True,
    citacao="Atendimento à distância para orientações, acompanhamento e dúvidas, com indicação de avaliação presencial sempre que necessário.",
    faq=[("Como funciona a teleconsulta?", "A consulta é agendada pelo WhatsApp e feita por vídeo, no horário combinado. Tenha à mão a Caderneta da Criança e os exames recentes."),
         ("Atende famílias de outras cidades?", "Sim, para situações adequadas ao atendimento à distância. Quando é preciso examinar a criança, a Dra. Tarcila indica a avaliação presencial."),
         ("A telemedicina substitui a consulta presencial?", "Não. Ela complementa o acompanhamento. Exame físico, primeira consulta do recém nascido e situações de urgência pedem atendimento presencial.")]),
"puericultura": dict(
    titulo="Puericultura em Sinop MT | Acompanhamento do Bebê e da Criança | Dra. Tarcila",
    desc="Puericultura em Sinop, MT: acompanhamento de rotina do bebê e da criança, com peso, altura, desenvolvimento, alimentação, sono e vacinas. Pediatra em Sinop.",
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
    citacao="A Pediatria vai além de acompanhar peso e altura. É compreender a criança de forma integral.",
    faq=[("Puericultura é só para bebê?", "Não. O acompanhamento vai do recém nascido à adolescência; o que muda é o intervalo entre as consultas."),
         ("Se meu filho está bem, preciso levar?", "Sim. A puericultura existe justamente para acompanhar a criança saudável e perceber cedo qualquer mudança."),
         ("O que levar?", "A Caderneta da Criança, para registrar medidas e vacinas, e as dúvidas da família.")]),
"alimentacao": dict(
    titulo="Introdução Alimentar em Sinop MT | Pediatra " + D["nome"],
    desc="Orientação de introdução alimentar em Sinop, MT: quando começar, sinais de prontidão, como oferecer e como montar o prato do bebê. Pediatra em Sinop.",
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
    citacao="Um plano prático, que caiba na rotina da casa e respeite o tempo de cada bebê.",
    faq=[("Com quantos meses começar?", "Por volta dos 6 meses, quando o bebê mostra sinais de prontidão. A idade certa para cada bebê é combinada na consulta."),
         ("Pode dar mel e açúcar?", "Mel não deve ser oferecido antes de 1 ano, e o açúcar deve ser evitado até os 2 anos."),
         ("Precisa de uma consulta só para isso?", "Pode ser parte da consulta de rotina ou uma consulta dedicada, quando a família quer um plano mais detalhado.")]),
}

def pagina_sub(slug):
    s = SUB[slug]
    _, rot, icone, titulo_card, _, _ = ATEND_POR_SLUG[slug]
    evals = "\n".join(f'      <div class="eval reveal d{n % 3}"><span class="eval-n">{n + 1:02d}</span><h3>{t}</h3><p>{d}</p></div>' for n, (t, d) in enumerate(s["ev"]))
    checks = "\n".join(f'        <li>{ico("check")}<span>{c}</span></li>' for c in s["ck"])
    alerta = ('<p class="alert"><b>Urgência:</b> dificuldade para respirar, convulsão, criança muito abatida ou febre em bebê com menos de 3 meses pedem atendimento imediato no pronto atendimento mais próximo.</p>'
              if s["alerta"] else "")
    outros = "\n".join(card(a[0], longo=False) for a in ATEND if a[0] != slug)
    corpo = f'''
<section class="hero hero-sub">
  <div class="hero-pattern" aria-hidden="true"></div>
  <img class="hero-mark" src="/assets/img/logo-simbolo.png" alt="" aria-hidden="true" width="512" height="504">
  <div class="wrap">
    <div class="hero-copy hero-copy-sub">
      <nav class="crumbs reveal" aria-label="Você está em"><a href="/">Início</a><span aria-hidden="true">/</span><a href="/#atendimentos">Atendimentos</a><span aria-hidden="true">/</span><span aria-current="page">{rot}</span></nav>
      <p class="kicker reveal">{ico(icone)}{titulo_card}</p>
      <h1 class="reveal d1">{s["h1"]} <span class="h1-sub">{s["sub"]}</span></h1>
      <p class="lede reveal d2">{s["lead"]}</p>
      <div class="hero-cta reveal d3">
        <a class="btn btn-1 btn-lg" href="{wa(s["msg"])}" target="_blank" rel="noopener">{ico("wa")}{s["cta"]}</a>
        <a class="btn btn-ghost btn-lg" href="#contato">Ver endereço</a>
      </div>
      <div class="reveal d4">{prova()}</div>
    </div>
  </div>
</section>

<section class="section evals-sec">
  <div class="wrap">
    {sec_head(rot, s["ev_t"], s["ev_p"])}
    <div class="evals">
{evals}
    </div>
  </div>
</section>

<section class="section quando">
  <div class="wrap quando-in">
    <div class="quando-copy">
      <p class="kicker reveal">{rot} em Sinop</p>
      <h2 class="reveal d1">{s["ck_t"]}</h2>
      <p class="reveal d2">{s["ck_p"]}</p>
      <ul class="checks reveal d2">
{checks}
      </ul>
      {alerta}
      <a class="btn btn-1 reveal d3" href="{wa(s["msg"])}" target="_blank" rel="noopener">{ico("wa")}Agendar pelo WhatsApp</a>
    </div>
    <aside class="medica reveal d2" aria-label="Sobre a pediatra">
      <img src="/assets/img/dra-tarcila-pediatra-sinop.jpg" alt="{D["nome"]}" width="780" height="975" loading="lazy">
      <blockquote><p>{s["citacao"]}</p></blockquote>
      <p class="medica-nome">{D["nome"]}</p>
      <p class="medica-crm">Pediatra · {D["crm"]} · {D["rqe"]}</p>
      <ul class="medica-tags">
        <li>Doutorado em Lisboa</li><li>Pós graduação em Neonatologia</li><li>Residência em Pediatria pela UFMT</li>
      </ul>
      <a class="medica-link" href="/#sobre">Conhecer a trajetória {ico("arrow")}</a>
    </aside>
  </div>
</section>
<section class="section outros">
  <div class="wrap">
    {sec_head("Outros atendimentos", "Também com a <em>Dra. Tarcila</em>", f"Atendimentos em {D['cidade']}, do pré natal à adolescência.")}
    <div class="cards cards-sm">
{outros}
    </div>
  </div>
</section>
{contato()}
{faq(s["faq"])}'''
    crumbs_ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Início", "item": D["dominio"] + "/"},
        {"@type": "ListItem", "position": 2, "name": rot, "item": f'{D["dominio"]}/{slug}/'}]}
    servico_ld = {"@context": "https://schema.org", "@type": "MedicalWebPage",
                  "name": s["titulo"], "url": f'{D["dominio"]}/{slug}/', "inLanguage": "pt-BR",
                  "about": {"@type": "MedicalProcedure", "name": titulo_card},
                  "author": {"@id": ID_MEDICA}, "reviewedBy": {"@id": ID_MEDICA},
                  "audience": {"@type": "PeopleAudience", "geographicArea": {"@type": "City", "name": "Sinop"}}}
    return head(s["titulo"], s["desc"], f"/{slug}/", [faq_ld(s["faq"]), crumbs_ld, servico_ld]) + header(slug) + corpo + footer()

def pagina_404():
    corpo = f'''
<section class="hero hero-sub hero-404">
  <div class="hero-pattern" aria-hidden="true"></div>
  <img class="hero-mark" src="/assets/img/logo-simbolo.png" alt="" aria-hidden="true" width="512" height="504">
  <div class="wrap">
    <div class="hero-copy hero-copy-sub">
      <p class="kicker">Página não encontrada</p>
      <h1>Esta página não existe <span class="h1-sub">Mas a Dra. Tarcila continua atendendo em {D["cidade"]}</span></h1>
      <p class="lede">O endereço pode ter mudado. Volte para o início ou fale direto pelo WhatsApp.</p>
      <div class="hero-cta">
        <a class="btn btn-1 btn-lg" href="/">Ir para o início</a>
        <a class="btn btn-ghost btn-lg" href="{wa()}" target="_blank" rel="noopener">{ico("wa")}Falar no WhatsApp</a>
      </div>
    </div>
  </div>
</section>'''
    return head(f"Página não encontrada | {D['nome']}", "Página não encontrada.", "/404", []).replace(
        '<meta name="robots" content="index, follow, max-image-preview:large">', '<meta name="robots" content="noindex">') + header() + corpo + footer()

# ---------------------------------------------------------------- arquivos de apoio
def sitemap():
    urls = ["/"] + [f"/{a[0]}/" for a in ATEND]
    itens = "\n".join(f"  <url><loc>{D['dominio']}{u}</loc><changefreq>monthly</changefreq><priority>{'1.0' if u == '/' else '0.8'}</priority></url>" for u in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{itens}\n</urlset>\n'

def robots():
    return f"User-agent: *\nAllow: /\n\nSitemap: {D['dominio']}/sitemap.xml\n"

def vercel():
    headers = [{"source": "/assets/(.*)", "headers": [{"key": "Cache-Control", "value": "public, max-age=31536000, immutable"}]}]
    if not PUBLICAR:
        headers.insert(0, {"source": "/(.*)", "headers": [{"key": "X-Robots-Tag", "value": "noindex, nofollow"}]})
    return json.dumps({"$schema": "https://openapi.vercel.sh/vercel.json", "cleanUrls": True, "trailingSlash": True, "headers": headers}, indent=2, ensure_ascii=False) + "\n"

# ---------------------------------------------------------------- gravar e conferir
def gravar(caminho, conteudo):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    io.open(caminho, "w", encoding="utf-8").write(conteudo)

def texto_visivel(doc):
    doc = re.sub(r"(?s)<(script|style|svg)\b.*?</\1>", " ", doc)
    doc = re.sub(r"(?s)<head>.*?</head>", " ", doc)
    attrs = " ".join(re.findall(r'(?:alt|aria-label|title|data-cap)="([^"]*)"', doc))
    return H.unescape(re.sub(r"<[^>]+>", " ", doc) + " " + attrs)

if __name__ == "__main__":
    paginas = {os.path.join(BASE, "index.html"): pagina_home(), os.path.join(BASE, "404.html"): pagina_404()}
    for slug, *_ in ATEND:
        paginas[os.path.join(BASE, slug, "index.html")] = pagina_sub(slug)
    problemas = 0
    for caminho, conteudo in paginas.items():
        gravar(caminho, conteudo)
        vis = texto_visivel(conteudo)
        for m in re.finditer(r"[\-‐-―]", vis):
            problemas += 1
            print("HÍFEN em", os.path.relpath(caminho, BASE), "→", vis[max(0, m.start() - 30):m.end() + 30].replace("\n", " "))
    gravar(os.path.join(BASE, "sitemap.xml"), sitemap())
    gravar(os.path.join(BASE, "robots.txt"), robots())
    gravar(os.path.join(BASE, "vercel.json"), vercel())
    print(f"{len(paginas)} páginas geradas ({'publicável' if PUBLICAR else 'noindex, fora do Google'}). Hífens no texto visível: {problemas}")
