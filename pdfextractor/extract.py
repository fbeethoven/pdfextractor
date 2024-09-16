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
        logger.error("could not translate line")

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
    lines: list[PageObject] = []
    try:
        reader = PdfReader(file_path)
        lines = reader.pages
    except Exception as e:
        logger.error(f"could not read pdf {e}")
    return lines


def read_pdf(file_path: str) -> list[Page]:
    pages: list[list[dict[str,str]]] = []
    pdf_pages = get_pdf_pages(file_path)
    total_pages = len(pdf_pages)

    for i, page in enumerate(pdf_pages):
        logger.debug(f"  page {i}/{total_pages}")
        lines = page.extract_text().split("\n")
        lines_filtered = "\n".join([line for line in lines if not line.isspace()])
        if len("\n".join(lines_filtered)) == 0:
            continue
        pages.append(translate(lines_filtered))

    return pages


def generate_summary() -> Summary:
    documents: Summary = {}

    all_pdfs = [file for file in os.listdir() if file.endswith(".pdf")]
    for document in all_pdfs:
        logger.info(f"processing document: '{document}'...")
        document_text = read_pdf(document)

        if len(document_text) == 0:
            continue
        documents[document] = document_text

    return documents

