import requests
import xml.etree.ElementTree as ET
import pandas as pd
import os
import time

# Base URL for the TSDR API
BASE_URL = "https://tsdrapi.uspto.gov"

# Replace with your actual TSDR API key
API_KEY = "YOUR_API_KEY"

# Updated headers with User-Agent added
HEADERS = {
    "USPTO-API-KEY": API_KEY,
    "Accept": "application/xml",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"
}

# Define the namespaces as used in the XML sample
NAMESPACES = {
    'ns1': 'http://www.wipo.int/standards/XMLSchema/ST96/Common',
    'ns2': 'http://www.wipo.int/standards/XMLSchema/ST96/Trademark',
    'ns3': 'urn:us:gov:doc:uspto:trademark'
}

def get_case_status(case_id):
    """
    Retrieve case status information for a given case_id.
    This function parses the XML response and extracts key details.
    """
    url = f"{BASE_URL}/ts/cd/casestatus/{case_id}/info"
    print(f"Requesting URL: {url}")
    response = requests.get(url, headers=HEADERS)
    
    # Rate limit handling example
    if response.status_code == 429:
        retry_after = int(response.headers.get("Retry-After", "15"))
        print(f"Rate limit hit. Waiting {retry_after} seconds...")
        time.sleep(retry_after)
        response = requests.get(url, headers=HEADERS)
    
    if response.status_code != 200:
        print(f"Error fetching status for case {case_id}: {response.status_code}")
        print("Response content:", response.text)
        return None

    try:
        root = ET.fromstring(response.content)
        
        # Extract fields using the defined namespaces and element paths
        application_number = root.findtext(".//ns1:ApplicationNumberText", namespaces=NAMESPACES)
        application_date = root.findtext(".//ns2:ApplicationDate", namespaces=NAMESPACES)
        filing_place = root.findtext(".//ns1:FilingPlace", namespaces=NAMESPACES)
        status_code = root.findtext(".//ns2:MarkCurrentStatusCode", namespaces=NAMESPACES)
        status_date = root.findtext(".//ns2:MarkCurrentStatusDate", namespaces=NAMESPACES)
        mark_verbal_element = root.findtext(".//ns2:MarkVerbalElementText", namespaces=NAMESPACES)
        image_file_name = root.findtext(".//ns2:MarkImage/ns1:FileName", namespaces=NAMESPACES)
        applicant_name = root.findtext(".//ns2:ApplicantBag/ns2:Applicant/ns1:Contact/ns1:Name/ns1:PersonName/ns1:PersonFullName", namespaces=NAMESPACES)
        status_description = root.findtext(".//ns2:NationalTrademarkInformation/ns2:MarkCurrentStatusExternalDescriptionText", namespaces=NAMESPACES)
        
        return {
            "case_id": case_id,
            "application_number": application_number,
            "application_date": application_date,
            "filing_place": filing_place,
            "status_code": status_code,
            "status_date": status_date,
            "mark_verbal_element": mark_verbal_element,
            "image_file_name": image_file_name,
            "applicant_name": applicant_name,
            "status_description": status_description
        }
    except ET.ParseError as e:
        print(f"XML parsing error for case {case_id}: {e}")
        return None

def download_case_document(case_id):
    """
    Download a document for a given case using the download endpoint.
    Saves the file as {case_id}_document.pdf.
    """
    url = f"{BASE_URL}/ts/cd/casedocs/{case_id}/download.pdf"
    print(f"Downloading document from: {url}")
    response = requests.get(url, headers=HEADERS)
    
    # Rate limit handling for bulk download (if needed)
    if response.status_code == 429:
        retry_after = int(response.headers.get("Retry-After", "15"))
        print(f"Rate limit hit on document download. Waiting {retry_after} seconds...")
        time.sleep(retry_after)
        response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        print(f"Error downloading document for case {case_id}: {response.status_code}")
        print("Response content:", response.text)
        return None

    filename = f"{case_id}_document.pdf"
    with open(filename, "wb") as f:
        f.write(response.content)
    print(f"Downloaded document for case {case_id} as {filename}")
    return filename

def main():
    # Minimal CLI UI for case ID input
    case_id = input("Please enter a case ID (e.g., 97890330): ").strip()
    if not case_id:
        print("No case ID entered. Exiting.")
        return

    summary_data = []
    status_data = get_case_status(case_id)
    if not status_data:
        print("Failed to retrieve case data.")
        return
    
    # Optionally download the associated document
    doc_filename = download_case_document(case_id)
    status_data["document_filename"] = doc_filename if doc_filename else "Download Error"
    summary_data.append(status_data)
    
    # Export summary data to an Excel file if data is available
    if summary_data:
        df = pd.DataFrame(summary_data)
        excel_filename = "case_summary.xlsx"
        df.to_excel(excel_filename, index=False)
        print(f"Case summary written to {excel_filename}")
    else:
        print("No case data available to write.")

if __name__ == "__main__":
    main()
