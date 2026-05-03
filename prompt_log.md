# Prompt Log

AI tool used: ChatGPT

This file summarizes the AI assistance used while preparing the assessment solution.

## Prompt 1

I described the assessment task: fetch the latest SEC 10-K reports for Apple, Meta, Alphabet, Amazon, Netflix, and Goldman Sachs, convert them to PDF, and submit Python source code with run instructions and a prompt log.

Purpose: Get guidance on possible HTML-to-PDF conversion methods.

## Prompt 2

I shared an initial SEC metadata extraction solution using company CIK values, the SEC submissions JSON endpoint, pandas filtering, and SEC archive URL construction.

Purpose: Ask for alternatives to `pdfkit` because saving the SEC HTML pages as PDFs was problematic.

## Prompt 3

I chose Playwright and asked for a simple example for saving one report URL as a PDF.

Purpose: Learn the minimal Playwright code needed to open a URL and export a PDF.

## Prompt 4

I reported the error:

```text
Error: It looks like you are using Playwright Sync API inside the asyncio loop.
Please use the Async API instead.
```

Purpose: Understand why the synchronous Playwright API failed in an async environment and how to use the async Playwright API.

## Prompt 5

I asked to adjust the Playwright solution to use `headless=False` and close the browser after rendering the PDF.

Purpose: Match the manual workflow of opening the report in a visible browser, saving it as PDF, and closing the browser.

## Prompt 6

I shared my working code that fetched filing metadata from SEC and used Playwright to save each report as a PDF.

Purpose: Ask for submission guidance based on the assessment requirements.

## Prompt 7

I reported the script error:

```text
RuntimeError: asyncio.run() cannot be called from a running event loop
```

Purpose: Understand the difference between running async code in Jupyter/IPython and running it as a normal `.py` script.

## Prompt 8

I reported the script error:

```text
NameError: name 'main' is not defined
```

Purpose: Understand how to structure a Python script with `async def main()` and `asyncio.run(main())`.

## Prompt 9

I reported a runtime warning caused by calling an async function without `await`.

Purpose: Fix the call to `store_pdf(...)` by using `await store_pdf(...)` and replacing `time.sleep(...)` with `await asyncio.sleep(...)`.

## Prompt 10

I shared the final code and asked to generate `README.md`, `requirements.txt`, and `prompt_log.md`.

Purpose: Prepare the final GitHub submission files.
