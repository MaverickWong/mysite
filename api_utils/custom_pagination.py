from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from collections import OrderedDict
from rest_framework.response import Response


class LargeResultsSetPagination(LimitOffsetPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10000

    def get_paginated_response(self, data):
        code = 20000
        msg = 'success'
        if not data:
            code = 404
            msg = "Data Not Found"

        return Response(OrderedDict([
            ('code', code),
            ('msg', msg),
            ('count', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('data', data),
        ]))


from collections import OrderedDict, namedtuple
from rest_framework import pagination


class UserPagination(pagination.PageNumberPagination):
    '''自定义分页'''
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10000

    def get_paginated_response(self, data):
        code = 20000
        msg = 'success'
        if not data:
            code = 404
            msg = "Data Not Found"

        return Response(OrderedDict([
            ('code', code),
            ('msg', msg),

            ('totalCount', self.page.paginator.count),
            ('pageIndex', self.page.number),
            ('pageCount', self.page.paginator.num_pages),
            ('pageSize', self.page_size),

            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),

            ('items', data)
        ]))
