import json

class Rubrica:

    def __init__(self, dict_rubrica):          
        self.dict_rubrica = dict_rubrica  
        

    def add(self, name, last_name, number):
        print(len(name))
        print(name)
        print(last_name)
        print(number)
        for i in range(len(name)):
            self.dict_rubrica['contatti'].append(
                {
                    'nome' : name[i],
                    'cognome' : last_name[i],
                    'numero' : number[i]
                } )

    def show(self, contact_indexes):
        if not contact_indexes:
            print('Nessun contatto trovato')
        else:
            for index in contact_indexes:
                contact = self.dict_rubrica['contatti'][index]
                print(f'Indice contatto : {index}')
                print(f'Nome    : {contact['nome']}')
                print(f'Cognome : {contact['cognome']}')
                print(f'Numero  : {contact['numero']}')
                print('\n\n')

        

    def modify(self, index, name, last_name, number):
        self.dict_rubrica['contatti'][index]['nome'] = name
        self.dict_rubrica['contatti'][index]['cognome'] = last_name
        self.dict_rubrica['contatti'][index]['numero'] = number
        return 0

    def delete(self, index):
        self.dict_rubrica['contatti'].pop(index)
        return 0

    def find(self, name, last_name):
        contact_indexes = []
        if name == '' and last_name == '':
            return contact_indexes
        else:
            if name != '' and last_name != '':
                contact_indexes = [index for index, contatto in enumerate(self.dict_rubrica["contatti"])
                                    if contatto["nome"].strip().lower() == name.strip().lower() and contatto["cognome"].strip().lower() == last_name.strip().lower()]
            elif name != '':
                contact_indexes = [index for index, contatto in enumerate(self.dict_rubrica["contatti"])
                                    if contatto["nome"].strip().lower() == name.strip().lower()]
            else: 
                contact_indexes = [index for index, contatto in enumerate(self.dict_rubrica["contatti"])
                                    if contatto["cognome"].strip().lower() == last_name.strip().lower()]    
            return contact_indexes

    def load(delf, f):
        return 0

    def save(self, file_name):
        with open(file_name, 'w') as f:
            json.dump(self.dict_rubrica, f, indent=3)    


    def is_empty(self):
        if not self.dict_rubrica['contatti']:
            return True  # la lista dei contatti è vuota
        else:
            return False
        

    def __repr__(self):
        stringa_print = str('')

        for elem in self.dict_rubrica['contatti']:
            stringa_print += f'Nome    : {elem['nome']}\n'
            stringa_print += f'Cognome : {elem['cognome']}\n'
            stringa_print += f'Numero  : {elem['numero']}\n'
            stringa_print += '\n\n'

        return stringa_print