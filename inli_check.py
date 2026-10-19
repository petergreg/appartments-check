#!/usr/bin/env python3
import requests

URLS = {
    "Paris":            "https://www.inli.fr/locations/offres/paris-departement_d:75?price_max=900",
    "Clichy":           "https://www.inli.fr/locations/offres/clichy_clichy?price_max=900",
    "Saint-Ouen":       "https://www.inli.fr/locations/offres/saint-ouen-sur-seine_saint-ouen-sur-seine?price_max=900",
    "Levallois-Perret": "https://www.inli.fr/locations/offres/levallois-perret_levallois-perret?price_max=900",
    "Pantin":           "https://www.inli.fr/locations/offres/pantin_pantin?price_max=900",
    "Bagnolet":         "https://www.inli.fr/locations/offres/bagnolet_bagnolet?price_max=900",
    "Vincennes":        "https://www.inli.fr/locations/offres/vincennes_vincennes?price_max=900",
}

EMPTY_MARKER = "Aucune annonce disponible"
PAGE_MARKER = "In'li"
HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) Firefox/130.0"}


def check(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        r.raise_for_status()
    except requests.RequestException:
        return "⚠️ Erreur réseau"
    if PAGE_MARKER not in r.text:
        return "⚠️ Page inattendue"
    return "⚪ Vide" if EMPTY_MARKER in r.text else "🟢 **Annonces disponibles**"


def section():
    lines = ["## In'li\n", "| Ville | État |", "|---|---|"]
    for name, url in URLS.items():
        status = check(url)
        print(f"[inli] {name}: {status}")
        lines.append(f"| [{name}]({url}) | {status} |")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    print(section())