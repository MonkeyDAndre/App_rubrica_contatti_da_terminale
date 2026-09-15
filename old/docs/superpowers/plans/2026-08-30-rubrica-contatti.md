# ContactEase — Rubrica contatti — Piano di implementazione

> **Per esecutori:** implementare task per task. Gli step usano checkbox (`- [ ]`).

**Goal:** costruire `ContactEase.ipynb`, un notebook Colab-compatibile con una
rubrica contatti OOP (classi `Contatto` e `Rubrica`), interfaccia a menu
formattata con `rich`, persistenza su JSON e una cella di test `assert`.

**Architettura:** tre livelli — `Contatto` (dato) → `Rubrica` (logica CRUD +
persistenza, nessun `rich`) → funzioni di interfaccia `rich` → `main()` (ciclo
menu). A ogni passo l'output della cella viene ripulito: si vede solo
l'intestazione dell'azione corrente e le informazioni del momento.

**Tech Stack:** Python 3, `rich`, `json`, `IPython.display.clear_output`,
notebook Jupyter/Colab.

**Spec:** `docs/superpowers/specs/2026-08-30-rubrica-contatti-design.md`

## Global Constraints

- Tutto in un solo notebook `ContactEase.ipynb`, eseguibile su Google Colab.
- Nessuna dipendenza oltre `rich` (installata con `%pip install -q rich`) e la
  standard library. Vietati `InquirerPy`, `subprocess`, `console.screen()`.
- Codice in italiano (nomi, commenti, stringhe), commentato e non troppo
  complesso; ogni cella una responsabilità chiara.
- `Contatto`: campi `id, nome, cognome, numero, email, indirizzo`.
- File JSON: `{"prossimo_id": int, "contatti": [ {id,nome,cognome,numero,email,indirizzo}, ... ]}`.
- Nessun metodo di `Rubrica` usa `rich`; solo `print` per file assente/corrotto in `carica()`.
- `cerca`: sottostringa case-insensitive su nome **o** cognome; testo vuoto → `[]`.
- `elenco`: ordinato per cognome, poi nome (case-insensitive).
- Salvataggio esplicito (voce 6) + conferma all'uscita (voce 7); nessun autosave.
- A ogni passo: `intestazione(titolo)` ripulisce lo schermo e stampa il pannello del titolo.

## Struttura file

- `ContactEase.ipynb` — il deliverable (12 celle, vedi spec).
- `scratch/contactease_ref.py` — implementazione di riferimento usata durante lo
  sviluppo per eseguire i test fuori dal notebook; **non** fa parte del
  deliverable, si può rimuovere alla fine.

Le celle di codice del notebook (4, 6, 8, 10, 11, 12) corrispondono 1:1 a
sezioni di `scratch/contactease_ref.py`, così i test girano sullo stesso codice
che finisce nel notebook.

---

### Task 1: Classe `Contatto`

**Files:**
- Create: `scratch/contactease_ref.py` (sezione `Contatto`)
- Test: `scratch/test_ref.py`

**Interfaces:**
- Produce: `Contatto(id:int, nome:str, cognome:str, numero:str, email:str, indirizzo:str)`;
  `.to_dict() -> dict`; `Contatto.from_dict(d:dict) -> Contatto`.

- [ ] **Step 1: test di round-trip**

```python
from contactease_ref import Contatto

def test_contatto_roundtrip():
    c = Contatto(1, "Mario", "Rossi", "333", "m@x.it", "Via Roma 1")
    d = c.to_dict()
    assert d == {"id": 1, "nome": "Mario", "cognome": "Rossi",
                 "numero": "333", "email": "m@x.it", "indirizzo": "Via Roma 1"}
    c2 = Contatto.from_dict(d)
    assert (c2.id, c2.nome, c2.cognome, c2.numero, c2.email, c2.indirizzo) == \
           (1, "Mario", "Rossi", "333", "m@x.it", "Via Roma 1")
```

- [ ] **Step 2: eseguire, verificare che fallisce** — `python scratch/test_ref.py` → `ModuleNotFoundError`/`AttributeError`.

