# appartments-check

Surveille les logements à louer chez In'li et CDC Habitat (loyer max 900 €, Paris et petite couronne). Le README.md sert de tableau de bord.

- `README.md` est généré par `main.py`, puis commité par GitHub Actions (cron toutes les 15 min, déclenché aussi par cron-job.org via `workflow_dispatch`) : ne pas l'éditer à la main
- Un nouveau site = un module exposant `section()` qui renvoie du markdown, à ajouter dans `main.py`
- La limite de loyer (900) est codée en dur dans les URLs de `inli_check.py` et dans `cdc_check.py` : à changer aux deux endroits
- `main.py` compare l'ancien et le nouveau README et envoie une notification ntfy (`notify.py`) quand une ligne passe à 🟢 ou change de nombre ; le topic vient du secret GitHub Actions `NTFY_TOPIC` (sans lui, aucun envoi)
- Lancer en local : `python main.py`
