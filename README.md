# cis6930fa24 -- Project0

Name: Sai Sree Sadhan Polimera

# Assignment Description 

This project involves developing a Python application that automates the extraction and processing of incident data from publicly available PDF reports issued by the Norman, Oklahoma Police Department. These reports are distributed in the form of PDFs and contain incident summaries, arrest records, and case information.

The primary objective is to streamline the collection, extraction, transformation, and storage of only the incident data into a structured format, suitable for analysis and reporting. By leveraging Python, SQL, regular expressions, and command-line tools, the data will be cleaned and inserted into a relational database for further querying and analysis.

The Incident Sumamry data can be accessed from Norman, Oklahoma police department activity reports [here](https://www.normanok.gov/public-safety/police-department/crime-prevention-data/department-activity-reports).

**Assignment Objective:**
The goal of this project is to develop a Python-based application that:
1) Downloads incident summary PDFs from the Norman, Oklahoma Police Department’s website.
2) Extracts relevant data fields from the PDF, including:
      - Date/Time
      - Incident Number
      - Location
      - Nature of the Incident
      - Incident ORI
3) Stores the extracted data into a structured format using an SQLite database.
4) Inserts the extracted data into the database.
5) Outputs the incident details in a structured format, along with a count of how many times each "nature" of the incident appears:

       Nature|Count(*)
   
**Requirements:**
1) Data Extraction: Use a Python script to download the incident summary PDF, extract relevant fields, and handle edge cases such as missing data or improperly formatted PDFs.
2) Database Creation: Design an SQLite database that will store the incident data. This database should include a table to capture the required fields.
3) Data Insertion: Once the data is extracted from the PDF, insert it into the SQLite database.
4) Data Reporting: Print a list of incidents, categorized by the nature of the incident, and display how many times each category appears.

# How to install
Install pipenv using the command: 

      pip install pipenv

Install urllib3 library using the command: 

      pipenv install urllib3

Install PyPdf library using the command: 

      pipenv install pypdf

Install pytest testing framework using the command: 

      pipenv install pytest 

## How to run
To execute the project, navigate to the project directory and run the following commands:

1) To output a page use command:

         pipenv run python project0/main.py --incidents <url>

   For instance (command used in my local):

         pipenv run python project0/main.py --incidents "https://www.normanok.gov/sites/default/files/documents/2024-08/2024-08-01_daily_incident_summary.pdf"

## Test Cases run
Running the following pipenv command runs the pytest cases. This project have 5 test cases.
command to run test cases: 

      pipenv run python -m pytest -v

![video](video)

## Functions
### main.py
**main(url)**

The main.py script is the main entry point for the incident data extraction and processing application. It accepts a URL to an incident summary PDF and performs the following actions:
**Functionality:**
1) Download Incident Data: Fetches the incident summary PDF from the specified URL.
2) Extract Incident Data: Extracts relevant fields such as date, incident number, location, nature, and incident ORI from the PDF.
3) Create and Populate SQLite Database: Creates a new SQLite database and stores the extracted data in the database.
4) Print Incident Report: Outputs a summary of incidents, grouped by their nature, and displays how many times each nature appears.

Arguments:

    --incidents (required): The URL of the incident summary PDF.

Code Breakdown:
1) Command-line Parsing: Uses argparse to handle command-line arguments, where the user must specify the URL of the incident summary PDF.

        parser = argparse.ArgumentParser()
        parser.add_argument("--incidents", type=str, required=True, help="Incident summary URL.")
        args = parser.parse_args()

2) Main Function: The **main(url)** function contains the execution of the script, performing the following steps:
    - Fetches the PDF using **project0.fetch_incidents**.
    - Extracts incident data from the PDF using **project0.extract_incidents**.
    - Creates a new SQLite database using **project0.createdb**.
    - Inserts the extracted data into the database using **project0.populatedb**.
    - Finally, prints the summary report of incidents using **project0.status**.

All the functions referenced in the **main()** function, such as **fetch_incidents, extract_incidents, createdb, populatedb, and status**, are defined in the **project0.py** module.

### project0.py
1) **fetch_incidents(url)**
    - Downloads an incident summary PDF from the provided URL and saves it to a temporary file.
    - Parameters:
        - url: The URL of the incident summary PDF.
    - Returns: The file path of the saved PDF in a temporary location.

   In this project, the incident summary PDF is downloaded and stored temporarily using Python’s built-in **tempfile** module. The reason for choosing this approach is:
    - Dynamic File Management: By using **tempfile.NamedTemporaryFile**, the file is stored in a temporary directory (often /tmp in Linux-based systems or a similar temp directory in other operating systems) that is managed by the operating system. This ensures that files are automatically cleaned up when no longer needed.
    - Automatic Cleanup: While the **delete=False** option is used to keep the file for further processing, it can be easily cleaned up programmatically after the data has been extracted.
    - Security and Safety: Storing the file in a temporary location ensures that sensitive data (like incident summaries) is not permanently stored in the file system, reducing the risk of leaving behind sensitive or personal information.
    - Next Step Readability: The function returns the path to the temporary file, allowing subsequent methods (such as extract_incidents()) to read the file directly without requiring any complex file path configurations or hardcoded paths. This ensures the file is always accessible to the next function in the process.

