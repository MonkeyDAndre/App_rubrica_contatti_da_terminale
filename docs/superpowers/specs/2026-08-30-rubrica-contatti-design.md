# ContactEase — Rubrica contatti in un notebook — Design

**Data:** 2026-08-30
**Stato:** approvato in brainstorming, in attesa di revisione finale prima del piano di implementazione

## Obiettivo

Realizzare "ContactEase", un'applicazione console interattiva per la gestione di
una rubrica di contatti telefonici, **interamente dentro un unico Jupyter
notebook** (`ContactEase.ipynb`), consegnabile tramite link pubblico a Google
Colab.

Il codice deve essere:

- comprensibile e ben commentato;
- non troppo complesso;
- organizzato in celle ben strutturate, ognuna con una responsabilità chiara;
- con interfaccia formattata in modo curato tramite la libreria `rich`;
- **compatibile con Google Colab** in ogni sua parte.

## Requisiti dalla traccia

1. **OOP in Python** — struttura a oggetti solida e leggibile.
2. **Struttura dati** — efficiente per memorizzare i contatti.
3. **Interfaccia utente** — da linea di comando, interattiva, con un menu
   principale a opzioni chiare.
4. **Funzionalità:**
   - Aggiunta di un contatto
   - Visualizzazione di tutti i contatti
   - Modifica di un contatto esistente
   - Eliminazione di un contatto
   - Ricerca di un contatto per nome o cognome
   - Salvataggio su file e caricamento all'avvio (formato JSON)
5. **Consegna** — link pubblico a un notebook Google Colab.

## Decisioni di design (dal brainstorming)

| Tema | Decisione |
|---|---|
| Interfaccia in Colab | Loop di menu con `input()` / `rich.prompt` + output formattato con `rich`. Niente `InquirerPy`, `console.screen()`, `os.system('cls')`, `subprocess`: non compatibili con Colab. |
| Campi del contatto | `nome`, `cognome`, `numero`, `email`, `indirizzo`. |
| Persistenza | File JSON locale (`contatti.json`) nella cartella di lavoro di Colab. Una cella markdown spiega che i dati durano per la sessione e come montare Google Drive per una persistenza permanente. |
| Selezione contatto per modifica/elimina | Ogni contatto ha un `id` numerico stabile assegnato alla creazione, salvato nel JSON tramite un contatore `prossimo_id`. |
| Struttura OOP | Due classi: `Contatto` (dato) e `Rubrica` (operazioni + persistenza). La UI resta in funzioni separate. |
| Nome notebook | `ContactEase.ipynb` |
| Test | Una cella finale con controlli `assert` sui metodi di `Rubrica`. |
| Pulizia dello schermo | A ogni passo dell'esecuzione l'output della cella viene ripulito: si vede solo l'intestazione dell'azione corrente e le informazioni necessarie in quel momento. Vedi "Principio: una schermata per volta". |

## Principio: una schermata per volta

L'applicazione gira dentro l'output di una singola cella del notebook. Ogni
volta che l'utente fa una scelta, quell'output viene **ripulito** prima di
mostrare il passo successivo. In ogni momento a schermo compaiono soltanto:

1. l'**intestazione** dell'azione corrente (un pannello `rich` con il titolo,
   es. "Aggiungi contatto", "Cerca contatto", "Menu principale");
2. le **informazioni necessarie in quel preciso momento** (una tabella, una
   domanda, un messaggio di esito) — niente residui dei passi precedenti.

Concretezza dell'implementazione:

- Una funzione `intestazione(titolo: str)` esegue `pulisci_schermo()` e poi
  stampa il pannello del titolo. Viene chiamata all'inizio del ciclo del menu
  e all'inizio di **ogni** azione (1-7).
- Dentro un'azione a più passi (es. "Modifica": elenco -> chiedi ID -> form ->
  esito) si richiama `intestazione(titolo)` prima di ogni passo, così il passo
  precedente sparisce e resta visibile solo l'intestazione più il passo
  corrente.
- Il messaggio di esito (`messaggio_ok` / `messaggio_errore`) viene mostrato
  dopo un'ultima `intestazione(titolo)`, seguito da `pausa()`. Alla pressione
  di Invio il ciclo riparte e `intestazione("Menu principale")` ripulisce
  tutto.

## Architettura

Tre livelli, dal più interno al più esterno:

```
Contatto  ->  Rubrica  ->  funzioni di interfaccia (rich)  ->  main()
(dato)        (logica +     (input/output a schermo)          (ciclo menu)
              persistenza)
```

