# Contesto del progetto — ContactEase (rubrica contatti in Python)

> File di contesto per il **restart da zero** del progetto. Il tentativo
> precedente è stato spostato in [old/](old/) per riferimento, ma si
> riparte con un nuovo brainstorming/design/piano.

## 1. Origine del compito

Deliverable per un corso ("modulo Python"). Richiesta originale in
[Richiesta.png](Richiesta.png) (rimasta in root, non è "vecchio materiale").

## 2. Requisiti della consegna (da Richiesta.png)

**Titolo:** Software di una rubrica di contatti con Python — "ContactEase
Solutions".

**Obiettivo:** applicazione console interattiva per gestire contatti
telefonici (aggiungere, modificare, eliminare, visualizzare, cercare), con
salvataggio/caricamento dati.

**Requisiti espliciti:**
1. **OOP in Python** — struttura solida e scalabile.
2. **Struttura dati** efficiente per memorizzare i contatti.
3. **Interfaccia utente** a riga di comando, interattiva e facile da usare.
4. **Funzionalità richieste:**
   - Aggiunta di un contatto
   - Visualizzazione di tutti i contatti
   - Modifica di un contatto esistente
   - Eliminazione di un contatto
   - Ricerca di un contatto per **nome o cognome**
   - Salvataggio su file e caricamento automatico all'avvio (es. JSON)

**Interfaccia:** menu principale con opzioni chiare, adatta anche a utenti
poco esperti.

**Modalità di consegna:** **link pubblico a un notebook Google Colab.**
→ Vincolo pesante: tutto deve girare in celle Jupyter/Colab, niente
librerie o pattern che richiedano un vero terminale (vedi §4).

## 3. Materiale del tentativo precedente (ora in `old/`)

Un primo giro di lavoro era già stato completato e funzionante:

- `old/ContactEase.ipynb` — notebook consegnabile, classi `Contatto` +
  `Rubrica`, interfaccia a menu con libreria `rich`, persistenza JSON
  (`old/contatti.json`), test rapidi inclusi in una cella finale.
- `old/scratch/` — sorgenti di sviluppo usati per **generare** il notebook
  (`build_notebook.py`) più suite di test separate (`test_main.py`,
  `test_ref.py`, `test_ui.py`, `contactease_ref.py`, `run_cells.py`).
- `old/docs/superpowers/` — spec e piano scritti con un flusso "superpowers"
  fatto a mano (`specs/2026-08-30-rubrica-contatti-design.md`,
  `plans/2026-08-30-rubrica-contatti.md`), **prima** di avere il plugin
  `superpowers` reale installato.
- `old/brainstorming.md`, `old/execute_plan.md`, `old/write_plan.md` — file
  di skill "fatte in casa" in root, ora superate dal plugin
  `superpowers@claude-plugins-official` effettivamente installato.
- `old/Rubrica.py`, `old/main.py`, `old/main_old.py`, `old/ui.py` — versione
  ancora precedente, non a notebook (script `.py` separati), poi abbandonata
  a favore del notebook unico.

**Perché ripartire da zero:** l'utente vuole rifare il progetto "per bene",
ora con il plugin `superpowers` reale (skill: brainstorming, writing-plans,
executing-plans, TDD, ecc.) invece del flusso artigianale precedente. Il
codice in `old/` è un riferimento utile (soluzioni già validate, es. per il
bug di `input()` dopo `clear_output()` su Colab) ma **non va riusato
automaticamente**: le decisioni di design vanno riprese da capo nel nuovo
brainstorming.

## 4. Vincoli tecnici noti (validi a prescindere dal design che sceglieremo)

Emersi dal lavoro precedente, restano vincoli oggettivi di Google Colab:

- Niente librerie che richiedono un vero terminale/TTY: no `InquirerPy`,
  no `subprocess`, no `console.screen()` di `rich`.
- L'unico modo per avere un'interfaccia "interattiva" in Colab è un loop a
  menu basato su `input()` in una cella, eventualmente abbellito con
  `rich` (pannelli, tabelle, colori) o anche solo `print()`.
- Bug noto Jupyter/Colab: la **prima** `input()` dopo
  `IPython.display.clear_output()` può restituire una stringa vuota subito,
  senza aspettare l'utente — serve un `flush` + piccola pausa prima di
  `input()`, o un'altra strategia.
- Persistenza dati: il filesystem di Colab è **volatile** (si azzera alla
  fine della sessione) — il notebook deve poter salvare/caricare un JSON
  locale, con eventualmente una nota su come puntare a Google Drive per
  persistenza reale.

## 5. Stato strumenti/skill disponibili ora

- Plugin `superpowers@claude-plugins-official` installato e disponibile via
  CLI/estensione (skill: `brainstorming`, `writing-plans`,
  `executing-plans`, `test-driven-development`, `systematic-debugging`,
  `requesting-code-review`, `verification-before-completion`, ecc.).
- C'è anche una memoria persistente (`contactease-project.md` nel sistema
  di memoria dell'assistente) con i vincoli decisi nel brainstorming del
  30/08/2026 (notebook unico, classi `Contatto`+`Rubrica`, "una schermata
  per volta", ecc.). Va trattata come **riferimento storico**, da
  confermare o rivedere nel nuovo brainstorming, non come decisione già
  presa per questo restart.

## 6. Stato repository dopo il restart

- `Richiesta.png` resta in root.
- Tutto il resto del tentativo precedente è stato spostato in `old/`
  (con `git mv` per i file tracciati, per preservare la history).
- Questo file (`contesto-progetto.md`) è il nuovo punto di partenza.
- Prossimo passo (da fare **con l'utente**, non ancora eseguito): nuovo
  giro di `superpowers:brainstorming` per ridefinire il design da zero.