2) **extract_incidents(pdf_file_path)**
    - Extracts incident data from the provided PDF file that is stored as a temp file from the **fetch_incident()** function and structures it into a pandas DataFrame.
    - Parameters:
        - pdf_file_path (str): The file path to the PDF containing the incident data.
    - Returns:
        - pandas.DataFrame: A DataFrame containing the extracted incident data, with columns:
            - incident_time: The date and time of the incident.
            - incident_number: The unique number identifying the incident.
            - incident_location: The location where the incident occurred.
            - nature: The nature of the incident (e.g., Theft, Vandalism).
            - incident_ori: The ORI (Originating Agency Identifier) associated with the incident.
    - This function reads the PDF using a layout-based extraction method to preserve the structure of the data and splits the text into relevant fields using regular expressions.
    - Header information is extracted only from the first page, while subsequent pages are processed for incident details.
    - Incident data is validated to ensure that each row contains at least three valid fields, and any rows missing fields or values are filtered out.
    - The **extract_incidents()** function utilizes **PyPDF** library and its **PdfReader** module to read and extract text content from the incident summary PDFs. This allows for precise text extraction across multiple pages, maintaining the layout and structure of the PDF for accurate data parsing.

4) **createdb()**
    - Creates an SQLite database and returns the connection object.
    - The database will contain a table named `incidents` with the specified schema.
    - Returns:
        - sqlite3.Connection: A connection object to interact with the SQLite database.
    - Directory Creation: The function first ensures that a resources directory exists in the project root directory. If the directory is missing, it creates it dynamically.
    - Database Creation: It creates a new SQLite database file (normanpd.db) in the resources directory. If an existing database with the same name is present, it deletes the old file to ensure a fresh start.
    - Return Value: The function returns a connection object to interact with the database, allowing other parts of the application to insert and query data.
    - Automatic Directory Management: This function dynamically creates the resources directory if doesn’t exist, providing a clean and organized storage location for the database file.
    - Fresh Database: To avoid conflicts with existing data, any existing database is deleted at the start of the script’s execution, ensuring that the data is always fresh.

5) **populatedb(conn, incidents_df)**
    - Inserts incident data from a pandas DataFrame into the SQLite database.
    - Parameters:
        - conn: The SQLite database connection object.
        - incidents_df: A pandas DataFrame containing incident data to be inserted.
    - This function reads each row from the DataFrame (which contains the incident data) and inserts it into the incidents table in the database.
    - Transaction Safety: The function uses a transaction mechanism where changes are committed to the database only after all rows are inserted. In case of an error, the changes are rolled back to prevent partial or corrupt data insertion to ensure the database integrity.
        - This function uses **commit()** to ensure all data is saved after the full DataFrame is inserted. If an error occurs, **rollback()** is used to undo any incomplete changes, maintaining database consistency.
    - Cursor Management: The function uses a cursor to execute SQL queries and ensures it is properly closed after data insertion is completed. 
  
6) **status(conn)**

    - Prints a summary of the nature of incidents and the number of times each has occurred.
    - The list is sorted alphabetically by the nature of the incident.
    - Parameters
        - conn: The SQLite database connection object.
    - The status() function generates a report summarizing the incidents stored in the database. It retrieves the count of each type of incident (grouped by its nature) and prints the results in alphabetical order.
    - The results are printed to the console, showing the incident nature and its corresponding count, separated by a pipe (|).
  
## Example Usage to run commands:
- To process the incident summary from a specified URL, use the following command:

      pipenv run python project0/main.py --incidents "https://www.normanok.gov/sites/default/files/documents/2024-08/2024-08-01_daily_incident_summary.pdf"

### test_functions.py
1) **test_fetch_incidents()**

   - Tests the fetch_incidents() function to ensure it correctly downloads a PDF from a given URL.
   - Steps:
       - Provides a sample URL to a PDF file for testing.
       - Calls fetch_incidents() to download the PDF and returns the file path.
       - Verifies that the downloaded file exists at the specified path.
       - Cleans up by removing the temporary file after the test.
   - This test checks whether the PDF is properly fetched and saved.

2) **test_extract_incidents()**

   - Tests the extract_incidents() function to ensure it correctly extracts data from a PDF and returns a pandas DataFrame.
   - Steps:
       - Provides a sample URL to a PDF file for testing.
       - Calls fetch_incidents() to download the PDF and returns the file path.
       - Calls extract_incidents() to extract incident data from the downloaded PDF.
       - Verifies that the output is a valid pandas DataFrame.
       - Checks if the DataFrame contains the correct columns: 'incident_time', 'incident_number', 'incident_location', 'nature', and 'incident_ori'.
       - Ensures that the DataFrame is not empty (assuming the PDF contains data).
       - Cleans up by removing the temporary file after the test.
   - The test ensures that the incident data is correctly extracted from the PDF and structured in a DataFrame.

