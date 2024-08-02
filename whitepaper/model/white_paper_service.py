from abc import ABC


class WhitePaperService(ABC):
    def __init__(self, source: str):
        self.source = source

    def get_white_paper(self, path: str, paper_id: str):
        pass
