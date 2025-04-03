# payments/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import BillingAddressForm
from apps.orders.models import Order
from .models import Payment
import stripe
from django.conf import settings

# Replace with your actual Stripe secret key from settings
stripe.api_key = settings.STRIPE_SECRET_KEY  # Ideally, use settings.STRIPE_SECRET_KEY

@login_required
def checkout_view(request):
    if request.method == 'POST':
        billing_form = BillingAddressForm(request.POST, prefix='billing')
        shipping_form = BillingAddressForm(request.POST, prefix='shipping')
        if billing_form.is_valid() and shipping_form.is_valid():
            # Save billing address
            billing_address = billing_form.save(commit=False)
            billing_address.user = request.user
            billing_address.address_type = 'B'  # Billing
            billing_address.save()

            # Save shipping address
            shipping_address = shipping_form.save(commit=False)
            shipping_address.user = request.user
            shipping_address.address_type = 'S'  # Shipping
            shipping_address.save()

            try:
                # Get the user's pending order
                order = Order.objects.get(user=request.user, ordered=False)
                order.billing_address = billing_address
                order.shipping_address = shipping_address
                order.save()

                # Process payment with Stripe
                stripe_token = request.POST.get('stripeToken')
                if stripe_token:
                    try:
                        charge = stripe.Charge.create(
                            amount=int(order.get_total_price * 100),  # Convert to cents
                            currency='usd',  # Adjust currency as needed (e.g., 'kzt' for Kazakhstani Tenge)
                            source=stripe_token,
                            description=f'Charge for order {order.id}'
                        )
                        # Create payment record
                        payment = Payment.objects.create(
                            stripe_charge_id=charge.id,
                            user=request.user,
                            amount=order.get_total_price,
                            status='completed'
                        )
                        # Update order
                        order.payment = payment
                        order.ordered = True
                        order.save()
                        messages.success(request, 'Your order was successfully placed!')
                        return redirect('order_success')  # Define this URL later
                    except stripe.error.StripeError as e:
                        messages.error(request, f'Payment error: {str(e)}')
                else:
                    messages.error(request, 'Invalid payment information')
            except Order.DoesNotExist:
                messages.error(request, 'No pending order found.')
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        billing_form = BillingAddressForm(prefix='billing')
        shipping_form = BillingAddressForm(prefix='shipping')

    # Get the current order for display (e.g., total price)
    try:
        order = Order.objects.get(user=request.user, ordered=False)
    except Order.DoesNotExist:
        order = None

    context = {
        'billing_form': billing_form,
        'shipping_form': shipping_form,
        'order': order,
        'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
    }
    return render(request, 'payments/checkout.html', context)