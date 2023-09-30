from django.shortcuts import render


def main(request):
    """
    Функция главной страницы
    :param request: запрос
    :return: html страница
    """

    return render(request, "main.html")
