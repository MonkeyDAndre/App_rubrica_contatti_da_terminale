"""Assembla ContactEase.ipynb (12 celle) a partire da sorgenti verificati."""

import os
import nbformat
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell

QUI = os.path.dirname(__file__)
DESTINAZIONE = os.path.join(QUI, "..", "ContactEase.ipynb")


# --- Cella 1 : introduzione -------------------------------------------------
MD_INTRO = """\
# ContactEase — Rubrica di contatti

**ContactEase Solutions** — applicazione console interattiva per gestire una
rubrica di contatti telefonici.

Il progetto applica i principi della **programmazione orientata agli oggetti**
in Python e permette di:

| # | Funzionalità |
|---|---|
| 1 | Aggiungere un contatto |
| 2 | Visualizzare tutti i contatti |
| 3 | Cercare un contatto per nome o cognome |
| 4 | Modificare un contatto esistente |
| 5 | Eliminare un contatto |
| 6 | Salvare i contatti su file (formato **JSON**) |
| | Caricare automaticamente i contatti all'avvio |

## Come è organizzato il notebook

1. Introduzione (questa cella)
2. Installazione librerie e import
3. – 4. Classe `Contatto`
5. – 6. Classe `Rubrica` (operazioni + salvataggio/caricamento)
7. – 8. Funzioni dell'interfaccia (formattazione con la libreria `rich`)
9. – 10. Funzione `main()` con il menu
11. Avvio dell'applicazione
12. Verifica rapida (test facoltativi)

**Esegui le celle in ordine dall'alto verso il basso**, poi usa la cella 11
per avviare la rubrica.

## Nota sulla persistenza dei dati su Google Colab

I contatti vengono salvati nel file `contatti.json` nella cartella di lavoro
di Colab. Questa cartella **viene azzerata quando la sessione si chiude**: i
dati restano quindi disponibili finché la sessione è attiva.

Per conservare i contatti in modo permanente puoi montare Google Drive e
spostare il file lì, cambiando `NOME_FILE` nella cella 10:

```python
from google.colab import drive
drive.mount('/content/drive')
NOME_FILE = '/content/drive/MyDrive/contatti.json'
```
"""


# --- Cella 2 : setup ------------------------------------------------------
CODE_SETUP = """\
# Installa la libreria "rich" per l'interfaccia formattata.
# Su Google Colab spesso è già presente: in quel caso questa riga non fa nulla.
!pip install -q rich

import json
import os

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
from IPython.display import clear_output
"""


# --- Cella 3 : spiegazione Contatto ---------------------------------------
MD_CONTATTO = """\
## La classe `Contatto`

Rappresenta **un singolo contatto** della rubrica. È una classe semplice: tiene
insieme i dati di una persona e sa convertirsi da/verso un dizionario, il
formato usato per salvare su file JSON.

Attributi:

- `id` — numero identificativo, assegnato dalla `Rubrica` e **stabile** nel tempo
- `nome`, `cognome`, `numero` — dati obbligatori
- `email`, `indirizzo` — dati facoltativi (possono essere stringhe vuote)

Metodi:

- `to_dict()` — restituisce un dizionario con i campi del contatto
- `from_dict(d)` — *metodo di classe*: ricostruisce un `Contatto` da un dizionario
"""


# --- Cella 4 : classe Contatto ------------------------------------------
CODE_CONTATTO = '''\
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
'''


# --- Cella 5 : spiegazione Rubrica --------------------------------------
MD_RUBRICA = """\
## La classe `Rubrica`

È il **cuore dell'applicazione**: conserva l'elenco dei contatti in memoria e
si occupa di tutte le operazioni e del salvataggio su file. Non stampa nulla a
schermo (a parte un avviso se il file non c'è o è danneggiato): la parte
grafica è tenuta separata, nelle funzioni dell'interfaccia.

Stato interno:

- `percorso_file` — nome del file JSON dei contatti
- `contatti` — lista di oggetti `Contatto`
- `prossimo_id` — prossimo `id` libero da assegnare

Metodi principali:

| Metodo | Cosa fa |
|---|---|
| `aggiungi(...)` | crea un nuovo contatto con l'`id` corrente e lo aggiunge |
| `trova_per_id(id)` | restituisce il contatto con quell'`id`, oppure `None` |
| `modifica(id, ...)` | aggiorna i campi di un contatto; `True` se esiste |
| `elimina(id)` | rimuove un contatto; `True` se esisteva |
| `cerca(testo)` | contatti il cui **nome o cognome** contiene `testo` (maiuscole/minuscole indifferenti) |
| `elenco()` | tutti i contatti ordinati per cognome, poi nome |
| `is_vuota()` | `True` se non ci sono contatti |
| `salva()` | scrive i contatti nel file JSON |
| `carica()` | legge i contatti dal file JSON, se esiste ed è valido |

### Formato del file `contatti.json`

```json
{
  "prossimo_id": 3,
  "contatti": [
    {"id": 1, "nome": "Mario", "cognome": "Rossi",
     "numero": "+39 333 1234567", "email": "mario@example.com",
     "indirizzo": "Via Roma 1, Milano"}
  ]
}
```

Il contatore `prossimo_id` è salvato nel file: così gli `id` restano stabili
anche dopo eliminazioni e riavvii dell'applicazione.
"""


