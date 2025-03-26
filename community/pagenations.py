from rest_framework.pagination import PageNumberPagination


class PostPageNumberPagination(PageNumberPagination):
    page_size = 10  # 기본 페이지당 항목 수
    page_size_query_param = (
        "page_size"  # 클라이언트가 원하는 페이지당 항목 수를 설정하는 쿼리 파라미터
    )
    max_page_size = 50  # 최대 페이지 크기
