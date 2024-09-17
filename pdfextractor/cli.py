from argparse import ArgumentParser
import os


class Config:
    def __init__(self, dest: str, documents: list[str]):
        self.dest = dest
        self.documents = documents


def cli_args_parse() -> Config:
    parser = ArgumentParser(
        prog = "pdfextractor",
        description = "Extract polish text from pdf and produce a bilingual summary"
    )

    parser.add_argument(
        "-s",
        "--source",
        type = str,
        nargs = "?",
        default = ".",
        help = "source pdf to read"
    )

    parser.add_argument(
        "files",
        type = str,
        nargs = "*",
        help = "pdf files to process"
    )

    parser.add_argument(
        "-d",
        "--dest",
        type = str,
        nargs = "?",
        default = ".",
        help = "destination directory for generated summary"
    )

    args = parser.parse_args()

    files = []
    if len(args.files) == 0:
        files = [file for file in os.listdir(args.source) if file.endswith(".pdf")]
    else: 
        files = args.files

    return Config(args.dest, files)

