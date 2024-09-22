import urllib.request
import pypdf
from pypdf import PdfReader
import tempfile

def fetch_incidents(url):
    """
    Downloads the incident PDF from the provided URL and saves it to a temporary file.
    
    :param url: URL of the incident PDF file
    :return: Path to the saved PDF file
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
    }
    
    req = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(req)
    
    # Read the content of the PDF
    pdf_content = response.read()
    
    # Write the PDF content to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        temp_pdf.write(pdf_content)
        temp_pdf_path = temp_pdf.name
    
    return temp_pdf_path

def extract_incidents(pdf_file_path):
    """
    Extracts incident data from the provided PDF file.
    
    :param pdf_file_path: Path to the PDF file
    :return: List of extracted incidents with fields like Date/Time, Incident Number, Location, Nature, and Incident ORI
    """
    incidents = []

    # Load the PDF content
    reader = pypdf.PdfReader(pdf_file_path)
    
    # Loop through each page and extract text
    for page in reader.pages:
        text = page.extract_text()
        
        # Here you would need to process the extracted text to isolate relevant fields
        # For example, splitting the text by known delimiters or patterns
        
        print("Extracted Text from PDF Page:")
        print(text)
        
        incidents.append(text)
    
    return incidents
