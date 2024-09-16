from tkinter import *
from PIL import ImageTk, Image
import pyodbc
import os
import csv
from tkinter import ttk
import re
from tkinter import messagebox
import threading
from datetime import datetime
import datetime
import time

def apri_gestione_iscrizioni():
    global gestione_iscrizioni
    global iscrizioni_image_photo
    global frame_contenuto_iscrizioni
    global frame_iscrizioni_iscrizioni
    global frame_risultati_iscrizioni

    gestione_iscrizioni = Toplevel(root)
    gestione_iscrizioni.title('Gestione Iscrizioni')
    gestione_iscrizioni.geometry("1280x900")
    gestione_iscrizioni.configure(bg="#ffffff")
    gestione_iscrizioni.resizable(False, False)

    banner_iscrizioni = Frame(gestione_iscrizioni, background="white", height=100, width=900)
    banner_iscrizioni.grid(row=0, column=0, columnspan=2, sticky="nsew")
    iscrizioni_image_path = os.path.join(os.path.dirname(__file__), 'logo-unitre-arvalia.jpg')
    iscrizioni_image = Image.open(iscrizioni_image_path)
    iscrizioni_image = iscrizioni_image.resize((100, 100), Image.LANCZOS)  # Modifica la dimensione in base alle tue esigenze
    iscrizioni_image_photo = ImageTk.PhotoImage(iscrizioni_image)
    iscrizioni_image_label = Label(banner_iscrizioni, image=iscrizioni_image_photo, bg="#ffffff")
    iscrizioni_image_label.pack(side=LEFT, padx=10)
    title_iscrizioni = Label(banner_iscrizioni, text="Gestione Iscrizioni", font=("Open Sans", 16), bg="#ffffff", fg="#118e21")
    title_iscrizioni.pack(side=LEFT, padx=275)
    frame_bottoni = Frame(gestione_iscrizioni, background="white", height=75, width=900)
    frame_bottoni.grid(row=1, column=0, columnspan=2, sticky="nsew")
    nuova_iscrizione_button = Button(frame_bottoni, text="Nuova Iscrizione", font=("Open Sans", 10), bg="#ffffff", fg="#118e21", command=inserisci_iscrizione)
    nuova_iscrizione_button.pack(side=LEFT, padx= 10, pady=10)
    frame_contenuto_iscrizioni = Frame(gestione_iscrizioni, background="white", height=350, width=900)
    frame_contenuto_iscrizioni.grid(row=3, column=0, columnspan=2, sticky="nsew")
    frame_risultati_iscrizioni = Frame(gestione_iscrizioni, background="white", height=350, width=900)
    frame_risultati_iscrizioni.grid(row=4, column=0, columnspan=2, sticky="nsew") 
    frame_iscrizioni_iscrizioni = Frame(gestione_iscrizioni, background="white", height=350, width=900)
    frame_iscrizioni_iscrizioni.grid(row=5, column=0, columnspan=2, sticky="nsew")

def inserisci_iscrizione():
    global frame_contenuto_iscrizioni
    global frame_risultati_iscrizioni

    for widget in frame_contenuto_iscrizioni.winfo_children():
        widget.destroy()
    for widget in frame_risultati_iscrizioni.winfo_children():
        widget.destroy()

    label = Label(frame_contenuto_iscrizioni, text="Inserisci Iscrizione", font=("Open Sans", 14), bg="#ffffff", fg="#118e21")
    label.grid(row=0, column=0, columnspan=2, pady=20)

    label_iscritto = Label(frame_contenuto_iscrizioni, text="Ricerca Iscritto per Cognome", font=("Open Sans", 10), bg="#ffffff", fg="#118e21")
    label_iscritto.grid(row=1, column=0, padx=10, pady=5, sticky="w")

    iscritto_ricerca = StringVar()
    iscritto_ricerca_entry = Entry(frame_contenuto_iscrizioni, textvariable=iscritto_ricerca, width=40)
    iscritto_ricerca_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    lista_iscritti = Listbox(frame_contenuto_iscrizioni, width=60, height=5)
    lista_iscritti.grid(row=2, column=1, columnspan=2, padx=10, pady=5, sticky="w")

    def cerca_iscritto():
        query = iscritto_ricerca.get()
        if not query:
            messagebox.showerror("Errore", "Inserisci un criterio di ricerca.", parent=frame_contenuto_iscrizioni)
            return
        try:
            cursor = mydb.cursor()
            cursor.execute("SELECT DISTINCT ID_Anagrafica, Nominativo, Codice_Fiscale FROM Anagrafiche WHERE Cognome LIKE ?", ('%' + query + '%'))
            iscritti = cursor.fetchall()
            lista_iscritti.delete(0, END)
            for iscritto in iscritti:
                lista_iscritti.insert(END, f"{iscritto[0]} - {iscritto[1]} - {iscritto[2]}")
        except pyodbc.Error as err:
            print("Errore nella connessione al database:", err)
    
    cerca_iscritto_button = Button(frame_contenuto_iscrizioni, text="Cerca", command=cerca_iscritto)
    cerca_iscritto_button.grid(row=1, column=2, padx=10, pady=5, sticky="w")

    label_anno_accademico = Label(frame_contenuto_iscrizioni, text="Anno Accademico", font=("Open Sans", 10), bg="#ffffff", fg="#118e21")
    label_anno_accademico.grid(row=3, column=0, padx=10, pady=5, sticky="w")

    anno_accademico_selezionato = StringVar()
    anno_accademico_combobox = ttk.Combobox(frame_contenuto_iscrizioni, textvariable=anno_accademico_selezionato)
    anno_accademico_combobox['state'] = 'readonly'
    anno_accademico_combobox.grid(row=3, column=1, padx=10, pady=5, sticky="w")
    anno_accademico_combobox.bind("<<ComboboxSelected>>", lambda event: aggiorna_corsi_combobox(anno_accademico_selezionato.get()))

    try:
        cursor = mydb.cursor()
        cursor.execute("SELECT DISTINCT Anno_Accademico FROM Anni_Accademici")
        anni_accademici = [row[0] for row in cursor.fetchall()]
        anno_accademico_combobox['values'] = anni_accademici
    except pyodbc.Error as err:
        print("Errore nella connessione al database:", err)

    label_corso = Label(frame_contenuto_iscrizioni, text="Corso", font=("Open Sans", 10), bg="#ffffff", fg="#118e21")
    label_corso.grid(row=4, column=0, padx=10, pady=5, sticky="w")

    corso_selezionato = StringVar()
    corso_selezionato_combobox = ttk.Combobox(frame_contenuto_iscrizioni, textvariable=corso_selezionato, width=40)
    corso_selezionato_combobox['state'] = 'readonly'
    corso_selezionato_combobox.grid(row=4, column=1, padx=10, pady=5, sticky="w")

    label_data_iscrizione = Label(frame_contenuto_iscrizioni, text="Data Iscrizione", font=("Open Sans", 10), bg="#ffffff", fg="#118e21")
    label_data_iscrizione.grid(row=5, column=0, padx=10, pady=5, sticky="w")
    data_iscrizione_box = Entry(frame_contenuto_iscrizioni, width=30)
    data_iscrizione_box.grid(row=5, column=1, padx=10, pady=5, sticky="w")

    def aggiorna_corsi_combobox(anno_accademico):
        try:
            cursor = mydb.cursor()
            cursor.execute("SELECT C.Denominazione_Corso FROM Corsi AS C JOIN Anni_Accademici AS A ON C.ID_Anno_Accademico = A.ID_Anno_Accademico JOIN (SELECT COUNT(*) AS Iscritti, ID_Corso FROM Iscrizioni GROUP BY ID_Corso) AS V ON C.ID_Corso = V.ID_Corso WHERE A.Anno_Accademico = ? AND (C.Limite_Iscrizioni - V.Iscritti) > 0", (anno_accademico,))
            corsi = [row[0] for row in cursor.fetchall()]
            corso_selezionato_combobox['values'] = corsi
        except pyodbc.Error as err:
            print("Errore nella connessione al database:", err)

    def is_valid_date(date):
        return re.match(r'^\d{2}/\d{2}/\d{4}$', date) is not None
    
    def anteprima_iscrizione():
        global corso_selezionato
        global id_anagrafica_selezionato
        global nominativo_selezionato

        corso_selezionato = corso_selezionato_combobox.get()
        if not corso_selezionato:
            messagebox.showerror("Errore", "Seleziona un corso.", parent=frame_risultati_iscrizioni)
            return
        
        anno_accademico_selezionato = anno_accademico_combobox.get()
        if not anno_accademico_selezionato:
            messagebox.showerror("Errore", "Seleziona un anno accademico.", parent=frame_risultati_iscrizioni)
            return
        
        selected_iscritto = lista_iscritti.get(ACTIVE)
        if not selected_iscritto:
            messagebox.showerror("Errore", "Seleziona un iscritto.", parent=frame_risultati_iscrizioni)
            return
        id_anagrafica_selezionato = selected_iscritto.split(" - ")[0]
        nominativo_selezionato = selected_iscritto.split(" - ")[1] 
        
        cursor_conta_corsi = mydb.cursor()
        cursor_conta_corsi.execute(
            "SELECT COUNT(I.ID_Corso) FROM Iscrizioni AS I \
                    JOIN Corsi AS C ON I.ID_Corso = C.ID_Corso \
                    JOIN Anni_Accademici AS A ON A.ID_Anno_Accademico = C.ID_Anno_Accademico \
                    WHERE A.Anno_Accademico = ? AND I.ID_Anagrafica = ?",
            (anno_accademico_selezionato, id_anagrafica_selezionato)
            )
        numero_corsi = cursor_conta_corsi.fetchone()[0]
        numero_corsi = numero_corsi + 1

        cursor_quote = mydb.cursor()
        cursor_quote.execute(
            "SELECT Q.Importo FROM Quote AS Q \
                    JOIN Anagrafiche AS A ON A.ID_Qualifica = Q.ID_Qualifica \
                    JOIN Anni_Accademici AS AC ON AC.ID_Anno_Accademico = Q.ID_Anno_Accademico \
                    WHERE AC.Anno_Accademico = ? AND A.ID_Anagrafica = ?",
            (anno_accademico_selezionato, id_anagrafica_selezionato)
        )
        quota = cursor_quote.fetchone()[0]

        if numero_corsi <= 2:
            quota_iscrizione = quota
        else: 
            quota_iscrizione = quota + ((numero_corsi-2)*20)
        
        id_anagrafica_selezionato = selected_iscritto.split(" - ")[0]
        nominativo_selezionato = selected_iscritto.split(" - ")[1]   

        def aggiungi_iscrizione():
            try:
                cursor_corso = mydb.cursor()
                cursor_corso.execute("SELECT ID_Corso FROM Corsi WHERE Denominazione_Corso = ?", (corso_selezionato,))
                risultato_corso = cursor_corso.fetchone()
                if risultato_corso is None:
                    messagebox.showerror("Errore", "Corso non trovato.", parent=frame_risultati_iscrizioni)
                    return
                id_corso_selezionato = risultato_corso[0]

                data_selezionata = data_iscrizione_box.get() or ""
                if not is_valid_date(data_selezionata):
                    messagebox.showerror("Errore", "Data di Iscrizione inserita non valida. Formato corretto: gg/mm/aaaa", parent=frame_risultati_iscrizioni)
                    return
                
                cursor_verifica = mydb.cursor()
                cursor_verifica.execute(
                    "SELECT * FROM Iscrizioni WHERE ID_Anagrafica = ? AND ID_Corso = ?",
                    (id_anagrafica_selezionato, id_corso_selezionato)
                )
                if cursor_verifica.fetchone():
                    messagebox.showerror("Errore", "Questa iscrizione esiste già.", parent=frame_risultati_iscrizioni)
                    return
                
                cursor_inserimento = mydb.cursor()
                cursor_inserimento.execute(
                "INSERT INTO Iscrizioni (ID_Anagrafica, ID_Corso, Data_Iscrizione) VALUES (?, ?, ?)",
                (id_anagrafica_selezionato, id_corso_selezionato, data_selezionata)
                )
                mydb.commit()
                cursor_verifica_corso = mydb.cursor()
                cursor_verifica_corso.execute(
                    "SELECT COUNT(*) FROM Iscrizioni WHERE ID_Corso = ?", (id_corso_selezionato,)
                )
                iscrizioni = cursor_verifica_corso.fetchone()[0]
                cursor_limite_corso = mydb.cursor()
                cursor_limite_corso.execute(
                    "SELECT Limite_Iscrizioni FROM Corsi WHERE ID_Corso = ?", (id_corso_selezionato,)
                )
                limite_iscrizioni = cursor_limite_corso.fetchone()[0]
                if iscrizioni >= limite_iscrizioni:
                    messagebox.showinfo("Successo", "Iscrizione Aggiunta con successo. " "Attenzione: Posti Disponibili per iscrizione al corso terminati!", parent=frame_risultati_iscrizioni)
                else:
                    messagebox.showinfo("Successo", "Iscrizione Aggiunta con successo.", parent=frame_risultati_iscrizioni)
                chiudi_gestione_iscrizioni()
            except Exception as e:
                messagebox.showerror("Errore", f"Errore durante l'inserimento nel database: {str(e)}", parent=frame_risultati_iscrizioni)         

        testo_label1 = f"Con l'iscrizione al corso {corso_selezionato} per l'anno accademico {anno_accademico_selezionato}, l'iscritto {nominativo_selezionato} ha completato l'iscrizione a {numero_corsi} Corsi."
        testo_label2 = f"Deve corrispondere come quota di iscrizione {quota_iscrizione} euro."
        label_quota_iscrizione1 = Label(frame_risultati_iscrizioni, text=testo_label1, font=("Open Sans", 12), bg="#ffffff", fg="#118e21")
        label_quota_iscrizione1.grid(row=7, column=0, padx=10, pady=10, sticky="w")
        label_quota_iscrizione2 = Label(frame_risultati_iscrizioni, text=testo_label2, font=("Open Sans", 12), bg="#ffffff", fg="#118e21")
        label_quota_iscrizione2.grid(row=8, column=0, padx=10, pady=5, sticky="w")
        conferma_button = Button(frame_risultati_iscrizioni, text="Conferma Iscrizione", command=aggiungi_iscrizione)
        conferma_button.grid(row=9, column=0, padx=10, pady=5, sticky="w")


    anteprima_iscrizione_button = Button(frame_contenuto_iscrizioni, text="Anteprima Iscrizione", command=anteprima_iscrizione)
    anteprima_iscrizione_button.grid(row=6, column=0, padx=10, pady=5, sticky="w")

