import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from urllib.parse import urljoin

PAGINA = "https://www.vozpopuli.com/economia"
ARCHIVO_RSS = "vozpopuli-economia.xml"

cabeceras = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/124.0 Safari/537.36"
    )
}

respuesta = requests.get(PAGINA, headers=cabeceras, timeout=30)
respuesta.raise_for_status()

sopa = BeautifulSoup(respuesta.text, "html.parser")

noticias = []
vistos = set()

for enlace in sopa.find_all("a", href=True):
    titulo = enlace.get_text(" ", strip=True)
    url = urljoin(PAGINA, enlace["href"])
    url = url.split("?")[0].split("#")[0]

    if (
        titulo
        and len(titulo) >= 20
        and url.startswith("https://www.vozpopuli.com/economia/")
        and url.endswith(".html")
        and url not in vistos
    ):
        vistos.add(url)
        noticias.append((titulo, url))

generador = FeedGenerator()
generador.id(PAGINA)
generador.title("Vozpópuli - Economía")
generador.description("Últimas noticias de Economía publicadas por Vozpópuli")
generador.link(href=PAGINA, rel="alternate")
generador.link(
    href="https://raw.githubusercontent.com/plis2100/rss-vozpopuli-economia/main/vozpopuli-economia.xml",
    rel="self"
)
generador.language("es")

for titulo, url in noticias[:50]:
    entrada = generador.add_entry()
    entrada.id(url)
    entrada.title(titulo)
    entrada.link(href=url)

generador.rss_file(ARCHIVO_RSS, pretty=True)

print(f"RSS creada con {len(noticias[:50])} noticias")
