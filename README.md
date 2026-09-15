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
