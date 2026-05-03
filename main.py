# imports
import asyncio
import pandas as pd
import requests
from playwright.async_api import async_playwright
from pathlib import Path



async def main() -> None:

    async def store_pdf(url:str, company:str, date:str, report_type:str='10-K'):
        """
        The function saves a report as PDF in the same view as a user would open it in the browser, with images in charts.
        For that, the actual browser breefly opens and closes, thus headless=False.

        Args:
        url (str):      Full URL of the financial report (e.g., a 10-K file).
        company (str):  Name of the company to reflect in the file's name.
        date (str):     Date of the report to reflect in the file's name.
        type (str, default 10-K):     Type of the report to reflect in the file's name.
        """
        async with async_playwright() as p:
                # To save the report "as is", with images in charts, we need to pop-up the actual browser,
                # thus headless=False. Otherwise, we cannot use url directly,
                # and would have to go with response.text solution keeping textual data only:

            browser = await p.chromium.launch(headless=False)  

            try:    
                context = await browser.new_context()
                page = await context.new_page()
                
                # Navigate to the target SEC URL and wait until the network is idle
                await page.goto(url, wait_until="networkidle")
                
                # Wait a short duration to ensure that dynamic charts and images are fully rendered
                await page.wait_for_timeout(500)
                
                # Export the page content to a PDF file and close the browser
                await page.pdf(path=f'output/{company}_{report_type}_{date}.pdf', format="A4", print_background=True)
            finally:
                await browser.close()   
        print(f'10-K report for {company} is saved.')    


    # creating dictionary Company-CIK for addressing SEC API.
    # CIKs are taken from https://www.sec.gov/search-filings manually since we have only 6 companies.
    # Another option would be to convert companies' names into tickers,
    # and then extract CIKs from https://www.sec.gov/files/company_tickers.json.
    # I prefer manual extraction because of companies like Goldman Sachs, where you have many entities with very similar names.

    companies_cik_dict = {
        'Apple': '0000320193',
        'Meta': '0001326801',
        'Alphabet': '0001652044',
        'Amazon': '0001018724',
        'Netflix': '0001065280',
        'Goldman Sachs': '0000886982'
        }


    # defining request headers as per SEC regulation on addressing API:
    headers = {'User-Agent': 'Dmitrii Medvedev dmedvedev09@gmail.com'}

    # creating the output folder for the reports:
    Path("output").mkdir(parents=True, exist_ok=True)


    # 10-K reports can be accessed via the link of the form
    # https://www.sec.gov/Archives/edgar/data/{cik}/{accessionNumber}/{primaryDocument}

    # CIK numbers are known, while Accession Numbers and Primary Ducoment's URLs,
    # as well as the dates of the latest submitted reports, are available
    # in the companies filing histories.

    # Browsing initially through the downloaded json-files it was defined, that
    # the data we are looking for is stored in subdictionaries ['filings']['recent'].


    # cycling through the dictionary companies_cik_dict to extract CIK for each company,
    # sending corresponding request to SEC API,

    for company in companies_cik_dict:
        cik = companies_cik_dict[company]
        filing_history = requests.get(f'https://data.sec.gov/submissions/CIK{cik}.json',
                                headers=headers)

        # converting the dictionary of interest into a table form and filtering out 10-K reports:   
        df_filings_recent = pd.DataFrame(filing_history.json()['filings']['recent'])
        df_10K = df_filings_recent.loc[df_filings_recent['form'] == '10-K']
        
        # Sorting the table by reporting date to extract the latest report from the top row:  
        df_10K = df_10K.sort_values(by="reportDate", ascending=False)
        latest_10K = df_10K.iloc[0]

        # Accession Number contains hyphens "-" which are to be removed for our purposes:
        accessionNumber = latest_10K['accessionNumber'].replace("-", "")
        primaryDocument = latest_10K["primaryDocument"]
        date = str((latest_10K["reportDate"])).replace("-", "")

        url_10k = f'https://www.sec.gov/Archives/edgar/data/{cik}/{accessionNumber}/{primaryDocument}'
    
        
        # Storing reports as PDFs:
        await store_pdf(url=url_10k, company=company, date=date)
            
        # adding time-delay between requests to account for SEC max request rate: 10 req/s.
        await asyncio.sleep(0.2)


if __name__ == "__main__":

    asyncio.run(main())