# --- Cella 6 : classe Rubrica -----------------------------------------
CODE_RUBRICA = '''\
class Rubrica:
    """Gestisce la lista dei contatti e la persistenza su file JSON."""

    def __init__(self, percorso_file):
        self.percorso_file = percorso_file
        self.contatti = []          # lista di oggetti Contatto
        self.prossimo_id = 1        # id da assegnare al prossimo contatto

    # ----- operazioni sui contatti --------------------------------------
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

    # ----- salvataggio e caricamento ----------------------------------
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
'''


# --- Cella 7 : spiegazione interfaccia --------------------------------
MD_UI = """\
## Le funzioni dell'interfaccia

Sono funzioni separate dalle classi: si occupano **solo** di mostrare cose a
schermo e di leggere l'input dell'utente, usando la libreria `rich` per una
resa ordinata (pannelli, tabelle, colori).

### Principio: una schermata per volta

L'applicazione gira dentro l'output di **una sola cella** (la cella 11). Ogni
volta che l'utente fa una scelta, quell'output viene **ripulito** prima di
mostrare il passo successivo. In ogni momento a schermo restano soltanto:

1. l'**intestazione** dell'azione corrente (il pannello con il titolo);
2. le **informazioni necessarie in quel momento** (una tabella, una domanda,
   un messaggio di esito) — senza residui dei passi precedenti.

La funzione `intestazione(titolo)` fa proprio questo: pulisce lo schermo e
stampa il pannello del titolo. Viene richiamata all'inizio del menu e prima di
ogni passo di ogni azione.

| Funzione | Ruolo |
|---|---|
| `pulisci_schermo()` | svuota l'output della cella |
| `intestazione(titolo)` | pulisce lo schermo e stampa il pannello del titolo |
| `mostra_menu()` | elenca le 7 voci del menu |
| `mostra_tabella(contatti, titolo)` | mostra i contatti in tabella |
| `chiedi_dati_contatto(correnti=None)` | chiede i 5 campi di un contatto |
| `leggi_intero(messaggio)` | legge un numero, ripetendo se l'input non è valido |
| `messaggio_ok / messaggio_errore / messaggio_info` | righe colorate di esito |
| `pausa()` | attende la pressione di Invio |
"""


# --- Cella 8 : funzioni interfaccia ----------------------------------
CODE_UI = '''\
# Un unico oggetto Console condiviso da tutte le funzioni di stampa.
console = Console()

# Voci del menu principale (posizione + 1 = numero mostrato a video).
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
    """Chiede un singolo campo.

    - Invio (risposta vuota) mantiene 'valore_corrente' se fornito (modifica).
    - Se il campo e' facoltativo e la risposta e' vuota, restituisce "".
    - Se e' obbligatorio e non c'e' un valore corrente, ripete la domanda.
    """
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

    In modifica, 'correnti' fornisce i valori di default: premere Invio
    su un campo ne mantiene il valore attuale.
    """
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
    input("\\nPremi Invio per continuare...")
'''


# --- Cella 9 : spiegazione main --------------------------------------
MD_MAIN = """\
## La funzione `main()`

Mette insieme tutti i pezzi:

1. crea una `Rubrica` che usa il file `NOME_FILE`;
2. chiama `carica()` per leggere i contatti salvati in precedenza;
3. entra nel **ciclo del menu**: mostra le opzioni, legge la scelta, esegue
   l'azione, attende Invio e ricomincia.

Ogni azione inizia con `intestazione(...)` (che pulisce lo schermo) e la
richiama prima di ogni passo successivo, così a video resta solo ciò che
serve in quel momento.

Il salvataggio è **esplicito**: la voce *6* salva su richiesta e, all'uscita
(voce *7*), viene chiesto se salvare le modifiche.
"""


