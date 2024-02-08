from django.http import HttpResponse
from django.shortcuts import render, redirect
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
    if request.method == 'GET':
        return render(request, 'signup.html')
    
    else:
        postData = request.POST
        firstName = postData.get('firstname')
        lastName = postData.get('lastname')
        email = postData.get('email')
        phone = postData.get('phone')
        address = postData.get('address')
        gender = postData.get('gender')
        password = postData.get('password')
        value = {
            'firstName': firstName,
            'lastName': lastName,
            'email': email,
            'phone': phone,
            'address': address
        }

        # MANDATORY CONDITIONS 
        print(firstName, lastName, email, phone, address, gender, password)
        
        customer = Customer(
            firstName=firstName,
            lastName=lastName,
            email=email,
            phone=phone,
            address=address,
            gender=gender,
            password=password
        )
        customer.register()
 # JavaScript code to show a pop-up and redirect to the homepage
        popup_script = """
            <script>
                alert('Signup successful!'); // You can customize this message
                window.location.href = '/';  // Change this URL to match your homepage URL
            </script>
        """
        
        return HttpResponse(popup_script + '<script>window.location.href = "/homepage";</script>')

        # If you want to pass the 'value' context to the template, uncomment the line below
        # return render(request, 'signup.html', {'value': value})
