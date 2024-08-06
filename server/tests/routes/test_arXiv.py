import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from server.routers.arXiv import arXiv_router
from server.dependencies.services import get_arxiv_service
from server.routers.models.arXiv_search import ArXivSearch
from server.tests.constants.category import PARSED_CATEGORY
from server.tests.constants.metadata import PARSED_METADATA


class MockArXivService:
    def get_white_paper(self, paper_id: str):
        return b"%PDF-1.4..."

    def get_metadata(self, paper_id: str):
        return PARSED_METADATA[0]

    def categories(self):
        return PARSED_CATEGORY

    def search(self, query: ArXivSearch):
        return PARSED_METADATA


@pytest.fixture
def client():
    app = FastAPI()

    # Override the ArXivService dependency
    app.dependency_overrides[get_arxiv_service] = lambda: MockArXivService()

    app.include_router(arXiv_router)

    yield TestClient(app)

    # Cleanup: Reset dependency overrides after tests
    app.dependency_overrides = {}


def test_get_white_paper_integration(client):
    paper_id = "1706.03762"
    response = client.get(f"/whitepaper/{paper_id}")

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert response.content == b"%PDF-1.4..."


def test_get_metadata_integration(client):
    paper_id = "1706.03762"
    response = client.get(f"/metadata/{paper_id}")

    assert response.status_code == 200
    assert response.json() == PARSED_METADATA[0].model_dump()


def test_get_categories_integration(client):
    response = client.get("/categories")

    assert response.status_code == 200
    assert response.json() == [category.model_dump() for category in PARSED_CATEGORY]


def test_search_papers_integration(client):
    params = {"category": "cs.LG"}
    response = client.post("/search", json=params)

    assert response.status_code == 200
    assert response.json() == [metadata.model_dump() for metadata in PARSED_METADATA]
