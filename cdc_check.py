#!/usr/bin/env python3
import json, time, requests

BASE_URL = "https://www.cdc-habitat.fr"
PAGE = f"{BASE_URL}/recherche/location?nbLoyerMax=900&cdTypeBien[]=Appartement"
SEARCH_URL = f"{BASE_URL}/Recherche/search"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"

PARIS = "PARIS (" + ",".join(f"750{n:02d}" for n in range(1, 21)) + ")"

LIEUX = [
    PARIS,
    "CLICHY (92110)",
    "ST OUEN SUR SEINE (93400)",
    "NEUILLY SUR SEINE (92200)",
    "LEVALLOIS PERRET (92300)",
    "PANTIN (93500)",
    "AUBERVILLIERS (93300)",
    "LES LILAS (93260)",
    "BAGNOLET (93170)",
    "VINCENNES (94300)",
]


def label(lieu):
    return "PARIS (75)" if lieu == PARIS else lieu


def search(session, lieu):
    data = {
        "cdTypage": "location",
        "order": "loyer_asc",
        "pagerGo": "",
        "newSearch": "",
        "lbLieu": lieu,
        "nbLoyerMin": "",
        "nbLoyerMax": "5000",
        "cdTypeBien[]": "Appartement",
        "nbSurfaceMin": "",
        "nbSurfaceMax": "",
        "expandToLotsBounds": "1",
    }
    headers = {"X-Requested-With": "XMLHttpRequest", "Referer": PAGE, "Origin": BASE_URL}
    r = session.post(SEARCH_URL, data=data, headers=headers, timeout=20)
    r.raise_for_status()
    return json.loads(r.text).get("lots") or []


def status(lots):
    if not lots:
        return "⚪ Vide"
    prix = []
    for lot in lots:
        try:
            prix.append(float(str(lot["nb_prix"]).replace(",", ".")))
        except (KeyError, ValueError):
            pass
    detail = f", dès {min(prix):.0f} €" if prix else ""
    return f"🟢 **{len(lots)} logement(s){detail}**"


def section():
    session = requests.Session()
    session.headers.update({"User-Agent": UA})
    try:
        session.get(PAGE, timeout=20)   # cookie de session
    except requests.RequestException as e:
        print(f"[cdc] page inaccessible ({e})")

    lines = [f"## [CDC Habitat]({PAGE})\n", "| Lieu | État |", "|---|---|"]
    for lieu in LIEUX:
        try:
            st = status(search(session, lieu))
        except (requests.RequestException, ValueError) as e:
            print(f"[cdc] {label(lieu)}: erreur ({e})")
            st = "⚠️ Erreur"
        print(f"[cdc] {label(lieu)}: {st}")
        lines.append(f"| {label(lieu)} | {st} |")
        time.sleep(1)
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    print(section())