from fastapi import APIRouter, HTTPException, Depends
from starlette.responses import FileResponse

from server.dependencies.services import get_arxiv_service
from server.routers.models.arXiv_search import ArXivSearch
from server.routers.swagger.arXiv_router import (
    get_white_paper_swagger,
    get_metadata_swagger,
    get_categories_swagger,
    search_papers_swagger,
)
from server.services.whitepaper.arXiv import ArXivService
from server.routers.utils.arXiv_query import get_arxiv_query

arXiv_router = APIRouter(
    prefix="", tags=["arXiv"], dependencies=[Depends(get_arxiv_service)]
)


@arXiv_router.get(**get_white_paper_swagger())
def get_white_paper(
    paper_id: str, arxiv_service: ArXivService = Depends(get_arxiv_service)
):
    try:
        res = arxiv_service.get_white_paper(paper_id)
        pdf_file_path = f"/tmp/{paper_id}.pdf"  # Temporary file path
        with open(pdf_file_path, "wb") as pdf_file:
            pdf_file.write(res)
        return FileResponse(pdf_file_path, media_type="application/pdf")
    except HTTPException as e:
        raise e


@arXiv_router.get(**get_metadata_swagger())
def get_metadata(
    paper_id: str, arxiv_service: ArXivService = Depends(get_arxiv_service)
):
    try:
        print(arxiv_service.get_metadata(paper_id))
        return arxiv_service.get_metadata(paper_id)
    except HTTPException as e:
        raise e


@arXiv_router.get(**get_categories_swagger())
def get_categories(arxiv_service: ArXivService = Depends(get_arxiv_service)):
    try:
        return arxiv_service.categories()
    except HTTPException as e:
        raise e


@arXiv_router.post(**search_papers_swagger())
def search_papers(
    params: ArXivSearch, arxiv_service: ArXivService = Depends(get_arxiv_service)
):
    query = get_arxiv_query(params)
    try:
        return arxiv_service.search(query)
    except HTTPException as e:
        raise e
