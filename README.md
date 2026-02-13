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
```

### 2. Instalace závislostí

```bash
pip install -r requirements.txt
```

---

## Spuštění projektu

Program vyžaduje dva povinné argumenty:

```bash
python main.py <odkaz-uzemniho-celku> <vystupni-soubor.csv>
```

### Argumenty

1. Odkaz na územní celek (stránka typu `ps32`)
2. Název výstupního CSV souboru

---

## Ukázka použití

### Hlavní město Praha

```bash
python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=1&xnumnuts=1100" "vysledky_praha.csv"
```

### Prostějov

```bash
python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103" "vysledky_prostejov.csv"
```

### Brno-město

```bash
python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6202" "vysledky_brno_mesto.csv"
```

### Karlovy Vary

```bash
python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=5&xnumnuts=4102" "vysledky_karlovy_vary.csv"
```

---

## Výstup

Výstupem je CSV soubor obsahující:

- kód obce
- název obce
- počet registrovaných voličů
- počet vydaných obálek
- počet platných hlasů
- počet hlasů pro jednotlivé kandidující strany

Ukázka struktury CSV:

```csv
code,location,registered,envelopes,valid,...
529303,Benešov,13104,8485,8437,...
...
```

---

## Použité technologie

- Python 3
- requests
- BeautifulSoup4
- csv

---

## Autor

Projekt vznikl v rámci Python Akademie od Engeta.
