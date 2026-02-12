

from django.shortcuts import render

def all_products(request):
    # image path ko /static/ se start kar do (simple approach)
    products = [
        {"id": 1, "name": "Burger",   "price": 120, "image": "/static/images/bugger.jpg"},
        {"id": 2, "name": "Pizza",    "price": 250, "image": "/static/images/pizza.jpg"},
        {"id": 3, "name": "Pasta",    "price": 180, "image": "/static/images/pasta.jpg"},
    
    ]
    return render(request, 'store/all_products.html', {'products': products})
