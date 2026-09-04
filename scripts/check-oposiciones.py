#!/usr/bin/env python3
"""Genera datos para el monitor de oposiciones.

La ejecución no falla si las fuentes oficiales cambian o no permiten
consultas automatizadas: conserva el último listado y registra la fecha.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

DATA_FILE = Path("data/oposiciones.json")


def load_existing_items() -> list[dict]:
    if not DATA_FILE.exists():
        return []
    try:
        with DATA_FILE.open(encoding="utf-8") as handle:
            payload = json.load(handle)
        items = payload.get("oposiciones", [])
        return items if isinstance(items, list) else []
    except (OSError, json.JSONDecodeError):
        return []


def main() -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "lastUpdated": datetime.now(timezone.utc).isoformat(),
        "sources": [
            {
                "name": "DOGV",
                "url": "https://dogv.gva.es/",
                "status": "pending-source-integration"
            },
            {
                "name": "BOP de Valencia",
                "url": "https://bop.dival.es/",
                "status": "pending-source-integration"
            }
        ],
        "oposiciones": load_existing_items()
    }
    with DATA_FILE.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    print(f"Datos actualizados: {len(payload['oposiciones'])} resultados conservados")


if __name__ == "__main__":
    main()
