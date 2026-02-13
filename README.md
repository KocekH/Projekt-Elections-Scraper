# Projekt-Elections-Scraper
Web scraper výsledků voleb do Poslanecké sněmovny 2017 z volby.cz (export do CSV)

# Projekt-Elections-Scraper

Web scraper výsledků voleb do Poslanecké sněmovny 2017 z volby.cz (export do CSV).

---

## Popis projektu

Tento projekt slouží k automatizovanému získávání výsledků hlasování
z parlamentních voleb v roce 2017.

Skript stáhne výsledky pro všechny obce z vybraného územního celku
(stránka typu `ps32`) a uloží je do CSV souboru.

Zdroj dat:  
https://www.volby.cz/pls/ps2017nss/

---

## Instalace knihoven

Doporučuje se použít virtuální prostředí.

### 1. Ověření verze pip

```bash
pip --version

2. Instalace závislostí
pip install -r requirements.txt

Spuštění projektu

Program vyžaduje dva povinné argumenty:

python main.py <odkaz-uzemniho-celku> <vystupni-soubor.csv>

Argumenty:

Odkaz na územní celek (stránka typu ps32)

Název výstupního CSV souboru

Ukázka použití
Prostějov
python main.py \
"https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103" \
"vysledky_prostejov.csv"

Brno-město
python main.py \
"https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6202" \
"vysledky_brno_mesto.csv"

Karlovy Vary
python main.py \
"https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=5&xnumnuts=4102" \
"vysledky_karlovy_vary.csv"

Výstup

Výstupem je CSV soubor obsahující:

kód obce

název obce

počet registrovaných voličů

počet vydaných obálek

počet platných hlasů

počet hlasů pro jednotlivé kandidující strany
