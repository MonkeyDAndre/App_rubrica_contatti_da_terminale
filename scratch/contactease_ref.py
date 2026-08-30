"""Implementazione di riferimento di ContactEase.

Questo file NON fa parte del deliverable: serve solo per eseguire i test
durante lo sviluppo. Il codice qui dentro viene poi trascritto 1:1 nelle
celle del notebook ContactEase.ipynb.
"""

import json
import os

try:
    from IPython.display import clear_output
except ImportError:                       # esecuzione fuori da Jupyter (test)
    def clear_output(wait=False):
        pass

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box


# ===========================================================================
# CELLA 4 - Classe Contatto
# ===========================================================================
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


# ===========================================================================
# CELLA 6 - Classe Rubrica
# ===========================================================================
class Rubrica:
    """Gestisce la lista dei contatti e la persistenza su file JSON."""

    def __init__(self, percorso_file):
        self.percorso_file = percorso_file
        self.contatti = []          # lista di oggetti Contatto
        self.prossimo_id = 1        # id da assegnare al prossimo contatto

    # --- operazioni sui contatti -------------------------------------------
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

    # --- persistenza ------------------------------------------------------
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


# ===========================================================================
# CELLA 8 - Funzioni di interfaccia (rich)
# ===========================================================================
console = Console()

# Voci del menu principale (indice + 1 = numero mostrato a video).
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
    input("\nPremi Invio per continuare...")


# ===========================================================================
# CELLA 10 - main()
# ===========================================================================
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
