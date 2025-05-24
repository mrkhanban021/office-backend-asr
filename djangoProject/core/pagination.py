from rest_framework.pagination import LimitOffsetPagination


class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 30
    max_limit = 100
    limit_query_param = 'limit'
    offset_query_param = 'offset'
