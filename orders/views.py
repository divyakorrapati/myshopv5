from django.shortcuts import render, redirect
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from .models import Order
from django.core.mail import send_mail
from django.http import HttpResponse
from django.template.loader import render_to_string, get_template
from .utils import render_to_pdf
from django.contrib.auth.decorators import login_required
from shop.models import Category
from django.core.mail import send_mail, EmailMessage


def order_create(request):
    categories = Category.objects.all()
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                        product=item['product'],
                                        price=item['price'],
                                        quantity=item['quantity'])
            # clear the cart
            cart.clear()
            order_created(request, order.id)
            # launch asynchronous task
            #set the order in the session
            request.session['order_id'] = order.id
            #redirect for payment
            return redirect (reverse('payment:process'))

    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form, 'categories':categories})

@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                  'admin/orders/order/detail.html',
                  {'order': order})

def order_created(request, order_id):
    email_success = 'false'
   #Task to send an e-mail notification when an order is successfully created.
    order = Order.objects.get(id=order_id)
    subject = 'V5 store order summary for Order nr. {}'.format(order.id)
    message = 'Dear {},\n\nYou have successfully placed an order.Your order id is {}.'.format(order.first_name,order.id)
    to_email_id = [order.email]
    context = {'order': order}
    #orderpdf =generate_order_pdf(request,order_id)
    orderFileName = 'OrderSummary_' + str(order_id) + '.pdf'
    msg = EmailMessage(subject, message, from_email="v5storein@gmail.com", to=[to_email_id])
    #msg.attach(orderFileName, orderpdf, 'application/pdf')
    msg.content_subtype = "html"
    msg.send()
    email_success = 'true'
    return render(request, 'orders/order/pdf.html', {'order': order,
                                                     'email_success': email_success})
@login_required
def cust_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                  'orders/order/detail.html',
                  {'order': order})
@login_required
def cust_order_pdf(request, order_id, context):
    order = get_object_or_404(Order, id=order_id)
    print(order.id, order.first_name)
    template = get_template('orders/order/pdf.html')
    context = {'order': order}
    html = template.render(context)
    pdf = render_to_pdf('orders/order/pdf.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = 'Summary_' + str(order.first_name+order.last_name) + '.pdf'
        content = "inline; filename='%s'" % (filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" % (filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("not found")



def generate_order_pdf(request, order_id):
        order = get_object_or_404(Order, id=order_id)
        print(order.id, order.first_name)
        template = get_template('orders/order/pdf.html')
        context = {
            'order': order
        }
        html = template.render(context)
        pdf = render_to_pdf('orders/order/pdf.html', context)
        if pdf:
         return pdf
        return pdf



def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    print(order.id, order.first_name)
    template = get_template('orders/order/pdf.html')
    context = {
         'order':order
        }
    html = template.render(context)
    pdf = render_to_pdf('orders/order/pdf.html',context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = 'Summary_' + str(order.id) + '.pdf'
        content = "inline; filename='%s'" % (filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" % (filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("not found")