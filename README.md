# Pdfextractor

It will read pdfs in Polish from `references` directory and output a line-by-line 
translation to english in json to the `data` directory.

Example output

```json
{
    "name_of_pdf.json": [
        [
            {
                "english": "Polish as a Foreign Language",
                "polish": "Języka Polskiego jako Obcego"
            },
        ],
        [
            {
                "english": "Second page",
                "polish": "Druga strona"
            },
        ]

    ]
}
```

