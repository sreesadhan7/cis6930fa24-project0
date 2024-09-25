import os
import pytest
import pandas as pd
from project0.project0 import fetch_incidents, extract_incidents
import sqlite3
from project0.project0 import createdb, populatedb, status


"""
    Tests the fetch_incidents() function to ensure it correctly downloads a PDF from a given URL.

    Steps:
    1. Provides a sample URL to a PDF file for testing.
    2. Calls fetch_incidents() to download the PDF and returns the file path.
    3. Verifies that the downloaded file exists at the specified path.
    4. Cleans up by removing the temporary file after the test.

    The test checks whether the PDF is properly fetched and saved.
    """
def test_fetch_incidents():
    # Replace with a sample URL of a PDF for testing
    test_url = "https://www.normanok.gov/sites/default/files/documents/2024-08/2024-08-01_daily_incident_summary.pdf"
    
    # Fetch the PDF file
    pdf_path = fetch_incidents(test_url)
    
    # Check that the returned path is a valid file
    assert os.path.exists(pdf_path), "PDF file not downloaded properly."
    
    # Clean up the temporary file after testing
    os.remove(pdf_path)


"""
    Tests the extract_incidents() function to ensure it correctly extracts data from a PDF and returns a pandas DataFrame.

    Steps:
    1. Provides a sample URL to a PDF file for testing.
    2. Calls fetch_incidents() to download the PDF and returns the file path.
    3. Calls extract_incidents() to extract incident data from the downloaded PDF.
    4. Verifies that the output is a valid pandas DataFrame.
    5. Checks if the DataFrame contains the correct columns: 'incident_time', 'incident_number', 
       'incident_location', 'nature', and 'incident_ori'.
    6. Ensures that the DataFrame is not empty (assuming the PDF contains data).
    7. Cleans up by removing the temporary file after the test.

    The test ensures that the incident data is correctly extracted from the PDF and structured in a DataFrame.
    """
def test_extract_incidents():
    # Provide a sample URL to a PDF file (replace this with the actual URL)
    test_url = "https://www.normanok.gov/sites/default/files/documents/2024-08/2024-08-01_daily_incident_summary.pdf"
    
    # Fetch the PDF file
    pdf_path = fetch_incidents(test_url)
    
    # Extract the incidents from the fetched PDF
    incidents_df = extract_incidents(pdf_path)
    
    # Check if the result is a valid DataFrame
    assert isinstance(incidents_df, pd.DataFrame), "Output is not a DataFrame."
    
    # Check if the DataFrame has the correct columns
    expected_columns = ['incident_time', 'incident_number', 'incident_location', 'nature', 'incident_ori']
    assert list(incidents_df.columns) == expected_columns, "DataFrame columns do not match expected columns."
    
    # Ensure DataFrame is not empty (assuming the PDF contains data)
    assert not incidents_df.empty, "Extracted DataFrame is empty."
    
    # Clean up the temporary file after testing
    os.remove(pdf_path)


"""
    Tests the createdb() function to ensure that:

    1. A new SQLite database file is created in the 'resources' directory.
    2. The 'incidents' table is correctly created in the database.

    Steps:
    - Calls createdb() to create the database.
    - Verifies that the database file exists at the expected location.
    - Queries the 'sqlite_master' table to confirm the 'incidents' table is created.
    - Cleans up by closing the connection and removing the database file.
    """
def test_createdb():
    # Create a test database
    conn = createdb()
    
    # Ensure that the database file exists
    db_path = os.path.join(os.path.dirname(__file__), '..', 'resources', 'normanpd.db')
    assert os.path.exists(db_path), "Database file not created."
    
    # Check that the table exists
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='incidents';")
    result = cursor.fetchone()
    assert result is not None, "Table 'incidents' not created."
    
    # Clean up
    cursor.close()
    conn.close()
    os.remove(db_path)


"""
    Tests the populatedb() function to ensure that:

    1. A pandas DataFrame containing mock incident data is correctly inserted into the database.
    2. The 'incidents' table is populated with the mock data, and the data is retrievable.

    Steps:
    - Creates a mock DataFrame with test incident data.
    - Calls createdb() to create a test database.
    - Uses populatedb() to insert the mock data into the database.
    - Verifies that the data has been successfully inserted by querying the database.
    - Cleans up by closing the database connection and removing the test database file.
    """
def test_populatedb():
    # Create a test DataFrame with mock data
    data = {
        'incident_time': ['2021-01-01 10:00:00'],
        'incident_number': ['123456'],
        'incident_location': ['Location A'],
        'nature': ['Nature A'],
        'incident_ori': ['ORI123']
    }
    incidents_df = pd.DataFrame(data)
    
    # Create a test database
    conn = createdb()
    
    # Populate the database
    populatedb(conn, incidents_df)
    
    # Check if the data has been inserted
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM incidents WHERE incident_number = '123456';")
    result = cursor.fetchone()
    assert result is not None, "Data not inserted into the database."
    
    # Clean up
    cursor.close()
    conn.close()
    db_path = os.path.join(os.path.dirname(__file__), '..', 'resources', 'normanpd.db')
    os.remove(db_path)


"""
    Tests the status() function to ensure that the correct output is printed
    for the nature of incidents and their respective counts.

    Steps:
    1. Creates a mock DataFrame with incident data, where 'Nature A' and 'Nature B' occur once each.
    2. Calls createdb() to create a test SQLite database.
    3. Inserts the mock data into the database using populatedb().
    4. Calls the status() function, which prints the nature of incidents and their counts.
    5. Captures the printed output using capsys.readouterr().
    6. Verifies that 'Nature A|1' and 'Nature B|1' are present in the output, ensuring the correct counts are printed.
    7. Cleans up by closing the database connection and removing the test database file.

    The test ensures that the status() function correctly prints the nature of incidents and their occurrence count.
    """
def test_status(capsys):
    # Create a test DataFrame with mock data
    data = {
        'incident_time': ['2021-01-01 10:00:00', '2021-01-02 12:00:00'],
        'incident_number': ['123456', '654321'],
        'incident_location': ['Location A', 'Location B'],
        'nature': ['Nature A', 'Nature B'],
        'incident_ori': ['ORI123', 'ORI321']
    }
    incidents_df = pd.DataFrame(data)
    
    # Create a test database
    conn = createdb()
    
    # Populate the database
    populatedb(conn, incidents_df)
    
    # Call the status function and capture the output
    status(conn)
    
    # Capture the output of the print statement
    captured = capsys.readouterr()
    
    # Ensure the correct output is printed
    assert "Nature A|1" in captured.out, "Nature A count incorrect."
    assert "Nature B|1" in captured.out, "Nature B count incorrect."
    
    # Clean up
    conn.close()
    db_path = os.path.join(os.path.dirname(__file__), '..', 'resources', 'normanpd.db')
    os.remove(db_path)