from whitepaper.model.arXiv_metadata import ArXivMetadata

METADATA_XML = """
<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
    <link href="http://arxiv.org/api/query?search_query%3D%26id_list%3D2408.00716%26start%3D0%26max_results%3D10" rel="self" type="application/atom+xml"/>
    <title type="html">ArXiv Query: search_query=&amp;id_list=2408.00716&amp;start=0&amp;max_results=10</title>
    <id>http://arxiv.org/api/Xw65Mwc06w2m6bT+eDXxVJal3Nc</id>
    <updated>2024-08-03T00:00:00-04:00</updated>
    <opensearch:totalResults xmlns:opensearch="http://a9.com/-/spec/opensearch/1.1/">1</opensearch:totalResults>
    <opensearch:startIndex xmlns:opensearch="http://a9.com/-/spec/opensearch/1.1/">0</opensearch:startIndex>
    <opensearch:itemsPerPage xmlns:opensearch="http://a9.com/-/spec/opensearch/1.1/">10</opensearch:itemsPerPage>
    <entry>
        <id>http://arxiv.org/abs/2408.00716v1</id>
        <updated>2024-08-01T17:01:29Z</updated>
        <published>2024-08-01T17:01:29Z</published>
        <title>A Natural Language Processing Framework for Hotel Recommendation Based on Users' Text Reviews</title>
        <summary>  
Recently, the application of Artificial Intelligence algorithms in hotel
recommendation systems has become an increasingly popular topic. One such
method that has proven to be effective in this field is Deep Learning,
especially Natural Language processing models, which are able to extract
semantic knowledge from user's text reviews to create more efficient
recommendation systems.
        </summary>
        <author>
            <name>Lavrentia Aravani</name>
        </author>
        <author>
            <name>Emmanuel Pintelas</name>
        </author>
        <author>
            <name>Christos Pierrakeas</name>
        </author>
        <author>
            <name>Panagiotis Pintelas</name>
        </author>
        <link href="http://arxiv.org/abs/2408.00716v1" rel="alternate" type="text/html"/>
        <link title="pdf" href="http://arxiv.org/pdf/2408.00716v1" rel="related" type="application/pdf"/>
        <arxiv:primary_category xmlns:arxiv="http://arxiv.org/schemas/atom" term="cs.LG" scheme="http://arxiv.org/schemas/atom"/>
        <category term="cs.LG" scheme="http://arxiv.org/schemas/atom"/>
    </entry>
</feed>
"""

PARSED_METADATA = [
    ArXivMetadata(
        title="A Natural Language Processing Framework for Hotel Recommendation Based on Users' Text Reviews",
        id="2408.00716v1",
        released="2024-08-01T17:01:29Z",
        authors=[
            "Lavrentia Aravani",
            "Emmanuel Pintelas",
            "Christos Pierrakeas",
            "Panagiotis Pintelas",
        ],
        abstract="Recently, the application of Artificial Intelligence algorithms in hotel recommendation systems has "
        "become an increasingly popular topic. One such method that has proven to be effective in this field "
        "is Deep Learning, especially Natural Language processing models, which are able to extract semantic "
        "knowledge from user's text reviews to create more efficient recommendation systems.",
        primary_category="cs.LG",
    )
]
