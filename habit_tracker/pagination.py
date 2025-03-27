from rest_framework.pagination import PageNumberPagination


class HabitPagination(PageNumberPagination):
    page_size = 5  # Количество привычек на одной странице
    page_size_query_param = "page_size"  # Позволяет клиенту изменять размер страницы (например, ?page_size=10)
    max_page_size = 20  # Максимальное количество элементов на одной странице
