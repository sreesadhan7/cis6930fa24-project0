import pandas as pd
import urllib.request
import pypdf
from pypdf import PdfReader
import tempfile
import re
import sqlite3
import os

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

# def extract_incidents(pdf_file_path):
#     """
#     Extracts incident data from the provided PDF file and combines multi-line records into a single line.
    
#     :param pdf_file_path: Path to the PDF file
#     :return: List of extracted incidents
#     """
#     incidents = []

#     # Load the PDF file
#     reader = PdfReader(pdf_file_path)

#     # Regular expression to match the pattern of the start of a new record (e.g., a date at the beginning)
#     record_start_pattern = re.compile(r"\d{1,2}/\d{1,2}/\d{4}")

#     # Flag to determine when the header ends and data starts
#     data_started = False

#     # Temporary storage for current incident record
#     current_record = ""

#     # Loop through each page and extract text
#     for page in reader.pages:
#         text = page.extract_text()

#         # Split the text into lines
#         lines = text.split("\n")

#         # Process each line and combine multi-line records
#         for line in lines:
#             # Skip lines until we find the header
#             if not data_started:
#                 if "Date / Time" in line:  # Assuming "Date / Time" is in the header
#                     data_started = True
#                 continue  # Skip this line as it is part of the header

#             # Now that data has started, we look for record lines
#             if record_start_pattern.match(line):
#                 # If we have accumulated a record, add it to the list
#                 if current_record:
#                     incidents.append(current_record.strip())
                
#                 # Start a new record
#                 current_record = line
#             else:
#                 # Continue appending to the current record
#                 current_record += " " + line

#     return incidents


# def extract_incidents(pdf_file_path):
#     """
#     Extracts incident data from the provided PDF file, structures it into a pandas DataFrame.

#     Parameters:
#     pdf_file_path (str): Path to the PDF file

#     Returns:
#     pandas.DataFrame: DataFrame containing extracted incident data
#     """
#     is_first_page = True
#     field_count = 3
#     header_lines   = 3
#     table_header_row = 2

#     def regex_splitline(line):
#         return [item.strip() for item in re.split(r"\s{2,}", line)]
    
#     data_store = []
#     pdf_file = PdfReader(pdf_file_path)
#     pdf_file.pages[0].extract_text()

#     for page in pdf_file.pages:

#         # extracting the context with layout method, the behavior can be truly unpredictable if the pdf format/structure changes
#         get_data = page.extract_text(
#             extraction_mode="layout", layout_mode_space_vertically=False
#         ).split("\n")

#         if is_first_page is True:

#             # extracting the field names
#             table_header_names = regex_splitline(get_data[table_header_row])[1:]
#             # removing the junk lines
#             get_data = get_data[header_lines  :]
#             is_first_page = False

#         # splitting the extracted line for respective field values
#         data_store.extend([regex_splitline(item) for item in get_data])

#         #location data can be in multiple lines, so removing the rows which have less than 3 fields. Also, removing rows that have no values.
#         data_store = [item for item in data_store if len(item) >= field_count]

#     # converting the list of list to pandas dataframe
#     df = pd.DataFrame(data_store, columns=['incident_time', 'incident_number', 'incident_location', 'nature', 'incident_ori'])
#     df['nature'] = df['nature'].apply(lambda x : '' if x is None else x )

#     print(df)
#     return df

