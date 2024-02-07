from django.http import HttpResponse
from django.shortcuts import render
from .models.product import Product
from .models.category import Category
from .models.customer import Customer

def index(request):
    # Print the category_id to check if it's being extracted correctly
    products = None
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    print('Category ID:', categoryID)

    if categoryID:
        products = Product.get_all_by_categoryid(categoryID)
    else:
        products = Product.get_all()

    data = {
        'products': products,
        'categories': categories,
    }

    return render(request, 'index.html', data)


def signup(request):
    if request.method =='GET':
        return render(request,'signup.html')
    
    else:
        postData = request.POST
        firstName= postData.get('firstname')
        lastName= postData.get('lastname')
        email= postData.get('email')
        phone= postData.get('phone')
        address= postData.get('address')
        gender= postData.get('gender')
        password= postData.get('password')
        # MANDATORY CONDITIONS 
        
        print(firstName,lastName,email,phone,address,gender,password)
        customer = Customer(firstName=firstName,
                            lastName=lastName,
                            email=email,
                            phone=phone,
                            address=address,
                            gender=gender,
                            password=password)
        customer.register()
        return HttpResponse("Your account has been created")
    
