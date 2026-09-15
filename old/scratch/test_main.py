"""Test end-to-end di main() pilotato da una sequenza di input."""

import os
import json
import builtins
import tempfile

import contactease_ref as m


def test_flusso_completo():
    percorso = tempfile.mktemp(suffix=".json")
    m.NOME_FILE = percorso
    passi = [
        "1", "Mario", "Rossi", "333", "m@x.it", "Via Roma 1", "",   # aggiungi + pausa
        "1", "Anna", "Bianchi", "347", "", "", "",                  # aggiungi + pausa
        "2", "",                                                    # visualizza + pausa
        "3", "ross", "",                                            # cerca + pausa
        "4", "1", "", "", "999", "", "", "",                        # modifica id 1: numero -> 999
        "5", "2", "",                                               # elimina id 2 + pausa
        "6", "",                                                    # salva + pausa
        "7", "s",                                                   # esci salvando
    ]
    it = iter(passi)
    orig = builtins.input
    builtins.input = lambda *a, **k: next(it)
    try:
        m.main()
    finally:
        builtins.input = orig

    with open(percorso, encoding="utf-8") as f:
        dati = json.load(f)
    os.remove(percorso)

    assert dati["prossimo_id"] == 3
    assert len(dati["contatti"]) == 1
    solo = dati["contatti"][0]
    assert solo["id"] == 1
    assert solo["nome"] == "Mario"
    assert solo["numero"] == "999"


def test_opzione_non_valida_e_uscita_senza_salvare():
    percorso = tempfile.mktemp(suffix=".json")
    m.NOME_FILE = percorso
    passi = ["9", "", "7", "n"]        # opzione non valida -> pausa -> esci senza salvare
    it = iter(passi)
    orig = builtins.input
    builtins.input = lambda *a, **k: next(it)
    try:
        m.main()
    finally:
        builtins.input = orig
    assert not os.path.exists(percorso)   # niente salvataggio


if __name__ == "__main__":
    passati = 0
    for nome, fn in sorted(globals().items()):
        if nome.startswith("test_") and callable(fn):
            fn()
            print(f"  ok  {nome}")
            passati += 1
    print(f"\n{passati} test superati.")
