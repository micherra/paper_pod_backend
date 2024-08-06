from server.routers.models.arXiv_search import ArXivSearch


def format_query_param(key: str, value: str):
    param_format = {
        "id": f"id_list:{value}",
        "title": f"ti:{value}",
        "author": f"au:{value}",
        "abstract": f"abs:{value}",
        "category": f"cat:{value}",
        "start": f"start={value}",
        "max_results": f"max_results={value}",
        "sort_by": f"sortBy={value}",
        "sort_order": f"sortOrder={value}",
    }
    return param_format[key]


def get_arxiv_query(params: ArXivSearch):
    enum_params = ["sort_by", "sort_order"]
    search_query_keys = ["id", "title", "author", "abstract", "category"]
    search_query = []
    query_params = []

    for key, value in params.model_dump().items():
        if key in search_query_keys and value is not None:
            search_query.append(format_query_param(key, value))
        elif key in enum_params and value is not None:
            query_params.append(format_query_param(key, value.name))
        elif value is not None:
            query_params.append(format_query_param(key, value))

    return "search_query=" + "+AND+".join(search_query) + "&" + "&".join(query_params)
