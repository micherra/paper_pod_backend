import bibtexparser
import requests

from bs4 import BeautifulSoup

from whitepaper.model.white_paper_service import WhitePaperService


class ArXivService(WhitePaperService):
    def __init__(self, source: str):
        super().__init__(source)
        self.PDF_PATH = "/pdf/"
        self.SOURCE = (
            "/src/"  # Could be used to retrieve images and figures in the future
        )
        self.BIBTEX = "/bibtex/"
        self.ABSTRACT = "/abs/"

    def get_white_paper(self, paper_id: str) -> Exception | bytes:
        url = f"{self.source}{self.PDF_PATH}{paper_id}"
        try:
            pdf_res = requests.get(url)
            pdf_res.raise_for_status()
            print(f"Retrieved the PDF from {pdf_res.url}")
            return pdf_res.content
        except requests.exceptions.RequestException as e:
            return Exception(f"Failed to retrieve the PDF: {e}")

    def get_metadata(self, paper_id: str) -> Exception | dict:
        try:
            abstract_res = requests.get(f"{self.source}{self.ABSTRACT}{paper_id}")
            abstract_res.raise_for_status()
            print("Retrieved the metadata.")
            abstract = self.parse_html(abstract_res.text)
        except requests.exceptions.RequestException as e:
            return Exception(f"Failed to retrieve the metadata: {e}")

        try:
            bibtex_res = requests.get(f"{self.source}{self.BIBTEX}{paper_id}")
            bibtex_res.raise_for_status()
            print("Retrieved the BibTeX.")
            bibtex = self.parse_bibtex(bibtex_res.text)
        except requests.exceptions.RequestException as e:
            return Exception(f"Failed to retrieve the BibTeX: {e}")

        return bibtex | {"abstract": abstract}

    @staticmethod
    def parse_html(html: str) -> str:
        soup = BeautifulSoup(html, "html.parser")
        abstract_block = soup.select_one('blockquote[class*="abstract"]')
        if abstract_block is None:
            return "No abstract available."
        else:
            text = abstract_block.get_text(strip=True)
            if text.startswith("Abstract:"):
                text = text[len("Abstract:") :].strip()
            return text

    @staticmethod
    def parse_bibtex(bibtex: str) -> dict:
        bib_database = bibtexparser.loads(bibtex)
        entry = bib_database.entries[0]
        return {
            "title": entry.get("title", ""),
            "authors": entry.get("author", "").split(" and "),
        }
