from .fulltext_search import init as init_fulltext, search as search_fulltext
from .tfidf_search import init as init_tfidf, search as search_tfidf
from .bm25_search import init as init_bm25, search as search_bm25
from .openai_search import init as init_openai, search as search_openai

from .st_1_search import init as init_st_1, search as search_st_1
from .st_2_search import init as init_st_2, search as search_st_2
from .st_3_search import init as init_st_3, search as search_st_3

from .hybrid_search import search as hybrid_search

def init_search_module(documents):
    init_fulltext(documents)
    init_tfidf(documents)
    init_bm25(documents)
    init_openai(documents)
    init_st_1(documents)
    init_st_2(documents)
    init_st_3(documents)
