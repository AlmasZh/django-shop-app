from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'products/index.html')

def manclothes(request):
    return render(request, 'products/Manclothes.html')  

def categories(request):
    return render(request,'products/categories.html')
def register(request):
    return render(request,'products/Register.html')
def personal(request):
    return render(request,'products/personal.html')
def itempage(request):
    return render(request,'products/itempage.html')
def girlclothes(request):
    return render(request,'products/Girlclothes.html')
def questionnaire(request):
    return render(request,'products/questionnaire.html')
def clothesadd(request):
    return render(request,'products/clothesadd.html')
