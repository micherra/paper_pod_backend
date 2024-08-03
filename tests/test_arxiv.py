import pytest
from unittest.mock import Mock, patch
import requests

from constants.abstract import ABSTRACT_HTML, PARSED_ABSTRACT
from constants.bibtex import BIBTEX_TEXT, PARSED_BIBTEX
from constants.category import CATEGORY_HTML, PARSED_CATEGORY
from whitepaper.arXiv_service import ArXivService


@pytest.fixture
def mock_bibtex():
    return BIBTEX_TEXT


@pytest.fixture
def mock_abstract():
    return ABSTRACT_HTML


@pytest.fixture
def mock_category():
    return CATEGORY_HTML


@pytest.fixture
def arxiv_service():
    source = "http://arxiv.org"
    return ArXivService(source=source)


@pytest.fixture
def mock_get():
    with patch("requests.get") as mock_get:
        yield mock_get


@pytest.fixture
def mock_abstract_response(mock_abstract):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = mock_abstract
    return mock_response


@pytest.fixture
def mock_bibtex_response(mock_bibtex):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = mock_bibtex
    return mock_response


def test_get_white_paper_success(mock_get, arxiv_service) -> None:
    paper_id = "1234.56789"
    path = "pdf"

    # Set up the mock to return a successful response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.content = b"PDF content"
    mock_response.url = f"{arxiv_service.source}/{path}/{paper_id}"
    mock_get.return_value = mock_response

    result = arxiv_service.get_white_paper(paper_id)

    # Assertions
    assert result == mock_response.content
    mock_get.assert_called_once_with(f"http://arxiv.org/{path}/{paper_id}")


def test_get_metadata_success(
    mock_get, arxiv_service, mock_bibtex_response, mock_abstract_response
) -> None:
    paper_id = "1234.56789"

    # Set up the mock to return the responses for abstract and bibtex
    mock_get.side_effect = [mock_abstract_response, mock_bibtex_response]

    result = arxiv_service.get_metadata(paper_id)

    # Assertions
    mock_get.assert_any_call(f"http://arxiv.org/abs/{paper_id}")
    mock_get.assert_any_call(f"http://arxiv.org/bibtex/{paper_id}")
    assert isinstance(result, dict)
    assert result == PARSED_BIBTEX | {"abstract": PARSED_ABSTRACT}


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

    arxiv_service.get_white_paper(paper_id)

    # Assertions
    assert isinstance(arxiv_service.get_white_paper(paper_id), Exception)
    assert (
        str(arxiv_service.get_white_paper(paper_id))
        == "Failed to retrieve the PDF: 404"
    )
    assert isinstance(arxiv_service.get_metadata(paper_id), Exception)
    assert (
        str(arxiv_service.get_metadata(paper_id))
        == "Failed to retrieve the metadata: 404"
    )
    assert isinstance(arxiv_service.categories(), Exception)
    assert str(arxiv_service.categories()) == "Failed to retrieve the categories: 404"


def test_parse_parse_bibtex(arxiv_service, mock_bibtex) -> None:
    result = arxiv_service.parse_bibtex(mock_bibtex)
    assert result == PARSED_BIBTEX


def test_parse_abstract_html(arxiv_service, mock_abstract) -> None:
    result = arxiv_service.parse_abstract_html(mock_abstract)
    assert result == PARSED_ABSTRACT


def test_parse_category_html(arxiv_service, mock_category) -> None:
    result = arxiv_service.parse_categories_html(mock_category)
    print(result)
    assert result == PARSED_CATEGORY
