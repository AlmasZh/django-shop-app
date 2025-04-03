# payments/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from apps.cart.models import Cart
from apps.orders.models import Order, OrderItem
from .models import BillingAddress
from .forms import BillingAddressForm

@login_required
def order_create_view(request):
    cart = Cart.objects.get(user=request.user)
    if not cart.items.exists():
        messages.error(request, 'Your cart is empty.')
        return redirect('products:personal_cart')

    if request.method == 'POST':
        billing_form = BillingAddressForm(request.POST, prefix='billing')
        shipping_form = BillingAddressForm(request.POST, prefix='shipping')
        if billing_form.is_valid() and shipping_form.is_valid():
            # Save billing address
            billing_address = billing_form.save(commit=False)
            billing_address.user = request.user
            billing_address.address_type = 'B'
            billing_address.save()

            # Save shipping address
            shipping_address = shipping_form.save(commit=False)
            shipping_address.user = request.user
            shipping_address.address_type = 'S'
            shipping_address.save()

            # Create new order
            order = Order.objects.create(
                user=request.user,
                ordered=False,
                delivery_status='pending',
                billing_address=billing_address,
                shipping_address=shipping_address
            )

            # Copy cart items to order items
            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity
                )

            # Clear the cart
            cart.items.all().delete()

            messages.success(request, 'Order created successfully! Proceed to payment.')
            return redirect('payments:process_payment', order_id=order.id)
    else:
        billing_form = BillingAddressForm(prefix='billing')
        shipping_form = BillingAddressForm(prefix='shipping')

    context = {
        'billing_form': billing_form,
        'shipping_form': shipping_form,
        'cart': cart,
    }
    return render(request, 'payments/order_create.html', context)


# payments/views.py
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from apps.orders.models import Order
from .models import Payment
from django.contrib import messages

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def payment_process_view(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user, ordered=False)
    if request.method == 'POST':
        token = request.POST.get('stripeToken')
        amount_in_tigs = int(order.get_total_price * 100)
        try:
            charge = stripe.Charge.create(
                amount=amount_in_tigs,  # In KZT (whole units)
                currency='kzt',
                description=f'Order {order.id}',
                source=token,
            )
            Payment.objects.create(
                order=order,
                stripe_charge_id=charge.id,
                amount=order.get_total_price
            )
            order.ordered = True
            order.delivery_status = 'processing'
            order.save()
            messages.success(request, 'Payment successful!')
            return redirect('payments:order_success')
        except stripe.error.StripeError as e:
            messages.error(request, f'Payment error: {str(e)}')
            return redirect('payments:process_payment', order_id=order.id)
    context = {
        'order': order,
        'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
    }
    return render(request, 'payments/payment_process.html', context)