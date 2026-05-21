from django.http import HttpResponse
from django.shortcuts import render

# # Create your views here.
# def home(request):
#     return render(request, 'home.html')

def home(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        return HttpResponse(f"Hello, {name}!")

    return render(request, "home.html")