# ContactEase Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ricostruire da zero, dentro un unico notebook `ContactEase.ipynb`, una rubrica di contatti OOP a riga di comando (aggiungi/visualizza/modifica/elimina/cerca, persistenza JSON), spiegata passo-passo, e preparare la repository come primo progetto di portfolio GitHub.

**Architecture:** Un notebook Colab/Jupyter con due classi (`Contatto`, `Rubrica` — quest'ultima basata su un dizionario `id -> Contatto`), funzioni di interfaccia con `rich`, un ciclo `main()` a menu, e un'unica cella finale di test automatici (`assert`). Ogni sezione di codice è preceduta da una cella markdown esplicativa.

**Tech Stack:** Python 3, Jupyter/Colab notebook (`.ipynb`), libreria `rich`, `json`/`os`/`time` della standard library, `IPython.display.clear_output`. Le celle del notebook vengono create/modificate con lo strumento `NotebookEdit`; l'esecuzione/verifica avviene lanciando le celle nel kernel Python già attivo su questo progetto (VS Code).

**Spec:** [docs/superpowers/specs/2026-09-15-contactease-design.md](../specs/2026-09-15-contactease-design.md)

## Global Constraints

- Tutto il codice e i commenti sono in **italiano**, semplici e leggibili (l'utente è un principiante): niente astrazioni non richieste.
- Tutto vive in **un solo notebook**, sviluppato direttamente cella per cella (nessun file `.py` separato che genera il notebook).
- Ogni sezione di codice è preceduta da una **cella markdown** che spiega cosa fa e perché.
- Interfaccia utente solo con `rich` + `input()`; niente `InquirerPy`, `subprocess`, `console.screen()` (incompatibili con Colab).
- `Rubrica` memorizza i contatti in un **dizionario** `{id: Contatto}` (non una lista) — motivato nello spec dalla ricerca O(1) per id.
- Persistenza: file JSON locale `contatti.json`; salvataggio **esplicito** (voce di menu + conferma in uscita), mai automatico.
- I **test formali** (con `assert`) vivono in un'**unica cella dedicata alla fine** del notebook, mai sparsi tra le altre celle.
- La repository finale deve includere `README.md`, `LICENSE` (MIT), `requirements.txt`; la cartella `old/` va rimossa dalla repo finale (resta in git history).

---

## Task 1: Scaffold del notebook

**Files:**
- Create: `ContactEase.ipynb`

**Interfaces:**
- Produces: notebook con 2 celle iniziali (introduzione markdown, import/installazione codice). Nessuna dipendenza da task precedenti.

- [ ] **Step 1: Crea il notebook con la cella di introduzione**

Con lo strumento `NotebookEdit` (azione `insert`, `cell_type: markdown`), crea `ContactEase.ipynb` con questa prima cella:

```markdown
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
2. Installazione libreria e import
3. – 4. Classe `Contatto`
5. – 8. Classe `Rubrica` (dati, ricerca, persistenza)
9. – 10. Funzioni dell'interfaccia (libreria `rich`)
11. – 12. Funzione `main()` con il menu
13. Avvio dell'applicazione
14. Test automatici

**Esegui le celle in ordine dall'alto verso il basso**, poi usa la cella di
avvio per far partire la rubrica.

## Nota sulla persistenza dei dati su Google Colab

I contatti vengono salvati nel file `contatti.json` nella cartella di lavoro
di Colab. Questa cartella **viene azzerata quando la sessione si chiude**: i
dati restano quindi disponibili finché la sessione è attiva.

Per conservare i contatti in modo permanente puoi montare Google Drive e
spostare il file lì, cambiando `NOME_FILE` più avanti nel notebook:

```python
from google.colab import drive
drive.mount('/content/drive')
NOME_FILE = '/content/drive/MyDrive/contatti.json'
```
```

- [ ] **Step 2: Aggiungi la cella di import e installazione**

Aggiungi (`insert` dopo la cella precedente) una cella markdown:

```markdown
## Import e installazione

Installiamo la libreria `rich` (serve per un'interfaccia a riga di comando
più leggibile: pannelli, tabelle, colori) e importiamo tutto ciò che serve.
Su Google Colab `rich` è quasi sempre già installata: il comando non farà
nulla in quel caso.
```

Seguita da una cella di codice:

```python
%pip install rich

import json
import os
import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
from IPython.display import clear_output
```

- [ ] **Step 3: Esegui entrambe le celle nel kernel**

Esegui le due celle nel notebook (kernel Python già configurato per questo
progetto). Verifica che non ci siano errori e che l'installazione di `rich`
vada a buon fine (o segnali "già installato").

- [ ] **Step 4: Commit**

```bash
git add ContactEase.ipynb
git commit -m "feat: scaffold notebook ContactEase con intro e import"
```

---

## Task 2: Classe `Contatto`

**Files:**
- Modify: `ContactEase.ipynb` (aggiunta di celle in coda)

**Interfaces:**
- Consumes: nessuno
- Produces: classe `Contatto(id, nome, cognome, numero, email, indirizzo)` con metodi `to_dict()` e class method `from_dict(d)`, usata da `Rubrica` nei task successivi.

- [ ] **Step 1: Aggiungi la cella markdown esplicativa**

```markdown
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
```

- [ ] **Step 2: Aggiungi la cella di codice**

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

- [ ] **Step 3: Esegui la cella e verifica a mano**

Esegui la cella di codice, poi in una cella **temporanea** (da eliminare
dopo il controllo) verifica il comportamento atteso:

```python
c = Contatto(1, "Mario", "Rossi", "333", "mario@example.com", "Via Roma 1")
assert c.to_dict() == {
    "id": 1, "nome": "Mario", "cognome": "Rossi", "numero": "333",
    "email": "mario@example.com", "indirizzo": "Via Roma 1",
}
c2 = Contatto.from_dict(c.to_dict())
assert c2.to_dict() == c.to_dict()
print("OK Contatto")
```

Expected: stampa `OK Contatto` senza errori. Elimina questa cella temporanea
di verifica (non fa parte del notebook consegnato: i test ufficiali vivono
solo nella cella finale, Task 8).

- [ ] **Step 4: Commit**

```bash
git add ContactEase.ipynb
git commit -m "feat: aggiungi la classe Contatto"
```

---

## Task 3: Classe `Rubrica` — dati di base (aggiungi, trova, modifica, elimina)

**Files:**
- Modify: `ContactEase.ipynb` (aggiunta di celle in coda)

**Interfaces:**
- Consumes: `Contatto` (Task 2)
- Produces: classe `Rubrica(percorso_file)` con attributi `contatti` (dict `id -> Contatto`) e `prossimo_id`; metodi `aggiungi(nome, cognome, numero, email, indirizzo)`, `trova_per_id(id)`, `modifica(id, nome, cognome, numero, email, indirizzo)`, `elimina(id)`. Usati dai task successivi e dalle funzioni di interfaccia.

- [ ] **Step 1: Aggiungi la cella markdown esplicativa**

```markdown
## La classe `Rubrica` — parte 1: dati di base

È il **cuore dell'applicazione**: conserva i contatti e si occupa delle
operazioni su di essi. Non stampa nulla a schermo: la parte grafica è
tenuta separata, nelle funzioni dell'interfaccia (più avanti).

Stato interno:

- `percorso_file` — nome del file JSON dei contatti
- `contatti` — **dizionario**: chiave = `id` del contatto, valore = oggetto
  `Contatto`
- `prossimo_id` — prossimo `id` libero da assegnare

Perché un dizionario e non una lista? Perché la ricerca per `id` (usata da
`modifica` ed `elimina`) diventa un accesso diretto — `self.contatti.get(id)`
— invece di dover scorrere tutti i contatti uno per uno. Quando i dati hanno
una chiave naturale e la cerchi spesso per quella chiave, il dizionario è la
struttura giusta.

Metodi di questa prima parte:

| Metodo | Cosa fa |
|---|---|
| `aggiungi(...)` | crea un nuovo contatto con l'`id` corrente, lo inserisce nel dizionario e aggiorna il contatore |
| `trova_per_id(id)` | restituisce il contatto con quell'`id`, oppure `None` |
| `modifica(id, ...)` | aggiorna i campi di un contatto; `True` se esiste |
| `elimina(id)` | rimuove un contatto; `True` se esisteva |
```

- [ ] **Step 2: Aggiungi la cella di codice**

```python
class Rubrica:
    """Gestisce i contatti (in un dizionario id -> Contatto) e la loro persistenza."""

    def __init__(self, percorso_file):
        self.percorso_file = percorso_file
        self.contatti = {}      # chiave: id (int) -> valore: oggetto Contatto
        self.prossimo_id = 1

    def aggiungi(self, nome, cognome, numero, email, indirizzo):
        """Crea un nuovo contatto, lo inserisce nel dizionario e lo restituisce."""
        contatto = Contatto(self.prossimo_id, nome, cognome, numero, email, indirizzo)
        self.contatti[contatto.id] = contatto
        self.prossimo_id += 1
        return contatto

    def trova_per_id(self, id):
        """Restituisce il contatto con quell'id, oppure None (accesso diretto)."""
        return self.contatti.get(id)

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
        if id not in self.contatti:
            return False
        del self.contatti[id]
        return True
```

- [ ] **Step 3: Esegui la cella e verifica a mano**

In una cella temporanea (da eliminare dopo):

```python
r = Rubrica("_verifica_.json")
c1 = r.aggiungi("Mario", "Rossi", "333", "", "")
c2 = r.aggiungi("Anna", "Bianchi", "347", "", "")
assert (c1.id, c2.id) == (1, 2)
assert r.prossimo_id == 3
assert r.trova_per_id(1) is c1
assert r.trova_per_id(99) is None
assert r.modifica(1, "Mario", "Verdi", "333", "m@x.it", "") is True
assert r.trova_per_id(1).cognome == "Verdi"
assert r.modifica(99, "x", "x", "x", "x", "x") is False
assert r.elimina(1) is True
assert r.trova_per_id(1) is None
assert r.elimina(1) is False
print("OK Rubrica parte 1")
```

Expected: stampa `OK Rubrica parte 1`. Elimina la cella temporanea dopo la
verifica.

- [ ] **Step 4: Commit**

```bash
git add ContactEase.ipynb
git commit -m "feat: aggiungi Rubrica con operazioni base su dizionario"
```

---

## Task 4: Classe `Rubrica` — ricerca ed elenco

**Files:**
- Modify: `ContactEase.ipynb` (aggiunta di celle in coda)

**Interfaces:**
- Consumes: `Rubrica` (Task 3)
- Produces: metodi `cerca(testo)`, `elenco()`, `is_vuota()` sulla stessa classe `Rubrica`.

- [ ] **Step 1: Aggiungi la cella markdown esplicativa**

```markdown
## La classe `Rubrica` — parte 2: ricerca ed elenco

Per **id** il dizionario ci dà un accesso diretto. Ma per cercare "chi si
chiama Mario" non c'è una chiave pronta: bisogna scorrere tutti i valori del
dizionario (`self.contatti.values()`) e controllare uno per uno. È il prezzo
da pagare quando si cerca per qualcosa di diverso dalla chiave — ma dato che
una rubrica personale ha al massimo qualche centinaio di contatti, scorrerli
tutti resta comunque velocissimo.

| Metodo | Cosa fa |
|---|---|
| `cerca(testo)` | contatti il cui **nome o cognome** contiene `testo` (maiuscole/minuscole indifferenti) |
| `elenco()` | tutti i contatti ordinati per cognome, poi nome |
| `is_vuota()` | `True` se non ci sono contatti |
```

- [ ] **Step 2: Aggiungi la cella di codice**

```python
    def cerca(self, testo):
        """Contatti il cui nome O cognome contiene 'testo' (case-insensitive)."""
        testo = testo.strip().lower()
        if testo == "":
            return []
        return [c for c in self.contatti.values()
                if testo in c.nome.lower() or testo in c.cognome.lower()]

    def elenco(self):
        """Tutti i contatti ordinati per cognome, poi nome."""
        return sorted(self.contatti.values(),
                      key=lambda c: (c.cognome.lower(), c.nome.lower()))

    def is_vuota(self):
        """True se non ci sono contatti."""
        return len(self.contatti) == 0
```

> Nota per chi esegue questo task: questi tre metodi vanno aggiunti
> **dentro** la classe `Rubrica` già presente nel notebook (stessa cella
> creata al Task 3, oppure una cella successiva se il notebook li mantiene
> separati — l'importante è che restino metodi della stessa classe
> `Rubrica`, con la stessa indentazione dei metodi già scritti).

- [ ] **Step 3: Esegui la cella e verifica a mano**

In una cella temporanea (da eliminare dopo):

```python
r = Rubrica("_verifica_.json")
r.aggiungi("Mario", "Rossi", "333", "", "")
r.aggiungi("Anna", "Bianchi", "347", "", "")
r.aggiungi("marco", "Rossini", "348", "", "")
assert {c.cognome for c in r.cerca("ross")} == {"Rossi", "Rossini"}
assert {c.nome for c in r.cerca("MAR")} == {"Mario", "marco"}
assert r.cerca("   ") == []
assert [c.cognome for c in r.elenco()] == ["Bianchi", "Rossi", "Rossini"]
assert r.is_vuota() is False
assert Rubrica("_altro_.json").is_vuota() is True
print("OK Rubrica parte 2")
```

Expected: stampa `OK Rubrica parte 2`. Elimina la cella temporanea dopo la
verifica.

- [ ] **Step 4: Commit**

```bash
git add ContactEase.ipynb
git commit -m "feat: aggiungi ricerca ed elenco a Rubrica"
```

---

## Task 5: Classe `Rubrica` — persistenza su file JSON

**Files:**
- Modify: `ContactEase.ipynb` (aggiunta di celle in coda)

**Interfaces:**
- Consumes: `Rubrica` (Task 3-4), `Contatto.to_dict`/`from_dict` (Task 2)
- Produces: metodi `salva()`, `carica()` sulla classe `Rubrica`.

- [ ] **Step 1: Aggiungi la cella markdown esplicativa**

```markdown
## La classe `Rubrica` — parte 3: salvataggio e caricamento

Ultimo pezzo: leggere e scrivere i contatti su un file JSON, così non si
perdono quando il programma si chiude.

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

| Metodo | Cosa fa |
|---|---|
| `salva()` | scrive contatti e contatore nel file JSON |
| `carica()` | legge i contatti dal file JSON, se esiste ed è valido |

Se il file manca o è danneggiato, `carica()` non solleva un errore: avvisa
e parte con una rubrica vuota, senza toccare il file esistente.
```

- [ ] **Step 2: Aggiungi la cella di codice**

```python
    def salva(self):
        """Scrive contatti e contatore su file JSON (UTF-8, leggibile)."""
        dati = {
            "prossimo_id": self.prossimo_id,
            "contatti": [c.to_dict() for c in self.contatti.values()],
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
        contatti_letti = [Contatto.from_dict(d) for d in dati.get("contatti", [])]
        self.contatti = {c.id: c for c in contatti_letti}
        if "prossimo_id" in dati:
            self.prossimo_id = dati["prossimo_id"]
        elif self.contatti:
            self.prossimo_id = max(self.contatti.keys()) + 1
        else:
            self.prossimo_id = 1
```

> Come nel Task 4, questi metodi vanno aggiunti dentro la classe `Rubrica`.

- [ ] **Step 3: Esegui la cella e verifica a mano**

In una cella temporanea (da eliminare dopo), usando un file di prova:

```python
percorso = "_verifica_salva_.json"
r = Rubrica(percorso)
r.aggiungi("Mario", "Rossi", "333", "", "")
r.aggiungi("Anna", "Bianchi", "347", "", "")
r.salva()

r2 = Rubrica(percorso)
r2.carica()
assert [c.to_dict() for c in r2.elenco()] == [c.to_dict() for c in r.elenco()]
assert r2.prossimo_id == r.prossimo_id

r3 = Rubrica("_file_inesistente_.json")
r3.carica()
assert r3.is_vuota() is True

os.remove(percorso)
print("OK Rubrica parte 3")
```

Expected: stampa `OK Rubrica parte 3`. Elimina la cella temporanea dopo la
verifica (il file `_verifica_salva_.json` viene già rimosso dal codice
stesso).

- [ ] **Step 4: Commit**

```bash
git add ContactEase.ipynb
git commit -m "feat: aggiungi salvataggio e caricamento JSON a Rubrica"
```

---

## Task 6: Funzioni dell'interfaccia utente (rich)

**Files:**
- Modify: `ContactEase.ipynb` (aggiunta di celle in coda)

**Interfaces:**
- Consumes: `Rubrica`/`Contatto` (Task 2-5), `rich` (Task 1)
- Produces: `console`, `VOCI_MENU`, `pulisci_schermo()`, `intestazione(titolo)`, `chiedi_riga(messaggio="")`, `mostra_menu()`, `mostra_tabella(contatti, titolo)`, `chiedi_dati_contatto(correnti=None)`, `leggi_intero(messaggio)`, `messaggio_ok(testo)`, `messaggio_errore(testo)`, `messaggio_info(testo)`, `pausa()`. Usate da `main()` nel Task 7.

- [ ] **Step 1: Aggiungi la cella markdown esplicativa**

```markdown
## Le funzioni dell'interfaccia

Sono funzioni separate dalle classi: si occupano **solo** di mostrare cose a
schermo e di leggere l'input dell'utente, usando la libreria `rich` per una
resa ordinata (pannelli, tabelle, colori).

### Principio: una schermata per volta

L'applicazione gira dentro l'output di **una sola cella** (quella con
`main()`). Ogni volta che l'utente fa una scelta, quell'output viene
**ripulito** prima di mostrare il passo successivo. A schermo restano solo:

1. l'**intestazione** dell'azione corrente;
2. le **informazioni necessarie in quel momento** — senza residui dei passi
   precedenti.

`intestazione(titolo)` fa proprio questo: pulisce lo schermo e stampa il
pannello del titolo.

### Come vengono lette le risposte

Tutte le domande passano da `chiedi_riga(messaggio)`, che stampa la domanda
nell'**output della cella** (così è visibile, non solo nella casella di
input del frontend) e poi legge una riga da tastiera. Il piccolo `flush` e
la pausa prima di `input()` evitano un difetto noto di Jupyter/Colab per cui
la prima `input()` dopo un `clear_output()` restituirebbe subito una
stringa vuota, senza aspettare che l'utente digiti.

| Funzione | Ruolo |
|---|---|
| `pulisci_schermo()` | svuota l'output della cella |
| `intestazione(titolo)` | pulisce lo schermo e stampa il pannello del titolo |
| `chiedi_riga(messaggio)` | stampa la domanda e legge una riga da tastiera |
| `mostra_menu()` | elenca le voci del menu |
| `mostra_tabella(contatti, titolo)` | mostra i contatti in tabella |
| `chiedi_dati_contatto(correnti=None)` | chiede i 5 campi di un contatto |
| `leggi_intero(messaggio)` | legge un numero, ripetendo se l'input non è valido |
| `messaggio_ok / messaggio_errore / messaggio_info` | righe colorate di esito |
| `pausa()` | attende la pressione di Invio |
```

- [ ] **Step 2: Aggiungi la cella di codice**

```python
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


def chiedi_riga(messaggio=""):
    """Stampa 'messaggio' nell'output della cella e legge una riga da tastiera."""
    print(messaggio, end="", flush=True)
    time.sleep(0.1)
    return input()


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
        risposta = chiedi_riga(f"{etichetta}{suffisso}: ").strip()
        if risposta == "" and valore_corrente is not None:
            return valore_corrente
        if risposta == "" and not obbligatorio:
            return ""
        if risposta != "":
            return risposta
        console.print("  [red]Campo obbligatorio.[/red]")


def chiedi_dati_contatto(correnti=None):
    """Raccoglie i 5 campi di un contatto e li restituisce in un dizionario."""
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
        risposta = chiedi_riga(f"{messaggio}: ").strip()
        if risposta == "":
            continue
        try:
            return int(risposta)
        except ValueError:
            console.print("  [red]Inserisci un numero intero.[/red]")


def messaggio_ok(testo):
    console.print(f"[bold green]OK[/bold green] {testo}")


def messaggio_errore(testo):
    console.print(f"[bold red]Errore[/bold red] {testo}")


def messaggio_info(testo):
    console.print(f"[cyan]{testo}[/cyan]")


def pausa():
    chiedi_riga("\nPremi Invio per continuare...")
```

- [ ] **Step 3: Esegui la cella e verifica a mano**

Esegui la cella (nessun `input()` viene chiamato all'esecuzione, quindi non
blocca). Verifica visivamente in una cella temporanea che `mostra_tabella`
funzioni:

```python
r = Rubrica("_verifica_.json")
r.aggiungi("Mario", "Rossi", "333", "", "")
mostra_tabella(r.elenco(), "Prova tabella")
```

Expected: viene stampata una tabella `rich` con la riga di Mario Rossi.
Elimina la cella temporanea dopo il controllo visivo.

- [ ] **Step 4: Commit**

```bash
git add ContactEase.ipynb
git commit -m "feat: aggiungi le funzioni dell'interfaccia utente"
```

---

## Task 7: Funzione `main()` e avvio dell'applicazione

**Files:**
- Modify: `ContactEase.ipynb` (aggiunta di celle in coda)

**Interfaces:**
- Consumes: `Rubrica` (Task 3-5), tutte le funzioni del Task 6
- Produces: `NOME_FILE`, funzione `main()`, cella di avvio che chiama `main()`.

- [ ] **Step 1: Aggiungi la cella markdown esplicativa**

```markdown
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
```

- [ ] **Step 2: Aggiungi la cella di codice**

```python
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
            testo = chiedi_riga("Nome o cognome da cercare: ")
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
            risposta = chiedi_riga("Salvare le modifiche? [s/n] (default s): ").strip().lower()
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

- [ ] **Step 3: Aggiungi la cella markdown "Esegui main" e la cella di avvio**

```markdown
# Esegui main
```

```python
# Avvia l'applicazione. Esegui questa cella e segui il menu.
# Per fermarla: scegli l'opzione 7 (Esci) oppure interrompi l'esecuzione
# della cella (menu Runtime -> Interrompi esecuzione).
main()
```

- [ ] **Step 4: Verifica end-to-end insieme all'utente**

Questo passo non è automatizzabile (richiede `input()` interattivo): esegui
la cella di avvio insieme all'utente e prova a mano, in ordine, ogni voce
del menu (1-7), incluse le modifiche/eliminazioni su ID inesistenti e
l'uscita con salvataggio. Spiega cosa succede a ogni passo mentre lo
provate.

Expected: nessun errore/crash; ogni voce di menu si comporta come descritto
nello spec (§ Gestione errori).

- [ ] **Step 5: Commit**

```bash
git add ContactEase.ipynb
git commit -m "feat: aggiungi main() e avvio dell'applicazione"
```

---

## Task 8: Cella finale di test automatici

**Files:**
- Modify: `ContactEase.ipynb` (aggiunta di celle in coda)

**Interfaces:**
- Consumes: `Rubrica`, `Contatto` (Task 2-5)
- Produces: nessuna nuova interfaccia (task terminale del notebook applicativo).

- [ ] **Step 1: Aggiungi la cella markdown esplicativa**

```markdown
# Verifica automatica

Questa cella controlla che i metodi della classe `Rubrica` funzionino come
previsto. Usa un file temporaneo: **non tocca** `contatti.json`.
```

- [ ] **Step 2: Aggiungi la cella di codice con i test**

```python
import tempfile

def _verifica():
    # 1) aggiungi() assegna id progressivi e aggiorna il contatore
    r = Rubrica("_test_.json")
    r.aggiungi("Mario", "Rossi", "333", "", "")
    r.aggiungi("Anna", "Bianchi", "347", "", "")
    r.aggiungi("marco", "Rossini", "348", "", "")
    assert list(r.contatti.keys()) == [1, 2, 3]
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
        assert [c.to_dict() for c in r2.elenco()] == [c.to_dict() for c in r.elenco()]
        assert r2.prossimo_id == r.prossimo_id
    finally:
        if os.path.exists(percorso):
            os.remove(percorso)

    print("✅ Tutti i test superati.")

_verifica()
```

- [ ] **Step 3: Esegui la cella**

Run: esegui la cella nel notebook.
Expected: stampa `✅ Tutti i test superati.` senza `AssertionError`.

- [ ] **Step 4: Commit**

```bash
git add ContactEase.ipynb
git commit -m "test: aggiungi la cella di verifica automatica finale"
```

---

## Task 9: Materiali da portfolio (README, LICENSE, requirements.txt)

**Files:**
- Create: `README.md`
- Create: `LICENSE`
- Create: `requirements.txt`
- Create: `contatti.json` (dati di esempio fittizi)
- Modify: `.gitignore` (verifica, nessuna modifica se già corretto)

**Interfaces:**
- Consumes: nessuno (file di corredo, non importati dal notebook)
- Produces: nessuno

- [ ] **Step 1: Crea `requirements.txt`**

```
rich
```

- [ ] **Step 2: Crea `LICENSE` (MIT)**

```
MIT License

Copyright (c) 2026 MonkeyDAndre

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

- [ ] **Step 3: Crea `contatti.json` di esempio**

```json
{
  "prossimo_id": 3,
  "contatti": [
    {
      "id": 1,
      "nome": "Mario",
      "cognome": "Rossi",
      "numero": "+39 333 1234567",
      "email": "mario.rossi@example.com",
      "indirizzo": "Via Roma 1, Milano"
    },
    {
      "id": 2,
      "nome": "Anna",
      "cognome": "Bianchi",
      "numero": "+39 347 7654321",
      "email": "",
      "indirizzo": ""
    }
  ]
}
```

- [ ] **Step 4: Crea `README.md`**

```markdown
# ContactEase

Rubrica di contatti a riga di comando, scritta in Python con un approccio
orientato agli oggetti. Progetto realizzato per un corso di programmazione
Python, eseguibile interamente da un notebook Jupyter/Google Colab.

## Funzionalità

- Aggiungere un contatto
- Visualizzare tutti i contatti
- Cercare un contatto per nome o cognome
- Modificare un contatto esistente
- Eliminare un contatto
- Salvare i contatti su file JSON e caricarli automaticamente all'avvio

## Come provarlo

**Su Google Colab (consigliato):** apri [ContactEase.ipynb](ContactEase.ipynb)
su Colab ed esegui le celle in ordine dall'alto verso il basso.

**In locale:**

```bash
pip install -r requirements.txt
jupyter notebook ContactEase.ipynb
```

Poi esegui le celle in ordine ed esegui l'ultima cella di avvio per
interagire con il menu.

## Struttura del progetto

- `ContactEase.ipynb` — l'intera applicazione (classi, interfaccia, test)
- `contatti.json` — file dati di esempio, nel formato usato dall'app
- `docs/superpowers/` — documenti di design e piano di implementazione del
  progetto

## Tecnologie

- Python 3
- [`rich`](https://github.com/Textualize/rich) per l'interfaccia a riga di
  comando

## Licenza

Distribuito con licenza MIT — vedi [LICENSE](LICENSE).
```

- [ ] **Step 5: Verifica `.gitignore`**

Controlla che `.gitignore` contenga almeno:

```
.git
.venv
__pycache__/
*.pyc
```

Se manca qualcosa, aggiungilo. Non serve modificarlo se è già a posto (è già
così da `.gitignore` esistente).

- [ ] **Step 6: Commit**

```bash
git add README.md LICENSE requirements.txt contatti.json .gitignore
git commit -m "docs: aggiungi README, licenza MIT e requirements per il portfolio"
```

---

## Task 10: Pulizia finale della repository

**Files:**
- Modify: `contesto-progetto.md` → spostato in `docs/contesto-progetto.md`
- Delete: `old/` (intera cartella)

**Interfaces:**
- Consumes: nessuno
- Produces: nessuno (task di pulizia)

- [ ] **Step 1: Sposta il file di contesto in `docs/`**

```bash
git mv contesto-progetto.md docs/contesto-progetto.md
```

- [ ] **Step 2: Rimuovi la cartella `old/` dalla repo**

```bash
git rm -r old/
```

(La cronologia resta comunque recuperabile con `git log --all --full-history -- old/`.)

- [ ] **Step 3: Verifica lo stato finale della repo**

Run: `git status` e `ls -la` nella root del progetto.

Expected: nella root restano solo `README.md`, `LICENSE`,
`requirements.txt`, `ContactEase.ipynb`, `contatti.json`, `.gitignore`,
`.git/`, `docs/` (con `superpowers/specs`, `superpowers/plans` e
`contesto-progetto.md`). Nessun residuo di `old/`, `__pycache__/`, file di
verifica temporanei.

- [ ] **Step 4: Commit finale**

```bash
git add -A
git commit -m "chore: rimuovi il tentativo precedente e riorganizza la repo per il portfolio"
```

- [ ] **Step 5: Promemoria per l'utente (non un'azione da eseguire ora)**

A questo punto il progetto è pronto per essere:
1. pubblicato su GitHub (repo pubblica);
2. aperto su Google Colab per generare il link pubblico richiesto dalla
   consegna del corso (File → Salva una copia su GitHub, o caricamento
   diretto di `ContactEase.ipynb` su Colab).
