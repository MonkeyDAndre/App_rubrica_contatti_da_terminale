# ContactEase — Design

**Data:** 2026-09-15
**Stato:** approvato in brainstorming, pronto per il piano di implementazione

## Contesto e obiettivi

ContactEase è una rubrica di contatti a riga di comando in Python, sviluppata
come deliverable per un corso ("modulo Python") e, in aggiunta, come primo
progetto di un portfolio personale su GitHub.

Requisiti della consegna (da `Richiesta.png`):

1. Programmazione orientata agli oggetti (OOP).
2. Una struttura dati efficiente per i contatti.
3. Interfaccia a riga di comando, interattiva e facile da usare.
4. Funzionalità: aggiungere, visualizzare, modificare, eliminare, cercare
   (per nome o cognome), salvare su file e caricare all'avvio.
5. Consegna: link pubblico a un notebook Google Colab.

**Vincolo aggiuntivo dell'utente:** l'utente è un principiante che sta
imparando Python ora. Priorità a leggibilità e semplicità sopra
l'ottimizzazione; ogni pezzo di codice va spiegato passo-passo, sia in
conversazione sia con celle markdown nel notebook.

**Vincolo aggiuntivo di consegna:** oltre al notebook, la repository deve
risultare pulita e presentabile come pezzo di portfolio GitHub.

## Decisioni di design

### Approccio di sviluppo

Il codice viene scritto **da zero**, direttamente dentro `ContactEase.ipynb`,
una cella alla volta, spiegando ogni pezzo mentre viene scritto (scelto
esplicitamente per il valore di apprendimento, invece di riprendere il
notebook del tentativo precedente, ora archiviato in `old/`).

Convenzione per ogni sezione di codice: **una cella markdown che spiega cosa
fa e perché**, seguita dalla cella di codice, commentata riga per riga dove
il "perché" non è ovvio.

### Struttura del notebook

1. Introduzione (markdown)
2. Import e installazione di `rich`
3. Classe `Contatto`
4. Classe `Rubrica`
5. Funzioni dell'interfaccia utente
6. Funzione `main()` e avvio dell'app
7. Cella finale con i test automatici

### Modello dati

**`Contatto`** — un oggetto che rappresenta una singola persona:

- Attributi: `id`, `nome`, `cognome`, `numero` (obbligatori: nome, cognome,
  numero), `email`, `indirizzo` (facoltativi).
- Metodi: `to_dict()` e il class method `from_dict(d)`, usati per il
  salvataggio/caricamento JSON.

**`Rubrica`** — gestisce la collezione di contatti e la persistenza:

```python
self.contatti = {}      # chiave: id (int) -> valore: oggetto Contatto
self.prossimo_id = 1
```

Scelta esplicita del **dizionario** (invece di una lista): l'accesso per
`id` — usato da modifica ed eliminazione — diventa O(1) con
`self.contatti.get(id)` invece di dover scorrere l'intera collezione. La
ricerca per nome/cognome resta comunque una scansione di
`self.contatti.values()`, perché lì non esiste una chiave diretta da usare:
è un'occasione didattica per mostrare che la struttura dati giusta dipende
da come i dati vengono interrogati.

Metodi previsti: `aggiungi`, `trova_per_id`, `modifica`, `elimina`, `cerca`,
`elenco` (contatti ordinati per cognome poi nome, per la visualizzazione),
`is_vuota`, `salva`, `carica`.

### Interfaccia utente

Menu a riga di comando dentro un ciclo in `main()`, con libreria `rich` per
la resa (pannelli, tabelle, colori). Funzioni di supporto:

- `intestazione(titolo)` — pulisce l'output della cella (`clear_output`) e
  stampa un pannello col titolo dell'azione corrente, per il principio "una
  schermata per volta".
- `chiedi_riga(messaggio)` — stampa la domanda e legge l'input; include un
  piccolo `flush` + pausa per evitare un difetto noto di Jupyter/Colab per
  cui la prima `input()` dopo un `clear_output()` restituirebbe subito una
  stringa vuota.
- `mostra_tabella(contatti, titolo)` — mostra i contatti in una tabella
  `rich`, o un messaggio se la lista è vuota.
- `chiedi_dati_contatto(correnti=None)` — raccoglie i campi di un contatto;
  in modifica, premere Invio mantiene il valore attuale.
- `leggi_intero(messaggio)` — legge un numero intero, ripetendo la domanda
  se l'input non è valido.

### Persistenza

File JSON locale `contatti.json`, caricato automaticamente all'avvio di
`main()`. Formato:

```json
{
  "prossimo_id": 3,
  "contatti": [
    {"id": 1, "nome": "Mario", "cognome": "Rossi", "numero": "333...",
     "email": "", "indirizzo": ""}
  ]
}
```

Salvataggio esplicito tramite voce di menu, più richiesta di conferma
all'uscita (nessun autosalvataggio silenzioso). Nota markdown su come
puntare il file a Google Drive per la persistenza tra sessioni Colab.

### Gestione errori

- Scelta di menu non valida → messaggio d'errore, si ritorna al menu.
- Campo obbligatorio (nome, cognome, numero) vuoto → si richiede di nuovo;
  email/indirizzo restano facoltativi.
- ID inesistente in modifica/eliminazione → messaggio d'errore chiaro,
  nessuna eccezione non gestita.
- `contatti.json` mancante o corrotto al caricamento → si parte con rubrica
  vuota e un avviso, senza sovrascrivere il file.

### Test

Un'unica cella finale con asserzioni (`assert`), senza framework esterni,
su un file JSON temporaneo (mai `contatti.json` vero). Scenari coperti:

1. `aggiungi()` assegna id progressivi e aggiorna `prossimo_id`.
2. `trova_per_id()` trova un contatto esistente, `None` se non esiste.
3. `cerca()` trova per nome o cognome, case-insensitive.
4. `modifica()` aggiorna i campi di un contatto esistente, `False` se l'id
   non esiste.
5. `elimina()` rimuove un contatto esistente, `False` se l'id non esiste.
6. `elenco()` restituisce i contatti ordinati per cognome poi nome.
7. `salva()` + `carica()` fanno un giro completo su file senza perdere dati.

Ogni assert ha un commento che spiega cosa verifica.

## Struttura della repository finale

```
README.md          — descrizione del progetto, funzionalità, link al
                      notebook Colab, istruzioni per eseguirlo in locale
LICENSE             — MIT
requirements.txt    — rich
ContactEase.ipynb   — il notebook, deliverable del corso
contatti.json       — 2-3 contatti di esempio fittizi (mostrano il formato
                      a chi apre la repo senza eseguire il notebook)
.gitignore          — verificato/aggiornato (__pycache__/, .venv/)
docs/
  superpowers/
    specs/          — questo documento e i futuri design
    plans/          — i piani di implementazione
  contesto-progetto.md  — spostato qui dalla root a fine progetto
```

La cartella `old/` (tentativo precedente) resta disponibile durante lo
sviluppo come riferimento, ma viene **rimossa dalla repo finale** come
ultimo step di pulizia — resta comunque recuperabile dalla cronologia git.

## Non-obiettivi (fuori scope)

- Nessun database esterno: solo file JSON locale.
- Nessuna interfaccia grafica: solo CLI testuale.
- Nessun supporto multi-utente/multi-rubrica.
- Nessun autosalvataggio silenzioso: il salvataggio è sempre esplicito o
  confermato in uscita.
- Nessuna ricerca "fuzzy": corrispondenza per sottostringa, case-insensitive,
  su nome o cognome.
