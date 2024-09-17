from django.shortcuts import render, redirect
from phones.models import Phone


def index(request):
    return redirect("catalog")


def show_catalog(request):
    template = "catalog.html"
    sort = request.GET.get("sort", "")

    if sort == "name":
        ordering = "name"
    elif sort == "min_price":
        ordering = "price"
    elif sort == "max_price":
        ordering = "-price"
    else:
        ordering = None

    phones = Phone.objects.all()

    if ordering:
        phones = phones.order_by(ordering)

    context = {"phones": phones}
    return render(request, template, context)


def show_product(request, slug):
    template = "product.html"
    phone = Phone.objects.filter(slug=slug).first()
    if not phone:
        return redirect("catalog")

    context = {"phone": phone}
    return render(request, template, context)
