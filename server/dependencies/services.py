from server.services.whitepaper.arXiv import ArXivService


def get_arxiv_service() -> ArXivService:
    return ArXivService()