def apri_gestione_anagrafiche():
    global gestione_anagrafiche
    global anagrafiche_image_photo
    global frame_contenuto_anagrafiche
    global frame_iscrizioni_anagrafiche
    global frame_risultati_anagrafiche

    gestione_anagrafiche = Toplevel(root)
    gestione_anagrafiche.title('Gestione Anagrafiche')
    gestione_anagrafiche.geometry("1280x900")
    gestione_anagrafiche.configure(bg="#ffffff")
    gestione_anagrafiche.resizable(True, True)

    banner_anagrafiche = Frame(gestione_anagrafiche, background="white", height=100, width=900)
    banner_anagrafiche.grid(row=0, column=0, columnspan=2, sticky="nsew")

    anagrafiche_image_path = os.path.join(os.path.dirname(__file__), 'logo-unitre-arvalia.jpg')
    anagrafiche_image = Image.open(anagrafiche_image_path)
    anagrafiche_image = anagrafiche_image.resize((100, 100), Image.LANCZOS)  # Modifica la dimensione in base alle tue esigenze
    anagrafiche_image_photo = ImageTk.PhotoImage(anagrafiche_image)

    anagrafiche_image_label = Label(banner_anagrafiche, image=anagrafiche_image_photo, bg="#ffffff")
    anagrafiche_image_label.pack(side=LEFT, padx=10)
    title_anagrafiche = Label(banner_anagrafiche, text="Gestione Anagrafiche", font=("Open Sans", 16), bg="#ffffff", fg="#118e21")
    title_anagrafiche.pack(side=LEFT, padx=275)

    frame_bottoni = Frame(gestione_anagrafiche, background="white", height=75, width=900)
    frame_bottoni.grid(row=1, column=0, columnspan=2, sticky="nsew")

    nuova_anagrafica_button = Button(frame_bottoni, text="Nuova Anagrafica", font=("Open Sans", 10), bg="#ffffff", fg="#118e21", command=mostra_nuova_anagrafica)
    nuova_anagrafica_button.pack(side=LEFT, padx= 10, pady=10)
    modifica_anagrafica_button = Button(frame_bottoni, text="Modifica Anagrafica", font=("Open Sans", 10), bg="#ffffff", fg="#118e21", command=mostra_modifica_anagrafica)
    modifica_anagrafica_button.pack(side=LEFT, padx= 10, pady=10)

    frame_contenuto_anagrafiche = Frame(gestione_anagrafiche,background="white", height=350, width=900)
    frame_contenuto_anagrafiche.grid(row=3, column=0, columnspan=2, sticky="nsew")
    frame_risultati_anagrafiche = Frame(gestione_anagrafiche, background="white", height=350, width=900)
    frame_risultati_anagrafiche.grid(row=4, column=0, columnspan=2, sticky="nsew") 
    frame_iscrizioni_anagrafiche = Frame(gestione_anagrafiche, background="white", height=350, width=900)
    frame_iscrizioni_anagrafiche.grid(row=5, column=0, columnspan=2, sticky="nsew")