def extract_incidents(pdf_file_path):
    """
    Extracts incident data from the provided PDF file, structures it into a pandas DataFrame.

    Parameters:
    pdf_file_path (str): Path to the PDF file

    Returns:
    pandas.DataFrame: DataFrame containing extracted incident data
    """
    is_first_page = True
    field_count = 3
    header_lines   = 3
    table_header_row = 2

   # Reading the PDF and initializing necessary variables
    data_store = [] # List to store the extracted data
    read_file = PdfReader(pdf_file_path)
    read_file.pages[0].extract_text() # Extracting the text from the first page to avoid unnecessary data

    page_index = 0 # Initializing the page index
    num_pages = len(read_file.pages) # Getting the total number of pages in the PDF

    while page_index < num_pages:
        page = read_file.pages[page_index]
        
        # Getting the page data using the layout method
        get_data = page.extract_text(extraction_mode="layout", layout_mode_space_vertically=False).split("\n")
        
        if is_first_page:
            # Extracting the headers from the first page
            table_headers = re.split(r"\s{2,}", get_data[table_header_row])  # Split the header row based on two or more spaces
            table_header_names = []

            for item in table_headers[1:]:  # Skip the first element and process the rest
                table_header_names.append(item.strip())  # Strip each field name and add to the list
            
            # Removing the unnecessary header lines
            get_data = get_data[header_lines:]
            is_first_page = False

        # Splitting each extracted line for respective field values and cleaning up extra spaces
        data_store.extend([ [item.strip() for item in re.split(r"\s{2,}", line)] for line in get_data ])

        # Increment page index to continue with the next page
        page_index += 1

    # Initializing a new list to store valid rows
    filtered_data = []

    # Iterate over each item in the data_store
    for item in data_store:
        # Check if the row has at least 'field_count' fields and contains values
        if len(item) >= field_count and any(item):
            filtered_data.append(item)

    # Replacing the original data_store with the filtered data
    data_store = filtered_data

    # Creating a DataFrame with appropriate columns
    incidents_df = pd.DataFrame(data_store, columns=['incident_time', 'incident_number', 'incident_location', 'nature', 'incident_ori'])

    # print(incidents_df)
    return incidents_df


def createdb():
    """
    Creates an SQLite database and returns the connection object.
    The database will contain a table `incidents` with the specified schema.
    """
    # Set the absolute path for the resources folder in the root directory
    root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    resources_path = os.path.join(root_path, "resources")
    
    # Ensure the resources directory exists
    if not os.path.exists(resources_path):
        os.makedirs(resources_path)
    
    # Define the database path in the resources folder
    db_path = os.path.join(resources_path, "normanpd.db")
    
    # Remove the existing database if it exists to start fresh
    if os.path.exists(db_path):
        os.remove(db_path)
        # print("Removeing the existing database.")

    # Create a connection to the SQLite database
    conn = sqlite3.connect(db_path)
    # print("Created the database in the resources folder.")
    
    # Create the incidents table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS incidents (
            incident_time TEXT,
            incident_number TEXT,
            incident_location TEXT,
            nature TEXT,
            incident_ori TEXT
        );
    ''')
    
    # Commit changes and return the connection
    conn.commit()
    return conn

def populatedb(conn, incidents_df):
    """
    Inserts a DataFrame of incidents into the database.
    
    :param conn: The SQLite database connection object.
    :param incidents_df: A pandas DataFrame containing incident data.
    """
    cursor = conn.cursor()

    # Query to insert data into the incidents table
    insert_query = '''
        INSERT INTO incidents (incident_time, incident_number, incident_location, nature, incident_ori)
        VALUES (?, ?, ?, ?, ?);
    '''

    # Inserting each row from the DataFrame into the database
    try:
        for index, row in incidents_df.iterrows():
            cursor.execute(insert_query, (
                row['incident_time'],
                row['incident_number'],
                row['incident_location'],
                row['nature'],
                row['incident_ori']
            ))
        
        conn.commit()
    except Exception as e:
        conn.rollback()  # Rollback any changes if there's an error
    finally:
        cursor.close()

def status(conn):
    """
    Prints to standard out a list of the nature of incidents and the number of times
    they have occurred. The list is sorted alphabetically by the nature of the incident.
    
    :param conn: The SQLite database connection object.
    """
    cursor = conn.cursor()

    # Query to get the count of each nature of incident
    cursor.execute('''
        SELECT nature, COUNT(*) as count
        FROM incidents
        GROUP BY nature
        ORDER BY nature ASC;
    ''')
    
    # Fetch all results
    results = cursor.fetchall()
    
    # Print the results in the ascending format of nature
    for row in results:
        nature, count = row
        print(f"{nature}|{count}")