- `Contatto` non conosce nessuno.
- `Rubrica` conosce solo `Contatto` e il modulo `json`. L'unica stampa a
  schermo ammessa dentro `Rubrica` è nei messaggi di `carica()` sugli stati
  anomali del file (file assente o corrotto), fatti con un semplice `print`.
- Le funzioni di interfaccia conoscono `rich` e chiamano i metodi di `Rubrica`.
- `main()` mette insieme tutto: crea la `Rubrica`, la carica, esegue il ciclo
  del menu.

## Modello dati

### Classe `Contatto`

Attributi:

- `id: int` — identificativo stabile, assegnato dalla `Rubrica`.
- `nome: str`
- `cognome: str`
- `numero: str` — stringa (per conservare prefissi, spazi, `+`).
- `email: str` — può essere stringa vuota.
- `indirizzo: str` — può essere stringa vuota.

Metodi:

- `__init__(self, id, nome, cognome, numero, email, indirizzo)`
- `to_dict(self) -> dict` — restituisce
  `{"id", "nome", "cognome", "numero", "email", "indirizzo"}`.
- `from_dict(cls, d: dict) -> "Contatto"` — classmethod; ricostruisce un
  `Contatto` da un dizionario letto dal JSON.

### Formato del file `contatti.json`

```json
{
  "prossimo_id": 4,
  "contatti": [
    {
      "id": 1,
      "nome": "Mario",
      "cognome": "Rossi",
      "numero": "+39 333 1234567",
      "email": "mario.rossi@example.com",
      "indirizzo": "Via Roma 1, Milano"
    }
  ]
}
```

- `prossimo_id` — prossimo identificativo libero; salvato nel file così gli ID
  restano stabili anche dopo eliminazioni e riavvii.
- `contatti` — lista di oggetti contatto serializzati.

## Classe `Rubrica`

### Stato

- `self.percorso_file: str` — percorso del file JSON.
- `self.contatti: list[Contatto]` — contatti in memoria.
- `self.prossimo_id: int` — contatore degli ID (parte da 1).

### Metodi

| Firma | Comportamento |
|---|---|
| `__init__(self, percorso_file: str)` | Inizializza `percorso_file`, `contatti = []`, `prossimo_id = 1`. Non carica automaticamente: il caricamento è esplicito in `main()`. |
| `carica(self) -> None` | Se il file non esiste: resta vuota e mostra un messaggio informativo. Se esiste ma è JSON non valido: mostra un messaggio di errore e resta vuota (non sovrascrive il file). Se valido: popola `contatti` con `Contatto.from_dict(...)` e imposta `prossimo_id` dal file (se assente, `max(id)+1` o `1`). |
| `salva(self) -> None` | Scrive su `percorso_file` un dizionario `{"prossimo_id": ..., "contatti": [c.to_dict() ...]}` con `json.dump(..., indent=2, ensure_ascii=False)`. |
| `aggiungi(self, nome, cognome, numero, email, indirizzo) -> Contatto` | Crea `Contatto(self.prossimo_id, ...)`, lo aggiunge a `contatti`, incrementa `prossimo_id`, restituisce il contatto creato. |
| `modifica(self, id, nome, cognome, numero, email, indirizzo) -> bool` | Cerca per `id`. Se trovato, sovrascrive i cinque campi e restituisce `True`. Se non trovato, restituisce `False`. |
| `elimina(self, id) -> bool` | Rimuove il contatto con quell'`id`. `True` se rimosso, `False` se inesistente. |
| `cerca(self, testo: str) -> list[Contatto]` | Restituisce i contatti il cui `nome` **oppure** `cognome` contiene `testo` come sottostringa, confronto case-insensitive e con `strip()`. Se `testo` è vuoto dopo `strip()`, restituisce lista vuota. |
| `trova_per_id(self, id) -> Contatto | None` | Helper: primo contatto con quell'`id`, altrimenti `None`. |
| `elenco(self) -> list[Contatto]` | Tutti i contatti ordinati per `cognome`, poi `nome` (case-insensitive). |
| `is_vuota(self) -> bool` | `True` se `contatti` è vuota. |

Note:

- `modifica` sovrascrive sempre tutti i campi con i valori ricevuti. La logica
  "premi Invio per tenere il valore attuale" vive nell'interfaccia
  (`chiedi_dati_contatto` passa i valori correnti come default), non nel
  metodo.
- Nessun metodo di `Rubrica` usa `rich`. Gli unici output ammessi sono i
  `print` di `carica()` sugli stati anomali del file (assente o corrotto).

