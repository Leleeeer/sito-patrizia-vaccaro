"""Genera il sito statico di patriziavaccaro.net.

Uso: python3 _sorgenti/build.py   (dalla cartella principale del repository)

Sorgenti, tutte in _sorgenti/:
  pagina.html  testi e stile della pagina principale
  articoli.py  articoli (il primo dell'elenco compare per primo sul sito)
  foto.jpg     foto
  fonts/       caratteri
Tutto il resto del repository viene rigenerato: non modificarlo a mano.
"""
import os, re, shutil, sys
sys.path.insert(0, os.path.dirname(__file__))
from articoli import ARTICOLI

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "pagina.html")
OUT = os.path.dirname(BASE)
KEEP = {".git", "_sorgenti", "CNAME", "README.md", ".gitignore"}
DOMINIO = "https://patriziavaccaro.net"

src = open(SRC, encoding="utf-8").read()
css = re.search(r"<style>(.*?)</style>", src, re.S).group(1)
body = src.split("</style>", 1)[1].split("<script>", 1)[0]

# Font ospitati sul sito (niente chiamate a Google)
font_css = """
@font-face { font-family: "Young Serif"; src: url("fonts/young-serif-400.woff2") format("woff2"); font-weight: 400; font-display: swap; }
@font-face { font-family: "Source Sans 3"; src: url("fonts/source-sans-3-400.woff2") format("woff2"); font-weight: 400; font-display: swap; }
@font-face { font-family: "Source Sans 3"; src: url("fonts/source-sans-3-600.woff2") format("woff2"); font-weight: 600; font-display: swap; }
"""
extra_css = """
:root { padding-top: env(safe-area-inset-top, 0px); padding-bottom: env(safe-area-inset-bottom, 0px); }
body { margin: 0; }
img { max-width: 100%; }
[hidden] { display: none !important; }
.cta-card { display: grid; gap: 1rem; align-content: start; border: 1px solid var(--line); border-radius: 6px; padding: 1.75rem; min-width: 0; }
.cta-card .actions { display: flex; flex-wrap: wrap; gap: 0.75rem; }
.pubs { margin-top: 3rem; display: grid; gap: 0.75rem; max-width: var(--measure); }
.pubs h3 { margin-bottom: 0.25rem; }
.pubs ul { margin: 0; padding-left: 1.1rem; display: grid; gap: 0.4rem; }
.article { max-width: 68ch; margin: 0 auto; }
.article h1 { font-size: var(--step-3); margin-top: 0.75rem; }
.article .body { display: grid; gap: 1.1rem; margin-top: 2rem; }
.article .back { display: inline-block; margin-top: 3rem; }
.article .body h2 { font-size: var(--step-1); margin-top: 1rem; }
.article .body h3 { font-size: var(--step-0); margin-top: 0.5rem; }
.article .body hr { border: 0; border-top: 1px solid var(--line); width: 100%; margin: 1rem 0 0; }
.article .body ul { margin: 0; padding-left: 1.1rem; display: grid; gap: 0.4rem; }
.posts li { grid-template-columns: 1fr; }
"""
style = font_css + css + extra_css

# Contatti: il modulo diventa "Scrivimi"
cta = """<div class="cta-card">
        <h3>Scrivimi</h3>
        <p style="color:var(--muted)">Puoi scrivermi un'email o chiamarmi per richiedere un primo colloquio o informazioni su gruppi e proposte per aziende.</p>
        <div class="actions">
          <a class="btn primary" href="mailto:patrizia.vaccaro@gmail.com?subject=Richiesta%20primo%20colloquio">Scrivimi</a>
          <a class="btn ghost" href="tel:+393393721226">Chiama</a>
        </div>
      </div>"""