- [ ] **Step 3: implementare**

```python
class Contatto:
    """Rappresenta un singolo contatto della rubrica."""

    def __init__(self, id, nome, cognome, numero, email, indirizzo):
        self.id = id
        self.nome = nome
        self.cognome = cognome
        self.numero = numero
        self.email = email
        self.indirizzo = indirizzo

    def to_dict(self):
        """Converte il contatto in un dizionario pronto per il JSON."""
        return {
            "id": self.id,
            "nome": self.nome,
            "cognome": self.cognome,
            "numero": self.numero,
            "email": self.email,
            "indirizzo": self.indirizzo,
        }

    @classmethod
    def from_dict(cls, d):
        """Ricostruisce un Contatto da un dizionario letto dal JSON."""
        return cls(d["id"], d["nome"], d["cognome"],
                   d["numero"], d["email"], d["indirizzo"])
```

- [ ] **Step 4: eseguire, verificare che passa.**
- [ ] **Step 5: commit** — `git add scratch && git commit -m "feat: classe Contatto con to_dict/from_dict"`

---

### Task 2: `Rubrica` — operazioni in memoria

**Files:**
- Modify: `scratch/contactease_ref.py` (sezione `Rubrica`)
- Test: `scratch/test_ref.py`

**Interfaces:**
- Consuma: `Contatto`.
- Produce: `Rubrica(percorso_file:str)` con `.contatti:list`, `.prossimo_id:int`;
  `.aggiungi(nome,cognome,numero,email,indirizzo) -> Contatto`;
  `.trova_per_id(id) -> Contatto|None`;
  `.modifica(id,nome,cognome,numero,email,indirizzo) -> bool`;
  `.elimina(id) -> bool`; `.cerca(testo) -> list`; `.elenco() -> list`;
  `.is_vuota() -> bool`.

- [ ] **Step 1: test**

```python
from contactease_ref import Rubrica

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
```

- [ ] **Step 2: eseguire, verificare che fallisce.**

- [ ] **Step 3: implementare**

```python
class Rubrica:
    """Gestisce la lista dei contatti e la persistenza su file JSON."""

    def __init__(self, percorso_file):
        self.percorso_file = percorso_file
        self.contatti = []          # lista di oggetti Contatto
        self.prossimo_id = 1        # id da assegnare al prossimo contatto

    def aggiungi(self, nome, cognome, numero, email, indirizzo):
        """Crea e aggiunge un nuovo contatto, restituendolo."""
        contatto = Contatto(self.prossimo_id, nome, cognome, numero, email, indirizzo)
        self.contatti.append(contatto)
        self.prossimo_id += 1
        return contatto

    def trova_per_id(self, id):
        """Restituisce il contatto con quell'id, oppure None."""
        for contatto in self.contatti:
            if contatto.id == id:
                return contatto
        return None

    def modifica(self, id, nome, cognome, numero, email, indirizzo):
        """Aggiorna i campi del contatto con quell'id. True se esiste."""
        contatto = self.trova_per_id(id)
        if contatto is None:
            return False
        contatto.nome = nome
        contatto.cognome = cognome
        contatto.numero = numero
        contatto.email = email
        contatto.indirizzo = indirizzo
        return True

    def elimina(self, id):
        """Rimuove il contatto con quell'id. True se esisteva."""
        contatto = self.trova_per_id(id)
        if contatto is None:
            return False
        self.contatti.remove(contatto)
        return True

    def cerca(self, testo):
        """Contatti il cui nome O cognome contiene 'testo' (case-insensitive)."""
        testo = testo.strip().lower()
        if testo == "":
            return []
        return [c for c in self.contatti
                if testo in c.nome.lower() or testo in c.cognome.lower()]

    def elenco(self):
        """Tutti i contatti ordinati per cognome, poi nome."""
        return sorted(self.contatti,
                      key=lambda c: (c.cognome.lower(), c.nome.lower()))

    def is_vuota(self):
        """True se non ci sono contatti."""
        return len(self.contatti) == 0
```

