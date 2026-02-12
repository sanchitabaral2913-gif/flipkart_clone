import random
from django.shortcuts import render, redirect
from django.http import JsonResponse

# Home Page
def home(request):
    products = [
        {"id": 1, "name": "Burger", "price": 120, "image": "images/burger1.jpg", "ribbon": "Best Seller"},
        {"id": 2, "name": "Pizza", "price": 250, "image": "images/pizza1.jpg", "ribbon": "20% Off"},
        {"id": 3, "name": "Momos", "price": 90, "image": "images/momos1.jpg", "ribbon": "New"},
        {"id": 4, "name": "Sandwich", "price": 80, "image": "images/sandwich1.jpg", "ribbon": None},
    ]
    
    
    
    if "cart" not in request.session:
        request.session["cart"] = {}
    return render(request, "food/home.html", {"products": products})

# Menu Data
ribbon_choices = ["Best Seller", "20% Off", "New", None]
menu = {
    "Burgers": [
        {"id": 1, "name": "Cheese Burger", "price": 120, "images": ["images/burger1.jpg", "images/buger1_2.jpg"]},
        {"id": 2, "name": "Veggie Burger", "price": 100, "images": ["images/burger2.jpg", "images/buger2_2.jpg"]},
        {"id": 3, "name": "Chicken Burger", "price": 150, "images": ["images/burger3.jpg", "images/buger3_2.jpg"]},
    ],
    "Pizzas": [
        {"id": 4, "name": "Margherita", "price": 250, "images": ["images/pizza1.jpg", "images/pizza1_2.jpg"]},
        {"id": 5, "name": "Veggie Pizza", "price": 270, "images": ["images/pizza2.jpg", "images/pizza2_2.jpg"]},
        {"id": 6, "name": "Pepperoni Pizza", "price": 300, "images": ["images/pizza3.jpg", "images/pizza3_2.jpg"]},
    ],
    "Momos": [
        {"id": 7, "name": "Veg Momos", "price": 90, "images": ["images/momos1.jpg", "images/momos1_2.jpg"]},
        {"id": 8, "name": "Chicken Momos", "price": 120, "images": ["images/momos2.jpg", "images/momos2_2.jpg"]},
        {"id": 9, "name": "Paneer Momos", "price": 110, "images": ["images/momos3.jpg", "images/momos3_2.jpg"]},
    ],
    "Sandwiches": [
        {"id": 10, "name": "Grilled Sandwich", "price": 80, "images": ["images/sandwich1.jpg", "images/sandwich1_2.jpg"]},
        {"id": 11, "name": "Veg Sandwich", "price": 70, "images": ["images/sandwich2.jpg", "images/sandwich2_2.jpg"]},
        {"id": 12, "name": "Cheese Sandwich", "price": 100, "images": ["images/sandwich3.jpg", "images/sandwich3_2.jpg"]},
    ],
}

# Assign ribbons
for cat in menu.values():
    for prod in cat:
        prod["ribbon"] = random.choice(ribbon_choices)

# Menu Page
def menu_view(request):
    cart = request.session.get("cart", {})
    return render(request, "food/menu.html", {"menu": menu, "cart": cart})

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def add_to_cart(request, product_id):
    qty = int(request.GET.get("qty", 1))
    cart = request.session.get("cart", {})

    # Find product from menu
    product = None
    for items in menu.values():
        for item in items:
            if item["id"] == product_id:
                product = item
                break
        if product: break

    if not product:
        return JsonResponse({"success": False})

    if str(product_id) in cart:
        cart[str(product_id)]["quantity"] += qty
    else:
        cart[str(product_id)] = {
            "name": product["name"],
            "price": product["price"],
            "quantity": qty,
            "image": product["images"][0]
        }

    request.session["cart"] = cart
    request.session.modified = True

    cart_count = sum(item["quantity"] for item in cart.values())
    return JsonResponse({"success": True, "cart_count": cart_count})

def remove_from_cart(request, product_id):
    cart = request.session.get("cart", {})
    cart.pop(str(product_id), None)
    request.session["cart"] = cart
    request.session.modified = True
    return redirect(request.META.get("HTTP_REFERER", "/"))

def update_cart(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        action = request.POST.get("action")
        cart = request.session.get("cart", {})
        if product_id in cart:
            if action == "increment": cart[product_id]["quantity"] += 1
            if action == "decrement": 
                cart[product_id]["quantity"] -= 1
                if cart[product_id]["quantity"] <= 0: del cart[product_id]
            request.session["cart"] = cart
            request.session.modified = True
            total_price = sum(item["price"]*item["quantity"] for item in cart.values())
            return JsonResponse({"success": True, "quantity": cart.get(product_id, {}).get("quantity", 0), "total_price": total_price})
    return JsonResponse({"success": False})

def cart_summary(request):
    cart = request.session.get("cart", {})
    items = []
    total = 0
    for pid, qty in cart.items():
        # Assuming product lookup from your data
        product = next((p for cat in menu.values() for p in cat if p["id"] == int(pid)), None)
        if product:
            item_total = product["price"] * qty
            items.append({"name": product["name"], "qty": qty, "total": item_total})
            total += item_total
    return JsonResponse({"items": items, "count": sum(cart.values()), "total": total})

# Other Pages
def about(request): return render(request, "food/about.html")
def booktable(request): return render(request, "food/booktable.html")
def feedback(request): return render(request, "food/feedback.html")
def order_view(request):
    cart = request.session.get("cart", {})
    total_price = sum(item["price"]*item["quantity"] for item in cart.values())
    return render(request, "food/order.html", {"cart": cart, "total_price": total_price})
