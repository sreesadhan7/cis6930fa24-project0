import argparse
import project0

def main(url):
    # Download data
    print("Testing download...")
    incident_data = project0.fetch_incidents(url)
    
    if incident_data:
        print(f"Download successful! File saved at {incident_data}")
    else:
        print("Download failed!")

    # Extract data
    print("Testing extraction...")
    incidents = project0.extract_incidents(incident_data)
   
    if incidents:
        print(f"Extraction successful! Extracted {len(incidents)} incidents.")
        # Print each incident's details
        for incident in incidents:
            print(incident)
    else:
        print("Extraction failed!")
	
    # Create new database
    db = project0.createdb()
	
    # Insert data
    project0.populatedb(db, incidents)
	
    # Print incident counts
    project0.status(db)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--incidents", type=str, required=True, help="Incident summary url.")
     
    args = parser.parse_args()
    if args.incidents:
        main(args.incidents)