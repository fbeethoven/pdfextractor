from unittest.mock import patch, Mock

from pdfextractor.extract import read_pdf 


@patch("pdfextractor.extract.get_pdf_pages")
@patch("pdfextractor.extract.translate")
def test_read_pdf(mock_translate, mock_pages):
    mock_pdf_file = "mock_file_path.pdf"
    pdf_input = "jeden\n \ndwa"
    expected_output = "jeden\ndwa"

    page_1 = Mock()
    page_1.extract_text.return_value = pdf_input

    page_2 = Mock()
    page_2.extract_text.return_value = pdf_input

    mock_pages.return_value = [page_1, page_2]

    read_pdf(mock_pdf_file)

    mock_pages.assert_called_once_with(mock_pdf_file)
    page_1.extract_text.assert_called_once()
    page_2.extract_text.assert_called_once()

    mock_translate.assert_called_with(expected_output)
    mock_translate.assert_called_with(expected_output)

