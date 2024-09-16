import os
import urllib.parse
import requests

from pypdf import PdfReader, PageObject
from loguru import logger

from .config import TRANSLATE_URL


Page = list[dict[str, str]]
Summary = dict[str, list[Page]]


def translate(line: str) -> Page:
    request = urllib.parse.quote_plus(line)
    response = requests.get(f"{TRANSLATE_URL}{request}")

    if response.status_code != 200:
        logger.error("got an issue translating line")

    response_json = response.json()

    if len(response_json) == 0:
        logger.error("no data in translated response")

    translation: list[dict[str, str]] = []
    for res_lines in response_json[0]:
        translation.append({
            "english": res_lines[0].strip(),
            "polish": res_lines[1].strip()
        })

    return translation


def get_pdf_pages(file_path: str) -> list[PageObject]:
    reader = PdfReader(file_path)
    return reader.pages


def read_pdf(file_path: str) -> list[Page]:
    pages: list[list[dict[str,str]]] = []
    pdf_pages = get_pdf_pages(file_path)
    total_pages = len(pdf_pages)

    for i, page in enumerate(pdf_pages):
        logger.info(f"  page {i}/{total_pages}")
        lines = page.extract_text().split("\n")
        lines_filtered = [line for line in lines if not line.isspace()]
        pages.append(translate("\n".join(lines_filtered)))

    return pages


def generate_summary() -> Summary:
    documents: Summary = {}
    all_pdfs = [file for file in os.listdir() if file.endswith(".pdf")]
    for document in all_pdfs:
        logger.info(f"processing document: '{document}'...")
        documents[document] = read_pdf(document)

    return documents

