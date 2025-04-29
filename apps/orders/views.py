from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Order, OrderStatusHistory

@login_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        new_status = request.POST.get('new_status')
        valid_statuses = dict(Order.DELIVERY_STATUS_CHOICES)
        # if str(new_status) not in valid_statuses:
        # if new_status and new_status.strip().lower() in valid_statuses:
            # return redirect('')  # Replace with your error page URL

        # Manager actions
        print('User:', request.user)
        print('Order:', hasattr(request.user, 'is_manager'))
        if (hasattr(request.user, 'is_courier') and request.user.is_courier) or  request.user.is_superuser: 
            if order.delivery_status == 'processing' and new_status == 'shipped':
                order.delivery_status = new_status
                OrderStatusHistory.objects.create(order=order, status=new_status)
                order.save()
            elif order.delivery_status == 'shipped' and new_status == 'delivered':
                order.delivery_status = new_status
                OrderStatusHistory.objects.create(order=order, status=new_status)
                order.save()
            # else:
                # return redirect('error_page')  # Invalid transition
        # User actions (cancellation)
        elif request.user == order.user:
            if order.delivery_status in ('pending', 'processing') and new_status == 'cancelled':
                order.delivery_status = new_status
                OrderStatusHistory.objects.create(order=order, status=new_status)
                order.save()
            else:
                return redirect('products:personal_orders')  # Not allowed
        else:
            return redirect('products:personal_orders')  # Not authorized

        return redirect('products:personal_orders')  # Replace with your orders page URL
    return redirect('products:personal_orders')  # GET requests not allowed