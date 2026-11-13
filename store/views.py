from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from .models import Product, Order, OrderItem
from .forms import CheckoutForm


def store_home(request):
    products = Product.objects.all()
    category = request.GET.get('category', '')
    query = request.GET.get('q', '')

    if category:
        products = products.filter(category=category)
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    cart = request.session.get('cart', {})
    cart_count = sum(cart.values()) if cart else 0

    context = {
        'products': products,
        'category': category,
        'query': query,
        'category_choices': Product.CATEGORY_CHOICES,
        'cart_count': cart_count,
    }
    return render(request, 'store/store_home.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = request.session.get('cart', {})
    in_cart_qty = cart.get(str(pk), 0)

    context = {
        'product': product,
        'in_cart_qty': in_cart_qty,
        'max_order_qty': max(0, product.quantity - in_cart_qty),
    }
    return render(request, 'store/product_detail.html', context)


def add_to_cart(request, pk):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=pk)
        try:
            qty_to_add = int(request.POST.get('quantity', 1))
        except (ValueError, TypeError):
            qty_to_add = 1

        if qty_to_add <= 0:
            qty_to_add = 1

        cart = request.session.get('cart', {})
        current_in_cart = cart.get(str(pk), 0)

        if current_in_cart + qty_to_add > product.quantity:
            messages.error(request, f'Sorry, only {product.quantity} units of "{product.name}" are in stock.')
        else:
            cart[str(pk)] = current_in_cart + qty_to_add
            request.session['cart'] = cart
            messages.success(request, f'Added {qty_to_add}x "{product.name}" to your cart.')

    next_url = request.POST.get('next')
    if next_url:
        return redirect(next_url)
    return redirect('store_home')


def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    # Clean up any removed products
    clean_cart = {}
    for product_id, qty in cart.items():
        try:
            product = Product.objects.get(pk=int(product_id))
            subtotal = product.price * qty
            total += subtotal
            cart_items.append({
                'product': product,
                'quantity': qty,
                'subtotal': subtotal,
                'is_available': product.quantity >= qty,
            })
            clean_cart[str(product.id)] = qty
        except (Product.DoesNotExist, ValueError):
            pass

    if clean_cart != cart:
        request.session['cart'] = clean_cart

    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'store/cart.html', context)


def update_cart(request, pk):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=pk)
        try:
            new_qty = int(request.POST.get('quantity', 1))
        except (ValueError, TypeError):
            new_qty = 1

        cart = request.session.get('cart', {})
        str_pk = str(pk)

        if new_qty <= 0:
            cart.pop(str_pk, None)
            messages.info(request, f'Removed "{product.name}" from your cart.')
        elif new_qty > product.quantity:
            cart[str_pk] = product.quantity
            messages.warning(request, f'Adjusted quantity to maximum available stock ({product.quantity}).')
        else:
            cart[str_pk] = new_qty
            messages.success(request, f'Updated quantity for "{product.name}".')

        request.session['cart'] = cart
    return redirect('view_cart')


def remove_from_cart(request, pk):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        str_pk = str(pk)
        if str_pk in cart:
            cart.pop(str_pk)
            request.session['cart'] = cart
            messages.info(request, 'Item removed from your cart.')
    return redirect('view_cart')


@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, 'Your shopping cart is empty.')
        return redirect('store_home')

    # Resolve items and check stock
    cart_items = []
    total = 0
    stock_errors = []

    for product_id, qty in cart.items():
        try:
            product = Product.objects.get(pk=int(product_id))
            if qty > product.quantity:
                stock_errors.append(f'"{product.name}" only has {product.quantity} in stock (requested {qty}).')
            subtotal = product.price * qty
            total += subtotal
            cart_items.append({'product': product, 'quantity': qty, 'subtotal': subtotal})
        except Product.DoesNotExist:
            pass

    if not cart_items:
        request.session['cart'] = {}
        messages.error(request, 'The items in your cart are no longer available.')
        return redirect('store_home')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            if stock_errors:
                for err in stock_errors:
                    messages.error(request, err)
                return render(request, 'store/checkout.html', {'form': form, 'cart_items': cart_items, 'total': total})

            try:
                with transaction.atomic():
                    # Deduct quantities and place order
                    order = form.save(commit=False)
                    order.user = request.user
                    order.total_amount = total

                    # Determine payment status
                    if order.payment_method == 'online':
                        order.payment_status = 'paid'
                        order.status = 'confirmed'
                    else:
                        order.payment_status = 'pending'
                        order.status = 'confirmed'

                    order.save()

                    for item in cart_items:
                        prod = Product.objects.select_for_update().get(pk=item['product'].pk)
                        if prod.quantity < item['quantity']:
                            raise ValueError(f'Insufficient stock for {prod.name}')
                        prod.quantity -= item['quantity']
                        prod.save()

                        OrderItem.objects.create(
                            order=order,
                            product=prod,
                            product_name=prod.name,
                            quantity=item['quantity'],
                            price_at_purchase=prod.price,
                        )

                    # Empty the session cart
                    request.session['cart'] = {}
                    messages.success(request, f'🎉 Order #{order.pk} placed successfully!')
                    return redirect('order_detail', pk=order.pk)
            except ValueError as e:
                messages.error(request, str(e))
    else:
        # Pre-populate with user's details if available
        initial = {
            'full_name': request.user.get_full_name() or request.user.username,
        }
        try:
            initial['phone'] = request.user.profile.phone
            initial['shipping_address'] = request.user.profile.location
        except Exception:
            pass
        form = CheckoutForm(initial=initial)

    context = {
        'form': form,
        'cart_items': cart_items,
        'total': total,
        'stock_errors': stock_errors,
    }
    return render(request, 'store/checkout.html', context)


@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'store/order_detail.html', {'order': order})


@login_required
def download_receipt(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'store/receipt.html', {'order': order})


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product')
    return render(request, 'store/my_orders.html', {'orders': orders})

