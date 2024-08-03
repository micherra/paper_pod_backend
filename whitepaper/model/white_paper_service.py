from abc import ABC


class WhitePaperService(ABC):
    def __init__(self, source: str):
        self.source = source

    def get_white_paper(self, paper_id: str):
        pass

    def get_metadata(self, paper_id: str):
        pass
