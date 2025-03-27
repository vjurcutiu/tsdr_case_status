# USPTO TSDR API Case Status and Document Retrieval

This Python script demonstrates a proof-of-concept (PoC) for interacting with the USPTO TSDR API. The script performs the following functions:

- Prompts the user via a command-line interface (CLI) to input a case ID.
- Fetches case status information from the USPTO TSDR API.
- Downloads an associated PDF document for the case.
- Extracts key information from the XML response.
- Exports the collected data into an Excel spreadsheet.

## Prerequisites

- Python 3.6 or higher  
- An active USPTO TSDR API key. (Register via your USPTO.gov account and follow the instructions provided in the API documentation).

## Installation

1. **Clone the Repository or Download the Script**

  You can either clone this repository or directly download the script file (e.g., `tsdr_case_status.py`).

2. **Set Up a Virtual Environment (Optional but Recommended)**

  ```bash
  python3 -m venv venv 
  ```
  ```bash
  source venv/bin/activate # On Windows, use: venv\Scripts\activate
  ```

3. **Install Required Dependencies**

  The script uses the following Python libraries:

  - `requests` (for making HTTP requests)  
  - `pandas` (for data manipulation and Excel export) 
  - `openpyxl` (for Excel file creation)  
  - `xml.etree.ElementTree` (standard library, no installation required)

  Install the required dependencies with pip:

  ```bash  
  pip install requests pandas openpyxl  
  ```

## Configuration

1. **API Key**

  Open the script file (`tsdr_case_status.py`) and replace the placeholder (`"YOUR_API_KEY"`) with your actual USPTO TSDR API key:

  ```python  
  API_KEY = "YOUR_API_KEY"  
  ```

2. **Running the Script**

To run the script from the command line:

```bash  
python tsdr_case_status.py  
```

You will be prompted to enter a case ID. For example:

```  
Please enter a case ID (e.g., 97890330): 97890330  
```

The script will then:

- Fetch the case status information.  
- Download the associated PDF document.  
- Export the retrieved information to an Excel file named `case_summary.xlsx`.

## Troubleshooting

- **404 or 401 Errors:**  
  Ensure that the case ID is entered in the correct format and that your API key is valid. 
