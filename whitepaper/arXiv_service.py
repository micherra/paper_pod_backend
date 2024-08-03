import re
from typing import List

import requests

from bs4 import BeautifulSoup
from requests import Response

from whitepaper.model.arXiv_category import ArXivCategory
from whitepaper.model.arXiv_metadata import ArXivMetadata
from whitepaper.model.white_paper_service import WhitePaperService


class ArXivService(WhitePaperService):
    def __init__(self):
        super().__init__()
        self.arXiv_search_url = "https://export.arxiv.org/api/query"
        self.arXiv_org = "https://arxiv.org"
        self.PDF_PATH = "/pdf/"

    def get_white_paper(self, paper_id: str) -> bytes:
        url = f"{self.arXiv_org}{self.PDF_PATH}{paper_id}"
        try:
            pdf_res = requests.get(url)
            pdf_res.raise_for_status()
            print(f"Retrieved the PDF from {pdf_res.url}")
            return pdf_res.content
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to retrieve the PDF: {e}")

    def get_metadata(self, paper_id: str) -> List[ArXivMetadata]:
        metadata_res = self.query(f"id_list={paper_id}")
        return self.parse_metadata_xml(metadata_res.text)

    def categories(self) -> List[ArXivCategory]:
        url = f"{self.arXiv_org}/category_taxonomy"
        try:
            res = requests.get(url)
            res.raise_for_status()
            print("Retrieved the categories.")
            return self.parse_categories_html(res.text)
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to retrieve the categories: {e}")

    def search(self, query: str) -> List[ArXivMetadata]:
        search_res = self.query(query)
        return self.parse_metadata_xml(search_res.text)

    def query(self, query: str) -> Response:
        url = f"{self.arXiv_search_url}?{query}"
        print(url)
        try:
            res = requests.get(url)
            res.raise_for_status()
            print(f"Retrieved search results for '{query}'.")
            return res
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to retrieve search results: {e}")

    @staticmethod
    def parse_metadata_xml(xml: str) -> List[ArXivMetadata]:
        soup = BeautifulSoup(str(xml), "xml")
        entries = soup.find_all("entry")
        metadata: List[ArXivMetadata] = []

        for entry in entries:
            processed_entry = ArXivMetadata(
                title=entry.find("title").text.strip().replace("\n", ""),
                id=entry.find("id").text.strip().split("/")[-1],
                released=entry.find("published").text.strip(),
                abstract=entry.find("summary").text.strip().replace("\n", " "),
                authors=[
                    author.find("name").text.strip()
                    for author in entry.find_all("author")
                ],
                primary_category=entry.find("arxiv:primary_category")["term"],
            )
            metadata.append(processed_entry)

        return metadata

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
