# Utility functions for reading uploaded files

from pypdf import PdfReader

def read_uploaded_file(uploaded_file):

    # Check the file extension
    file_extension = uploaded_file.name.split(".")[-1].lower()  #.lower in order to handle case-insensitive file extensions
                                                                # .split(".")[-1] gets the last part of the filename after the last dot, which is the file extension
    # Read the file based on its extension
    if file_extension == "txt":
                document_text = uploaded_file.read().decode("utf-8")
    
    # Handle PDF files
    elif file_extension == "pdf":
        pdf_reader = PdfReader(uploaded_file)

        document_text = ""

        for page in pdf_reader.pages:
            page_text = page.extract_text()

            if page_text:
                document_text += page_text + "\n"
        if not document_text.strip():
            raise ValueError("No readable text found in PDF.")
    
    # Error handling for unsupported file types
    else:
        raise ValueError(f"Unsupported file type: {file_extension}")

    return document_text