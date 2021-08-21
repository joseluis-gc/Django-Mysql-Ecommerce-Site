from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import Category, Product
# Create your views here.


def Index(request):
    text_var ='This is my first django webapp'
    return HttpResponse(text_var)


#Categories
def allProductCat(request, c_slug=None):
    c_page = None
    products = None
    if c_slug != None:
        c_page = get_object_or_404(Category, slug=c_slug)
        products = Product.objects.filter(category=c_page, available=True)
    else:
        products = Product.objects.all().filter(available=True)
    return render(request, 'shop/category.html', {'category':c_page, 'products':products})


def ProdCatDetail(request, c_slug, product_slug):
    try:
        product = Product.objects.get(category__slug=c_slug, slug=product_slug)
    except Exception as e:
        raise e
    return render(request, 'shop/product.html', {'product':product})