- [ ] **Step 4: eseguire, verificare che passa.**
- [ ] **Step 5: commit** — `git commit -am "feat: Rubrica - CRUD, ricerca, elenco ordinato"`

---

### Task 3: `Rubrica` — persistenza `salva` / `carica`

**Files:**
- Modify: `scratch/contactease_ref.py` (metodi `salva`, `carica` in `Rubrica`; `import json` in testa)
- Test: `scratch/test_ref.py`

**Interfaces:**
- Produce: `.salva() -> None`; `.carica() -> None`.

- [ ] **Step 1: test**

```python
import os, json, tempfile
from contactease_ref import Rubrica

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
        # un nuovo aggiungi non riusa un id gia' visto
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
```

- [ ] **Step 2: eseguire, verificare che fallisce.**

- [ ] **Step 3: implementare** (aggiungere `import json` in testa al file)

```python
    def salva(self):
        """Scrive contatti e contatore su file JSON (UTF-8, leggibile)."""
        dati = {
            "prossimo_id": self.prossimo_id,
            "contatti": [c.to_dict() for c in self.contatti],
        }
        with open(self.percorso_file, "w", encoding="utf-8") as f:
            json.dump(dati, f, indent=2, ensure_ascii=False)

    def carica(self):
        """Carica i contatti dal file JSON, se esiste ed e' valido."""
        if not os.path.exists(self.percorso_file):
            print(f"File '{self.percorso_file}' non trovato: rubrica vuota.")
            return
        try:
            with open(self.percorso_file, encoding="utf-8") as f:
                dati = json.load(f)
        except (json.JSONDecodeError, OSError):
            print(f"File '{self.percorso_file}' illeggibile o corrotto: "
                  f"rubrica vuota (il file non e' stato modificato).")
            return
        self.contatti = [Contatto.from_dict(d) for d in dati.get("contatti", [])]
        if "prossimo_id" in dati:
            self.prossimo_id = dati["prossimo_id"]
        elif self.contatti:
            self.prossimo_id = max(c.id for c in self.contatti) + 1
        else:
            self.prossimo_id = 1
```

Aggiungere `import os` in testa (serve anche a Task 4? no — solo qui).

- [ ] **Step 4: eseguire tutti i test** — `python scratch/test_ref.py` → tutti PASS.
- [ ] **Step 5: commit** — `git commit -am "feat: Rubrica - persistenza salva/carica con gestione errori file"`

---

### Task 4: Funzioni di interfaccia con `rich`

**Files:**
- Modify: `scratch/contactease_ref.py` (sezione UI)
- Test: `scratch/test_ui.py` (smoke test)

**Interfaces:**
- Consuma: `Contatto`, `rich`.
- Produce: `console`; `pulisci_schermo()`; `intestazione(titolo)`; `mostra_menu()`;
  `mostra_tabella(contatti, titolo)`; `chiedi_dati_contatto(correnti=None) -> dict`;
  `leggi_intero(messaggio) -> int`; `messaggio_ok(t)`, `messaggio_errore(t)`,
  `messaggio_info(t)`; `pausa()`.

