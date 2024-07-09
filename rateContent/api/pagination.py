from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination
from rest_framework.response import Response


class TitleListPagination(PageNumberPagination):
    page_size = 6
    page_query_param = "p"
    page_size_query_param = "size"

    max_page_size = 10
    last_page_strings = "end"

class TitleListLFPagination(LimitOffsetPagination):
    default_limit = 5
    max_limit = 10
    limit_query_param = "limit"
    offset_query_param = "start"

class TitleListCPagination(CursorPagination):
    page_size = 5
    ordering = 'created'
    cursor_query_param = "record"

