import time
from rich.console import Console
from rich.panel import Panel
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from rich import box
from rich.prompt import Prompt
import ui
import time
from rich.console import Console
from InquirerPy import inquirer
import json
from Rubrica import Rubrica

FILE_NAME = 'contatti.json'

MENU_PRINCIPALE = '''
    1 ) Aggiungi contatto\n
    2 ) Visualizza contatti\n
    3 ) Ricerca un contatto\n
    4 ) Elimina tutti i contatti\n 
    5 ) Esci\n\n
    '''.replace('   ', '')

INSERIMENTO_CONTATTI = '''
    Aggiungi nuovi contatti 
    '''.replace('   ', '')

try:
    with open(FILE_NAME, 'r') as f:
        rubrica = Rubrica(json.load(f))  

except FileNotFoundError as e:
    with open(FILE_NAME, 'w') as f:
        json.dump({'contatti' : []}, f, indent=3) 
        rubrica = Rubrica({'contatti' : []}) 
        

console = Console()

def main():
    while True:
        with console.screen():
            ui.menu_panel(MENU_PRINCIPALE, 'Menù Principale Rubrica')

            scelta = inquirer.rawlist(
                message= '(Digita un numero o usa le frecce per navigare le opzioni e premi invio per confermare)',
                choices=["Aggiungi contatto", "Visualizza contatti", "Ricerca un contatto", 
                         "Elimina tutti i contatti", "Esci"]
            ).execute()
                    
            if scelta == 'Aggiungi contatto':
                name = []
                number = []
                email = []
                address = []
                while True:
                    ui.menu_panel(INSERIMENTO_CONTATTI, 'Inserimento Contatti')
                    name.append(input('Inserire nome contatto       : '))        
                    number.append(input('Inserire numero contatto     : '))
                    email.append(input('Inserire email contatto      : '))
                    address.append(input('Inserire indirizzo contatto  : '))
                    while True:
                        ui.menu_panel(INSERIMENTO_CONTATTI, 'Vuoi inserire un altro contatto?')
                        scelta_inserimento = inquirer.rawlist(
                                    message= '(Digita un numero o usa le frecce per navigare le opzioni e premi invio per confermare)',
                                    choices=["Si", "No"]).execute()
            
                        if scelta_inserimento == 'Si':
                            break
                        else:
                            break

                    if scelta_inserimento == 'No':
                        break

            elif scelta == 'Visualizza contatti':

                input()

            elif scelta == 'Ricerca un contatto':
                input()

            elif scelta == 'Elimina tutti i contatti':
                input()

            elif scelta == 'Esci':
                exit(1)



if __name__ == "__main__":
    main()