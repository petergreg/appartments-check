#!/usr/bin/env python3
import pathlib
import inli_check, cdc_check

README = pathlib.Path(__file__).parent / "README.md"

parts = ["# Suivi appartements\n"]
for module in (inli_check, cdc_check):
    try:
        parts.append(module.section())
    except Exception as e:   # un site en panne ne bloque pas l'autre
        print(f"[{module.__name__}] ERREUR : {e}")
        parts.append(f"## {module.__name__}\n\n⚠️ Erreur : {e}\n")

README.write_text("\n".join(parts))
print("README.md mis à jour")