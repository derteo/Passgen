import csv
import os

NOME_FILE = 'studenti.csv'
FIELDNAMES = ['cf', 'nome', 'cognome', 'classe', 'voti', 'preferenze']

def caricaDaCSV():
    dizionario = {}
    if not os.path.exists(NOME_FILE):
        return dizionario

    try:
        with open(NOME_FILE, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                cf = row['cf']
                voti = []
                if row['voti']:
                    voti = [float(v) for v in row['voti'].strip('[]').split(',') if v.strip()]

                preferenze = {}
                if row['preferenze']:
                    parti = row['preferenze'].split('|')
                    for p in parti:
                        m, c = p.split(':')
                        preferenze[m] = int(c)

                dizionario[cf] = {
                    'nome': row['nome'],
                    'cognome': row['cognome'],
                    'cf': cf,
                    'classe': row['classe'],
                    'voti': voti,
                    'preferenze': preferenze
                }
    except Exception as e:
        print(f"Errore nel caricamento: {e}")
    return dizionario

def salvaSuCSV():
    try:
        with open(NOME_FILE, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()
            for cf, s in dizionarioStudenti.items():
                pref_str = "|".join([f"{m}:{c}" for m, c in s['preferenze'].items()])
                writer.writerow({
                    'cf': cf,
                    'nome': s['nome'],
                    'cognome': s['cognome'],
                    'classe': s['classe'],
                    'voti': s['voti'],
                    'preferenze': pref_str
                })
    except Exception as e:
        print(f"Errore nel salvataggio: {e}")

def visualizzaMenu():
    print("\n--- MENU ---")
    print("1. Inserimento nuovi dati questionario")
    print("2. Modifica dati di uno studente esistente")
    print("3. Eliminazione di uno o più questionari (per CF)")
    print("4. Ricerca questionari mediante un criterio da specificare")
    print("5. Visualizzare tutti i dati dei questionari raccolti")
    print("6. Aggiungere/Modificare voti per uno studente")
    print("7. Studente con media più alta")
    print("8. Preferenze: Contatore di tutte le materie (per ciascuno studente)")
    print("9. Preferenze: Visualizzare preferenze per una specifica materia")
    print("0. Uscita dal sistema")

def compilaQuestionario():
    nome = input("Inserisci Nome: ").strip()
    cognome = input("Inserisci Cognome: ").strip()

    while True:
        cf = input("Inserisci Codice Fiscale (identificatore unico): ").upper().strip()
        if not cf:
            print("Il codice fiscale non può essere vuoto!")
        elif cf in dizionarioStudenti:
            print("Codice fiscale già presente, non univoco!")
        else:
            break

    voti_iniziali = []
    materie_preferite = {}

    print("Inserisci i voti conseguiti (separati da virgola o spazio). Se non ci sono voti, premi Invio.")
    voti_input = input("Voti: ").strip()
    if voti_input:
        voti_iniziali = [float(v.strip()) for v in voti_input.replace(',', ' ').split()]

    print("Inserisci le materie preferite (separate da virgola). Es: Programmazione, Networking, AI")
    materie_input = input("Materie preferite: ").strip()
    if materie_input:
        for materia in [m.strip().lower() for m in materie_input.split(',')]:
            if materia:
                materie_preferite[materia] = materie_preferite.get(materia, 0) + 1

    nuovo_studente = {
        'nome': nome,
        'cognome': cognome,
        'cf': cf,
        'classe': input("Inserisci la classe frequentata (es. ITS-3): ").strip(),
        'voti': voti_iniziali,
        'preferenze': materie_preferite
    }
    dizionarioStudenti[cf] = nuovo_studente
    salvaSuCSV()
    print("Dati questionario inseriti!")

def modificaDatiStudenti():
    cf_ricerca = input("Inserisci il Codice Fiscale dello studente da modificare: ").strip().upper()

    if cf_ricerca not in dizionarioStudenti:
        print(f"Studente con CF {cf_ricerca} non trovato.")
        return

    studente = dizionarioStudenti[cf_ricerca]
    print("\n--- Dati Correnti ---")
    print(f"Nome: {studente['nome']} | Cognome: {studente['cognome']}")
    print(f"Classe: {studente['classe']} | Voti: {studente['voti']}")

    print("\nQuale campo vuoi modificare?")
    print("1. Nome")
    print("2. Cognome")
    print("3. Classe frequentata")

    scelta = input("Scelta (1-3): ").strip()

    if scelta == '1':
        studente['nome'] = input("Inserisci il nuovo Nome: ").strip()
        print("Nome aggiornato.")
    elif scelta == '2':
        studente['cognome'] = input("Inserisci il nuovo Cognome: ").strip()
        print("Cognome aggiornato.")
    elif scelta == '3':
        studente['classe'] = input("Inserisci la nuova Classe: ").strip()
        print("Classe aggiornata.")
    else:
        print("Scelta non valida.")

    salvaSuCSV()

def eliminaQuestionari():
    if not dizionarioStudenti:
        print("Nessuno studente presente.")
        return

    criterio = input("Inserisci il Codice Fiscale: ").strip().upper()
    if criterio in dizionarioStudenti:
        del dizionarioStudenti[criterio]
        salvaSuCSV()
        print(f"Studente con CF {criterio} eliminato.")
    else:
        print(f"Nessuno studente con CF {criterio} trovato.")

def ricercaQuestionari():
    if not dizionarioStudenti:
        print("Nessuno studente presente.")
        return

    print("Ricercare per:")
    print("1. Codice Fiscale")
    print("2. Classe")
    print("3. Nome")
    scelta = input("Scelta (1-3): ").strip()

    if scelta == '1':
        criterio = input("Inserisci il Codice Fiscale: ").strip().upper()
        if criterio in dizionarioStudenti:
            stampaStudente(dizionarioStudenti[criterio])
        else:
            print(f"Nessuno studente con CF {criterio} trovato.")

    elif scelta == '2':
        criterio = input("Inserisci la Classe: ").strip().lower()
        trovati = [s for s in dizionarioStudenti.values() if s['classe'].lower() == criterio]
        if not trovati:
            print(f"Nessuno studente in classe {criterio} trovato.")
        else:
            for s in trovati: stampaStudente(s)

    elif scelta == '3':
        criterio = input("Inserisci il Nome: ").strip().lower()
        trovati = [s for s in dizionarioStudenti.values() if s['nome'].lower() == criterio]
        if not trovati:
            print(f"Nessuno studente con nome {criterio} trovato.")
        else:
            for s in trovati: stampaStudente(s)
    else:
        print("Scelta non valida.")

def stampaStudente(studente):
    media = sum(studente['voti']) / len(studente['voti']) if studente['voti'] else None
    media_str = f"{media:.2f}" if media is not None else "N/D"
    print(f"Nome: {studente['nome']} {studente['cognome']} | CF: {studente['cf']} | "
          f"Classe: {studente['classe']} | Voti: {studente['voti']} | Media: {media_str} | "
          f"Preferenze: {studente['preferenze']}")

def visualizzaTuttiQuestionari():
    if not dizionarioStudenti:
        print("Nessuno studente presente.")
        return

    count = len(dizionarioStudenti)
    print(f"\n--- Tutti i Questionari ({count} student{'e' if count==1 else 'i'}) ---")

    for studente in dizionarioStudenti.values():
        stampaStudente(studente)

def gestisciVoti():
    if not dizionarioStudenti:
        print("Nessuno studente presente.")
        return

    cf_ricerca = input("Inserisci il Codice Fiscale dello studente: ").strip().upper()

    if cf_ricerca not in dizionarioStudenti:
        print(f"Studente con CF {cf_ricerca} non trovato.")
        return

    studente = dizionarioStudenti[cf_ricerca]
    print(f"\nStudente: {studente['nome']} {studente['cognome']}")
    print(f"Voti attuali: {studente['voti']}")

    voti_input = input("Inserisci i voti da aggiungere (separati da virgola o spazio): ").strip()
    if voti_input:
        try:
            nuovi = [float(v.strip()) for v in voti_input.replace(',', ' ').split()]
            studente['voti'].extend(nuovi)
            salvaSuCSV()
            print(f"Aggiunti {len(nuovi)} voti. Voti aggiornati: {studente['voti']}")
        except ValueError:
            print("Formato voti non valido.")

def contatorePreferenzePerStudente():
    if not dizionarioStudenti:
        print("Nessuno studente presente.")
        return

    print("\n--- Preferenze per studente ---")
    for studente in dizionarioStudenti.values():
        nome_completo = f"{studente['nome']} {studente['cognome']}"
        if studente['preferenze']:
            print(f"\n{nome_completo} ({studente['cf']}):")
            for materia, conteggio in studente['preferenze'].items():
                print(f"  {materia.title()}: {conteggio}")
        else:
            print(f"\n{nome_completo} ({studente['cf']}): nessuna preferenza registrata.")

def preferenzePerMateria():
    if not dizionarioStudenti:
        print("Nessuno studente presente.")
        return

    materia_ricerca = input("Inserisci il nome della materia: ").strip().lower()
    if not materia_ricerca:
        print("Nome materia non valido.")
        return

    trovati = [(s, s['preferenze'][materia_ricerca])
               for s in dizionarioStudenti.values()
               if materia_ricerca in s['preferenze']]

    if not trovati:
        print(f"Nessuno studente ha indicato '{materia_ricerca.title()}' come preferenza.")
        return

    trovati.sort(key=lambda x: x[1], reverse=True)
    print(f"\n--- Studenti che preferiscono '{materia_ricerca.title()}' ---")
    for studente, conteggio in trovati:
        print(f"  {studente['nome']} {studente['cognome']} ({studente['cf']}) "
              f"| Classe: {studente['classe']} | Volte indicata: {conteggio}")
    print(f"Totale studenti: {len(trovati)}")

def main():
    global dizionarioStudenti
    dizionarioStudenti = caricaDaCSV()

    while True:
        visualizzaMenu()
        scelta = input("\nScegli un'opzione (0-9): ").strip()

        if scelta == '1': compilaQuestionario()
        elif scelta == '2': modificaDatiStudenti()
        elif scelta == '3': eliminaQuestionari()
        elif scelta == '4': ricercaQuestionari()
        elif scelta == '5': visualizzaTuttiQuestionari()
        elif scelta == '6': gestisciVoti()
        elif scelta == '7': "non implementato: studente con media più alta (ziopera)"
        elif scelta == '8': contatorePreferenzePerStudente()
        elif scelta == '9': preferenzePerMateria()
        elif scelta == '0':
            print("Uscita.")
            break
        else:
            print("Scelta non valida. Riprova.")

dizionarioStudenti = {}
main()
