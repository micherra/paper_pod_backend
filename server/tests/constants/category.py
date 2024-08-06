from server.services.whitepaper.model.arXiv_category import ArXivCategory

CATEGORY_HTML = """
<html>
    <body class="with-cu-identity">
        <div id="category_taxonomy_list" class="large-data-list">
            <h2 class="accordion-head">Computer Science</h2>
                <div class="accordion-body">
                    <div class=" columns ">
                        <div class="column">
                            <div class="columns divided">
                                <div class="column is-one-fifth">
                                    <h4>cs.AI <span>(Artificial Intelligence)</span></h4>
                                </div>
                                <div class="column">
                                    <p>Covers all areas of AI except Vision, Robotics, Machine Learning, Multiagent
                                        Systems, and Computation and Language (Natural Language Processing), which
                                        have separate subject areas. In particular, includes Expert Systems, Theorem
                                        Proving (although this may overlap with Logic in Computer Science),
                                        Knowledge Representation, Planning, and Uncertainty in AI. Roughly includes
                                        material in ACM Subject Classes I.2.0, I.2.1, I.2.3, I.2.4, I.2.8, and
                                        I.2.11.</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            <h2 class="accordion-head">Economics</h2>
            <div class="accordion-body">
                <div class=" columns ">
                    <div class="column">
                        <div class="columns divided">
                            <div class="column is-one-fifth">
                                <h4>econ.EM <span>(Econometrics)</span></h4>
                            </div>
                            <div class="column">
                                <p>Econometric Theory, Micro-Econometrics, Macro-Econometrics, Empirical Content
                                    of Economic Relations discovered via New Methods, Methodological Aspects of
                                    the Application of Statistical Inference to Economic Data.</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </body>
</html>
"""

PARSED_CATEGORY = [
    ArXivCategory(
        id="cs.AI",
        name="Artificial Intelligence",
        category="Computer Science",
        description="Covers all areas of AI except Vision, Robotics, Machine Learning, Multiagent Systems, "
        "and Computation and Language (Natural Language Processing), which have separate subject "
        "areas. In particular, includes Expert Systems, Theorem Proving (although this may overlap "
        "with Logic in Computer Science), Knowledge Representation, Planning, and Uncertainty in "
        "AI. Roughly includes material in ACM Subject Classes I.2.0, I.2.1, I.2.3, I.2.4, I.2.8, "
        "and I.2.11.",
    ),
    ArXivCategory(
        id="econ.EM",
        name="Econometrics",
        category="Economics",
        description="Econometric Theory, Micro-Econometrics, Macro-Econometrics, Empirical Content of Economic "
        "Relations discovered via New Methods, Methodological Aspects of the Application of "
        "Statistical Inference to Economic Data.",
    ),
]
