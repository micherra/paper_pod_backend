import re
from typing import List

import bibtexparser
import requests

from bs4 import BeautifulSoup

from whitepaper.model.arXiv_bibtex import ArXivBibtex
from whitepaper.model.arXiv_category import ArXivCategory
from whitepaper.model.arXiv_metadata import ArXivMetadata
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

    def get_metadata(self, paper_id: str) -> Exception | ArXivMetadata:
        try:
            abstract_res = requests.get(f"{self.source}{self.ABSTRACT}{paper_id}")
            abstract_res.raise_for_status()
            print("Retrieved the metadata.")
            abstract = self.parse_abstract_html(abstract_res.text)
        except requests.exceptions.RequestException as e:
            return Exception(f"Failed to retrieve the metadata: {e}")

        try:
            bibtex_res = requests.get(f"{self.source}{self.BIBTEX}{paper_id}")
            bibtex_res.raise_for_status()
            print("Retrieved the BibTeX.")
            bibtex = self.parse_bibtex(bibtex_res.text)
        except requests.exceptions.RequestException as e:
            return Exception(f"Failed to retrieve the BibTeX: {e}")

        return ArXivMetadata(**bibtex, abstract=abstract)

    def categories(self) -> Exception | list[ArXivCategory]:
        url = f"{self.source}/category_taxonomy"
        try:
            res = requests.get(url)
            res.raise_for_status()
            print("Retrieved the categories.")
            return self.parse_categories_html(res.text)
        except requests.exceptions.RequestException as e:
            return Exception(f"Failed to retrieve the categories: {e}")

    @staticmethod
    def parse_abstract_html(html: str) -> str:
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
    def parse_bibtex(bibtex: str) -> ArXivBibtex:
        bib_database = bibtexparser.loads(bibtex)
        entry = bib_database.entries[0]
        return ArXivBibtex(
            title=entry.get("title", ""), authors=entry.get("author", "").split(" and ")
        )

    @staticmethod
    def parse_categories_html(html: str) -> List[ArXivCategory]:
        categories: List[ArXivCategory] = []
        soup = BeautifulSoup(html, "html.parser")
        category_taxonomy_list = soup.find_all("div", id="category_taxonomy_list")

        for category in category_taxonomy_list:
            for group_name_element in category.find_all("h2", class_="accordion-head"):
                category_name = group_name_element.text.strip()
                accordion_body = group_name_element.find_next_sibling(
                    "div", class_="accordion-body"
                )

                if accordion_body:
                    topics = accordion_body.find_all("h4")
                    for topic in topics:
                        parsed_topic = re.match(r"(.+?)\s*\((.+?)\)", topic.text)
                        if parsed_topic:
                            topic_id = parsed_topic.group(1).strip()
                            topic_name = parsed_topic.group(2).strip()
                            description = re.sub(
                                r"\s+", " ", topic.find_next("p").text
                            ).strip()
                            categories.append(
                                ArXivCategory(
                                    id=topic_id,
                                    name=topic_name,
                                    category=category_name,
                                    description=description,
                                )
                            )
        return categories
