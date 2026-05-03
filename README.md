# SEC 10-K PDF Fetcher

This project fetches the latest annual 10-K reports for a predefined list of companies from the SEC EDGAR system and saves each report as a PDF.

## Companies covered

- Apple
- Meta
- Alphabet
- Amazon
- Netflix
- Goldman Sachs

## Approach

The script uses manually selected CIK values for the 6 target companies taken from https://www.sec.gov/search-filings. Since the assignment scope is limited to 6 known companies, manual CIK selection keeps the solution simple and avoids ambiguity for companies with multiple similarly named entities (e.g. Goldman Sachs).



For each company, the script:

1. Requests the company's SEC submissions JSON file from `data.sec.gov`.
2. Converts the recent filings metadata into a pandas DataFrame.
3. Filters the filings to form `10-K`.
4. Sorts the 10-K filings by `reportDate` and selects the latest one.
5. Builds the SEC filing URL using:
   - CIK
   - accession number
   - primary document name
6. Opens the report URL in Chromium using Playwright.
7. Saves the rendered page as a PDF in the `output/` directory.
8. Waits between companies to avoid excessive request rates (SEC max request rate: 10 req/s).

## Project structure

```text
.
├── main.py
├── README.md
├── requirements.txt
├── prompt_log.md
└── output/
```

The `output/` directory is created automatically by the script if it does not already exist.

## Requirements

- Python 3.10 or newer recommended
- Chromium installed through Playwright

Python dependencies are listed in `requirements.txt`.

## Setup

Create and activate a virtual environment.

### macOS / Linux

```bash
python -m venv .venv
source .venv/bin/activate
```

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Install the Chromium browser used by Playwright:

```bash
playwright install chromium
```

## Run

From the project root, run:

```bash
python main.py
```

The generated PDF files will be saved in:

```text
output/
```

Example output filenames:

```text
output/Apple_10-K_20240928.pdf
output/Meta_10-K_20241231.pdf
output/Goldman Sachs_10-K_20241231.pdf
```

The exact report dates depend on the latest filings available from SEC at runtime.

## Notes on SEC access

The script declares a `User-Agent` header when calling the SEC submissions endpoint. It also includes a delay between companies to avoid sending requests too aggressively.

The SEC documentation states that `data.sec.gov` provides JSON-formatted data APIs for EDGAR data, including submissions history by filer. SEC developer guidance also asks automated users to use efficient scripting and moderate request rates.

Useful SEC references:

- EDGAR Application Programming Interfaces: https://www.sec.gov/search-filings/edgar-application-programming-interfaces
- SEC Developer Resources and Fair Access guidance: https://www.sec.gov/about/developer-resources
- Accessing EDGAR Data: https://www.sec.gov/search-filings/edgar-search-assistance/accessing-edgar-data

## Design decisions

### Manual CIK mapping

The company list is fixed and small, so the script uses a hardcoded company-to-CIK dictionary. This avoids possible name-matching ambiguity, especially for companies such as Goldman Sachs where multiple SEC entities can exist.

### Playwright for PDF generation

The script uses Playwright with Chromium to render each SEC filing page and export it as a PDF. This approach is close to manually opening the filing in a browser and printing it to PDF.

### Visible browser mode

The script launches Chromium with `headless=False`. This was chosen because it matches the manual browser workflow used during development and successfully renders the SEC report pages before saving them as PDFs.

## AI usage

AI assistance was used during development for:

- Comparing HTML-to-PDF conversion options
- Debugging Playwright usage
- Understanding `asyncio` behavior in scripts versus notebooks
- Preparing repository documentation

See `prompt_log.md` for details.
