import os
import subprocess



def starting_menu():
    MENU = '''
================ Menù Rubrica ContactEase ================\n

1 ) Aggiungi contatto\n
2 ) Visualizza contatti\n
3 ) Ricerca un contatto\n
4 ) Esci\n\n
    '''
    print(MENU)


def clear_screen():
    comando = 'cls' if os.name == 'nt' else 'clear'
    # 'shell=True' passa il comando al terminale di sistema
    subprocess.run(comando, shell=True)


def add_contact_menu():
    ADD_CONTACT_MENU = '''
================ Aggiungi nuovi contatti ================\n\n\n
    '''
    print(ADD_CONTACT_MENU)


def show_contacts_menu():
    ADD_CONTACT_MENU = '''
================ Contatti presenti in rubrica ================\n\n\n
    '''
    print(ADD_CONTACT_MENU)

def exit_message():
    EXIT_MESSAGE = '''
================ Chiusura applicazione rubrica ================\n\n\n

Modifiche salvate


Ciao :)
    '''
    print(EXIT_MESSAGE)

def search_contacts_menu():
    SEARCH_CONTACTS_MENU = '''
================ Ricerca contatti presenti in rubrica ================\n\n
Puoi cercare dei contatti inserenso solo nome, solo congome o entrambi
Inserire nome o cognome del contatto da ricercare : \n
    '''
    print(SEARCH_CONTACTS_MENU)

def search_contacts_menu_choice(l):
    if l == 0:
        SEARCH_CONTACTS_MENU_CHOICE = '''
        Vuoi cercare un altro contatto? (y/n)
        '''
        print(SEARCH_CONTACTS_MENU_CHOICE)
    elif l == 1:
        SEARCH_CONTACTS_MENU_CHOICE = '''
Vuoi modificare o eliminare il contatto trovato?\n
Inserisci:\n
1) Per eliminare il contatto\n
2) Per modificare il contatto\n
3) Per tornare al menù iniziale\n\n
        '''
        print(SEARCH_CONTACTS_MENU_CHOICE)
    else:
        SEARCH_CONTACTS_MENU_CHOICE = '''
Vuoi modificare o eliminare uno dei contatti trovati?\n
Inserisci:\n
1) Per eliminare un contatto\n
2) Per modificare un contatto\n
3) Per tornare al menù iniziale\n\n
        '''
        print(SEARCH_CONTACTS_MENU_CHOICE)


def delete_contacts_menu():
    DELETE_CONTACTS_MENU_CHOICE = '''
================ Ricerca contatto da eliminare ================\n\n
Puoi cercare dei contatti inserenso solo nome, solo congome o entrambi
Inserire nome o cognome del contatto da ricercare : \n
    '''
    print(DELETE_CONTACTS_MENU_CHOICE)

def blank_rows(n):
    print('\n'*n)


def error_message(err, valori_validi):
    if err != 0:
        print(f'Inserito valore non valido. I valori validi sono {valori_validi}.')

