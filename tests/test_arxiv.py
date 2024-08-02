import pytest
from unittest.mock import Mock, patch
from whitepaper.arXivService import ArXivService


@pytest.fixture
def arxiv_service():
    source = "http://arxiv.org"
    return ArXivService(source=source)


@pytest.fixture
def mocker():
    with patch("requests.get") as mock_get:
        yield mock_get


def test_get_white_paper_success(mocker, arxiv_service) -> None:
    paper_id = "1234.56789"
    path = "pdf"

    # Set up the mock to return a successful response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.content = b"PDF content"
    mock_response.url = f"{arxiv_service.source}/{path}/{paper_id}"
    mocker.return_value = mock_response

    result = arxiv_service.get_white_paper(path, paper_id)

    # Assertions
    assert result == mock_response.content
    mocker.assert_called_once_with(f"http://arxiv.org/{path}/{paper_id}")


def test_get_white_paper_failure(mocker, arxiv_service) -> None:
    paper_id = "9876.54321"
    path = "pdf"

    # Set up the mock to return a failed response
    mock_response = Mock()
    mock_response.status_code = 404
    mocker.return_value = mock_response

    result = arxiv_service.get_white_paper(path, paper_id)

    # Assertions
    assert result is None
    mocker.assert_called_once_with(f"http://arxiv.org/{path}/{paper_id}")
