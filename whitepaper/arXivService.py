import requests

from whitepaper.model.white_paper_service import WhitePaperService


class ArXivService(WhitePaperService):
    def __init__(self, source: str):
        super().__init__(source)

    def get_white_paper(self, path: str, paper_id: str) -> Exception | bytes:
        url = f"{self.source}/{path}/{paper_id}"
        pdf_res = requests.get(url)
        if pdf_res.status_code == 200:
            print(f"Retrieved the PDF from {pdf_res.url}")
            return pdf_res.content
        else:
            return Exception(f"Failed to retrieve the PDF: {pdf_res.status_code}")
