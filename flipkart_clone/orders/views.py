from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cart, Order, OrderItem
from products.models import Product

# ---------------- CUSTOMER ORDERS ----------------

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/my_orders.html', {'orders': orders})


@login_required
def order_detail_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})


# ---------------- CART ----------------

@login_required
def add_to_cart(request, product_id):
    if request.user.role != 'customer':
        return redirect('product_list')

    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')


@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = 0

    for item in cart_items:
        item.subtotal = item.product.price * item.quantity
        total += item.subtotal

    return render(
        request,
        'orders/cart.html',
        {'cart_items': cart_items, 'total': total}
    )


@login_required
def cart_increment(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')


@login_required
def cart_decrement(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')


@login_required
def cart_remove(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.delete()
    return redirect('cart')


# ---------------- CHECKOUT ----------------



def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)

    total = 0
    for item in cart_items:
        total += item.product.price * item.quantity

    order = Order.objects.create(
        user=request.user,
        total_amount=total
    )

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )

    cart_items.delete()
    return redirect('order_detail', order.id)



# ---------------- CANCEL ORDER (AUTO DELETE) ----------------

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status == 'pending':
        order.delete()
    return redirect('my_orders')


# ---------------- SELLER ----------------

@login_required
def seller_orders(request):
    if request.user.role != 'seller':
        return redirect('home')

    orders = Order.objects.filter(
        orderitem__product__seller=request.user
    ).distinct()

    return render(request, 'orders/seller_orders.html', {
        'orders': orders
    })


@login_required
def complete_order(request, order_id):
    order = Order.objects.get(id=order_id)

    # seller check
    if request.user.role != 'seller':
        return redirect('seller_orders')

    # check seller ke product order me hain ya nahi
    if not order.orderitem_set.filter(product__seller=request.user).exists():
        return redirect('seller_orders')

    order.status = 'completed'
    order.save()

    return redirect('seller_orders')



#@login_required
#def seller_dashboard(request):
    if request.user.role != 'seller':
        return redirect('home')

    # Seller ke liye pending orders count
    pending_orders_count = Order.objects.filter(
        orderitem__product__seller=request.user,
        status='pending'
    ).distinct().count()

    return render(request, 'products/seller_dashboard.html', {
        'pending_orders_count': pending_orders_count
    })



@login_required
def seller_pending_orders(request):
    if request.user.role != 'seller':
        return redirect('home')

    # Seller ke pending orders
    orders = Order.objects.filter(
        orderitem__product__seller=request.user,
        status='pending'
    ).distinct()

    pending_orders_count = orders.count()

    return render(request, 'orders/seller_orders.html', {
        'orders': orders,
        'pending_orders_count': pending_orders_count
    })

@login_required
def update_order_status(request, order_id, status):
    order = get_object_or_404(Order, id=order_id)

    # Sirf admin ya seller hi update kar sakta hai
    if request.user.role in ['admin', 'seller']:
        if status in ['shipped', 'delivered']:
            order.status = status
            order.save()

    return redirect('admin_orders')  # ya seller_orders