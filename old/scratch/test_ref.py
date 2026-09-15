"""Test dei metodi di Contatto e Rubrica (nessun rich, nessun input)."""

import os
import json
import tempfile

from contactease_ref import Contatto, Rubrica


def test_contatto_roundtrip():
    c = Contatto(1, "Mario", "Rossi", "333", "m@x.it", "Via Roma 1")
    d = c.to_dict()
    assert d == {"id": 1, "nome": "Mario", "cognome": "Rossi",
                 "numero": "333", "email": "m@x.it", "indirizzo": "Via Roma 1"}
    c2 = Contatto.from_dict(d)
    assert (c2.id, c2.nome, c2.cognome, c2.numero, c2.email, c2.indirizzo) == \
           (1, "Mario", "Rossi", "333", "m@x.it", "Via Roma 1")


def _rub():
    r = Rubrica("dummy.json")
    r.aggiungi("Mario", "Rossi", "333", "", "")
    r.aggiungi("Anna", "Bianchi", "347", "", "")
    r.aggiungi("marco", "Rossini", "348", "", "")
    return r


def test_aggiungi_assegna_id_progressivi():
    r = _rub()
    assert [c.id for c in r.contatti] == [1, 2, 3]
    assert r.prossimo_id == 4


def test_cerca_per_nome_e_cognome_case_insensitive():
    r = _rub()
    assert {c.id for c in r.cerca("mar")} == {1, 3}      # Mario, marco
    assert {c.id for c in r.cerca("ROSS")} == {1, 3}     # Rossi, Rossini
    assert r.cerca("   ") == []


def test_modifica():
    r = _rub()
    assert r.modifica(2, "Anna", "Verdi", "999", "a@x.it", "Via A") is True
    c = r.trova_per_id(2)
    assert (c.cognome, c.numero, c.email) == ("Verdi", "999", "a@x.it")
    assert r.modifica(99, "x", "x", "x", "x", "x") is False


def test_elimina():
    r = _rub()
    assert r.elimina(1) is True
    assert r.trova_per_id(1) is None
    assert len(r.contatti) == 2
    assert r.elimina(1) is False


def test_elenco_ordinato_per_cognome_poi_nome():
    r = _rub()
    assert [c.cognome for c in r.elenco()] == ["Bianchi", "Rossi", "Rossini"]


def test_is_vuota():
    assert Rubrica("dummy.json").is_vuota() is True
    assert _rub().is_vuota() is False


def test_salva_e_carica_roundtrip():
    percorso = tempfile.mktemp(suffix=".json")
    try:
        r = Rubrica(percorso)
        r.aggiungi("Mario", "Rossi", "333", "m@x.it", "Via Roma 1")
        r.aggiungi("Anna", "Bianchi", "347", "", "")
        r.salva()

        r2 = Rubrica(percorso)
        r2.carica()
        assert [c.to_dict() for c in r2.contatti] == [c.to_dict() for c in r.contatti]
        assert r2.prossimo_id == r.prossimo_id            # 3
        assert r2.aggiungi("X", "Y", "0", "", "").id == 3
    finally:
        if os.path.exists(percorso):
            os.remove(percorso)


def test_carica_file_assente_parte_vuota():
    r = Rubrica(tempfile.mktemp(suffix=".json"))
    r.carica()
    assert r.contatti == [] and r.prossimo_id == 1


def test_carica_file_corrotto_non_sovrascrive():
    percorso = tempfile.mktemp(suffix=".json")
    with open(percorso, "w", encoding="utf-8") as f:
        f.write("{ questo non e' json ")
    try:
        r = Rubrica(percorso)
        r.carica()
        assert r.contatti == [] and r.prossimo_id == 1
        with open(percorso, encoding="utf-8") as f:
            assert f.read() == "{ questo non e' json "   # intatto
    finally:
        os.remove(percorso)


if __name__ == "__main__":
    passati = 0
    for nome, fn in sorted(globals().items()):
        if nome.startswith("test_") and callable(fn):
            fn()
            print(f"  ok  {nome}")
            passati += 1
    print(f"\n{passati} test superati.")
