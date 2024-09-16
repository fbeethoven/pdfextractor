import json
from datetime import datetime

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfgen.canvas import Canvas, PDFTextObject
from loguru import logger

from .config import FONT_DIR
from .extract import generate_summary, Page, Summary


def main():
    summary: Summary = generate_summary() 

    if len(summary) == 0:
        logger.info("There are no pdf files to generate")

    for file_name, pages in summary.items():
        logger.info(f"generating summary for file: {file_name}")
        create_pdf("summary_" + file_name, pages)


def draw_column(c: Canvas, width: int, writer: PDFTextObject, line: str):
    words = line.split()
    for word in words:
        if writer.getX() + c.stringWidth(word + " ") > width:
            writer.textLine()
        writer.textOut(word + " ")


def create_pdf(file_name: str, pages: list[Page]):
    c = canvas.Canvas(file_name, pagesize=letter)
    width, height = letter

    pdfmetrics.registerFont(TTFont(
        "Roboto",
        f"{FONT_DIR}/Roboto-Regular.ttf"
    ))

    pdfmetrics.registerFont(TTFont(
        "Roboto-Bold",
        f"{FONT_DIR}/Roboto-Bold.ttf"
    ))

    column_width = int(width / 2)

    for i, page in enumerate(pages):
        c.setFont("Roboto-Bold", 16)
        c.drawString(50, height - 50, f"{file_name}  page {i}/{len(pages)}")
        y_position = int(height - 100)

        text_a = c.beginText(50, y_position)
        text_b = c.beginText(column_width + 50, y_position)

        text_a.setFont("Roboto", 12)
        text_b.setFont("Roboto", 12)

        for line in page:
            draw_column(c, column_width, text_a, line["polish"])
            draw_column(c, 2 * column_width - 50, text_b, line["english"])

            text_a.textLine()
            text_a.textLine()
            text_b.textLine()
            text_b.textLine()

            y_value = max(text_a.getY(), text_b.getY())

            if y_value < 0.25 * height:
                c.drawText(text_a)
                c.drawText(text_b)
                c.showPage()
                text_a = c.beginText(50, y_position)
                text_b = c.beginText(column_width + 50, y_position)

                text_a.setFont("Roboto", 12)
                text_b.setFont("Roboto", 12)

        c.drawText(text_a)
        c.drawText(text_b)
        c.showPage()

    c.save()

