from django.core.exceptions import ObjectDoesNotExist
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from shop.models import Product
from . models import Cart, CartItem
import stripe
from django.conf import settings
from order_app.models import Order, orderItem
from django.template.loader import get_template
from django.core.mail import EmailMessage

# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )    
        cart.save()
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart
        )        
        cart_item.save()
    return redirect ('cart_app:cart_detail')





def cart_detail(request, total=0, counter=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        for cart_item in cart_items:
            total+= (cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity
            print('name: ' + cart_item.product.name)
    except ObjectDoesNotExist :
        pass


    """stripe settings"""

    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe_total = int(total * 100)
    description = 'My Shop - Ner Order'
    data_key = settings.STRIPE_PUBLISHABLE_KEY

    if request.method == 'POST':

        try:
                token = request.POST['stripeToken']
                email = request.POST['stripeEmail']

                billingName = request.POST['stripeBillingName']
                billingAddress1 = request.POST['stripeBillingAddressLine1']
                billingcity = request.POST['stripeBillingAddressCity']
                billingPostcode = request.POST['stripeBillingAddressZip']
                billingCountry = request.POST['stripeBillingAddressCountryCode']
                shippingName = request.POST['stripeShippingName']
                shippingAddress1 = request.POST['stripeShippingAddressLine1']
                shippingcity = request.POST['stripeShippingAddressCity']
                shippingPostcode = request.POST['stripeShippingAddressZip']
                shippingCountry = request.POST['stripeShippingAddressCountryCode']




                customer = stripe.Customer.create(
						email=email,
						source = token
				)
                charge = stripe.Charge.create(
						amount=stripe_total,
						currency="usd",
						description=description,
						customer=customer.id
				)


                ''' Creating order '''
                try:
                    order_details = Order.objects.create(
                            token = token,
                            total = total,
                            email_address = email,
                            billingName = billingName,
                            billingAddress1 = billingAddress1,
                            billingCity = billingcity,
                            billingPostCode = billingPostcode,
                            billingCountry = billingCountry,
                            ShippingName = shippingName,
                            ShippingAddress1 = shippingAddress1,
                            ShippingCity = shippingcity,
                            ShippingPostCode = shippingPostcode,
                            ShippingCountry = shippingCountry
                        )
                    order_details.save()

                    for order_item in cart_items:
                        #print('name-item-order: ' + cart_item.product.name)
                        oi = orderItem.objects.create(
                                product = order_item.product.name,
                                quantity = order_item.quantity,
                                price = order_item.product.price,
                                order = order_details
                        )   
                        
                        oi.save()

                        '''Reduce stock when order is placed or saved'''
                        products = Product.objects.get(id=order_item.product.id)
                        products.stock = int(order_item.product.stock - order_item.quantity)
                        products.save()
                        order_item.delete()
                        '''The terminal will print this message when the order is saved'''
                        print('The order has been created')
                    
                    try:
                        #sending an email with the order details.
                        sendEmail(order_details.id)
                        print('The email has been sent to the customer')
                    except IOError as e:
                        return e
                                
                    return redirect('order_app:thanks', order_details.id)

                except ObjectDoesNotExist:
                    pass


                ''' Creating order end'''
        except stripe.error.CardError as e:
            return False,e



    """stripe settings end"""
    return render(request, 'cart.html', dict(cart_items = cart_items, total=total, counter=counter, data_key=data_key, stripe_total=stripe_total, description=description))


def cart_remove(request, product_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(cart=cart, product=product)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart_app:cart_detail')    

def full_remove(request, product_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(cart=cart, product=product)
    cart_item.delete()
    return redirect('cart_app:cart_detail')    



def sendEmail(order_id):
    transaction = Order.objects.get(id=order_id)
    order_items = orderItem.objects.filter(order=transaction)
    try:
        #sending email order
    	subject = "Perfect Cushion Store - New Order #{}".format(transaction.id)
    	to = ['{}'.format(transaction.email_address)]
    	from_email = "orders@perfectcushionstore.com"
    	order_information = {
    	'transaction' : transaction,
    	'order_items' :	order_items
    	}
    	message = get_template('email/email.html').render(order_information)
    	msg = EmailMessage(subject, message, to=to, from_email=from_email)
    	msg.content_subtype = 'html'
    	msg.send()
    except IOError as e:
    	return e









def checkout(request):
    
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        for cart_item in cart_items:
            total+= (cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity
    except ObjectDoesNotExist :
        pass

    return render(request, 'cart.html', dict(cart_items = cart_items, total=total, counter=counter))

