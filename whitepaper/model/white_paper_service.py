from abc import ABC


class WhitePaperService(ABC):
    def get_white_paper(self, paper_id: str):
        pass

    def get_metadata(self, paper_id: str):
        pass

    def categories(self):
        pass

    def search(self, query: str):
        pass
