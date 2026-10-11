"""Gestore di attività da terminale.

Permette di aggiungere, visualizzare, completare ed eliminare attività.
I dati vengono salvati nel file tasks.json, quindi restano anche dopo
aver chiuso il programma.
"""

import json
from pathlib import Path

FILE_DATI = Path("tasks.json")


def carica_attivita():
    """Legge le attività dal file. Se il file non esiste, restituisce una lista vuota."""
    if not FILE_DATI.exists():
        return []
    with open(FILE_DATI, "r", encoding="utf-8") as file:
        return json.load(file)


def salva_attivita(attivita):
    """Scrive le attività sul file."""
    with open(FILE_DATI, "w", encoding="utf-8") as file:
        json.dump(attivita, file, indent=2, ensure_ascii=False)


def mostra_attivita(attivita):
    """Stampa l'elenco numerato delle attività."""
    if not attivita:
        print("\nNessuna attività presente.")
        return
    print("\nLe tue attività:")
    for numero, attivita_singola in enumerate(attivita, start=1):
        stato = "[x]" if attivita_singola["completata"] else "[ ]"
        print(f"  {numero}. {stato} {attivita_singola['titolo']}")


def aggiungi_attivita(attivita):
    titolo = input("Titolo della nuova attività: ").strip()
    if not titolo:
        print("Il titolo non può essere vuoto.")
        return
    attivita.append({"titolo": titolo, "completata": False})
    salva_attivita(attivita)
    print("Attività aggiunta!")


def chiedi_numero(attivita, messaggio):
    """Chiede un numero all'utente e controlla che sia valido. Restituisce l'indice o None."""
    try:
        numero = int(input(messaggio))
    except ValueError:
        print("Devi inserire un numero.")
        return None
    if numero < 1 or numero > len(attivita):
        print("Numero non valido.")
        return None
    return numero - 1


def completa_attivita(attivita):
    mostra_attivita(attivita)
    if not attivita:
        return
    indice = chiedi_numero(attivita, "Numero dell'attività da completare: ")
    if indice is not None:
        attivita[indice]["completata"] = True
        salva_attivita(attivita)
        print("Attività completata!")


def elimina_attivita(attivita):
    mostra_attivita(attivita)
    if not attivita:
        return
    indice = chiedi_numero(attivita, "Numero dell'attività da eliminare: ")
    if indice is not None:
        rimossa = attivita.pop(indice)
        salva_attivita(attivita)
        print(f"Eliminata: {rimossa['titolo']}")


def main():
    attivita = carica_attivita()
    while True:
        print("\n=== GESTORE ATTIVITÀ ===")
        print("1. Mostra attività")
        print("2. Aggiungi attività")
        print("3. Completa attività")
        print("4. Elimina attività")
        print("0. Esci")
        scelta = input("Scegli un'opzione: ").strip()

        if scelta == "1":
            print(">>> HO RICEVUTO 1, attività:", attivita)
            mostra_attivita(attivita)
        elif scelta == "2":
            aggiungi_attivita(attivita)
        elif scelta == "3":
            completa_attivita(attivita)
        elif scelta == "4":
            elimina_attivita(attivita)
        elif scelta == "0":
            print("A presto!")
            break
        else:
            print("Opzione non valida, riprova.")


if __name__ == "__main__":
    main()