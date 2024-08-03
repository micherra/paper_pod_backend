from whitepaper.model.arXiv_bibtex import ArXivBibtex

BIBTEX_TEXT = """
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

PARSED_BIBTEX = ArXivBibtex(
    title="A Natural Language Processing Framework for Hotel Recommendation Based on Users' Text Reviews",
    authors=[
        "Lavrentia Aravani",
        "Emmanuel Pintelas",
        "Christos Pierrakeas",
        "Panagiotis Pintelas",
    ],
)
