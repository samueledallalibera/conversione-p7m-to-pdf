import re
import os

def extract_pdf_from_p7m(input_file, output_dir):
    """
    Estrae un file PDF da un file .p7m non compresso, includendo tutto dal primo %PDF- all'ultimo %%EOF.
    
    Parametri:
        input_file (str): Percorso del file .p7m da processare.
        output_dir (str): Percorso della cartella di destinazione per il PDF estratto.
    """
    # Legge il contenuto del file p7m
    with open(input_file, 'rb') as f:
        contents = f.read()

    # Cerca il primo %PDF- e l'ultimo %%EOF
    pdf_pattern = re.compile(rb'%PDF-.*%%EOF', re.MULTILINE | re.DOTALL)
    match = pdf_pattern.search(contents)

    if not match:
        raise ValueError(f"Nessun contenuto PDF trovato nel file '{input_file}'.")

    pdf_contents = match.group()

    # Determina il nome del file di output
    output_file = os.path.join(output_dir, os.path.basename(input_file).replace('.p7m', '.pdf'))

    # Scrive il contenuto PDF estratto in un nuovo file
    with open(output_file, 'wb') as f:
        f.write(pdf_contents)

    print(f"PDF estratto con successo: {output_file}")

def process_p7m_directory(input_dir, output_dir):
    """
    Elabora tutti i file .p7m in una cartella e salva i PDF estratti in un'altra cartella.
    
    Parametri:
        input_dir (str): Percorso della cartella contenente i file .p7m.
        output_dir (str): Percorso della cartella di destinazione per i PDF estratti.
    """
    if not os.path.isdir(input_dir):
        raise NotADirectoryError(f"La cartella '{input_dir}' non esiste.")

    # Crea la cartella di output se non esiste
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Processa ogni file .p7m nella cartella
    p7m_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.p7m')]
    if not p7m_files:
        print(f"Nessun file .p7m trovato nella cartella '{input_dir}'.")
        return

    for file_name in p7m_files:
        input_file = os.path.join(input_dir, file_name)
        try:
            extract_pdf_from_p7m(input_file, output_dir)
        except Exception as e:
            print(f"Errore durante l'elaborazione di '{file_name}': {e}")

# Interfaccia interattiva per Jupyter Notebook
def process_p7m_files_in_bulk():
    """
    Permette all'utente di specificare una cartella di input con file .p7m e una cartella di output.
    """
    # Chiedi il percorso della cartella di input
    input_dir = input("Inserisci il percorso completo della cartella contenente i file .p7m: ").strip()
    if not os.path.isdir(input_dir):
        print(f"Errore: La cartella '{input_dir}' non esiste.")
        return

    # Chiedi il percorso della cartella di output
    output_dir = input("Inserisci il percorso completo della cartella di destinazione: ").strip()
    if not os.path.exists(output_dir):
        create_dir = input(f"La cartella '{output_dir}' non esiste. Vuoi crearla? (s/n): ").strip().lower()
        if create_dir == 's':
            os.makedirs(output_dir)
        else:
            print("Operazione annullata.")
            return

    # Processa la cartella
    process_p7m_directory(input_dir, output_dir)

# Esegui la funzione interattiva
process_p7m_files_in_bulk()