# --- Cella 10 : main() ---------------------------------------------
CODE_MAIN = '''\
# Nome del file in cui vengono salvati i contatti.
# Su Colab, per una persistenza permanente, si può puntare a Google Drive
# (vedi la nota nella prima cella).
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
                console.print("Premi Invio per mantenere il valore attuale.\\n")
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
'''


# --- Cella 11 : avvio --------------------------------------------
CODE_AVVIO = '''\
# Avvia l'applicazione. Esegui questa cella e segui il menu.
# Per fermarla: scegli l'opzione 7 (Esci) oppure interrompi l'esecuzione
# della cella (menu Runtime -> Interrompi esecuzione).
main()
'''


# --- Cella 12 : verifica rapida --------------------------------------
CODE_TEST = '''\
# Verifica rapida (facoltativa): controlla che i metodi della classe Rubrica
# funzionino come previsto. Usa un file temporaneo: NON tocca "contatti.json".
import tempfile

def _verifica():
    # 1) aggiungi() assegna id progressivi e aggiorna il contatore
    r = Rubrica("_test_.json")
    r.aggiungi("Mario", "Rossi", "333", "", "")
    r.aggiungi("Anna", "Bianchi", "347", "", "")
    r.aggiungi("marco", "Rossini", "348", "", "")
    assert [c.id for c in r.contatti] == [1, 2, 3]
    assert r.prossimo_id == 4

    # 2) cerca() per nome o cognome, senza distinzione maiuscole/minuscole
    assert {c.id for c in r.cerca("mar")} == {1, 3}
    assert {c.id for c in r.cerca("ROSS")} == {1, 3}
    assert r.cerca("   ") == []            # testo vuoto -> nessun risultato

    # 3) modifica() aggiorna un contatto esistente, altrimenti False
    assert r.modifica(2, "Anna", "Verdi", "999", "a@x.it", "Via A") is True
    assert r.trova_per_id(2).cognome == "Verdi"
    assert r.modifica(99, "x", "x", "x", "x", "x") is False

    # 4) elimina() rimuove un contatto esistente, altrimenti False
    assert r.elimina(1) is True
    assert r.trova_per_id(1) is None
    assert r.elimina(1) is False

    # 5) elenco() ordina per cognome, poi nome
    #    Restano: id 2 "Anna Verdi" e id 3 "marco Rossini" -> ordinati per cognome
    assert [c.cognome for c in r.elenco()] == ["Rossini", "Verdi"]

    # 6) salva() + carica(): i dati sopravvivono a un giro su file
    percorso = tempfile.mktemp(suffix=".json")
    try:
        r.percorso_file = percorso
        r.salva()
        r2 = Rubrica(percorso)
        r2.carica()
        assert [c.to_dict() for c in r2.contatti] == [c.to_dict() for c in r.contatti]
        assert r2.prossimo_id == r.prossimo_id
    finally:
        if os.path.exists(percorso):
            os.remove(percorso)

    print("✅ Tutti i test superati.")

_verifica()
'''


def main():
    nb = new_notebook()
    nb.cells = [
        new_markdown_cell(MD_INTRO),
        new_code_cell(CODE_SETUP),
        new_markdown_cell(MD_CONTATTO),
        new_code_cell(CODE_CONTATTO),
        new_markdown_cell(MD_RUBRICA),
        new_code_cell(CODE_RUBRICA),
        new_markdown_cell(MD_UI),
        new_code_cell(CODE_UI),
        new_markdown_cell(MD_MAIN),
        new_code_cell(CODE_MAIN),
        new_code_cell(CODE_AVVIO),
        new_code_cell(CODE_TEST),
    ]
    nb.metadata["language_info"] = {"name": "python"}
    nb.metadata["kernelspec"] = {
        "name": "python3", "display_name": "Python 3", "language": "python",
    }
    with open(DESTINAZIONE, "w", encoding="utf-8") as f:
        nbformat.write(nb, f)
    print(f"Scritto {os.path.abspath(DESTINAZIONE)} ({len(nb.cells)} celle)")


if __name__ == "__main__":
    main()
