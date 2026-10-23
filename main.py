#!/usr/bin/env python3
import pathlib, re
import inli_check, cdc_check, notify

README = pathlib.Path(__file__).parent / "README.md"


def statuses(markdown):
    """{(section, lieu): état} extrait des tableaux du README."""
    result, section = {}, ""
    for line in markdown.splitlines():
        if line.startswith("## "):
            section = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", line[3:]).strip()
        elif line.startswith("|") and not line.startswith(("| Ville", "| Lieu", "|---")):
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) == 2:
                result[(section, re.sub(r"\[(.*?)\]\(.*?\)", r"\1", cells[0]))] = cells[1]
    return result


parts = ["# Suivi appartements\n"]
for module in (inli_check, cdc_check):
    try:
        parts.append(module.section())
    except Exception as e:   # un site en panne ne bloque pas l'autre
        print(f"[{module.__name__}] ERREUR : {e}")
        parts.append(f"## {module.__name__}\n\n⚠️ Erreur : {e}\n")

new = "\n".join(parts)
old = README.read_text() if README.exists() else ""

before = statuses(old)
news = [f"{section} - {lieu} : {state.replace('**', '')}"
        for (section, lieu), state in statuses(new).items()
        if "🟢" in state and before.get((section, lieu)) != state]
if news:
    notify.send("Nouveaux logements", "\n".join(news), "https://github.com/petergreg/appartments-check")

README.write_text(new)
print("README.md mis à jour")
