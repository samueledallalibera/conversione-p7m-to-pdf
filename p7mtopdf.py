import os
import re
import zipfile
import streamlit as st
import io

def extract_pdf_from_p7m(contents, file_name):
    """
    Estrae un file PDF da contenuti binari di un file .p7m, includendo tutto dal primo %PDF- all'ultimo %%EOF.
    
    Parametri:
        contents (bytes): Contenuti del file .p7m.
        file_name (str): Nome del file per riferimenti.
    
    Ritorna:
        bytes: Contenuto del PDF estratto.
    """
    pdf_pattern = re.compile(rb'%PDF-.*%%EOF', re.MULTILINE | re.DOTALL)
    match = pdf_pattern.search(contents)

    if not match:
        raise ValueError(f"Nessun contenuto PDF trovato in '{file_name}'.")

    return match.group()

def process_zip_file(zip_file):
    """
    Elabora un archivio ZIP contenente file .p7m e restituisce un archivio ZIP con i PDF estratti.
    
    Parametri:
        zip_file (UploadedFile): Archivio ZIP caricato dall'utente.
    
    Ritorna:
        bytes: Archivio ZIP con i PDF estratti.
    """
    # Utilizzare un oggetto BytesIO per creare un file ZIP in memoria
    output_zip_io = io.BytesIO()

    with zipfile.ZipFile(output_zip_io, 'w', zipfile.ZIP_DEFLATED) as output_zip:
        with zipfile.ZipFile(zip_file, 'r') as z_in:
            for file_name in z_in.namelist():
                if file_name.lower().endswith('.p7m'):
                    try:
                        # Leggi i contenuti del file .p7m
                        contents = z_in.read(file_name)
                        # Estrai il contenuto del PDF
                        pdf_contents = extract_pdf_from_p7m(contents, file_name)
                        # Salva il PDF nell'archivio ZIP di output
                        pdf_name = file_name.replace('.p7m', '.pdf')
                        output_zip.writestr(pdf_name, pdf_contents)
                    except Exception as e:
                        st.warning(f"Errore durante l'elaborazione di '{file_name}': {e}")
    
    # Riportare la posizione all'inizio del file in memoria per il download
    output_zip_io.seek(0)

    return output_zip_io

# Streamlit app
st.title("Estrazione PDF da file P7M")

# Caricamento del file ZIP
uploaded_zip = st.file_uploader("Carica un file ZIP contenente file .p7m:", type="zip")

if uploaded_zip is not None:
    try:
        # Processa il file ZIP e ottieni l'archivio con i PDF estratti
        result_zip_io = process_zip_file(uploaded_zip)
        # Offri il download del file ZIP con i PDF estratti
        st.success("Elaborazione completata! Scarica l'archivio ZIP con i PDF estratti:")
        st.download_button("Scarica PDF estratti", data=result_zip_io, file_name="extracted_pdfs.zip", mime="application/zip")
    except Exception as e:
        st.error(f"Si è verificato un errore durante l'elaborazione: {e}")