## Interfaccia utente (funzioni con `rich`)

Modulo di funzioni a livello di cella, con un unico oggetto condiviso
`console = Console()`.

| Funzione | Comportamento |
|---|---|
| `pulisci_schermo() -> None` | `IPython.display.clear_output(wait=True)` — pulisce l'output della cella in Colab/Jupyter. |
| `intestazione(titolo: str) -> None` | Chiama `pulisci_schermo()` e poi stampa un `rich.panel.Panel` con `titolo`. È il modo standard per iniziare ogni schermata (menu e ogni passo di ogni azione), così resta visibile solo l'intestazione corrente più il passo attuale. |
| `mostra_menu() -> None` | Stampa le 7 voci numerate del menu (dentro il pannello aperto da `intestazione("Menu principale")`). |
| `mostra_tabella(contatti: list[Contatto], titolo: str) -> None` | Stampa una `rich.table.Table` con colonne ID, Nome, Cognome, Numero, Email, Indirizzo. Se la lista è vuota, stampa un messaggio informativo invece della tabella. |
| `chiedi_dati_contatto(correnti: dict | None = None) -> dict` | Chiede i cinque campi con `rich.prompt.Prompt.ask`. In inserimento `correnti` è `None`. In modifica `correnti` contiene i valori attuali, passati come `default=` (Invio conferma). `nome`, `cognome`, `numero` obbligatori: se vuoti (dopo `strip()`) la domanda si ripete. `email` e `indirizzo` facoltativi. Restituisce un dizionario con le cinque chiavi. |
| `leggi_intero(messaggio: str) -> int` | Legge un intero con ciclo di validazione; ripete finché l'input non è un numero intero valido. Usato per la scelta di menu e per l'ID. |
| `messaggio_ok(testo: str)` / `messaggio_errore(testo: str)` / `messaggio_info(testo: str)` | Righe colorate (verde / rosso / ciano) con `console.print`. |
| `pausa() -> None` | `input("\nPremi Invio per continuare...")`. |

## `main()` e ciclo del menu

Ogni azione parte con `intestazione(titolo)` (che ripulisce lo schermo) e la
richiama di nuovo prima di ogni passo successivo, così a video restano solo
l'intestazione corrente e il passo attuale.

```
def main():
    rubrica = Rubrica("contatti.json")
    rubrica.carica()
    while True:
        intestazione("Menu principale")          # pulisce lo schermo + pannello
        mostra_menu()
        scelta = leggi_intero("Seleziona un'opzione")

        1 -> Aggiungi:
                intestazione("Aggiungi contatto")
                dati = chiedi_dati_contatto()
                c = rubrica.aggiungi(**dati)
                intestazione("Aggiungi contatto"); messaggio_ok(...)
        2 -> Visualizza:
                intestazione("Tutti i contatti")
                mostra_tabella(rubrica.elenco(), "Tutti i contatti")
        3 -> Cerca:
                intestazione("Cerca contatto")
                testo = Prompt.ask("Nome o cognome da cercare")
                intestazione("Cerca contatto")
                mostra_tabella(rubrica.cerca(testo), f"Risultati per '{testo}'")
        4 -> Modifica:
                intestazione("Modifica contatto")
                mostra_tabella(rubrica.elenco(), "Tutti i contatti")
                id = leggi_intero("ID del contatto da modificare")
                c = rubrica.trova_per_id(id)
                se None -> intestazione("Modifica contatto"); messaggio_errore(...)
                altrimenti ->
                    intestazione("Modifica contatto")
                    dati = chiedi_dati_contatto(correnti=c.to_dict())
                    rubrica.modifica(id, **dati)
                    intestazione("Modifica contatto"); messaggio_ok(...)
        5 -> Elimina:
                intestazione("Elimina contatto")
                mostra_tabella(rubrica.elenco(), "Tutti i contatti")
                id = leggi_intero("ID del contatto da eliminare")
                intestazione("Elimina contatto")
                se rubrica.elimina(id) -> messaggio_ok(...) altrimenti messaggio_errore(...)
        6 -> Salva:
                intestazione("Salva su file")
                rubrica.salva(); messaggio_ok(...)
        7 -> Esci:
                intestazione("Esci")
                se Prompt.ask("Salvare le modifiche? [s/n]", default="s") == "s":
                    rubrica.salva()
                messaggio_info("Arrivederci"); break
        altro -> intestazione("Menu principale"); messaggio_errore("Opzione non valida")

        se scelta != 7: pausa()
```

### Voci del menu

