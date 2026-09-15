"""Smoke test delle funzioni di interfaccia (input simulato)."""

import builtins

import contactease_ref as m
from contactease_ref import Contatto


def _con_input(valori, fn):
    """Esegue fn() sostituendo input() con una sequenza di valori."""
    it = iter(valori)
    orig = builtins.input
    builtins.input = lambda *a, **k: next(it)
    try:
        return fn()
    finally:
        builtins.input = orig


def test_output_non_solleva():
    m.mostra_menu()
    m.mostra_tabella([], "Vuota")
    m.mostra_tabella([Contatto(1, "Mario", "Rossi", "333", "", "")], "Una riga")
    m.messaggio_ok("ok")
    m.messaggio_errore("err")
    m.messaggio_info("info")


def test_leggi_intero_ripete_finche_valido():
    assert _con_input(["abc", "", "7"], lambda: m.leggi_intero("n")) == 7


def test_chiedi_dati_contatto_obbligatori_e_default():
    dati = _con_input(["", "Mario", "Rossi", "333", "", ""],
                      lambda: m.chiedi_dati_contatto())
    assert dati == {"nome": "Mario", "cognome": "Rossi", "numero": "333",
                    "email": "", "indirizzo": ""}

    correnti = {"nome": "Mario", "cognome": "Rossi", "numero": "333",
                "email": "m@x.it", "indirizzo": "Via Roma 1"}
    dati2 = _con_input(["", "", "", "", ""],
                       lambda: m.chiedi_dati_contatto(correnti=correnti))
    assert dati2 == {k: correnti[k] for k in
                     ("nome", "cognome", "numero", "email", "indirizzo")}


def test_chiedi_dati_contatto_modifica_cambia_un_campo():
    correnti = {"nome": "Mario", "cognome": "Rossi", "numero": "333",
                "email": "m@x.it", "indirizzo": "Via Roma 1"}
    # cambia solo il numero, tiene il resto
    dati = _con_input(["", "", "999", "", ""],
                      lambda: m.chiedi_dati_contatto(correnti=correnti))
    assert dati["numero"] == "999"
    assert dati["nome"] == "Mario" and dati["email"] == "m@x.it"


if __name__ == "__main__":
    passati = 0
    for nome, fn in sorted(globals().items()):
        if nome.startswith("test_") and callable(fn):
            fn()
            print(f"  ok  {nome}")
            passati += 1
    print(f"\n{passati} test superati.")
