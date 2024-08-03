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
def mock_category():
    return """
        <html>
            <body>
                <div id="category_taxonomy_list" class="large-data-list">
                    <h2 class="accordion-head">Computer Science</h2>
                        <div class="accordion-body">
                            <div class=" columns ">
                                <div class="column">
                                    <div class="columns divided">
                                        <div class="column is-one-fifth">
                                            <h4>
                                                cs.AI <span>(Artificial Intelligence)</span>
                                            </h4>
                                        </div>
                                        <div class="column">
                                            <p>Covers all areas of AI except Vision, Robotics, Machine Learning, Multiagent Systems, and Computation and Language (Natural Language Processing), which have separate subject areas. In particular, includes Expert Systems, Theorem Proving (although this may overlap with Logic in Computer Science), Knowledge Representation, Planning, and Uncertainty in AI. Roughly includes material in ACM Subject Classes I.2.0, I.2.1, I.2.3, I.2.4, I.2.8, and I.2.11.</p>
                                        </div>
                                    </div>
                                    <div class="columns divided">
                                        <div class="column is-one-fifth">
                                            <h4>
                                                cs.AR <span>(Hardware Architecture)</span>
                                            </h4>
                                        </div>
                                        <div class="column">
                                            <p>Covers systems organization and hardware architecture. Roughly includes material in ACM Subject Classes C.0, C.1, and C.5.</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </h2>
                </div>
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
    assert result == {
        "title": "A Natural Language Processing Framework for Hotel Recommendation Based on Users' Text Reviews",
        "authors": [
            "Lavrentia Aravani",
            "Emmanuel Pintelas",
            "Christos Pierrakeas",
            "Panagiotis Pintelas",
        ],
        "abstract": "This is a test abstract.",
    }


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


def test_parse_abstract_html(arxiv_service, mock_abstract) -> None:
    result = arxiv_service.parse_abstract_html(mock_abstract)
    assert result == "This is a test abstract."


def test_parse_category_html(arxiv_service, mock_category) -> None:
    result = arxiv_service.parse_categories_html(mock_category)
    print(result)
    assert result == [
        {
            "name": "Artificial Intelligence",
            "group": "Computer Science",
            "category": "cs.AI",
            "description": "Covers all areas of AI except Vision, Robotics, Machine Learning, Multiagent Systems, "
            "and Computation and Language (Natural Language Processing), which have separate subject "
            "areas. In particular, includes Expert Systems, Theorem Proving (although this may overlap "
            "with Logic in Computer Science), Knowledge Representation, Planning, and Uncertainty in "
            "AI. Roughly includes material in ACM Subject Classes I.2.0, I.2.1, I.2.3, I.2.4, I.2.8, "
            "and I.2.11.",
        },
        {
            "name": "Hardware Architecture",
            "group": "Computer Science",
            "category": "cs.AR",
            "description": "Covers systems organization and hardware architecture. Roughly includes material in ACM "
            "Subject Classes C.0, C.1, and C.5.",
        },
    ]
