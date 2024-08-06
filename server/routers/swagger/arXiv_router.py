def get_white_paper_swagger():
    return {
        "path": "/whitepaper/{paper_id}",
        "summary": "Get the white paper PDF",
        "response_description": "The white paper PDF",
        "description": "Get the white paper PDF from the arXiv.org website.",
        "responses": {
            "200": {
                "content": {"application/pdf": {}},
                "description": "The white paper PDF",
            },
            "404": {
                "description": "The white paper was not found",
            },
            "500": {"description": "Internal server error"},
        },
    }


def get_metadata_swagger():
    return {
        "path": "/metadata/{paper_id}",
        "summary": "Get the white paper metadata",
        "response_description": "The white paper metadata",
        "description": "Get the white paper metadata from the arXiv.org website.",
        "responses": {
            "200": {
                "description": "The white paper metadata",
            },
            "404": {
                "description": "The white paper was not found",
            },
            "500": {"description": "Internal server error"},
        },
    }


def get_categories_swagger():
    return {
        "path": "/categories",
        "summary": "Get the arXiv categories",
        "response_description": "The arXiv categories",
        "description": "Get the arXiv categories from the arXiv.org website.",
        "responses": {
            "200": {
                "description": "The arXiv categories",
            },
            "404": {"description": "The arXiv categories were not found"},
            "500": {"description": "Internal server error"},
        },
    }


def search_papers_swagger():
    return {
        "path": "/search",
        "summary": "Search for white papers",
        "response_description": "The white papers",
        "description": "Search for white papers from the arXiv.org website.",
        "responses": {
            "200": {
                "description": "List of white papers metadata",
            },
            "500": {"description": "Internal server error"},
        },
    }
