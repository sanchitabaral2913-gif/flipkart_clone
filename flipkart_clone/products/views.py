from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from orders.models import OrderItem
from .models import Product, Category, Review
from .forms import ProductForm, ReviewForm
from django.db.models import Q


# --------------------
# HOME
# --------------------
def home(request):
    categories = Category.objects.all()
    products = Product.objects.filter(status='approved')
    return render(request, 'products/home.html', {
        'categories': categories,
        'products': products
    })



def all_products(request):
    query = request.GET.get('q')   # search value
    products = Product.objects.filter(status='approved')

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__icontains=query)
        )

    return render(request, 'products/all_products.html', {
        'products': products
    })



# --------------------
# PRODUCT DETAIL + REVIEW
# --------------------



def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # All approved reviews
    reviews = product.reviews.filter(status='approved').order_by('-created_at')

    # Logged in user ka review
    user_review = None
    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()

    # Review form handling
    if request.method == 'POST' and request.user.is_authenticated and request.user.role == 'customer':

        if user_review:
            form = ReviewForm(request.POST, instance=user_review)
        else:
            form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.status = 'approved'
            review.save()
            return redirect('product_detail', pk=product.pk)

    else:
        form = ReviewForm(instance=user_review)

    # Product images list (IMPORTANT: field names match model)
    product_images = []

    if product.image_front:
        product_images.append(product.image_front)

    if product.image_back:
        product_images.append(product.image_back)

    if product.image_left:
        product_images.append(product.image_left)

    if product.image_right:
        product_images.append(product.image_right)

    return render(request, 'products/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'form': form,
        'user_review': user_review,
        'product_images': product_images
    })


 #----------------
# SELLER ADD PRODUCT
# --------------------
@login_required
def add_product(request):
    if request.user.role != 'seller':
        return redirect('home')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            return redirect('my_products')
    else:
        form = ProductForm()

    return render(request, 'products/add_product.html', {
        'form': form
    })


# --------------------
# SELLER MY PRODUCTS
# --------------------
@login_required
def my_products(request):
    products = Product.objects.filter(seller=request.user)
    return render(request, 'products/my_products.html', {
        'products': products
    })


@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.user != product.seller:
        return redirect('my_products')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('my_products')
    else:
        form = ProductForm(instance=product)

    return render(request, 'products/edit_product.html', {
        'form': form
    })


@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.user == product.seller:
        product.delete()

    return redirect('my_products')


# --------------------
# ADMIN DASHBOARD
# --------------------
@login_required
def admin_dashboard(request):
    # Admin check
    if not request.user.is_superuser:
        return redirect('home')

    products = Product.objects.all().order_by('-created_at')
    reviews = Review.objects.all().order_by('-created_at')

    return render(request, 'products/admin_dashboard.html', {
        'products': products,
        'reviews': reviews
    })


# --------------------
# PRODUCT LIST
# --------------------


def product_list(request):
    category_id = request.GET.get('category')

    categories = Category.objects.all()

    if category_id:
        products = Product.objects.filter(
            category_id=category_id,
            status='approved'
        )
    else:
        products = Product.objects.filter(status='approved')

    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': categories
    })


# --------------------
# PRODUCT APPROVE / REJECT
# --------------------
@login_required
def approve_product(request, product_id):
    # YAHAN LIKHNA HAI
    if not request.user.is_superuser:
        return redirect('home')

    product = get_object_or_404(Product, id=product_id)
    product.status = 'approved'
    product.save()
    return redirect('admin_dashboard')

@login_required
def reject_product(request, product_id):
    if not request.user.is_superuser:
        return redirect('home')

    product = get_object_or_404(Product, id=product_id)
    product.status = 'rejected'
    product.save()
    return redirect('admin_dashboard')

# --------------------
# CATEGORY PRODUCTS
# --------------------
def category_products(request, category_name):
    products = Product.objects.filter(
        category__name=category_name,
        status='approved'
    )
    return render(request, 'products/category_products.html', {
        'products': products,
        'category_name': category_name
    })


# --------------------
# SELLER DASHBOARD
# --------------------
@login_required
def seller_dashboard(request):
    if request.user.role != 'seller':
        return redirect('home')

    products = Product.objects.filter(seller=request.user)
    orders = OrderItem.objects.filter(product__seller=request.user)

    return render(request, 'products/seller_dashboard.html', {
        'products': products,
        'orders': orders
    })


# --------------------
# CUSTOMER DASHBOARD
# --------------------
@login_required
def customer_dashboard(request):
    if request.user.role != 'customer':
        return redirect('home')

    products = Product.objects.filter(status='approved')
    return render(request, 'products/customer_dashboard.html', {
        'products': products
    })


# --------------------
# REVIEW DELETE
# --------------------
@login_required
def delete_review(request, review_id):
    review = get_object_or_404(
        Review,
        id=review_id,
        user=request.user
    )

    product_id = review.product.id
    review.delete()

    return redirect('product_detail', pk=product_id)


# --------------------
# REVIEW EDIT
# --------------------
@login_required
def edit_review(request, review_id):
    review = get_object_or_404(
        Review,
        id=review_id,
        user=request.user
    )

    product = review.product

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('product_detail', pk=product.id)
    else:
        form = ReviewForm(instance=review)

    reviews = product.reviews.all()

    return render(request, 'products/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'form': form,
        'user_review': review
    })
