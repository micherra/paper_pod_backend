import pytest
from unittest.mock import Mock, patch
import requests

from server.tests.constants.category import CATEGORY_HTML, PARSED_CATEGORY
from server.tests.constants.metadata import METADATA_XML, PARSED_METADATA
from server.services.whitepaper.arXiv import ArXivService


@pytest.fixture
def mock_category():
    return CATEGORY_HTML


@pytest.fixture
def mock_metadata():
    return METADATA_XML


@pytest.fixture
def arxiv_service():
    return ArXivService()


@pytest.fixture
def mock_get():
    with patch("requests.get") as mock_get:
        yield mock_get


def test_get_white_paper_success(mock_get, arxiv_service) -> None:
    paper_id = "1234.56789"
    path = "pdf"

    # Set up the mock to return a successful response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.content = b"PDF content"
    mock_response.url = f"{arxiv_service.arXiv_org}/{path}/{paper_id}"
    mock_get.return_value = mock_response

    result = arxiv_service.get_white_paper(paper_id)

    # Assertions
    assert result == mock_response.content
    mock_get.assert_called_once_with(f"https://arxiv.org/{path}/{paper_id}")


def test_get_metadata_success(mock_get, arxiv_service, mock_metadata) -> None:
    paper_id = "1234.56789"

    # Set up the mock to return the response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = mock_metadata
    mock_get.return_value = mock_response

    result = arxiv_service.get_metadata(paper_id)

    # Assertions
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["id"] == "2408.00716v1"
    mock_get.assert_called_once_with(
        f"https://export.arxiv.org/api/query?id_list={paper_id}"
    )


def test_categories_success(mock_get, arxiv_service, mock_category) -> None:
    # Set up the mock to return a successful response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = mock_category
    mock_get.return_value = mock_response

    result = arxiv_service.categories()

    # Assertions
    assert isinstance(result, list)
    assert len(result) == 2


def test_api_failures(mock_get, arxiv_service) -> None:
    paper_id = "9876.54321"

    # Set up the mock to return a failed response
    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(404)
    mock_get.return_value = mock_response

    # Assertions for get_white_paper
    with pytest.raises(Exception) as excinfo:
        arxiv_service.get_white_paper(paper_id)
    assert str(excinfo.value) == "Failed to retrieve the PDF: 404"

    # Assertions for get_metadata
    with pytest.raises(Exception) as excinfo:
        arxiv_service.get_metadata(paper_id)
    assert str(excinfo.value) == "Failed to retrieve search results: 404"

    # Assertions for categories
    with pytest.raises(Exception) as excinfo:
        arxiv_service.categories()
    assert str(excinfo.value) == "Failed to retrieve the categories: 404"

    # Assertions for search
    with pytest.raises(Exception) as excinfo:
        arxiv_service.search("query")
    assert str(excinfo.value) == "Failed to retrieve search results: 404"


def test_parse_category_html(arxiv_service, mock_category) -> None:
    result = arxiv_service.parse_categories_html(mock_category)
    assert result == PARSED_CATEGORY


def test_parse_metadata_xml(arxiv_service, mock_metadata) -> None:
    result = arxiv_service.parse_metadata_xml(mock_metadata)
    assert result == PARSED_METADATA