3) **test_createdb()**

   - Tests the createdb() function to ensure that:
       - A new SQLite database file is created in the 'resources' directory.
       - The 'incidents' table is correctly created in the database.
   - Steps:
       - Calls createdb() to create the database.
       - Verifies that the database file exists at the expected location.
       - Queries the 'sqlite_master' table to confirm the 'incidents' table is created.
       - Cleans up by closing the connection and removing the database file.

4) **test_populatedb()**

   - Tests the populatedb() function to ensure that:
       - A pandas DataFrame containing mock incident data is correctly inserted into the database.
       - The 'incidents' table is populated with the mock data, and the data is retrievable.
   - Steps:
       - Creates a mock DataFrame with test incident data.
       - Calls createdb() to create a test database.
       - Uses populatedb() to insert the mock data into the database.
       - Verifies that the data has been successfully inserted by querying the database.
       - Cleans up by closing the database connection and removing the test database file.

5) **test_status(capsys)**

   - Tests the status() function to ensure that the correct output is printed for the nature of incidents and their respective counts.
   - capsys is a fixture provided by pytest that captures stdout and stderr output during the test.
   - Steps:
       - Creates a mock DataFrame with incident data, where 'Nature A' and 'Nature B' occur once each.
       - Calls createdb() to create a test SQLite database.
       - Inserts the mock data into the database using populatedb().
       - Calls the status() function, which prints the nature of incidents and their counts.
       - Captures the printed output using capsys.readouterr().
       - Verifies that 'Nature A|1' and 'Nature B|1' are present in the output, ensuring the correct counts are printed.
       - Cleans up by closing the database connection and removing the test database file.
     - This test ensures that the status() function correctly prints the nature of incidents and their occurrence count.

## Database Development
This project uses an SQLite database to store and manage the incident data extracted from the incident summary PDFs. The following details outline how the database is created, structured, and used within the project.

**Database Creation:**
The SQLite database is created dynamically when the script is executed. It is stored in the resources directory of the project, and the database file is named normanpd.db. If an existing database with the same name is found, it is deleted and replaced with a fresh instance to avoid duplication and ensure clean data storage.

The database is created using the **createdb()** function, which defines the schema for storing incident data in a single table named incidents.

**Table Schema:**
The incidents table is structured with the following columns:
  - incident_time (TEXT): The date and time the incident occurred.
  - incident_number (TEXT): A unique identifier for the incident.
  - incident_location (TEXT): The location where the incident took place.
  - nature (TEXT): The nature or type of the incident (e.g., Theft, Vandalism).
  - incident_ori (TEXT): The ORI (Originating Agency Identifier) code representing the agency handling the incident.

Each row in this table represents a unique incident, and the table is designed to efficiently store and query incident records.

**Data Insertion:**
Data is inserted into the database using the **populatedb()** function, which reads rows from the pandas DataFrame (populated with incident data) and inserts them into the incidents table. For each row in the DataFrame, the relevant data fields are mapped to the appropriate columns in the table. The insertion process is handled within a transaction, ensuring that if an error occurs, any changes are rolled back to maintain the integrity of the database.

**Querying the Data:**
The **status()** function is used to query the database, retrieving and displaying a summary of the incident data. It executes a SQL query to group the incidents by their nature (ex: Alarm, Assault) and counts how many times each type of incident has occurred. The results are sorted alphabetically by the incident nature and printed to the console.

Query to get the count of each nature of incident:
            
    SELECT nature, COUNT(*) as count FROM incidents GROUP BY nature ORDER BY nature ASC;

**Transaction Management:**
To ensure data integrity, all operations with the database are handled within transactions. The script commits the transaction once all rows are successfully inserted into the database. If an error occurs during insertion, a rollback is performed to revert any partial changes, preventing corrupt or incomplete data from being stored.

**Cleanup and Maintenance:**
At the end of the script execution, temporary files (such as the downloaded PDF) are deleted, and the SQLite database remains for further querying or analysis. If the script is run again, the database will be re-created, overwriting the existing file to ensure no duplicate data is stored.

## Bugs and Assumptions
1) Assumption: The script assumes that all incident summary PDFs follow a consistent structure, including field headers, row spacing, and column formatting. Any deviation from this format may require modifications to the extraction logic.
2) Simple Incident Structures: It is assumed that the incident data in the PDF is expected to follow a simple, table-like structure. Complex incident descriptions spanning multiple lines or columns could result in data parsing errors or incorrect extractions.
3) Inconsistent PDF Formatting: If the structure of the PDF differs from the expected format (e.g., different column spacing, missing headers), the extraction process might fail or produce incorrect data.
4) PDF Layout Extraction Issues: The use of PyPDF's layout mode for text extraction may not perfectly capture complex layouts or images embedded within the PDF. This can cause misalignment in the extracted data fields.
5) Temporary File Cleanup: In case of a script failure or crash, the temporary files created for downloading PDFs may not be properly cleaned up, leaving residual files in the temp directory.