- [ ] **Step 1: smoke test** (le funzioni di solo output non devono sollevare eccezioni; l'input viene simulato)

```python
import builtins, contactease_ref as m
from contactease_ref import Contatto

def test_output_non_solleva():
    m.mostra_menu()
    m.mostra_tabella([], "Vuota")
    m.mostra_tabella([Contatto(1, "Mario", "Rossi", "333", "", "")], "Una riga")
    m.messaggio_ok("ok"); m.messaggio_errore("err"); m.messaggio_info("info")

def test_leggi_intero_ripete_su_input_non_valido(monkeypatch_inputs):
    pass  # vedi implementazione test sotto
```

Implementazione completa del test (sostituire lo stub):

```python
import io, sys, contactease_ref as m
from contactease_ref import Contatto

def _con_input(valori, fn):
    it = iter(valori)
    orig = __builtins__["input"] if isinstance(__builtins__, dict) else __builtins__.input
    import builtins
    builtins.input = lambda *a, **k: next(it)
    try:
        return fn()
    finally:
        builtins.input = orig

def test_output_non_solleva():
    m.mostra_menu()
    m.mostra_tabella([], "Vuota")
    m.mostra_tabella([Contatto(1, "Mario", "Rossi", "333", "", "")], "Una riga")
    m.messaggio_ok("ok"); m.messaggio_errore("err"); m.messaggio_info("info")

def test_leggi_intero_ripete_finche_valido():
    assert _con_input(["abc", "", "7"], lambda: m.leggi_intero("n")) == 7

def test_chiedi_dati_contatto_obbligatori_e_default():
    # nome: prima vuoto (ripete) poi "Mario"; cognome "Rossi"; numero "333";
    # email "" (facoltativo -> ok); indirizzo "" (facoltativo -> ok)
    dati = _con_input(["", "Mario", "Rossi", "333", "", ""],
                      lambda: m.chiedi_dati_contatto())
    assert dati == {"nome": "Mario", "cognome": "Rossi", "numero": "333",
                    "email": "", "indirizzo": ""}
    # modifica: Invio (stringa vuota) mantiene il valore corrente
    correnti = {"nome": "Mario", "cognome": "Rossi", "numero": "333",
                "email": "m@x.it", "indirizzo": "Via Roma 1"}
    dati2 = _con_input(["", "", "", "", ""],
                       lambda: m.chiedi_dati_contatto(correnti=correnti))
    assert dati2 == {k: correnti[k] for k in ("nome", "cognome", "numero", "email", "indirizzo")}
```

> Nota implementativa: per rendere i test semplici, `chiedi_dati_contatto` e
> `leggi_intero` usano `input()` della standard library (non `rich.prompt`),
> stampando le etichette con `console.print`. Questo mantiene identico il
> comportamento in Colab e permette di simulare l'input nei test.

- [ ] **Step 2: eseguire, verificare che fallisce.**

- [ ] **Step 3: implementare**

```python
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
try:
    from IPython.display import clear_output
except ImportError:                       # esecuzione fuori da Jupyter (test)
    def clear_output(wait=False):
        pass

console = Console()

# Voci del menu principale (indice+1 = numero mostrato).
VOCI_MENU = [
    "Aggiungi contatto",
    "Visualizza tutti i contatti",
    "Cerca contatto (per nome o cognome)",
    "Modifica contatto",
    "Elimina contatto",
    "Salva su file",
    "Esci",
]

def pulisci_schermo():
    """Svuota l'output della cella (Colab/Jupyter)."""
    clear_output(wait=True)

def intestazione(titolo):
    """Pulisce lo schermo e stampa il pannello dell'azione corrente."""
    pulisci_schermo()
    console.print(Panel(f"[bold]{titolo}[/bold]",
                        title="[bold cyan]ContactEase[/bold cyan]",
                        border_style="cyan", box=box.DOUBLE))

def mostra_menu():
    """Elenca le voci numerate del menu principale."""
    for numero, voce in enumerate(VOCI_MENU, start=1):
        console.print(f"  [bold yellow]{numero}[/bold yellow]) {voce}")
    console.print()

def mostra_tabella(contatti, titolo):
    """Mostra i contatti in una tabella; se vuota, un messaggio informativo."""
    if not contatti:
        messaggio_info("Nessun contatto da mostrare.")
        return
    tabella = Table(title=titolo, box=box.SIMPLE_HEAVY, title_style="bold")
    for colonna in ("ID", "Nome", "Cognome", "Numero", "Email", "Indirizzo"):
        tabella.add_column(colonna)
    for c in contatti:
        tabella.add_row(str(c.id), c.nome, c.cognome, c.numero, c.email, c.indirizzo)
    console.print(tabella)

def _chiedi_campo(etichetta, obbligatorio, valore_corrente=None):
    """Chiede un singolo campo. Invio -> mantiene valore_corrente (se presente).
    Se obbligatorio e non c'e' valore_corrente, ripete finche' non e' vuoto."""
    suffisso = f" [{valore_corrente}]" if valore_corrente not in (None, "") else ""
    while True:
        risposta = input(f"{etichetta}{suffisso}: ").strip()
        if risposta == "" and valore_corrente is not None:
            return valore_corrente
        if risposta == "" and not obbligatorio:
            return ""
        if risposta != "":
            return risposta
        console.print("  [red]Campo obbligatorio.[/red]")

def chiedi_dati_contatto(correnti=None):
    """Raccoglie i 5 campi di un contatto e li restituisce in un dizionario.
    In modifica, 'correnti' fornisce i valori di default (Invio li conferma)."""
    c = correnti or {}
    return {
        "nome":      _chiedi_campo("Nome", True, c.get("nome")),
        "cognome":   _chiedi_campo("Cognome", True, c.get("cognome")),
        "numero":    _chiedi_campo("Numero", True, c.get("numero")),
        "email":     _chiedi_campo("Email", False, c.get("email")),
        "indirizzo": _chiedi_campo("Indirizzo", False, c.get("indirizzo")),
    }

def leggi_intero(messaggio):
    """Legge un numero intero, ripetendo la domanda finche' non e' valido."""
    while True:
        try:
            return int(input(f"{messaggio}: ").strip())
        except ValueError:
            console.print("  [red]Inserisci un numero intero.[/red]")

def messaggio_ok(testo):
    console.print(f"[bold green]OK[/bold green] {testo}")

def messaggio_errore(testo):
    console.print(f"[bold red]Errore[/bold red] {testo}")

def messaggio_info(testo):
    console.print(f"[cyan]{testo}[/cyan]")

def pausa():
    input("\nPremi Invio per continuare...")
```

- [ ] **Step 4: eseguire i test UI** — `python scratch/test_ui.py` → PASS.
- [ ] **Step 5: commit** — `git commit -am "feat: funzioni di interfaccia rich (intestazione, menu, tabella, prompt)"`

---

### Task 5: `main()` — ciclo del menu

**Files:**
- Modify: `scratch/contactease_ref.py` (funzione `main` + `NOME_FILE`)
- Test: `scratch/test_main.py` (simulazione end-to-end via stdin)

**Interfaces:**
- Consuma: `Rubrica`, tutte le funzioni UI.
- Produce: `NOME_FILE = "contatti.json"`; `main() -> None`.

- [ ] **Step 1: test end-to-end** (pilota `main()` con una sequenza di input e verifica il file salvato)

```python
import os, json, builtins, tempfile
import contactease_ref as m

def test_flusso_completo(tmp_path=None):
    percorso = tempfile.mktemp(suffix=".json")
    m.NOME_FILE = percorso
    passi = [
        "1", "Mario", "Rossi", "333", "m@x.it", "Via Roma 1", "",   # aggiungi + pausa
        "1", "Anna", "Bianchi", "347", "", "", "",                  # aggiungi + pausa
        "2", "",                                                    # visualizza + pausa
        "3", "ross", "",                                            # cerca + pausa
        "4", "1", "", "", "999", "", "", "",                        # modifica id 1: solo numero -> 999
        "5", "2", "",                                               # elimina id 2 + pausa
        "6", "",                                                    # salva + pausa
        "7", "s",                                                   # esci salvando
    ]
    it = iter(passi)
    builtins.input = lambda *a, **k: next(it)
    try:
        m.main()
    finally:
        pass
    with open(percorso, encoding="utf-8") as f:
        dati = json.load(f)
    os.remove(percorso)
    assert dati["prossimo_id"] == 3
    assert len(dati["contatti"]) == 1
    solo = dati["contatti"][0]
    assert solo["id"] == 1 and solo["nome"] == "Mario" and solo["numero"] == "999"
```

- [ ] **Step 2: eseguire, verificare che fallisce** (`main` non definito).

- [ ] **Step 3: implementare**

```python
NOME_FILE = "contatti.json"

def main():
    """Avvia la rubrica: carica i dati ed esegue il ciclo del menu."""
    rubrica = Rubrica(NOME_FILE)
    rubrica.carica()

    while True:
        intestazione("Menu principale")
        mostra_menu()
        scelta = leggi_intero("Seleziona un'opzione")

        if scelta == 1:
            intestazione("Aggiungi contatto")
            dati = chiedi_dati_contatto()
            contatto = rubrica.aggiungi(**dati)
            intestazione("Aggiungi contatto")
            messaggio_ok(f"Contatto aggiunto con ID {contatto.id}.")

        elif scelta == 2:
            intestazione("Tutti i contatti")
            mostra_tabella(rubrica.elenco(), "Tutti i contatti")

        elif scelta == 3:
            intestazione("Cerca contatto")
            testo = input("Nome o cognome da cercare: ")
            intestazione("Cerca contatto")
            mostra_tabella(rubrica.cerca(testo), f"Risultati per '{testo.strip()}'")

        elif scelta == 4:
            intestazione("Modifica contatto")
            mostra_tabella(rubrica.elenco(), "Tutti i contatti")
            id_scelto = leggi_intero("ID del contatto da modificare")
            contatto = rubrica.trova_per_id(id_scelto)
            if contatto is None:
                intestazione("Modifica contatto")
                messaggio_errore(f"Nessun contatto con ID {id_scelto}.")
            else:
                intestazione("Modifica contatto")
                console.print("Premi Invio per mantenere il valore attuale.\n")
                dati = chiedi_dati_contatto(correnti=contatto.to_dict())
                rubrica.modifica(id_scelto, **dati)
                intestazione("Modifica contatto")
                messaggio_ok(f"Contatto {id_scelto} aggiornato.")

        elif scelta == 5:
            intestazione("Elimina contatto")
            mostra_tabella(rubrica.elenco(), "Tutti i contatti")
            id_scelto = leggi_intero("ID del contatto da eliminare")
            intestazione("Elimina contatto")
            if rubrica.elimina(id_scelto):
                messaggio_ok(f"Contatto {id_scelto} eliminato.")
            else:
                messaggio_errore(f"Nessun contatto con ID {id_scelto}.")

        elif scelta == 6:
            intestazione("Salva su file")
            rubrica.salva()
            messaggio_ok(f"Contatti salvati in '{rubrica.percorso_file}'.")

        elif scelta == 7:
            intestazione("Esci")
            risposta = input("Salvare le modifiche? [s/n] (default s): ").strip().lower()
            if risposta in ("", "s", "si", "sì"):
                rubrica.salva()
                messaggio_ok("Modifiche salvate.")
            messaggio_info("Arrivederci!")
            break

        else:
            intestazione("Menu principale")
            messaggio_errore("Opzione non valida: scegli un numero da 1 a 7.")

        if scelta != 7:
            pausa()
```

- [ ] **Step 4: eseguire** — `python scratch/test_main.py` → PASS. Rieseguire anche `test_ref.py` e `test_ui.py`.
- [ ] **Step 5: commit** — `git commit -am "feat: main() con ciclo del menu e pulizia schermo a ogni passo"`

---

### Task 6: Assemblare `ContactEase.ipynb`

**Files:**
- Create: `ContactEase.ipynb` (12 celle, vedi spec sezione "Struttura del notebook")
- Usare `nbformat` per costruirlo da uno script `scratch/build_notebook.py`.

**Contenuto celle** (codice preso 1:1 da `scratch/contactease_ref.py`):

1. **md** — titolo, descrizione, requisiti, nota Colab su persistenza + snippet Drive.
2. **code** — `%pip install -q rich` poi gli import (`import json, os` + import `rich` + `from IPython.display import clear_output`).
3. **md** — spiegazione `Contatto`.
4. **code** — classe `Contatto` (da Task 1).
5. **md** — spiegazione `Rubrica` + formato JSON.
6. **code** — classe `Rubrica` completa (Task 2 + Task 3).
7. **md** — spiegazione funzioni di interfaccia e principio "una schermata per volta".
8. **code** — `console`, `VOCI_MENU`, e tutte le funzioni UI (Task 4). *Nel notebook la `clear_output` è importata alla cella 2, quindi qui niente `try/except ImportError`.*
9. **md** — spiegazione di `main()` e come si usa l'app.
10. **code** — `NOME_FILE` + `main()` (Task 5).
11. **code** — `main()`  *(riga singola che avvia l'app)*.
12. **code** — cella "Verifica rapida (facoltativa)": gli `assert` sui metodi di `Rubrica` (aggiungi/id progressivi, cerca nome+cognome, cerca vuota, modifica true/false, elimina true/false, elenco ordinato, round-trip salva/carica su file temporaneo, pulizia file). Stampa finale `✅ Tutti i test superati`.

- [ ] **Step 1:** scrivere `scratch/build_notebook.py` che assembla le 12 celle con `nbformat.v4` e salva `ContactEase.ipynb` (`nbformat.write`).
- [ ] **Step 2:** generare il notebook: `python scratch/build_notebook.py`.
- [ ] **Step 3:** eseguire headless le celle sicure (tutte tranne la 11 che contiene il `main()` interattivo):
  `jupyter nbconvert --to notebook --execute --stdout ContactEase.ipynb --TagRemovePreprocessor... ` — in pratica: uno script `scratch/run_cells.py` che esegue con `nbclient` tutte le celle di codice **eccetto** quella con `main()`, e verifica che la cella 12 non sollevi `AssertionError`.
- [ ] **Step 4:** aprire il notebook con `nbformat.read`, controllare: 12 celle, tipi corretti nell'ordine md/code previsto, la cella 2 inizia con `%pip install -q rich`.
- [ ] **Step 5: commit** — `git add ContactEase.ipynb && git commit -m "feat: notebook ContactEase.ipynb completo (12 celle)"`

---

### Task 7: Verifica finale e pulizia

- [ ] **Step 1:** eseguire di nuovo tutti i test di `scratch/` — tutti PASS.
- [ ] **Step 2:** simulazione `main()` end-to-end (Task 5 test) — PASS.
- [ ] **Step 3:** verifica manuale del testo delle celle markdown (italiano, senza refusi, coerenti col codice).
- [ ] **Step 4:** decidere se rimuovere `scratch/` dal repo o tenerlo. Se rimosso: `git rm -r scratch && git commit -m "chore: rimuove i file di sviluppo scratch/"`.
- [ ] **Step 5:** aggiornare eventualmente `README`/nessuno; commit finale se restano modifiche.
- [ ] **Step 6:** riportare all'utente: come aprire il notebook in Colab e ottenere il link pubblico (File → Salva una copia su GitHub / Condividi).

---

## Self-review

- **Copertura spec:** Contatto (T1), Rubrica CRUD (T2), ricerca nome/cognome
  (T2), persistenza JSON + errori file (T3), interfaccia rich + pulizia schermo
  (T4), menu 7 voci + main (T5), notebook 12 celle + nota Colab (T6), cella
  test (T6 step, T7). Tutti i requisiti della traccia hanno un task.
- **Placeholder:** nessun "TBD"; ogni step di codice ha il codice reale.
- **Coerenza tipi/nomi:** `NOME_FILE` (non `FILE_NAME`), `intestazione`,
  `chiedi_dati_contatto(correnti=...)`, `trova_per_id`, `prossimo_id` usati in
  modo coerente tra i task. `chiedi_dati_contatto` restituisce dict con chiavi
  `nome,cognome,numero,email,indirizzo` — compatibili con `rubrica.aggiungi(**dati)`
  e `rubrica.modifica(id, **dati)` (firme corrispondenti).
- **Nota:** `email`/`indirizzo` facoltativi: in inserimento un campo vuoto
  diventa `""`; in modifica Invio mantiene il valore corrente. Coerente tra
  test T4 e implementazione `_chiedi_campo`.
