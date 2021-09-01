from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import Category, Product
from django.core.paginator import Page, Paginator, EmptyPage, InvalidPage
from django.contrib.auth.models import Group, User
from .forms import SignUpForm
# Create your views here.


def Index(request):
    text_var ='This is my first django webapp'
    return HttpResponse(text_var)


#Categories
def allProductCat(request, c_slug=None):
    c_page = None
    products_list = None
    if c_slug != None:
        c_page = get_object_or_404(Category, slug=c_slug)
        products_list = Product.objects.filter(category=c_page, available=True)
    else:
        products_list = Product.objects.all().filter(available=True)
    
    """Pagination Code"""

    paginator = Paginator(products_list,3)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    try:
        products = paginator.page(page)
    except(EmptyPage, InvalidPage):
        products = paginator.page(paginator.num_pages)
        

    return render(request, 'shop/category.html', {'category':c_page, 'products':products})


def ProdCatDetail(request, c_slug, product_slug):
    try:
        product = Product.objects.get(category__slug=c_slug, slug=product_slug)
    except Exception as e:
        raise e
    return render(request, 'shop/product.html', {'product':product})



def signupView(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            signup_user = User.objects.get(username = username)
            customer_group  = Group.objects.get(name='Customers')
            customer_group.user_set.add(signup_user)
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html',{'form':form})        
            