body = re.sub(r'<form id="modulo".*?</form>', cta, body, flags=re.S)
body = body.replace('<span>339 372 1226</span>', '<a href="tel:+393393721226">339 372 1226</a>')
body = body.replace('<span>patrizia.vaccaro@gmail.com</span>', '<a href="mailto:patrizia.vaccaro@gmail.com">patrizia.vaccaro@gmail.com</a>')
body = body.replace(DOMINIO + "/20", "/20")
body = body.replace('    <span>Privacy</span>\n', '')

pubs = """
      <div class="pubs">
        <h3>Pubblicazioni e articoli su altre riviste</h3>
        <ul>
          <li><a href="https://www.stateofmind.it/2017/10/infertilita-uomini-psicologia/">Infertilità. Dove sono finiti gli uomini?</a> – State of Mind, 2017</li>
          <li><a href="https://www.stateofmind.it/2017/11/mindfulness-sport/">Mindfulness e sport: lasciar andare e vincere</a> – State of Mind, 2017</li>
          <li><a href="https://www.stateofmind.it/2015/10/fecondazione-assistita-comunicarlo-bambini/">E adesso come glielo dico? Come comunicare ai bambini di essere nati dalla fecondazione assistita</a> – State of Mind, 2015</li>
          <li><a href="https://www.stateofmind.it/2015/03/infertilita-psicoterapia-cognitiva/">Infertilità: la psicoterapia cognitiva serve più del farmaco</a> – State of Mind, 2015</li>
          <li><a href="http://formazionecontinuainpsicologia.it/fecondazione-assistita-e-adesso-come-glielo-dico/">Mamma, papà… come sono nato?</a> – Psicologi@lavoro</li>
          <li><a href="http://formazionecontinuainpsicologia.it/cosa-farne-dellinfertilita-quando-la-psicologia-da-un-mano-alla-biologia/">Cosa farne dell'infertilità? Quando la psicologia dà una mano alla biologia</a> – Psicologi@lavoro</li>
          <li><a href="http://formazionecontinuainpsicologia.it/la-consulenza-psicologica-in-coppie-con-problemi-d-infertilita/">La consulenza psicologica in coppie con problemi di fertilità</a> – Psicologi@lavoro</li>
          <li>P. Vaccaro, <em>Equilibri interrotti. Studio sperimentale di terapia cognitiva di gruppo in pazienti con amenorrea ipotalamica</em>, Edizioni Accademiche Italiane, 2015</li>
        </ul>
      </div>"""
# Elenco articoli generato da articoli.py, senza date, seguito dalle pubblicazioni
lista = "\n".join(f'        <li><a href="/{a["data"].replace("-", "/")}/{a["slug"]}/">{a["titolo"]}</a></li>' for a in ARTICOLI)
body, n = re.subn(r'<ul class="posts">.*?</ul>', '<ul class="posts">\n' + lista + '\n      </ul>' + pubs, body, count=1, flags=re.S)
assert n == 1

header = re.search(r'<header class="top">.*?</header>', body, re.S).group(0)
footer = re.search(r'<footer>.*?</footer>', body, re.S).group(0)
header_sub = header.replace('href="#inizio"', 'href="/"').replace('href="#', 'href="/#')
body_home = body.replace('href="#inizio"', 'href="/"')

DESC = "Patrizia Vaccaro, psicologa e psicoterapeuta a Milano e online. Giovani adulti, adulti e coppie: transizioni di vita, stress e ansia, relazioni, salute della donna, persone e intelligenza artificiale."

def page(title, desc, path, content, tipo="website"):
    return f"""<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{DOMINIO}{path}">
<meta property="og:title" content="{title.replace(chr(39), '&#39;')}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{DOMINIO}{path}">
<meta property="og:image" content="{DOMINIO}/foto.jpg">
<meta property="og:locale" content="it_IT">
<meta property="og:type" content="{tipo}">
<link rel="icon" href="/foto.jpg">
<link rel="stylesheet" href="/style.css">
<script data-goatcounter="https://patriziavaccaro.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>
</head>
<body>
{content}
</body>
</html>
"""