def mostra_nuova_anagrafica():

    for widget in frame_contenuto_anagrafiche.winfo_children():
        widget.destroy()
    for widget in frame_risultati_anagrafiche.winfo_children():
        widget.destroy()

    label = Label(frame_contenuto_anagrafiche, text="Inserisci Nuova Anagrafica", font=("Open Sans", 14), bg="#ffffff", fg="#118e21")
    label.grid(row=0, column=0, columnspan=2, pady=20)

    def pulisci_campi_anagrafiche():
        cognome_box.delete(0, END)
        nome_box.delete(0, END)
        sesso_box.delete(0, END)
        luogo_nascita_box.delete(0, END)
        provincia_nascita_box.delete(0, END)
        data_nascita_box.delete(0, END)
        codice_fiscale_box.delete(0, END)
        indirizzo_residenza_box.delete(0, END)
        comune_residenza_box.delete(0, END)
        cap_box.delete(0, END)
        provincia_residenza_box.delete(0, END)
        mobile_box.delete(0, END)
        fisso_box.delete(0, END)
        email_box.delete(0, END)
        ambito_professionale_box.delete(0, END)
        ruolo_box.delete(0, END)
        numero_tessera_nazionale_box.delete(0, END)
        numero_tessera_locale_box.delete(0, END)
        data_associazione_box.delete(0, END)
        qualifica_box.delete(0, END)
        numero_ordine_registrazione_box.delete(0, END)

    def clean_input(value):
        return value if value != '' else None
    def is_valid_email(email):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_regex, email) is not None
    def is_valid_date(date):
        return re.match(r'^\d{2}/\d{2}/\d{4}$', date) is not None
    def is_valid_codice_fiscale(codice_fiscale):
        return re.match(r'^[A-Z0-9]{16}$', codice_fiscale) is not None
    def is_valid_int(value):
        try:
            int(value)
            return True
        except ValueError:
            return False
    
    def aggiungi_anagrafiche():
        cognome = clean_input(cognome_box.get() or "")
        nome = clean_input(nome_box.get() or "")
        nominativo = f"{cognome} {nome}"
        sesso = clean_input(sesso_box.get() or "")
        luogo_nascita = clean_input(luogo_nascita_box.get() or "")
        provincia_nascita = clean_input(provincia_nascita_box.get() or "")
        data_nascita = clean_input(data_nascita_box.get() or "")
        codice_fiscale = clean_input(codice_fiscale_box.get() or "")
        indirizzo_residenza = clean_input(indirizzo_residenza_box.get() or "")
        comune_residenza = clean_input(comune_residenza_box.get() or "")
        cap = clean_input(cap_box.get() or "")
        provincia_residenza = clean_input(provincia_residenza_box.get() or "")
        mobile = clean_input(mobile_box.get() or "")
        fisso = clean_input(fisso_box.get() or "")
        email = clean_input(email_box.get() or "")
        ambito_professionale = clean_input(ambito_professionale_box.get() or "")
        ruolo = clean_input(ruolo_box.get() or "")
        numero_tessera_nazionale = clean_input(numero_tessera_nazionale_box.get() or "")
        numero_tessera_locale = clean_input(numero_tessera_locale_box.get() or "")
        data_associazione = clean_input(data_associazione_box.get() or "")
        qualifica = clean_input(qualifica_box.get() or "")

        cursore = mydb.cursor()
        cursore.execute("SELECT ID_Qualifica FROM QUALIFICHE WHERE Qualifica = ?", (qualifica,))
        id_qualifica = cursore.fetchone()
        id_qualifica = id_qualifica[0] if id_qualifica else None
        
        numero_ordine_registrazione = clean_input(numero_ordine_registrazione_box.get() or "")

        if not (cognome and nome and sesso and luogo_nascita and provincia_nascita and data_nascita and codice_fiscale and indirizzo_residenza and comune_residenza and cap and provincia_residenza and data_associazione and qualifica):
            messagebox.showerror("Errore", "Tutti i campi obbligatori devono essere compilati.", parent=frame_contenuto_anagrafiche)
            return
        if len(cognome) > 30:
            messagebox.showerror("Errore", "Cognome troppo lungo. Massimo 30 caratteri.", parent=frame_contenuto_anagrafiche)
            return
        if len(nome) > 30:
            messagebox.showerror("Errore", "Nome troppo lungo. Massimo 30 caratteri.", parent=frame_contenuto_anagrafiche)
            return
        if len(luogo_nascita) > 40:
            messagebox.showerror("Errore", "Luogo di Nascita troppo lungo. Massimo 40 caratteri.", parent=frame_contenuto_anagrafiche)
            return
        if not is_valid_date(data_nascita):
            messagebox.showerror("Errore", "Data di Nascita inserita non valida. Formato corretto: gg/mm/aaaa", parent=frame_contenuto_anagrafiche)
            return
        if not is_valid_codice_fiscale(codice_fiscale):
            messagebox.showerror("Errore", "Formato Codice Fiscale non corretto. Il Codice Fiscale deve essere lungo 16 caratteri.", parent=frame_contenuto_anagrafiche)
            return
        if len(indirizzo_residenza) > 100:
            messagebox.showerror("Errore", "Indirizzo di Residenza troppo lungo. Massimo 100 caratteri.", parent=frame_contenuto_anagrafiche)
            return
        if len(comune_residenza) > 40:
            messagebox.showerror("Errore", "Comune di Residenza troppo lungo. Massimo 40 caratteri.", parent=frame_contenuto_anagrafiche)
            return
        if len(cap) != 5:
            messagebox.showerror("Errore", "Il CAP deve essere lungo 5 caratteri.", parent=frame_contenuto_anagrafiche)
            return
        if mobile and len(mobile) != 10:
            messagebox.showerror("Errore", "Il Cellulare deve essere lungo 10 caratteri.", parent=frame_contenuto_anagrafiche)
            return
        if fisso and len(fisso) != 10:
            messagebox.showerror("Errore", "Il Fisso deve essere lungo 10 caratteri.", parent=frame_contenuto_anagrafiche)
            return
        if email and not is_valid_email(email):
            messagebox.showerror("Errore", "Formato Email non corretto.", parent=frame_contenuto_anagrafiche)
            return
        if ambito_professionale and len(ambito_professionale) > 200:
            messagebox.showerror("Errore", "Ambito Professionale troppo lungo. Massimo 200 caratteri.", parent=frame_contenuto_anagrafiche)
            return
        if ruolo and len(ruolo) > 200:
            messagebox.showerror("Errore", "Ruolo troppo lungo. Massimo 200 caratteri.", parent=frame_contenuto_anagrafiche)
            return
        if numero_tessera_nazionale and len(numero_tessera_nazionale) > 10:
            messagebox.showerror("Errore", "Numero Tessera Nazionale troppo lungo. Massimo 10 caratteri.", parent=frame_contenuto_anagrafiche)
            return
        if numero_tessera_locale and len(numero_tessera_locale) > 10:
            messagebox.showerror("Errore", "Numero Tessera Locale troppo lungo. Massimo 10 caratteri.", parent=frame_contenuto_anagrafiche)
            return
        if not is_valid_date(data_associazione):
            messagebox.showerror("Errore", "Data di Associazione inserita non valida. Formato corretto: gg/mm/aaaa", parent=frame_contenuto_anagrafiche)
            return
        if numero_ordine_registrazione and not is_valid_int(numero_ordine_registrazione):
            messagebox.showerror("Errore", "Numero Ordine di Registrazione deve essere un numero intero.", parent=frame_contenuto_anagrafiche)
            return
        if id_qualifica is None:
            messagebox.showerror("Errore", "Qualifica non trovata nel database. Verifica la qualifica inserita.", parent=frame_contenuto_anagrafiche)
            return
        
        try:
            sql = """
                INSERT INTO Anagrafiche (
                    Cognome, Nome, Nominativo, Sesso, Luogo_Nascita, Provincia_Nascita, Data_Nascita, Codice_Fiscale, 
                    Indirizzo_Residenza, Comune_Residenza, Cap, Provincia_Residenza, Mobile, Fisso, Email, 
                    Ambito_Professionale, Ruolo, Numero_Tessera_Nazionale, Numero_Tessera_Locale, Data_Associazione,
                    ID_Qualifica, Numero_Ordine_Registrazione
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
            values = (cognome, nome, nominativo, sesso, luogo_nascita, provincia_nascita, data_nascita, codice_fiscale,
                    indirizzo_residenza, comune_residenza, cap, provincia_residenza, mobile, fisso, email,
                    ambito_professionale, ruolo, numero_tessera_nazionale, numero_tessera_locale, data_associazione,
                    id_qualifica, numero_ordine_registrazione)
            cursor = mydb.cursor()
            cursor.execute(sql, values)
            mydb.commit()
            messagebox.showinfo("Successo", "Anagrafica aggiunta con successo.", parent=frame_contenuto_anagrafiche)
            pulisci_campi_anagrafiche()
            chiudi_gestione_anagrafiche()
        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante l'inserimento nel database: {str(e)}", parent=frame_contenuto_anagrafiche)
    
    cognome_label = Label(frame_contenuto_anagrafiche, text="Cognome", font=("Open Sans", 10), bg="#ffffff", fg="#118e21").grid(row=1, column=0, sticky=W, padx="10")
    nome_label = Label(frame_contenuto_anagrafiche, text="Nome", font=("Open Sans", 10),bg="#ffffff", fg="#118e21").grid(row=1, column=2, sticky=W, padx="30")
    sesso_label = Label(frame_contenuto_anagrafiche, text="Sesso", font=("Open Sans", 10), bg="#ffffff", fg="#118e21").grid(row=3, column=0, sticky=W, padx="10")
    luogo_nascita_label = Label(frame_contenuto_anagrafiche, text="Luogo di Nascita", font=("Open Sans", 10), bg="#ffffff", fg="#118e21").grid(row=2, column=0, sticky=W, padx="10")
    provincia_nascita_label = Label(frame_contenuto_anagrafiche, text="Provincia di Nascita", font=("Open Sans", 10), bg="#ffffff", fg="#118e21").grid(row=2, column=2, sticky=W, padx="30")
    data_nascita_label = Label(frame_contenuto_anagrafiche, text="Data di Nascita", font=("Open Sans", 10), bg="#ffffff", fg="#118e21").grid(row=2, column=4, sticky=W, padx="30")
    codice_fiscale_label = Label(frame_contenuto_anagrafiche, text="Codice Fiscale", font=("Open Sans", 10), bg="#ffffff", fg="#118e21").grid(row=3, column=2, sticky=W, padx="30")
    indirizzo_residenza_label = Label(frame_contenuto_anagrafiche, text="Indirizzo di Residenza", font=("Open Sans", 10), bg="#ffffff", fg="#118e21").grid(row=4, column=0, sticky=W, padx="10")
    comune_residenza_label = Label(frame_contenuto_anagrafiche, text="Comune di Residenza", font=("Open Sans", 10), bg="#ffffff", fg="#118e21").grid(row=5, column=0, sticky=W, padx="10")
    cap_label = Label(frame_contenuto_anagrafiche, text="CAP", font=("Open Sans", 10), bg="#ffffff", fg="#118e21").grid(row=4, column=2, sticky=W, padx="30")
    provincia_residenza_label = Label(frame_contenuto_anagrafiche, text="Provincia di Residenza", font=("Open Sans", 10), bg="#ffffff", fg="#118e21").grid(row=5, column=2, sticky=W, padx="30")
    mobile_label = Label(frame_contenuto_anagrafiche, text="Cellulare", font=("Open Sans", 10), bg="#ffffff", fg="#118e21").grid(row=6, column=0, sticky=W, padx="10")
    fisso_label = Label(frame_contenuto_anagrafiche, text="Fisso", font=("Open Sans", 10), bg="#ffffff", fg="#118e21").grid(row=6, column=2, sticky=W, padx="30")
    email_label = Label(frame_contenuto_anagrafiche, text="Email", font=("Open Sans", 10), bg="#ffffff", fg="#118e21").grid(row=6, column=4, sticky=W, padx="30")
    ambito_professionale_label = Label(frame_contenuto_anagrafiche, text="Ambito Professionale", font=("Open Sans", 10), bg="#ffffff", fg="#118e21").grid(row=7, column=0, sticky=W, padx="10")
    ruolo_label = Label(frame_contenuto_anagrafiche, text="Ruolo", font=("Open Sans", 10), bg="#ffffff", fg="#118e21").grid(row=7, column=2, sticky=W, padx="30")
    numero_tessera_nazionale_label = Label(frame_contenuto_anagrafiche, text="Numero Tessera Nazionale", font=("Open Sans", 10), bg="#ffffff", fg="#118e21").grid(row=8, column=0, sticky=W, padx="10")
    numero_tessera_locale_label = Label(frame_contenuto_anagrafiche, text="Numero Tessera Locale", font=("Open Sans", 10), bg="#ffffff", fg="#118e21").grid(row=8, column=2, sticky=W, padx="30")
    data_associazione_label = Label(frame_contenuto_anagrafiche, text="Data Associazione", font=("Open Sans", 10), bg="#ffffff", fg="#118e21").grid(row=8, column=4, sticky=W, padx="30")
    qualifica_label = Label(frame_contenuto_anagrafiche, text="Qualifica", font=("Open Sans", 10), bg="#ffffff", fg="#118e21").grid(row=9, column=0, sticky=W, padx="10")
    numero_ordine_registrazione_label = Label(frame_contenuto_anagrafiche, text="Numero Ordine Registrazione", font=("Open Sans", 10), bg="#ffffff", fg="#118e21").grid(row=9, column=2, sticky=W, padx="30")

    province_italiane = [
    "AG", "AL", "AN", "AO", "AR", "AP", "AT", "AV", "BA", "BT", "BL", "BN", "BG", "BI", "BO", "BZ", "BS", "BR", "CA", 
    "CL", "CB", "CI", "CE", "CT", "CZ", "CH", "CO", "CS", "CR", "KR", "CN", "EN", "FM", "FE", "FI", "FG", "FC", "FR", 
    "GE", "GO", "GR", "IM", "IS", "SP", "AQ", "LT", "LE", "LC", "LI", "LO", "LU", "MC", "MN", "MS", "MT", "VS", "ME", 
    "MI", "MO", "MB", "NA", "NO", "NU", "OR", "PD", "PA", "PR", "PV", "PG", "PU", "PE", "PC", "PI", "PT", "PN", "PZ", 
    "PO", "RG", "RA", "RC", "RE", "RI", "RN", "RM", "RO", "SA", "SS", "SV", "SI", "SR", "SO", "TA", "TE", "TR", "TO", 
    "TP", "TN", "TV", "TS", "UD", "VA", "VE", "VB", "VC", "VR", "VV", "VI", "VT", "ES"]

    cursor_qualifiche = mydb.cursor()
    cursor_qualifiche.execute("SELECT DISTINCT Qualifica FROM Qualifiche")
    qualifiche = [row[0] for row in cursor_qualifiche.fetchall()]

    cognome_box = Entry(frame_contenuto_anagrafiche, width=30)
    cognome_box.grid(row=1, column=1, pady=5, sticky="w")
    nome_box = Entry(frame_contenuto_anagrafiche, width=30)
    nome_box.grid(row=1, column=3, pady=5, sticky="w")
    sesso_box = ttk.Combobox(frame_contenuto_anagrafiche, values=["M", "F"], width=5)
    sesso_box.grid(row=3, column=1, pady=5, sticky="w")
    sesso_box.current(0)
    luogo_nascita_box = Entry(frame_contenuto_anagrafiche, width=30)
    luogo_nascita_box.grid(row=2, column=1, pady=5, sticky="w")
    provincia_nascita_box = ttk.Combobox(frame_contenuto_anagrafiche, values=province_italiane, width=5)
    provincia_nascita_box.grid(row=2, column=3, pady=5, sticky="w")
    data_nascita_box = Entry(frame_contenuto_anagrafiche, width=15)
    data_nascita_box.grid(row=2, column=5, pady=5, sticky="w")
    codice_fiscale_box = Entry(frame_contenuto_anagrafiche, width=30)
    codice_fiscale_box.grid(row=3, column=3, pady=5, sticky="w")
    indirizzo_residenza_box = Entry(frame_contenuto_anagrafiche, width=40)
    indirizzo_residenza_box.grid(row=4, column=1, pady=5, sticky="w")
    comune_residenza_box = Entry(frame_contenuto_anagrafiche, width=30)
    comune_residenza_box.grid(row=5, column=1, pady=5, sticky="w")
    cap_box = Entry(frame_contenuto_anagrafiche, width=8)
    cap_box.grid(row=4, column=3, pady=5, sticky="w")
    provincia_residenza_box = ttk.Combobox(frame_contenuto_anagrafiche, values=province_italiane, width=5)
    provincia_residenza_box.grid(row=5, column=3, pady=5, sticky="w")
    mobile_box = Entry(frame_contenuto_anagrafiche)
    mobile_box.grid(row=6, column=1, pady=5, sticky="w")
    fisso_box = Entry(frame_contenuto_anagrafiche)
    fisso_box.grid(row=6, column=3, pady=5, sticky="w")
    email_box = Entry(frame_contenuto_anagrafiche, width=30)
    email_box.grid(row=6, column=5, pady=5, sticky="w")
    ambito_professionale_box = Entry(frame_contenuto_anagrafiche, width=30)
    ambito_professionale_box.grid(row=7, column=1, pady=5, sticky="w")
    ruolo_box = Entry(frame_contenuto_anagrafiche, width=30)
    ruolo_box.grid(row=7, column=3, pady=5, sticky="w")
    numero_tessera_nazionale_box = Entry(frame_contenuto_anagrafiche, width=30)
    numero_tessera_nazionale_box.grid(row=8, column=1, pady=5, sticky="w")
    numero_tessera_locale_box = Entry(frame_contenuto_anagrafiche, width=30)
    numero_tessera_locale_box.grid(row=8, column=3, pady=5, sticky="w")
    data_associazione_box = Entry(frame_contenuto_anagrafiche, width=30)
    data_associazione_box.grid(row=8, column=5, pady=5, sticky="w")
    qualifica_box = ttk.Combobox(frame_contenuto_anagrafiche, values=qualifiche, width=30) 
    qualifica_box.grid(row=9, column=1, pady=5, sticky="w")
    numero_ordine_registrazione_box = Entry(frame_contenuto_anagrafiche, width=30)
    numero_ordine_registrazione_box.grid(row=9, column=3, pady=5, sticky="w")

    bottone_aggiungi_anagrafica = Button(frame_contenuto_anagrafiche, text="Aggiungi Anagrafica", command=aggiungi_anagrafiche)
    bottone_aggiungi_anagrafica.grid(row=11, column=0, padx=10, pady=10)
    pulisci_campi_anagrafica = Button(frame_contenuto_anagrafiche, text="Pulisci i campi", command=pulisci_campi_anagrafiche)
    pulisci_campi_anagrafica.grid(row=11, column=2)

def cerca_ora_anagrafica():
    global id_anagrafica
    for widget in frame_risultati_anagrafiche.grid_slaves():
        widget.grid_forget()
    
    def clean_input(value):
        return value.strip() if value else ""
    
    selezionato = ricerca_per.get()
    sql = ""

    if selezionato == "Ricerca per ...":
        test = Label(frame_risultati_anagrafiche, text="Seleziona un campo valido", font=("Open Sans", 10), bg="#ffffff", fg="#118e21")
        test.grid(row=0, column=0, padx=10, pady=10)
        return
    
    if selezionato == "Cognome":
        sql = "SELECT ID_Anagrafica, Cognome, Nome, Nominativo, Sesso, Luogo_Nascita, Provincia_Nascita, Data_Nascita, Codice_Fiscale, Indirizzo_Residenza, Comune_Residenza, \
            CAP, Provincia_Residenza, Mobile, Fisso, Email, Ambito_Professionale, Ruolo , Numero_Tessera_Nazionale, Numero_Tessera_Locale, Data_Associazione, ID_Qualifica, \
            Numero_Ordine_Registrazione FROM Anagrafiche WHERE Cognome = ?"
    elif selezionato == "Email":
        sql = "SELECT ID_Anagrafica, Cognome, Nome, Nominativo, Sesso, Luogo_Nascita, Provincia_Nascita, Data_Nascita, Codice_Fiscale, Indirizzo_Residenza, Comune_Residenza, \
            CAP, Provincia_Residenza, Mobile, Fisso, Email, Ambito_Professionale, Ruolo , Numero_Tessera_Nazionale, Numero_Tessera_Locale, Data_Associazione, ID_Qualifica, \
            Numero_Ordine_Registrazione FROM Anagrafiche WHERE Email = ?"
    elif selezionato == "Numero Tessera Nazionale":
        sql = "SELECT ID_Anagrafica, Cognome, Nome, Nominativo, Sesso, Luogo_Nascita, Provincia_Nascita, Data_Nascita, Codice_Fiscale, Indirizzo_Residenza, Comune_Residenza, \
            CAP, Provincia_Residenza, Mobile, Fisso, Email, Ambito_Professionale, Ruolo , Numero_Tessera_Nazionale, Numero_Tessera_Locale, Data_Associazione, ID_Qualifica, \
            Numero_Ordine_Registrazione FROM Anagrafiche WHERE Numero_Tessera_Nazionale = ?"
    elif selezionato == "Numero Tessera Locale":
        sql = "SELECT ID_Anagrafica, Cognome, Nome, Nominativo, Sesso, Luogo_Nascita, Provincia_Nascita, Data_Nascita, Codice_Fiscale, Indirizzo_Residenza, Comune_Residenza, \
            CAP, Provincia_Residenza, Mobile, Fisso, Email, Ambito_Professionale, Ruolo , Numero_Tessera_Nazionale, Numero_Tessera_Locale, Data_Associazione, ID_Qualifica, \
            Numero_Ordine_Registrazione FROM Anagrafiche WHERE Numero_Tessera_Locale = ?"

    ricerca = ricerca_box.get()
    parametri = (ricerca, )
    cerca_anagrafica_cursor = mydb.cursor()
    cerca_anagrafica_cursor.execute(sql, parametri)
    result = cerca_anagrafica_cursor.fetchall()

    colonne = ("Cognome", "Nome", "Codice Fiscale", "Indirizzo Residenza", "Comune Residenza", "CAP")
    tabella = ttk.Treeview(frame_risultati_anagrafiche, columns=colonne, show='headings')
    tabella.heading('Cognome', text='Cognome')
    tabella.heading('Nome', text='Nome')
    tabella.heading('Codice Fiscale', text='Codice Fiscale')
    tabella.heading('Indirizzo Residenza', text='Indirizzo Residenza')
    tabella.heading('Comune Residenza', text='Comune Residenza')
    tabella.heading('CAP', text='CAP')

    id_map = {}

    for row in result:
        id_anagrafica = row[0]
        cognome = row[1]
        nome = row[2]
        codice_fiscale = row[8]
        indirizzo_residenza = row[9]
        comune_residenza = row[10]
        cap = row[11]
        valori = (cognome, nome, codice_fiscale, indirizzo_residenza, comune_residenza, cap)
        item = tabella.insert('', END, values=valori, iid=id_anagrafica)
        id_map[item] = id_anagrafica

    tabella.grid(row=0, column=0, sticky='nsew')

    def on_item_selected(event):
        selected_item = tabella.focus()
        id_anagrafica = id_map.get(selected_item)
    
    tabella.bind('<<TreeviewSelect>>', on_item_selected)

    def pulisci_campi():
        id_box2.config(state=NORMAL)
        id_box2.delete(0, END)
        id_box2.config(state=DISABLED)
        cognome_box2.delete(0, END)
        nome_box2.delete(0, END)
        sesso_box2.delete(0, END)
        luogo_nascita_box2.delete(0, END)
        provincia_nascita_box2.delete(0, END)
        data_nascita_box2.delete(0, END)
        cf_box2.delete(0, END)
        indirizzo_box2.delete(0, END)
        comune_box2.delete(0, END)
        cap_box2.delete(0, END)
        provincia_residenza_box2.delete(0, END)
        mobile_box2.delete(0, END)
        fisso_box2.delete(0, END)
        mail_box2.delete(0, END)
        ambito_box2.delete(0, END)
        ruolo_box2.delete(0, END)
        numero_tessera_nazionale_box2.delete(0, END)
        numero_tessera_locale_box2.delete(0, END)
        data_associazione_box2.delete(0, END)
        qualifica_box2.delete(0, END)
        numero_ordine_registrazione_box2.delete(0, END)

    def is_valid_email(email):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_regex, email) is not None
    def is_valid_date(date):
        return re.match(r'^\d{2}/\d{2}/\d{4}$', date) is not None
    def is_valid_codice_fiscale(codice_fiscale):
        return re.match(r'^[A-Z0-9]{16}$', codice_fiscale) is not None
    def is_valid_int(value):
        try:
            int(value)
            return True
        except ValueError:
            return False
    
    def update():
        for widget in frame_risultati_anagrafiche.grid_slaves():
            widget.grid_forget() 

        try:
            id = id_box2.get()
            cognome = clean_input(cognome_box2.get() or "")
            nome = clean_input(nome_box2.get() or "")
            nominativo = f"{cognome} {nome}"
            sesso = clean_input(sesso_box2.get() or "")
            luogo_nascita = clean_input(luogo_nascita_box2.get() or "")
            provincia_nascita = clean_input(provincia_nascita_box2.get() or "")
            data_nascita = clean_input(data_nascita_box2.get() or "")
            data_nascita_db_format = result_mod[0][7] if result_mod[0][7] is not None else ""
            data_nascita = clean_input(data_nascita_db_format.strftime('%d/%m/%Y') if data_nascita_db_format else "")
            cf = clean_input(cf_box2.get() or "")
            indirizzo = clean_input(indirizzo_box2.get() or "") 
            comune = clean_input(comune_box2.get() or "") 
            cap = clean_input(cap_box2.get() or "")
            provincia_residenza = clean_input(provincia_residenza_box2.get() or "")
            mobile = clean_input(mobile_box2.get() or "")
            fisso = clean_input(fisso_box2.get() or "")
            mail = clean_input(mail_box2.get() or "")
            ambito = clean_input(ambito_box2.get() or "")
            ruolo = clean_input(ruolo_box2.get() or "")
            numero_tessera_nazionale = clean_input(numero_tessera_nazionale_box2.get() or "")
            numero_tessera_locale = clean_input(numero_tessera_locale_box2.get() or "")
            data_associazione = clean_input(data_associazione_box2.get() or "")
            data_associazione_db_format = result_mod[0][20] if result_mod[0][20] is not None else ""
            data_associazione = clean_input(data_associazione_db_format.strftime('%d/%m/%Y') if data_associazione_db_format else "")
            qualifica = clean_input(qualifica_box2.get() or "")

            cursore2 = mydb.cursor()
            cursore2.execute("SELECT ID_Qualifica FROM QUALIFICHE WHERE Qualifica = ?", (qualifica,))
            id_qualifica = cursore2.fetchone()
            id_qualifica = id_qualifica[0] if id_qualifica else None
            
            numero_ordine_registrazione = clean_input(numero_ordine_registrazione_box2.get() or "")

            if not (cognome and nome and sesso and luogo_nascita and provincia_nascita and data_nascita and codice_fiscale and indirizzo_residenza and comune_residenza and cap and provincia_residenza and data_associazione and qualifica):
                messagebox.showerror("Errore", "Tutti i campi obbligatori devono essere compilati.", parent=frame_contenuto_anagrafiche)
                return
            if len(cognome) > 30:
                messagebox.showerror("Errore", "Cognome troppo lungo. Massimo 30 caratteri.", parent=frame_contenuto_anagrafiche)
                return
            if len(nome) > 30:
                messagebox.showerror("Errore", "Nome troppo lungo. Massimo 30 caratteri.", parent=frame_contenuto_anagrafiche)
                return
            if len(luogo_nascita) > 40:
                messagebox.showerror("Errore", "Luogo di Nascita troppo lungo. Massimo 40 caratteri.", parent=frame_contenuto_anagrafiche)
                return
            if not is_valid_date(data_nascita):
                messagebox.showerror("Errore", "Data di Nascita inserita non valida. Formato corretto: gg/mm/aaaa", parent=frame_contenuto_anagrafiche)
                return
            if not is_valid_codice_fiscale(codice_fiscale):
                messagebox.showerror("Errore", "Formato Codice Fiscale non corretto. Il Codice Fiscale deve essere lungo 16 caratteri.", parent=frame_contenuto_anagrafiche)
                return
            if len(indirizzo_residenza) > 100:
                messagebox.showerror("Errore", "Indirizzo di Residenza troppo lungo. Massimo 100 caratteri.", parent=frame_contenuto_anagrafiche)
                return
            if len(comune_residenza) > 40:
                messagebox.showerror("Errore", "Comune di Residenza troppo lungo. Massimo 40 caratteri.", parent=frame_contenuto_anagrafiche)
                return
            if len(cap) != 5:
                messagebox.showerror("Errore", "Il CAP deve essere lungo 5 caratteri.", parent=frame_contenuto_anagrafiche)
                return
            if mobile and len(mobile) != 10:
                messagebox.showerror("Errore", "Il Cellulare deve essere lungo 10 caratteri.", parent=frame_contenuto_anagrafiche)
                return
            if fisso and len(fisso) != 10:
                messagebox.showerror("Errore", "Il Fisso deve essere lungo 10 caratteri.", parent=frame_contenuto_anagrafiche)
                return
            if mail and not is_valid_email(mail):
                messagebox.showerror("Errore", "Formato Email non corretto.", parent=frame_contenuto_anagrafiche)
                return
            if ambito and len(ambito) > 200:
                messagebox.showerror("Errore", "Ambito Professionale troppo lungo. Massimo 200 caratteri.", parent=frame_contenuto_anagrafiche)
                return
            if ruolo and len(ruolo) > 200:
                messagebox.showerror("Errore", "Ruolo troppo lungo. Massimo 200 caratteri.", parent=frame_contenuto_anagrafiche)
                return
            if numero_tessera_nazionale and len(numero_tessera_nazionale) > 10:
                messagebox.showerror("Errore", "Numero Tessera Nazionale troppo lungo. Massimo 10 caratteri.", parent=frame_contenuto_anagrafiche)
                return
            if numero_tessera_locale and len(numero_tessera_locale) > 10:
                messagebox.showerror("Errore", "Numero Tessera Locale troppo lungo. Massimo 10 caratteri.", parent=frame_contenuto_anagrafiche)
                return
            if not is_valid_date(data_associazione):
                messagebox.showerror("Errore", "Data di Associazione inserita non valida. Formato corretto: gg/mm/aaaa", parent=frame_contenuto_anagrafiche)
                return
            if numero_ordine_registrazione and not is_valid_int(numero_ordine_registrazione):
                messagebox.showerror("Errore", "Numero Ordine di Registrazione deve essere un numero intero.", parent=frame_contenuto_anagrafiche)
                return
            if id_qualifica is None:
                messagebox.showerror("Errore", "Qualifica non trovata nel database. Verifica la qualifica inserita.", parent=frame_contenuto_anagrafiche)
                return
            sql_upd_anagrafiche = "UPDATE Anagrafiche SET Cognome = ?, Nome = ?, Nominativo = ?, Sesso = ?, Luogo_Nascita = ?, Provincia_Nascita = ?, Data_Nascita = ?, \
                Codice_Fiscale = ?, Indirizzo_Residenza = ?, Comune_Residenza = ?, CAP = ?, Provincia_Residenza = ?, Mobile = ?, Fisso = ?, Email = ?, \
                Ambito_Professionale = ?, Ruolo = ?, Numero_Tessera_Nazionale = ?, Numero_Tessera_Locale = ?, Data_Associazione = ?, ID_Qualifica = ?, \
                Numero_Ordine_Registrazione = ? WHERE ID_Anagrafica = ?"
            values2 = (cognome, nome, nominativo, sesso, luogo_nascita, provincia_nascita, data_nascita, codice_fiscale, indirizzo, comune, cap, provincia_residenza, mobile,
                      fisso, mail, ambito, ruolo, numero_tessera_nazionale, numero_tessera_locale, data_associazione, id_qualifica, numero_ordine_registrazione ,id)
            cursor = mydb.cursor()
            cursor.execute(sql_upd_anagrafiche, values2)
            mydb.commit()
            messagebox.showinfo("Successo", "Anagrafica aggiornata con successo.", parent=frame_risultati_anagrafiche)
            pulisci_campi()
            chiudi_gestione_anagrafiche()
        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante l'inserimento nel database: {str(e)}", parent=frame_risultati_anagrafiche)

    def modifica_anagrafica_ora():
        global result_mod, id_qualifica_map

        selected_item = tabella.focus()
        id_anagrafica = id_map.get(selected_item)
        if id_anagrafica:
            for widget in frame_risultati_anagrafiche.grid_slaves():
                widget.grid_forget()
        sql_mod = "SELECT * FROM Anagrafiche WHERE ID_Anagrafica = ?"
        name = (id_anagrafica,)
        cursor = mydb.cursor()
        result_mod = cursor.execute(sql_mod, name)
        result_mod = result_mod.fetchall()

        sql_qualifica = "SELECT Qualifica FROM Qualifiche WHERE ID_Qualifica = ?"
        cursor.execute(sql_qualifica, (result_mod[0][21],))
        qualifica_result = cursor.fetchone()
        qualifica_attuale = qualifica_result[0] if qualifica_result else ""

        id_qualifica_map = {}
        qualifiche_cursor = mydb.cursor()
        qualifiche_cursor.execute("SELECT ID_Qualifica, Qualifica FROM Qualifiche")
        qualifiche_results = qualifiche_cursor.fetchall()
        for qualifica in qualifiche_results:
            id_qualifica_map[qualifica[0]] = qualifica[1]

        index = 0

        cognome_label = Label(frame_risultati_anagrafiche, text="Cognome",  font=("Open Sans", 10), bg="#ffffff", fg="#118e21").grid(row=index+2, column=0, sticky=W, padx="10", pady="10")
        nome_label = Label(frame_risultati_anagrafiche, text="Nome", font=("Open Sans", 10), bg="#ffffff", fg="#118e21").grid(row=index+2, column=2, sticky=W, padx="10")
        sesso_label = Label(frame_risultati_anagrafiche, text="Sesso",  font=("Open Sans", 10), bg="#ffffff", fg="#118e21").grid(row=index+4, column=0, sticky=W, padx="10")
        luogo_nascita_label = Label(frame_risultati_anagrafiche, text="Luogo di Nascita",  font=("Open Sans", 10), bg="#ffffff", fg="#118e21").grid(row=index+3, column=0, sticky=W, padx="10")
        provincia_nascita_label = Label(frame_risultati_anagrafiche, text="Provincia di Nascita", font=("Open Sans", 10), bg="#ffffff", fg="#118e21").grid(row=index+3, column=2, sticky=W, padx="10")
        ata_nascita_label = Label(frame_risultati_anagrafiche, text="Data di Nascita",  font=("Open Sans", 10), bg="#ffffff", fg="#118e21").grid(row=index+3, column=4, sticky=W, padx="10")
        cf_label = Label(frame_risultati_anagrafiche, text="Codice Fiscale",  font=("Open Sans", 10), bg="#ffffff", fg="#118e21").grid(row=index+4, column=2, sticky=W, padx="10")
        indirizzo_label = Label(frame_risultati_anagrafiche, text="Indirizzo di Residenza",  font=("Open Sans", 10), bg="#ffffff", fg="#118e21").grid(row=index+5, column=0, sticky=W, padx="10")
        comune_label = Label(frame_risultati_anagrafiche, text="Comune di Residenza",  font=("Open Sans", 10), bg="#ffffff", fg="#118e21").grid(row=index+6, column=0, sticky=W, padx="10")
        cap_label = Label(frame_risultati_anagrafiche, text="CAP",  font=("Open Sans", 10), bg="#ffffff", fg="#118e21").grid(row=index+5, column=2, sticky=W, padx="10")
        provincia_residenza_label = Label(frame_risultati_anagrafiche, text="Provincia di Residenza",  font=("Open Sans", 10), bg="#ffffff", fg="#118e21").grid(row=index+6, column=2, sticky=W, padx="10")
        mobile_label = Label(frame_risultati_anagrafiche, text="Cellulare",  font=("Open Sans", 10), bg="#ffffff", fg="#118e21").grid(row=index+7, column=0, sticky=W, padx="10")
        fisso_label = Label(frame_risultati_anagrafiche, text="Fisso",  font=("Open Sans", 10), bg="#ffffff", fg="#118e21").grid(row=index+7, column=2, sticky=W, padx="10")
        mail_label = Label(frame_risultati_anagrafiche, text="Email",  font=("Open Sans", 10), bg="#ffffff", fg="#118e21").grid(row=index+7, column=4, sticky=W, padx="10")
        ambito_label = Label(frame_risultati_anagrafiche, text="Ambito Professionale",  font=("Open Sans", 10), bg="#ffffff", fg="#118e21").grid(row=index+8, column=0, sticky=W, padx="10")
        ruolo_label = Label(frame_risultati_anagrafiche, text="Ruolo",  font=("Open Sans", 10), bg="#ffffff", fg="#118e21").grid(row=index+8, column=2, sticky=W, padx="10")
        numero_tessera_nazionale_label = Label(frame_risultati_anagrafiche, text="Numero Tessera Nazionale",  font=("Open Sans", 10), bg="#ffffff", fg="#118e21").grid(row=index+9, column=0, sticky=W, padx="10")
        numero_tessera_locale_label = Label(frame_risultati_anagrafiche, text="Numero Tessera Locale",  font=("Open Sans", 10), bg="#ffffff", fg="#118e21").grid(row=index+9, column=2, sticky=W, padx="10")
        data_associazione_label = Label(frame_risultati_anagrafiche, text="Data Associazione",  font=("Open Sans", 10), bg="#ffffff", fg="#118e21").grid(row=index+9, column=4, sticky=W, padx="10")
        qualifica_label = Label(frame_risultati_anagrafiche, text="Qualifica",  font=("Open Sans", 10), bg="#ffffff", fg="#118e21").grid(row=index+10, column=0, sticky=W, padx="10")
        numero_ordine_registrazione_label = Label(frame_risultati_anagrafiche, text="Numero Ordine di Registrazione",  font=("Open Sans", 10), bg="#ffffff", fg="#118e21").grid(row=index+10, column=2, sticky=W, padx="10")
        id_label = Label(frame_risultati_anagrafiche, text="ID",  font=("Open Sans", 10), bg="#ffffff", fg="#118e21").grid(row=index+1, column=0, sticky=W, padx="10")

        province_italiane = [
        "AG", "AL", "AN", "AO", "AR", "AP", "AT", "AV", "BA", "BT", "BL", "BN", "BG", "BI", "BO", "BZ", "BS", "BR", "CA", 
        "CL", "CB", "CI", "CE", "CT", "CZ", "CH", "CO", "CS", "CR", "KR", "CN", "EN", "FM", "FE", "FI", "FG", "FC", "FR", 
        "GE", "GO", "GR", "IM", "IS", "SP", "AQ", "LT", "LE", "LC", "LI", "LO", "LU", "MC", "MN", "MS", "MT", "VS", "ME", 
        "MI", "MO", "MB", "NA", "NO", "NU", "OR", "PD", "PA", "PR", "PV", "PG", "PU", "PE", "PC", "PI", "PT", "PN", "PZ", 
        "PO", "RG", "RA", "RC", "RE", "RI", "RN", "RM", "RO", "SA", "SS", "SV", "SI", "SR", "SO", "TA", "TE", "TR", "TO", 
        "TP", "TN", "TV", "TS", "UD", "VA", "VE", "VB", "VC", "VR", "VV", "VI", "VT", "ES"]

        global cognome_box2
        cognome_box2 = Entry(frame_risultati_anagrafiche, width=30)
        cognome_box2.grid(row=index+2, column=1, pady=5, sticky=W)
        cognome_box2.insert(0, result_mod[0][1] if result_mod[0][1] is not None else "")

        global nome_box2
        nome_box2 = Entry(frame_risultati_anagrafiche, width=30)
        nome_box2.grid(row=index+2, column=3, pady=5, sticky=W)
        nome_box2.insert(0, result_mod[0][2] if result_mod[0][2] is not None else "")

        global sesso_box2
        sesso_box2 = ttk.Combobox(frame_risultati_anagrafiche, values=["M", "F"], width=5)
        sesso_box2.grid(row=index+4, column=1, pady=5, sticky=W)
        sesso_box2.insert(0, result_mod[0][4] if result_mod[0][4] is not None else "")

        global luogo_nascita_box2
        luogo_nascita_box2 = Entry(frame_risultati_anagrafiche, width=30)
        luogo_nascita_box2.grid(row=index+3, column=1, pady=5, sticky=W)
        luogo_nascita_box2.insert(0, result_mod[0][5] if result_mod[0][5] is not None else "")

        global provincia_nascita_box2
        provincia_nascita_box2 = ttk.Combobox(frame_risultati_anagrafiche, values=province_italiane, width=5)
        provincia_nascita_box2.grid(row=index+3, column=3, pady=5, sticky=W)
        provincia_nascita_box2.insert(0, result_mod[0][6] if result_mod[0][6] is not None else "")

        global data_nascita_box2
        data_nascita_box2 = Entry(frame_risultati_anagrafiche, width=15)
        data_nascita_box2.grid(row=index+3, column=5, pady=5, sticky=W)
        data_nascita_box2.insert(0, result_mod[0][7].strftime('%d/%m/%Y') if result_mod[0][7] is not None else "")

        global cf_box2
        cf_box2 = Entry(frame_risultati_anagrafiche, width=30)
        cf_box2.grid(row=index+4, column=3, pady=5, sticky=W)
        cf_box2.insert(0, result_mod[0][8] if result_mod[0][8] is not None else "")

        global indirizzo_box2
        indirizzo_box2 = Entry(frame_risultati_anagrafiche, width=40)
        indirizzo_box2.grid(row=index+5, column=1, pady=5, sticky=W)
        indirizzo_box2.insert(0, result_mod[0][9] if result_mod[0][9] is not None else "")

        global comune_box2
        comune_box2 = Entry(frame_risultati_anagrafiche, width=30)
        comune_box2.grid(row=index+6, column=1, pady=5, sticky=W)
        comune_box2.insert(0, result_mod[0][10] if result_mod[0][10] is not None else "")

        global cap_box2
        cap_box2 = Entry(frame_risultati_anagrafiche, width=8)
        cap_box2.grid(row=index+5, column=3, pady=5, sticky=W)
        cap_box2.insert(0, result_mod[0][11] if result_mod[0][11] is not None else "")

        global provincia_residenza_box2
        provincia_residenza_box2 = ttk.Combobox(frame_risultati_anagrafiche, values=province_italiane, width=5)
        provincia_residenza_box2.grid(row=index+6, column=3, pady=5, sticky=W)
        provincia_residenza_box2.insert(0, result_mod[0][12] if result_mod[0][12] is not None else "")

        global mobile_box2
        mobile_box2 = Entry(frame_risultati_anagrafiche)
        mobile_box2.grid(row=index+7, column=1, pady=5, sticky=W)
        mobile_box2.insert(0, result_mod[0][13] if result_mod[0][13] is not None else "")

        global fisso_box2
        fisso_box2 = Entry(frame_risultati_anagrafiche)
        fisso_box2.grid(row=index+7, column=3, pady=5, sticky=W)
        fisso_box2.insert(0, result_mod[0][14] if result_mod[0][14] is not None else "")

        global mail_box2
        mail_box2 = Entry(frame_risultati_anagrafiche, width=30)
        mail_box2.grid(row=index+7, column=5, pady=5, sticky=W)
        mail_box2.insert(0, result_mod[0][15] if result_mod[0][15] is not None else "")

        global ambito_box2
        ambito_box2 = Entry(frame_risultati_anagrafiche, width=30)
        ambito_box2.grid(row=index+8, column=1, pady=5, sticky=W)
        ambito_box2.insert(0, result_mod[0][16] if result_mod[0][16] is not None else "")

        global ruolo_box2
        ruolo_box2 = Entry(frame_risultati_anagrafiche, width=30)
        ruolo_box2.grid(row=index+8, column=3, pady=5, sticky=W)
        ruolo_box2.insert(0, result_mod[0][17] if result_mod[0][17] is not None else "")

        global numero_tessera_nazionale_box2
        numero_tessera_nazionale_box2 = Entry(frame_risultati_anagrafiche, width=30)
        numero_tessera_nazionale_box2.grid(row=index+9, column=1, pady=5, sticky=W)
        numero_tessera_nazionale_box2.insert(0, result_mod[0][18] if result_mod[0][18] is not None else "")

        global numero_tessera_locale_box2
        numero_tessera_locale_box2 = Entry(frame_risultati_anagrafiche, width=30)
        numero_tessera_locale_box2.grid(row=index+9, column=3, pady=5, sticky=W)
        numero_tessera_locale_box2.insert(0, result_mod[0][19] if result_mod[0][19] is not None else "")

        global data_associazione_box2
        data_associazione_box2 = Entry(frame_risultati_anagrafiche, width=30)
        data_associazione_box2.grid(row=index+9, column=5, pady=5, sticky=W)
        data_associazione_box2.insert(0, result_mod[0][20].strftime('%d/%m/%Y') if result_mod[0][20] is not None else "")

        global qualifica_box2
        qualifica_box2 = ttk.Combobox(frame_risultati_anagrafiche, values=list(id_qualifica_map.values()) ,width=30)
        qualifica_box2.grid(row=index+10, column=1, pady=5, sticky=W)
        qualifica_box2.set(qualifica_attuale)

        global numero_ordine_registrazione_box2
        numero_ordine_registrazione_box2 = Entry(frame_risultati_anagrafiche, width=30)
        numero_ordine_registrazione_box2.grid(row=index+10, column=3, pady=5, sticky=W)
        numero_ordine_registrazione_box2.insert(0, result_mod[0][22] if result_mod[0][22] is not None else "")

        global id_box2
        id_box2 = Entry(frame_risultati_anagrafiche, state='normal')
        id_box2.grid(row=index+1, column=1, pady=20, sticky=W)
        id_box2.insert(0, result_mod[0][0])
        id_box2.config(state='readonly')

        salva_record_anagrafiche = Button(frame_risultati_anagrafiche, text="Salva Record", command=update)
        salva_record_anagrafiche.grid(row=index+12, column=0, padx=10, pady=15)

    modifica_btn = Button(frame_risultati_anagrafiche, text="Modifica", command=modifica_anagrafica_ora)
    modifica_btn.grid(row=1, column=0)

def mostra_modifica_anagrafica():
    global ricerca_per
    global ricerca_box

    for widget in frame_contenuto_anagrafiche.winfo_children():
        widget.destroy()
    for widget in frame_risultati_anagrafiche.winfo_children():
        widget.destroy()

    label = Label(frame_contenuto_anagrafiche, text="Modifica Anagrafica", font=("Open Sans", 14), bg="#ffffff", fg="#118e21")
    label.grid(row=0, column=0, columnspan=2, padx=20, pady=20)
    label_cerca_anagrafica = Label(frame_contenuto_anagrafiche, text="Ricerca per ", font=("Open Sans", 10), bg="#ffffff", fg="#118e21")
    label_cerca_anagrafica.grid(row=1, column=0, padx=10, pady=5, sticky="w")

    ricerca_per = ttk.Combobox(frame_contenuto_anagrafiche, value=["Ricerca per ...","Cognome", "Email", "Numero Tessera Nazionale", "Numero Tessera Locale"])
    ricerca_per.current(0)
    ricerca_per.grid(row=1, column=1, padx=10)
    ricerca_box = Entry(frame_contenuto_anagrafiche, width=30)
    ricerca_box.grid(row=1, column=2, padx=20, pady=10)
    ricerca_bottone = Button(frame_contenuto_anagrafiche, text="Cerca", command=cerca_ora_anagrafica)
    ricerca_bottone.grid(row=1, column=3, padx=20)

def apri_gestione_corsi():
    global gestione_corsi
    global corsi_image_photo
    global frame_contenuto
    global frame_risultati
    global frame_iscrizioni

    gestione_corsi = Toplevel(root)
    gestione_corsi.title('Gestione Corsi')
    gestione_corsi.geometry("900x700")
    gestione_corsi.configure(bg="#ffffff")
    gestione_corsi.resizable(False, False)

    banner_corsi = Frame(gestione_corsi, background="white", height=100, width=900)
    banner_corsi.grid(row=0, column=0, columnspan=2, sticky="nsew")

    corsi_image_path = os.path.join(os.path.dirname(__file__), 'logo-unitre-arvalia.jpg')
    corsi_image = Image.open(corsi_image_path)
    corsi_image = corsi_image.resize((100, 100), Image.LANCZOS)  # Modifica la dimensione in base alle tue esigenze
    corsi_image_photo = ImageTk.PhotoImage(corsi_image)

    corsi_image_label = Label(banner_corsi, image=corsi_image_photo, bg="#ffffff")
    corsi_image_label.pack(side=LEFT, padx=10)

    title_corsi = Label(banner_corsi, text="Gestione Corsi", font=("Open Sans", 16), bg="#ffffff", fg="#118e21")
    title_corsi.pack(side=LEFT, padx=275)

    frame_bottoni = Frame(gestione_corsi, background="white", height=75, width=900)
    frame_bottoni.grid(row=1, column=0, columnspan=2, sticky="nsew")

    inserisci_corsi_button = Button(frame_bottoni, text="Inserisci Corso", font=("Open Sans", 10), bg="#ffffff", fg="#118e21", command=mostra_inserisci_corso)
    inserisci_corsi_button.pack(side=LEFT, padx= 10, pady=10)
    modifica_corsi_button = Button(frame_bottoni, text="Modifica Corso", font=("Open Sans", 10), bg="#ffffff", fg="#118e21", command=mostra_modifica_corso)
    modifica_corsi_button.pack(side=LEFT, padx= 10, pady=10)
    consulta_corsi_button = Button(frame_bottoni, text="Consulta Stato Iscrizioni ai Corsi", font=("Open Sans", 10), bg="#ffffff", fg="#118e21", command=mostra_consulta_corsi)
    consulta_corsi_button.pack(side=LEFT, padx= 10, pady=10)

    frame_contenuto = Frame(gestione_corsi,background="white", height=350, width=900)
    frame_contenuto.grid(row=3, column=0, columnspan=2, sticky="nsew")

    frame_risultati = Frame(gestione_corsi, background="white", height=350, width=900)
    frame_risultati.grid(row=4, column=0, columnspan=2, sticky="nsew") 

    frame_iscrizioni = Frame(gestione_corsi, background="white", height=350, width=900)
    frame_iscrizioni.grid(row=5, column=0, columnspan=2, sticky="nsew")

    # Funzioni per aggiornare il frame_contenuto

def mostra_inserisci_corso():
    for widget in frame_contenuto.winfo_children():
        widget.destroy()
    for widget in frame_risultati.winfo_children():
        widget.destroy()
    label = Label(frame_contenuto, text="Inserisci Corso", font=("Open Sans", 14), bg="#ffffff", fg="#118e21")
    label.grid(row=0, column=0, columnspan=2, pady=20)

    def pulisci_campi():
        denominazione_corso_box.delete(0, END)
        insegnante_box.delete(0, END)
        minimo_iscrizioni_box.delete(0, END)
        limite_iscrizioni_box.delete(0, END)
        sede_box.delete(0, END)
        giorno_lezione_box.delete(0, END)
        inizio_lezione_box.delete(0, END)
        fine_lezione_box.delete(0, END)
        note_box.delete(0, END)
        anno_accademico_box.set('')
    
    def clean_input(value):
        return value.strip() if value.strip() != '' else None
    def is_valid_int(value):
        try:
            int(value)
            return True
        except ValueError:
            return False
    def is_valid_time(time):
        return re.match(r'^\d{2}:\d{2}$', time) is not None
    
    def carica_anni_accademici():
        cursor = mydb.cursor()
        cursor.execute("SELECT ID_Anno_Accademico, Anno_Accademico FROM ANNI_ACCADEMICI")
        return cursor.fetchall()
    
    def aggiungi_corso():
        id_anno_accademico = anno_accademico_box.get()
        denominazione_corso = denominazione_corso_box.get().strip()
        insegnante = insegnante_box.get().strip()
        minimo_iscrizioni = minimo_iscrizioni_box.get().strip()
        limite_iscrizioni = limite_iscrizioni_box.get().strip()
        sede = sede_box.get().strip()
        giorno_lezione = giorno_lezione_box.get().strip()
        inizio_lezione = inizio_lezione_box.get().strip()
        fine_lezione = fine_lezione_box.get().strip()
        note = note_box.get().strip()

        if not (id_anno_accademico and denominazione_corso and insegnante and minimo_iscrizioni and limite_iscrizioni and sede and giorno_lezione and inizio_lezione and fine_lezione):
            messagebox.showerror("Errore", "Tutti i campi obbligatori devono essere compilati.", parent=frame_contenuto)
            return        
        if len(denominazione_corso) > 100:
            messagebox.showerror("Errore", "Denominazione corso troppo lunga. Massimo 100 caratteri.", parent=frame_contenuto)
            return
        if len(insegnante) > 30:
            messagebox.showerror("Errore", "Nome insegnante troppo lungo. Massimo 30 caratteri.", parent=frame_contenuto)
            return
        if not is_valid_int(minimo_iscrizioni):
            messagebox.showerror("Errore", "Minimo iscrizioni deve essere un numero intero.", parent=frame_contenuto)
            return
        if not is_valid_int(limite_iscrizioni):
            messagebox.showerror("Errore", "Limite iscrizioni deve essere un numero intero.", parent=frame_contenuto)
            return
        if len(sede) > 100:
            messagebox.showerror("Errore", "Nome sede troppo lungo. Massimo 100 caratteri.", parent=frame_contenuto)
            return
        if len(giorno_lezione) > 10:
            messagebox.showerror("Errore", "Nome giorno lezione troppo lungo. Massimo 10 caratteri.", parent=frame_contenuto)
            return
        if not is_valid_time(inizio_lezione):
            messagebox.showerror("Errore", "Orario di inizio non valido. Formato corretto: hh:mm", parent=frame_contenuto)
            return
        if not is_valid_time(fine_lezione):
            messagebox.showerror("Errore", "Orario di fine non valido. Formato corretto: hh:mm", parent=frame_contenuto)
            return
        if note and len(note) > 200:
            messagebox.showerror("Errore", "Note troppo lunghe. Massimo 200 caratteri.", parent=frame_contenuto)
            return
        
        try:
            id_anno_accademico = anni_accademici_dict.get(id_anno_accademico)
            if id_anno_accademico is None:
                messagebox.showerror("Errore", "Anno accademico non valido.", parent=frame_contenuto)
                return
            
            sql = "INSERT INTO Corsi (ID_Anno_Accademico, Denominazione_Corso, Insegnante, Minimo_Iscrizioni, Limite_Iscrizioni, Sede, Giorno_Lezione, Inizio_Lezione, Fine_Lezione, Note) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            values = (id_anno_accademico, denominazione_corso, insegnante, minimo_iscrizioni, limite_iscrizioni, sede, giorno_lezione, inizio_lezione, fine_lezione, note if note else None)
            cursor = mydb.cursor()
            cursor.execute(sql, values)
            mydb.commit()
            messagebox.showinfo("Successo", "Corso aggiunto con successo.", parent=frame_contenuto)
            pulisci_campi()            
        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante l'inserimento nel database: {str(e)}", parent=frame_contenuto)
            
    anni_accademici = carica_anni_accademici()
    anni_accademici_dict = {str(anno[1]): anno[0] for anno in anni_accademici}

    anno_accademico_label = Label(frame_contenuto, text="Anno Accademico (yyyy/yyyy)", font=("Open Sans", 10), bg="#ffffff", fg="#118e21").grid(row=1, column=0, sticky=W, padx="10")
    denominazione_corso_label = Label(frame_contenuto, text="Denominazione Corso", font=("Open Sans", 10), bg="#ffffff", fg="#118e21").grid(row=2, column=0, sticky=W, padx="10")
    insegnante_label = Label(frame_contenuto, text="Insegnante", font=("Open Sans", 10), bg="#ffffff", fg="#118e21").grid(row=3, column=0, sticky=W, padx="10")
    minimo_iscrizioni_label = Label(frame_contenuto, text="Minimo Iscrizioni", font=("Open Sans", 10), bg="#ffffff", fg="#118e21").grid(row=4, column=0, sticky=W, padx="10")
    limite_iscrizioni_label = Label(frame_contenuto, text="Limite Iscrizioni", font=("Open Sans", 10), bg="#ffffff", fg="#118e21").grid(row=5, column=0, sticky=W, padx="10")
    sede_iscrizioni_label = Label(frame_contenuto, text="Sede", font=("Open Sans", 10), bg="#ffffff", fg="#118e21").grid(row=6, column=0, sticky=W, padx="10")
    giorno_lezione_label = Label(frame_contenuto, text="Giorno", font=("Open Sans", 10), bg="#ffffff", fg="#118e21").grid(row=7, column=0, sticky=W, padx="10")
    inizio_lezione_label = Label(frame_contenuto, text="Orario di Inizio (hh:mm)", font=("Open Sans", 10), bg="#ffffff", fg="#118e21").grid(row=8, column=0, sticky=W, padx="10")
    fine_lezione_label = Label(frame_contenuto, text="Orario di Fine (hh:mm)", font=("Open Sans", 10), bg="#ffffff", fg="#118e21").grid(row=9, column=0, sticky=W, padx="10")
    note_label = Label(frame_contenuto, text="Note", font=("Open Sans", 10), bg="#ffffff", fg="#118e21").grid(row=10, column=0, sticky=W, padx="10")

    giorni = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"]

    anno_accademico_box = ttk.Combobox(frame_contenuto, values=list(anni_accademici_dict.keys()), width=15)
    anno_accademico_box.grid(row=1, column=1, pady=5, sticky="w")
    denominazione_corso_box = Entry(frame_contenuto, width=85)
    denominazione_corso_box.grid(row=2, column=1, pady=5, sticky="w")
    insegnante_box = Entry(frame_contenuto, width=85)
    insegnante_box.grid(row=3, column=1, pady=5, sticky="w")
    minimo_iscrizioni_box = Entry(frame_contenuto)
    minimo_iscrizioni_box.grid(row=4, column=1, pady=5, sticky="w")
    limite_iscrizioni_box = Entry(frame_contenuto)
    limite_iscrizioni_box.grid(row=5, column=1, pady=5, sticky="w")
    sede_box = Entry(frame_contenuto, width=85)
    sede_box.grid(row=6, column=1, pady=5, sticky="w")
    giorno_lezione_box = ttk.Combobox(frame_contenuto, values=giorni, state="readonly", width=20)
    giorno_lezione_box.grid(row=7, column=1, pady=5, sticky="w")
    inizio_lezione_box = Entry(frame_contenuto)
    inizio_lezione_box.grid(row=8, column=1, pady=5, sticky="w")
    fine_lezione_box = Entry(frame_contenuto)
    fine_lezione_box.grid(row=9, column=1, pady=5, sticky="w")
    note_box = Entry(frame_contenuto)
    note_box.grid(row=10, column=1, pady=5, sticky="w")

    inserisci_button = Button(frame_contenuto, text="Inserisci Corso", command=aggiungi_corso)
    inserisci_button.grid(row=12, column=0, columnspan=2, pady=20)
    pulisci_campi_corso = Button(frame_contenuto, text="Pulisci i campi", command=pulisci_campi)
    pulisci_campi_corso.grid(row=12, column=1)

anno_accademico_dict = {}

def aggiorna_corsi_combobox(anno_accademico, anno_accademico_dict):
    try:
        cursor = mydb.cursor()
        id_anno_accademico = anno_accademico_dict.get(anno_accademico, '')
        cursor.execute("SELECT Denominazione_Corso FROM Corsi WHERE ID_Anno_Accademico = ?", (id_anno_accademico,))
        corsi = [row[0] for row in cursor.fetchall()]
        corso_selezionato_combobox['values'] = corsi
    except pyodbc.Error as err:
        print("Errore nella connessione al database:", err)

def update():
    for widget in frame_risultati.grid_slaves():
        widget.grid_forget()
    
    def clean_input(value):
        return value if value != '' else None
    
    def pulisci_campi():
        id_box.config(state=NORMAL)
        id_box.delete(0, END)
        id_box.config(state=DISABLED)
        anno_accademico_box.delete(0, END)
        denominazione_corso_box.delete(0, END)
        insegnante_box.delete(0, END)
        minimo_iscrizioni_box.delete(0, END)
        limite_iscrizioni_box.delete(0, END)
        sede_box.delete(0, END)
        giorno_lezione_box.delete(0, END)
        inizio_lezione_box.delete(0, END)
        fine_lezione_box.delete(0, END)
        note_box.delete(0, END)
    
    def is_valid_anno_accademico(anno):
        return re.match(r'^\d{4}/\d{4}$', anno) is not None
    def is_valid_int(value):
        try:
            int(value)
            return True
        except ValueError:
            return False
    def is_valid_time(time):
        return re.match(r'^\d{2}:\d{2}$', time) is not None
    
    try:
        id = id_box.get()
        id_anno_accademico = anno_accademico_dict.get(anno_accademico_box.get(), '')
        denominazione_corso = clean_input(denominazione_corso_box.get() or "")
        insegnante = clean_input(insegnante_box.get() or "")
        minimo_iscrizioni = clean_input(minimo_iscrizioni_box.get() or "")
        limite_iscrizioni = clean_input(limite_iscrizioni_box.get() or "")
        sede = clean_input(sede_box.get() or "")
        giorno_lezione = clean_input(giorno_lezione_box.get() or "")
        inizio_lezione = clean_input(inizio_lezione_box.get() or "")
        fine_lezione = clean_input(fine_lezione_box.get() or "")
        note = clean_input(note_box.get() or "")

        if not (id_anno_accademico and denominazione_corso and insegnante and minimo_iscrizioni and limite_iscrizioni and sede and giorno_lezione and inizio_lezione and fine_lezione):
            messagebox.showerror("Errore", "Tutti i campi obbligatori devono essere compilati.", parent=frame_risultati)
            return

        if not is_valid_anno_accademico(anno_accademico_box.get()):
            messagebox.showerror("Errore", "Anno accademico non valido. Formato corretto: yyyy/yyyy", parent=frame_risultati)
            return
        
        if len(denominazione_corso) > 100:
            messagebox.showerror("Errore", "Denominazione corso troppo lunga. Massimo 100 caratteri.", parent=frame_risultati)
            return
        
        if len(insegnante) > 30:
            messagebox.showerror("Errore", "Nome insegnante troppo lungo. Massimo 30 caratteri.", parent=frame_risultati)
            return   
        if not is_valid_int(minimo_iscrizioni):
            messagebox.showerror("Errore", "Minimo iscrizioni deve essere un numero intero.", parent=frame_risultati)
            return        
        if not is_valid_int(limite_iscrizioni):
            messagebox.showerror("Errore", "Limite iscrizioni deve essere un numero intero.", parent=frame_risultati)
            return        
        if len(sede) > 100:
            messagebox.showerror("Errore", "Nome sede troppo lungo. Massimo 100 caratteri.", parent=frame_risultati)
            return        
        if len(giorno_lezione) > 10:
            messagebox.showerror("Errore", "Nome giorno lezione troppo lungo. Massimo 10 caratteri.", parent=frame_risultati)
            return
        if not is_valid_time(inizio_lezione):
            messagebox.showerror("Errore", "Orario di inizio non valido. Formato corretto: hh:mm", parent=frame_risultati)
            return
        if not is_valid_time(fine_lezione):
            messagebox.showerror("Errore", "Orario di fine non valido. Formato corretto: hh:mm", parent=frame_risultati)
            return
        if note and len(note) > 200:
            messagebox.showerror("Errore", "Note troppo lunghe. Massimo 200 caratteri.", parent=frame_risultati)
            return
        
        sql = "UPDATE Corsi SET ID_Anno_Accademico = ?, Denominazione_Corso = ?, Insegnante = ?, Minimo_Iscrizioni = ?, Limite_Iscrizioni = ?, Sede = ?, Giorno_Lezione = ?, \
            Inizio_Lezione = ?, Fine_Lezione = ?, Note = ? WHERE ID_Corso = ?"
        values = (id_anno_accademico, denominazione_corso, insegnante, minimo_iscrizioni, limite_iscrizioni, sede, giorno_lezione, inizio_lezione, fine_lezione, note, id)
        cursor = mydb.cursor()
        cursor.execute(sql, values)
        mydb.commit()
        messagebox.showinfo("Successo", "Corso aggiornato con successo.", parent=frame_risultati)
        pulisci_campi()
        chiudi_gestione_corsi()
    
    except Exception as e:
        messagebox.showerror("Errore", f"Errore durante l'aggiornamento nel database: {str(e)}", parent=frame_risultati)

def cerca_ora():
    for widget in frame_risultati.grid_slaves():
        widget.grid_forget()
    
    def clean_input(value):
        return value if value != '' else None
    
    cursor_cerca_corsi = mydb.cursor()
    id_anno_accademico = anno_accademico_dict.get(anno_accademico_combobox.get(), '')
    corso = corso_selezionato_combobox.get()
    values = (id_anno_accademico, corso)
    sql = "SELECT * FROM Corsi WHERE ID_Anno_Accademico = ? AND Denominazione_Corso = ?"
    result = cursor_cerca_corsi.execute(sql, values)
    result = cursor_cerca_corsi.fetchall()

    if not result:
        result = "Nessun risultato trovato"
        ricerca_label = Label(frame_risultati, text=result, font=("Open Sans", 10), bg="#ffffff", fg="#118e21")
        ricerca_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    else:
        id_corso_label = Label(frame_risultati, text="Id Corso", font=("Open Sans", 10), bg="#ffffff", fg="#118e21").grid(row=2, column=0, sticky=W, padx="10", pady="5")
        anno_accademico_label = Label(frame_risultati, text="Anno Accademico", font=("Open Sans", 10), bg="#ffffff", fg="#118e21").grid(row=3, column=0, sticky=W, padx="10", pady="5")
        denominazione_corso_label = Label(frame_risultati, text="Denominazione Corso", font=("Open Sans", 10), bg="#ffffff", fg="#118e21").grid(row=4, column=0, sticky=W, padx="10", pady="5")
        insegnante_label = Label(frame_risultati, text="Insegnante", font=("Open Sans", 10), bg="#ffffff", fg="#118e21").grid(row=5, column=0, sticky=W, padx="10", pady="5")
        minimo_iscrizioni_label = Label(frame_risultati, text="Minimo Iscrizioni", font=("Open Sans", 10), bg="#ffffff", fg="#118e21").grid(row=6, column=0, sticky=W, padx="10", pady="5")
        limite_iscrizioni_label = Label(frame_risultati, text="Limite Iscrizioni", font=("Open Sans", 10), bg="#ffffff", fg="#118e21").grid(row=7, column=0, sticky=W, padx="10", pady="5")
        sede_label = Label(frame_risultati, text="Sede", font=("Open Sans", 10), bg="#ffffff", fg="#118e21").grid(row=8, column=0, sticky=W, padx="10", pady="5")
        giorno_lezione_label = Label(frame_risultati, text="Giorno", font=("Open Sans", 10), bg="#ffffff", fg="#118e21").grid(row=9, column=0, sticky=W, padx="10", pady="5")
        inizio_lezione_label = Label(frame_risultati, text="Orario di Inizio (hh:mm)", font=("Open Sans", 10), bg="#ffffff", fg="#118e21").grid(row=10, column=0, sticky=W, padx="10", pady="5")
        fine_lezione_label = Label(frame_risultati, text="Orario di Fine (hh:mm)", font=("Open Sans", 10), bg="#ffffff", fg="#118e21").grid(row=11, column=0, sticky=W, padx="10", pady="5")
        note_label = Label(frame_risultati, text="Note", font=("Open Sans", 10), bg="#ffffff", fg="#118e21").grid(row=12, column=0, sticky=W, padx="10", pady="5")

        giorni = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"]

        global id_box
        id_box = Entry(frame_risultati)
        id_box.grid(row=2, column=1, sticky=W, padx="10", pady="5")
        id_box.insert(0, result[0][0] if result[0] is not None else "")
        id_box.config(state=DISABLED)

        global anno_accademico_box
        anno_accademico_box = Entry(frame_risultati)
        anno_accademico_box.grid(row=3, column=1, sticky=W, padx="10", pady="5")
        anno_accademico_box.insert(0, list(anno_accademico_dict.keys())[list(anno_accademico_dict.values()).index(result[0][1])] if result[0][1] is not None else "")

        global denominazione_corso_box
        denominazione_corso_box = Entry(frame_risultati, width=80)
        denominazione_corso_box.grid(row=4, column=1, sticky=W, padx="10", pady="5")
        denominazione_corso_box.insert(0, result[0][2] if result[0][2] is not None else "")

        global insegnante_box
        insegnante_box = Entry(frame_risultati, width=80)
        insegnante_box.grid(row=5, column=1, sticky=W, padx="10", pady="5")
        insegnante_box.insert(0, result[0][3] if result[0][3] is not None else "")

        global minimo_iscrizioni_box
        minimo_iscrizioni_box = Entry(frame_risultati)
        minimo_iscrizioni_box.grid(row=6, column=1, sticky=W, padx="10", pady="5")
        minimo_iscrizioni_box.insert(0, result[0][4] if result[0][4] is not None else "")

        global limite_iscrizioni_box
        limite_iscrizioni_box = Entry(frame_risultati)
        limite_iscrizioni_box.grid(row=7, column=1, sticky=W, padx="10", pady="5")
        limite_iscrizioni_box.insert(0, result[0][5] if result[0][5] is not None else "")

        global sede_box
        sede_box = Entry(frame_risultati, width=80)
        sede_box.grid(row=8, column=1, sticky=W, padx="10", pady="5")
        sede_box.insert(0, result[0][6] if result[0][6] is not None else "")

        global giorno_lezione_box
        giorno_lezione_box = ttk.Combobox(frame_risultati, values=giorni, state="readonly", width=20)
        giorno_lezione_box.grid(row=9, column=1, sticky=W, padx="10", pady="5")
        giorno_lezione_box.set(result[0][7] if result[0][7] is not None else "")

        global inizio_lezione_box
        inizio_lezione_box = Entry(frame_risultati)
        inizio_lezione_box.grid(row=10, column=1, sticky=W, padx="10", pady="5")
        inizio_lezione_box.insert(0, result[0][8] if result[0][8] is not None else "")

        global fine_lezione_box
        fine_lezione_box = Entry(frame_risultati)
        fine_lezione_box.grid(row=11, column=1, sticky=W, padx="10", pady="5")
        fine_lezione_box.insert(0, result[0][9] if result[0][9] is not None else "")

        global note_box
        note_box = Entry(frame_risultati, width=80)
        note_box.grid(row=12, column=1, sticky=W, padx="10", pady="5")
        note_box.insert(0, result[0][10] if result[0][10] is not None else "")

        salva_record = Button(frame_risultati, text="Salva Record", command=update)
        salva_record.grid(row=15, column=0, padx=30, pady=10, sticky=W)

def mostra_modifica_corso():
    global anno_accademico_combobox
    global corso_selezionato_combobox
    for widget in frame_contenuto.winfo_children():
        widget.destroy()
    for widget in frame_risultati.winfo_children():
        widget.destroy()

    label = Label(frame_contenuto, text="Modifica Corso", font=("Open Sans", 14), bg="#ffffff", fg="#118e21")
    label.grid(row=0, column=0, columnspan=2, pady=20)
    label_anno_accademico = Label(frame_contenuto, text="Anno Accademico", font=("Open Sans", 10), bg="#ffffff", fg="#118e21")
    label_anno_accademico.grid(row=1, column=0, padx=10, pady=5, sticky="w")

    anno_accademico_selezionato = StringVar()
    anno_accademico_combobox = ttk.Combobox(frame_contenuto, textvariable=anno_accademico_selezionato)
    anno_accademico_combobox['state'] = 'readonly'
    anno_accademico_combobox.grid(row=1, column=1, padx=10, pady=5, sticky="w")
    anno_accademico_combobox.bind("<<ComboboxSelected>>", lambda event: aggiorna_corsi_combobox(anno_accademico_selezionato.get(), anno_accademico_dict))

    try:
        cursor = mydb.cursor()
        cursor.execute("SELECT ID_Anno_Accademico, Anno_Accademico FROM Anni_Accademici")
        anni_accademici = cursor.fetchall()
        anno_accademico_dict.update({row[1]: row[0] for row in anni_accademici})
        anno_accademico_combobox['values'] = list(anno_accademico_dict.keys())
    except pyodbc.Error as err:
        print("Errore nella connessione al database:", err)

    label_corso = Label(frame_contenuto, text="Corso", font=("Open Sans", 10), bg="#ffffff", fg="#118e21")
    label_corso.grid(row=1, column=2, padx=10, pady=5, sticky="w")

    corso_selezionato = StringVar()
    corso_selezionato_combobox = ttk.Combobox(frame_contenuto, textvariable=corso_selezionato, width=40)
    corso_selezionato_combobox['state'] = 'readonly'
    corso_selezionato_combobox.grid(row=1, column=3, padx=10, pady=5, sticky="w")

    cerca_corso_button = Button(frame_contenuto, text="Cerca", command=cerca_ora)
    cerca_corso_button.grid(row=1, column=4, padx=10, pady=5, sticky="w")

def visualizza_corsi():
    def aggiorna_risultati():
        for widget in frame_risultati.grid_slaves():
            widget.grid_forget()
        anno_accademico = anno_accademico_selezionato.get()
        if not anno_accademico:
            messagebox.showerror("Errore", "Seleziona un anno accademico")
            return
        
        try:
            cursor = mydb.cursor()
            cursor.execute("EXEC CreateControlloIscrizioniView @anno_accademico = ?", anno_accademico)
            nuovi_risultati = cursor.fetchall()

            if nuovi_risultati != aggiorna_risultati.ultimi_risultati:
                aggiorna_risultati.ultimi_risultati = nuovi_risultati

                for widget in frame_iscrizioni.winfo_children():
                    widget.destroy()
                
                colonne = ['Corso', 'Totale Iscritti', 'Minimo Iscrizioni', 'Posti Disponibili', 'Stato Iscrizioni']
                treeview = ttk.Treeview(frame_iscrizioni, columns=colonne, show="headings", height=18)
                treeview.grid(row=0, column=0, padx=10, sticky="nsew")

                vsb = ttk.Scrollbar(frame_iscrizioni, orient="vertical", command=treeview.yview)
                vsb.grid(row=0, column=1, sticky='ns')

                treeview.configure(yscrollcommand=vsb.set)

                treeview.column('Corso', width=350, anchor='center')
                treeview.column('Totale Iscritti', width=100, anchor='center')
                treeview.column('Minimo Iscrizioni', width=100, anchor='center')
                treeview.column('Posti Disponibili', width=100, anchor='center')
                treeview.column('Stato Iscrizioni', width=200, anchor='center')

                for col in colonne:
                    treeview.heading(col, text=col, anchor='center')
                for row in nuovi_risultati:
                    treeview.insert('', 'end', values=(row[0], row[1], row[2], row[3], row[4]))
                frame_iscrizioni.grid_rowconfigure(0, weight=1)
                frame_iscrizioni.grid_columnconfigure(0, weight=1)

        except pyodbc.Error as err:
            messagebox.showerror("Errore", f"Errore nella connessione al database: {err}")

        frame_iscrizioni.after(60000, aggiorna_risultati)
    aggiorna_risultati.ultimi_risultati = None
    aggiorna_risultati()

def mostra_consulta_corsi():
    for widget in frame_contenuto.winfo_children():
        widget.destroy()
    for widget in frame_risultati.winfo_children():
        widget.destroy()
    
    label = Label(frame_contenuto, text="Consulta Stato Iscrizioni ai Corsi", font=("Open Sans", 14), bg="#ffffff", fg="#118e21")
    label.grid(row=0, column=0, columnspan=2, pady=20)
    label_anno_accademico = Label(frame_contenuto, text="Anno Accademico", font=("Open Sans", 10), bg="#ffffff", fg="#118e21")
    label_anno_accademico.grid(row=1, column=0, padx=10, pady=5, sticky="w")

    global anno_accademico_selezionato
    anno_accademico_selezionato = StringVar()
    anno_accademico_combobox = ttk.Combobox(frame_contenuto, textvariable=anno_accademico_selezionato)
    anno_accademico_combobox['state'] = 'readonly'
    anno_accademico_combobox.grid(row=1, column=1, padx=10, pady=5, sticky="w")
    
    try:
        cursor = mydb.cursor()
        cursor.execute("SELECT ID_Anno_Accademico, Anno_Accademico FROM Anni_Accademici")
        anni_accademici = cursor.fetchall()
        anno_accademico_dict.update({row[1]: row[0] for row in anni_accademici})
        anno_accademico_combobox['values'] = list(anno_accademico_dict.keys())
    except pyodbc.Error as err:
        print("Errore nella connessione al database:", err)

    visualizza_stato_corsi_button = Button(frame_contenuto, text="Visualizza Stato Corsi", command=visualizza_corsi)
    visualizza_stato_corsi_button.grid(row=1, column=4, padx=40, pady=5, sticky="w")

    global frame_iscrizioni
    frame_iscrizioni = Frame(frame_contenuto, bg="#ffffff")
    frame_iscrizioni.grid(row=2, column=0, columnspan=5, pady=20)

def chiudi_gestione_corsi():
    gestione_corsi.destroy()
def chiudi_gestione_anagrafiche():
    gestione_anagrafiche.destroy()
def chiudi_gestione_iscrizioni():
    gestione_iscrizioni.destroy()

def apri_finestra_principale():
    global root
    global mydb
    root = Tk()
    root.title('UniTre Roma Arvalia Management')
    ico_path = os.path.join(os.path.dirname(__file__), 'logo-unitre-arvalia.ico')
    root.iconbitmap(ico_path)
    root.geometry("900x600")
    root.configure(bg="#ffffff")
    root.resizable(False,False)

    try:
        mydb = pyodbc.connect(
    r"DRIVER={ODBC Driver 17 for SQL Server};"
        r"SERVER=LAPTOP-59547MC6\SQLEXPRESS;"
        r"DATABASE=UniTreRomaArvalia;"
        r"Trusted_Connection=yes;"
        )

        print("Connessione al database SQL Server riuscita.")

        # Esempio di esecuzione di una query
        cursor = mydb.cursor()
        cursor.execute("SELECT @@version;")
        row = cursor.fetchone()
        print("Versione del database:", row[0])

        # Chiudere il cursore
        cursor.close()

    except pyodbc.Error as err:
        print("Errore nella connessione al database:", err)
        # Gestione dell'errore, ad esempio mostrare un messaggio all'utente

    my_cursor = mydb.cursor()

    # schermata home - banner
    banner_home = Frame(root, background="white", height=100, width=900)
    banner_home.pack(fill=BOTH, expand=True)

    title_image_path = os.path.join(os.path.dirname(__file__), 'logo-unitre-arvalia.jpg')
    title_image = Image.open(title_image_path)
    title_image = title_image.resize((100, 100), Image.LANCZOS)
    title_photo = ImageTk.PhotoImage(title_image)

    image_label = Label(banner_home, image=title_photo, bg="#ffffff")
    image_label.pack(side=LEFT, padx=10)

    title_label = Label(banner_home, text="UniTre Roma Arvalia - Sistema Gestione Iscrizioni", font=("Open Sans", 16), bg="#ffffff", fg="#118e21")
    title_label.pack(side=LEFT, padx=75)

    # schermata home - center

    center_home = Frame(root, background="white", height=350, width=900)
    center_home.pack(fill=BOTH, expand=True)

    bg_image_path = os.path.join(os.path.dirname(__file__), 'bg.jpg')
    bg_image = Image.open(bg_image_path)
    bg_image = bg_image.resize((900, 350), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    canvas = Canvas(center_home, width=600, height=300)
    canvas.pack(fill=BOTH, expand=True)
    canvas.create_image(0, 0, image=bg_photo, anchor=NW)

    # schermata home - lower

    lower_home = Frame(root, background="white", height=50, width=900)
    lower_home.pack(fill=BOTH, expand=True)

    corsi_icon_path = os.path.join(os.path.dirname(__file__), 'corso.png')
    anagrafiche_icon_path = os.path.join(os.path.dirname(__file__), 'anagrafiche.png')
    iscrizioni_icon_path = os.path.join(os.path.dirname(__file__), 'iscrizioni.png')

    icon_size = (50, 50)

    corsi_icon = ImageTk.PhotoImage(Image.open(corsi_icon_path).resize(icon_size, Image.LANCZOS))    
    anagrafiche_icon = ImageTk.PhotoImage(Image.open(anagrafiche_icon_path).resize(icon_size, Image.LANCZOS))
    iscrizioni_icon = ImageTk.PhotoImage(Image.open(iscrizioni_icon_path).resize(icon_size, Image.LANCZOS))

    button_size = {'width': 120, 'height': 75}

    corsi_button = Button(lower_home, text="Gestisci Corsi", font=("Open Sans", 10), image=corsi_icon, compound=TOP, bg="#ffffff", fg="#118e21", **button_size, command=apri_gestione_corsi)
    corsi_button.pack(side=LEFT, padx= 80)
    anagrafiche_button = Button(lower_home, text="Gestisci Anagrafiche", font=("Open Sans", 10), image=anagrafiche_icon, compound=TOP, bg="#ffffff", fg="#118e21", **button_size, command=apri_gestione_anagrafiche)
    anagrafiche_button.pack(side=LEFT, padx= 80)
    iscrizioni_button = Button(lower_home, text="Gestisci Iscrizioni", font=("Open Sans", 10), image=iscrizioni_icon, compound=TOP, bg="#ffffff", fg="#118e21", **button_size, command=apri_gestione_iscrizioni)
    iscrizioni_button.pack(side=LEFT, padx= 80)

    root.mainloop()

    try:
        mydb.close()
        print("Connessione al database chiusa correttamente.")
    except pyodbc.Error as err:
        print("Errore durante la chiusura della connessione al database:", err)

# Avvia l'applicazione aprendo la finestra principale
apri_finestra_principale()