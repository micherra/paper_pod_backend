import pytest
from unittest.mock import Mock, patch
import requests
from whitepaper.arXiv_service import ArXivService


@pytest.fixture
def mock_bibtex():
    return """
        @misc{aravani2024naturallanguageprocessingframework,
            title={A Natural Language Processing Framework for Hotel Recommendation Based on Users' Text Reviews}, 
            author={Lavrentia Aravani and Emmanuel Pintelas and Christos Pierrakeas and Panagiotis Pintelas},
            year={2024},
            eprint={2408.00716},
            archivePrefix={arXiv},
            primaryClass={cs.LG},
            url={https://arxiv.org/abs/2408.00716}, 
        }
    """


@pytest.fixture
def mock_abstract():
    return """
        <html>
            <body>
                <blockquote class="abstract mathjax">
                    <span class="descriptor">Abstract:</span>This is a test abstract.
                </blockquote>
            </body>
        </html>
    """


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


def test_get_white_paper_failure(mock_get, arxiv_service) -> None:
    paper_id = "9876.54321"
    path = "pdf"

    # Set up the mock to return a failed response
    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(404)
    mock_get.return_value = mock_response

    result = arxiv_service.get_white_paper(paper_id)

    # Assertions
    assert isinstance(result, Exception)
    assert str(result) == "Failed to retrieve the PDF: 404"
    mock_get.assert_called_once_with(f"http://arxiv.org/{path}/{paper_id}")


def test_get_metadata_success(
    mock_get, arxiv_service, mock_bibtex_response, mock_abstract_response
) -> None:
    paper_id = "1234.56789"

    # Set up the mock to return the responses for abstract and bibtex
    mock_get.side_effect = [mock_abstract_response, mock_bibtex_response]

    result = arxiv_service.get_metadata(paper_id)

    # Assertions
    assert isinstance(result, dict)
    assert result["abstract"] == "This is a test abstract."
    mock_get.assert_any_call(f"http://arxiv.org/abs/{paper_id}")
    mock_get.assert_any_call(f"http://arxiv.org/bibtex/{paper_id}")


def test_parse_parse_bibtex(arxiv_service, mock_bibtex) -> None:
    actual = {
        "title": "A Natural Language Processing Framework for Hotel Recommendation Based on Users' Text Reviews",
        "authors": [
            "Lavrentia Aravani",
            "Emmanuel Pintelas",
            "Christos Pierrakeas",
            "Panagiotis Pintelas",
        ],
    }

    result = arxiv_service.parse_bibtex(mock_bibtex)
    assert result == actual


def test_parse_html(arxiv_service, mock_abstract) -> None:
    result = arxiv_service.parse_html(mock_abstract)
    assert result == "This is a test abstract."
