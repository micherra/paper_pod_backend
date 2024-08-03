from typing import TypedDict


class ArXivMetadata(TypedDict):
    """
    Represents the metadata of an arXiv article.
    :property title: The title of the article.
    :property id: arXiv id of the article.
    :property released: The date that current version of the article was submitted.
    :property abstract: The article abstract.
    :property authors: The authors of the article.
    :property primary_category: The primary arXiv category of the article.
    """

    title: str
    id: str
    released: str
    abstract: str
    authors: list[str]
    primary_category: str
