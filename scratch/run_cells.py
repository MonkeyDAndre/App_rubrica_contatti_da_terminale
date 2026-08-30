"""Esegue le celle di codice di ContactEase.ipynb tranne quella con main().

Verifica che classi, funzioni e la cella di test (12) girino senza errori.
La cella 11 (`main()`) e' interattiva e viene saltata.
"""

import os
import nbformat

QUI = os.path.dirname(__file__)
NOTEBOOK = os.path.join(QUI, "..", "ContactEase.ipynb")

nb = nbformat.read(NOTEBOOK, as_version=4)

tipi = [c.cell_type for c in nb.cells]
print("Celle:", len(nb.cells), tipi)
assert len(nb.cells) == 12, "attese 12 celle"
assert tipi == ["markdown", "code", "markdown", "code", "markdown", "code",
                "markdown", "code", "markdown", "code", "code", "code"]
assert "%pip install -q rich" in nb.cells[1].source

# Namespace condiviso in cui eseguire le celle, come farebbe il kernel.
ns = {"__name__": "__main__"}
for i, cella in enumerate(nb.cells):
    if cella.cell_type != "code":
        continue
    src = cella.source
    if src.strip().endswith("main()") and "def main" not in src:
        print(f"cella {i}: SALTATA (avvio interattivo)")
        continue
    # Le righe magiche ("%pip install", "!pip") non sono Python: le togliamo.
    righe = [r for r in src.splitlines()
             if not r.lstrip().startswith(("%pip", "!pip"))]
    exec(compile("\n".join(righe), f"<cella {i}>", "exec"), ns)
    print(f"cella {i}: OK")

print("\nTutte le celle di codice (tranne main) eseguite senza errori.")