```
1. Aggiungi contatto
2. Visualizza tutti i contatti
3. Cerca contatto (per nome o cognome)
4. Modifica contatto
5. Elimina contatto
6. Salva su file
7. Esci
```

Il salvataggio è esplicito (voce 6) più una richiesta di conferma all'uscita
(voce 7). Non c'è salvataggio automatico dopo ogni modifica: la scelta rende
visibile e didattico il ciclo carica/salva.

## Gestione errori

| Situazione | Comportamento |
|---|---|
| File `contatti.json` assente all'avvio | `carica()` mostra un messaggio informativo, la rubrica parte vuota. Il file viene creato al primo `salva()`. |
| File JSON corrotto / non parsabile | `carica()` cattura `json.JSONDecodeError`, mostra un messaggio di errore, la rubrica parte vuota e **non** sovrascrive il file. |
| Scelta di menu non numerica | `leggi_intero` cattura `ValueError` e ripete la domanda. |
| Scelta di menu fuori range (es. 9) | Ramo `else`: `messaggio_errore("Opzione non valida")`. |
| ID inesistente in modifica/elimina | `messaggio_errore`, nessuna modifica ai dati. |
| Campi obbligatori vuoti in inserimento/modifica | `chiedi_dati_contatto` ripete la singola domanda finché il valore non è non vuoto. |
| Ricerca con testo vuoto | `cerca` restituisce lista vuota; `mostra_tabella` stampa "nessun contatto". |

## Struttura del notebook (celle)

| # | Tipo | Contenuto |
|---|---|---|
| 1 | markdown | Titolo "ContactEase", descrizione del progetto, requisiti in breve, **nota Colab**: il file `contatti.json` vive nella sessione corrente e viene perso al riciclo della runtime; istruzioni per montare Google Drive se si vuole persistenza permanente. |
| 2 | code | `!pip install -q rich` + import (`json`, `os`, `rich...`, `IPython.display.clear_output`). |
| 3 | markdown | Spiegazione della classe `Contatto`: ruolo, attributi, `to_dict`/`from_dict`. |
| 4 | code | Classe `Contatto`. |
| 5 | markdown | Spiegazione della classe `Rubrica`: stato, elenco dei metodi, formato del file JSON. |
| 6 | code | Classe `Rubrica`. |
| 7 | markdown | Spiegazione delle funzioni di interfaccia e del perché sono separate dalle classi. |
| 8 | code | Funzioni di interfaccia con `rich`. |
| 9 | markdown | Spiegazione di `main()` e del ciclo del menu; come si usa l'app. |
| 10 | code | Funzione `main()`. |
| 11 | code | Avvio dell'applicazione: `main()`. |
| 12 | code | **Verifica rapida** (facoltativa): controlli `assert` sui metodi di `Rubrica` usando un file temporaneo, senza toccare `contatti.json`. |

## Cella 12 — verifica rapida (contenuto previsto)

Controlli `assert`, con stampa finale "Tutti i test superati":

- `aggiungi` incrementa `prossimo_id` e assegna ID progressivi (1, 2, 3).
- `cerca` trova per sottostringa del nome, case-insensitive.
- `cerca` trova per sottostringa del cognome.
- `cerca` con testo vuoto restituisce `[]`.
- `modifica` su ID esistente aggiorna i campi e restituisce `True`;
  su ID inesistente restituisce `False`.
- `elimina` su ID esistente restituisce `True` e riduce la lista;
  su ID inesistente restituisce `False`.
- `elenco` restituisce i contatti ordinati per cognome, poi nome.
- `salva()` seguito da una nuova `Rubrica(...).carica()` sullo stesso file
  temporaneo restituisce gli stessi contatti e lo stesso `prossimo_id`
  (round-trip di persistenza).
- Pulizia del file temporaneo al termine.

## Dipendenze

- `rich` — installata in Colab con `!pip install -q rich` (spesso già presente).
- Standard library: `json`, `os`, `tempfile` (solo nella cella di test).
- `IPython.display.clear_output` — già disponibile in Colab.
- **Escluse** rispetto ai prototipi: `InquirerPy`, `subprocess`, `console.screen()`.

## Fuori scope (YAGNI)

- Validazione avanzata di numero/email (regex, formati internazionali).
- Import/export CSV o vCard.
- Undo/redo, cronologia modifiche.
- Più rubriche o categorie/gruppi di contatti.
- Interfaccia grafica con `ipywidgets`.
- Test con `pytest` / framework esterni: la cella 12 con `assert` è sufficiente
  per un deliverable in notebook.
