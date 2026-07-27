import json
import ui
from Rubrica import Rubrica


FILE_NAME = 'contatti.json'






try:
    with open(FILE_NAME, 'r') as f:
        rubrica = Rubrica(json.load(f))  

except FileNotFoundError as e:
    with open(FILE_NAME, 'w') as f:
        json.dump({'contatti' : []}, f, indent=3) 
        rubrica = Rubrica({'contatti' : []}) 
        
err_menu_principale = 0
valori_validi_menu_principale = ['1', '2', '3', '4']

while True:
    ui.clear_screen()
    ui.starting_menu()
    ui.error_message(err_menu_principale, valori_validi_menu_principale)
    op = input('Seleziona opzione -> ')
    if op == '1':
        err_menu_principale = 0
        valori_validi = ['y', 'n']
        err = 0
        name = []
        last_name = []
        number = []
        while True:
            ui.clear_screen()
            ui.add_contact_menu()  
            name.append(input('Inserire nome contatto    : '))        
            last_name.append(input('Inserire cognome contatto : '))
            number.append(input('Inserire numero contatto  : '))
            while True:
                ui.blank_rows(2)
                ui.error_message(err, valori_validi)
                scelta = input('Inserire un nuovo contatto? (y/n)  ')
                if scelta in valori_validi:
                    err = 0
                    break
                else:
                    err = 1
            if scelta == 'n' :
                rubrica.add(name, last_name, number)
                break

    elif op == '2':
        err_menu_principale = 0
        ui.clear_screen()
        ui.show_contacts_menu()
        if rubrica.is_empty():
            ui.blank_rows(2)
            print('Non ci sono contatti nella rubrica')
        else:
            print(rubrica)
        ui.blank_rows(3)
        input('Premere invio per tornare al menù principale...')


    elif op == '3':
        err_menu_principale = 0
        ui.clear_screen()
        ui.search_contacts_menu()
        name        = input('Nome    : ')
        last_name   = input('Cognome : ')
        ui.blank_rows(2)
        err = 0
        valori_validi = []
        scelta = ''
        while True:
            if scelta == 'n' or scelta == '3':
                break
            ui.clear_screen()
            ui.search_contacts_menu()
            ui.blank_rows(2)
            if scelta == 'y':
                name        = input('Nome    : ')
                last_name   = input('Cognome : ')
            ui.blank_rows(2)
            contact_indexes = rubrica.find(name, last_name)
            rubrica.show(contact_indexes)
            ui.blank_rows(2)
            ui.search_contacts_menu_choice(len(contact_indexes))

            if len(contact_indexes) == 0:
                while True:
                    if err == 1:
                        ui.clear_screen()
                        ui.search_contacts_menu()
                        ui.blank_rows(2)
                        rubrica.show(contact_indexes)
                        ui.blank_rows(2)
                        print(f'Inserito valore non valido. I valori validi sono {valori_validi}.')
                    ui.blank_rows(1)
                    scelta = input('Scelta : ')
                    if scelta == 'y':
                        break
                    elif scelta == 'n':
                        break
                    else:
                        err = 1
                        valori_validi = ['y', 'n']

            elif len(contact_indexes) == 1:
                while True:
                    if err == 1:
                        ui.clear_screen()
                        ui.search_contacts_menu()
                        ui.blank_rows(2)
                        if contact_indexes:
                            rubrica.show(contact_indexes)
                        ui.blank_rows(2)
                        print(f'Inserito valore non valido. I valori validi sono {valori_validi}.')
                    scelta = input('Scelta : ')
                    if scelta == '1':
                        err = 0
                        index = int(contact_indexes[0])
                        rubrica.delete(index)
                        contact_indexes.remove(index)
                        
                    elif scelta == '2':
                        err = 0
                        index = int(contact_indexes[0])
                        new_name        = input('Inserire nome contatto    : ')     
                        new_last_name   = input('Inserire cognome contatto  : ')
                        new_number      = input('Inserire numero contatto  : ')
                        rubrica.modify(int(index), new_name, new_last_name, new_number)

                    elif scelta == '3':
                        err = 0
                        break
                    else:
                        ui.blank_rows(2)
                        err = 1
                        valori_validi = ['1', '2', '3']

            else:
                while True:
                    if err == 1:
                        ui.clear_screen()
                        ui.search_contacts_menu()
                        ui.blank_rows(2)
                        if contact_indexes:
                            rubrica.show(contact_indexes)
                        ui.blank_rows(2)
                        print(f'Inserito valore non valido. I valori validi sono {valori_validi}.')
                    if scelta == '1':
                        err = 0
                        ui.blank_rows(2)
                        index = input("Inserisci l'indice del contatto da eliminare : ")
                        rubrica.delete(int(index))
                        contact_indexes.remove(int(index))
                        
                    elif scelta == '2':
                        err = 0
                        ui.blank_rows(2)
                        index = input("Inserisci l'indice del contatto da modificare : ")
                        new_name        = input('Inserire nome contatto    : ')     
                        new_last_name   = input('Inserire cognome contatto  : ')
                        new_number      = input('Inserire numero contatto  : ')
                        rubrica.modify(int(index), new_name, new_last_name, new_number)
                        
                    elif scelta == '3':
                        err = 0
                        break

                    else:
                        ui.blank_rows(2)
                        err = 1
                        valori_validi = ['1', '2', '3']
                    

    elif op == '4':
        err_menu_principale = 0
        ui.clear_screen()
        rubrica.save(FILE_NAME)
        ui.exit_message()
        
        exit(1)    
    else:
        err_menu_principale = 1
