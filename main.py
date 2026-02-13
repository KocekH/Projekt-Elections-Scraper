#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import sys
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


HEADERS = {"User-Agent": "Mozilla/5.0 (Engeto-Elections-Scraper)"}


def clean_number(text):
    """Remove spaces and non-breaking spaces from numbers."""
    return text.replace("\xa0", "").replace(" ", "").strip()


def get_soup(url):
    """Download page and return BeautifulSoup object."""
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    r.encoding = "utf-8"  # important for Czech diacritics
    return BeautifulSoup(r.text, "html.parser")


def get_municipalities(ps32_url):
    """
    From ps32 page get list of municipalities.
    Returns list of tuples: (code, name, detail_url)
    """
    soup = get_soup(ps32_url)
    municipalities = []

    for row in soup.find_all("tr"):
        code_td = row.find("td", class_="cislo")
        name_td = row.find("td", class_="overflow_name")
        if not code_td or not name_td:
            continue

        a = code_td.find("a")
        if not a:
            continue

        code = clean_number(a.get_text(strip=True))
        href = a.get("href", "")

        # municipality detail page contains ps311 in link
        if not code.isdigit() or "ps311" not in href:
            continue

        detail_url = urljoin(ps32_url, href)
        name = name_td.get_text(" ", strip=True)
        municipalities.append((code, name, detail_url))

    if not municipalities:
        raise ValueError("Nepodařilo se najít obce na zadané stránce (ps32).")

    return municipalities


def get_turnout_and_parties(ps311_url):
    """
    From municipality detail (ps311) get turnout + party votes.
    Returns: (turnout_dict, parties_dict)
    """
    soup = get_soup(ps311_url)

    def find_cell(headers_value):
        td = soup.find("td", class_="cislo", attrs={"headers": headers_value})
        return clean_number(td.get_text(strip=True)) if td else ""

    turnout = {
        "registered": find_cell("sa2"),
        "envelopes": find_cell("sa3"),
        "valid": find_cell("sa6"),
    }

    parties = {}

    # party tables contain rows with: number, party name, votes, percent
    for row in soup.find_all("tr"):
        tds = row.find_all("td")
        if len(tds) < 4:
            continue

        order = tds[0].get_text(strip=True)
        if not order.isdigit():
            continue

        party_name = tds[1].get_text(" ", strip=True)
        votes = clean_number(tds[2].get_text(strip=True))

        if party_name and votes.isdigit():
            parties[party_name] = votes

    if not parties:
        raise ValueError("Nepodařilo se načíst hlasy stran z detailu obce.")

    return turnout, parties


def write_csv(filename, header, rows):
    """
    Write CSV as UTF-8 with BOM so Excel opens Czech characters correctly.
    """
    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main():
    if len(sys.argv) != 3:
        print("CHYBA: Spusť se 2 argumenty: <URL> <vystup.csv>")
        print('Příklad: python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103" "vysledky.csv"')
        return

    url = sys.argv[1].strip()
    output_file = sys.argv[2].strip()

    if "volby.cz/pls/ps2017nss/" not in url or "ps32" not in url:
        print("CHYBA: První argument musí být odkaz na stránku typu ps32 (výběr obce v okrese).")
        return

    if not output_file.lower().endswith(".csv"):
        print("CHYBA: Druhý argument musí být název CSV souboru končící na .csv")
        return

    try:
        print("STAHUJI DATA Z VYBRANEHO URL:", url)
        print("UKLADAM DO SOUBORU:", output_file)

        municipalities = get_municipalities(url)
        print("NALEZENO OBCÍ:", len(municipalities))

        # get party columns from first municipality
        first_code, first_name, first_detail = municipalities[0]
        turnout0, parties0 = get_turnout_and_parties(first_detail)
        party_names = list(parties0.keys())

        header = ["code", "location", "registered", "envelopes", "valid"] + party_names
        rows = []

        # first row
        row0 = {
            "code": first_code,
            "location": first_name,
            "registered": turnout0["registered"],
            "envelopes": turnout0["envelopes"],
            "valid": turnout0["valid"],
        }
        for p in party_names:
            row0[p] = parties0.get(p, "0")
        rows.append(row0)

        # remaining municipalities
        count = 1
        for code, name, detail_url in municipalities[1:]:
            count += 1
            if count % 100 == 0:
                print("PROGRESS:", count, "/", len(municipalities), "obcí...")

            turnout, parties = get_turnout_and_parties(detail_url)
            row = {
                "code": code,
                "location": name,
                "registered": turnout["registered"],
                "envelopes": turnout["envelopes"],
                "valid": turnout["valid"],
            }
            for p in party_names:
                row[p] = parties.get(p, "0")
            rows.append(row)

        write_csv(output_file, header, rows)
        print("UKONCUJI election-scraper")

    except Exception as e:
        print("CHYBA:", e)


if __name__ == "__main__":
    main()
