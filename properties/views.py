from django.shortcuts import render, get_object_or_404
from .models import Property, Category


def property_list(request):
    properties = Property.objects.all()
    categories = Category.objects.all()

    category = request.GET.get("category", "")
    transaction_type = request.GET.get("transaction_type", "")
    status = request.GET.get("status", "")
    city = request.GET.get("city", "")
    min_price = request.GET.get("min_price", "")
    max_price = request.GET.get("max_price", "")
    featured = request.GET.get("featured", "")

    if category:
        properties = properties.filter(category_id=category)

    if transaction_type:
        properties = properties.filter(transaction_type=transaction_type)

    if status:
        properties = properties.filter(status=status)

    if city:
        properties = properties.filter(city__icontains=city)

    if min_price:
        properties = properties.filter(price__gte=min_price)

    if max_price:
        properties = properties.filter(price__lte=max_price)

    if featured == "1":
        properties = properties.filter(is_featured=True)

    context = {
        "properties": properties,
        "categories": categories,
        "selected_category": category,
        "selected_transaction_type": transaction_type,
        "selected_status": status,
        "selected_city": city,
        "selected_min_price": min_price,
        "selected_max_price": max_price,
        "selected_featured": featured,
    }

    return render(request, "properties/property_list.html", context)


def property_detail(request, slug):
    property_obj = get_object_or_404(Property, slug=slug)

    context = {
        "property": property_obj,
    }

    return render(request, "properties/property_detail.html", context)