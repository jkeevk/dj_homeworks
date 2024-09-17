from datetime import datetime
from django.shortcuts import render, redirect
from books.models import Book


def index(request):
    return redirect("books")


def books_view(request):
    template = "books/books_list.html"
    books = Book.objects.all()
    context = {"books": books}
    return render(request, template, context)


def book_detail_view(request, pub_date):
    template = "books/book_detail.html"

    pub_date = datetime.strptime(pub_date, "%Y-%m-%d").date()
    books = Book.objects.filter(pub_date=pub_date)

    prev_date = Book.objects.filter(pub_date__lt=pub_date).order_by("-pub_date").first()
    next_date = Book.objects.filter(pub_date__gt=pub_date).order_by("pub_date").first()
    context = {
        "books": books,
        "prev_date": prev_date.pub_date if prev_date else None,
        "next_date": next_date.pub_date if next_date else None,
    }
    return render(request, template, context)