def relativize(rel, text):
    depth = rel.count("/")
    pre = "../" * depth
    text = text.replace('href="/', 'href="' + (pre or "./")).replace('src="/', 'src="' + pre)
    text = text.replace('url=/', 'url=' + (pre or "./"))
    return text.replace('href="./"', 'href="./"')

def write(rel, text):
    if rel.endswith(".html"):
        text = relativize(rel, text)
    p = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(text)

for name in os.listdir(OUT):
    if name in KEEP:
        continue
    p = os.path.join(OUT, name)
    shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
write("style.css", style.strip() + "\n")
shutil.copy(os.path.join(BASE, "foto.jpg"), os.path.join(OUT, "foto.jpg"))
shutil.copytree(os.path.join(BASE, "fonts"), os.path.join(OUT, "fonts"))

# Home: i link agli articoli diventano relativi
write("index.html", page("Patrizia Vaccaro – Psicologa e psicoterapeuta a Milano e online", DESC, "/", body_home))

# Articoli, agli stessi indirizzi del vecchio sito
for a in ARTICOLI:
    y, m, d = a["data"].split("-")
    path = f"/{y}/{m}/{d}/{a['slug']}/"
    content = f"""{header_sub}
<main class="band">
  <div class="wrap">
    <article class="article">
      <p class="eyebrow"><time datetime="{a['data']}">{a['data_it']}</time></p>
      <h1>{a['titolo']}</h1>
      <div class="body">{a['html']}</div>
      <a class="back" href="/#articoli">← Tutti gli articoli</a>
    </article>
  </div>
</main>
{footer}"""
    desc = a.get("descrizione") or re.sub(r"<[^>]+>", "", a["html"]).strip().split("\n")[0][:155].rsplit(" ", 1)[0] + "…"
    write(path.strip("/") + "/index.html", page(f"{a['titolo']} – Patrizia Vaccaro", desc.replace('"', "&quot;"), path, content, "article"))

# Vecchi indirizzi del sito WordPress: rimandano alla sezione giusta
redirects = {
    "about": "/#chi-sono", "chi-sono": "/#chi-sono", "cosa-faccio": "/#di-cosa-mi-occupo",
    "di-cosa-mi-occupo": "/#di-cosa-mi-occupo", "psicoterapia-e-infertilita": "/#di-cosa-mi-occupo",
    "persone-e-intelligenza-artificiale": "/#persone-e-ia", "articoli": "/#articoli",
    "contatti": "/#contatti", "contatti-2015": "/#contatti",
    "la-psicoterapia-cognitiva": "/#di-cosa-mi-occupo", "home": "/", "home-3": "/", "link": "/", "eventi": "/",
}
for slug, target in redirects.items():
    write(f"{slug}/index.html", f"""<!doctype html><html lang="it"><head><meta charset="utf-8">
<title>Patrizia Vaccaro</title><link rel="canonical" href="{DOMINIO}{target}">
<meta http-equiv="refresh" content="0; url={target}"></head>
<body><p><a href="{target}">Vai alla pagina</a></p></body></html>
""")

write("404.html", page("Pagina non trovata – Patrizia Vaccaro", DESC, "/404.html", f"""{header_sub}
<main class="band"><div class="wrap"><div class="article">
<h1>Pagina non trovata</h1>
<p style="margin-top:1rem">La pagina che cercavi non esiste più. <a href="/">Torna alla pagina iniziale</a>.</p>
</div></div></main>
{footer}"""))
write(".nojekyll", "")
write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {DOMINIO}/sitemap.xml\n")
urls = ["/"] + [f"/{a['data'].replace('-', '/')}/{a['slug']}/" for a in ARTICOLI]
write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
      + "".join(f"  <url><loc>{DOMINIO}{u}</loc></url>\n" for u in urls) + "</urlset>\n")
print("ok")
