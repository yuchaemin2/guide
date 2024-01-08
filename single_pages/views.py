from django.shortcuts import render
from shop.models import Item, User

# Create your views here.
def home(request):
    recent_items = Item.objects.order_by('-pk')[:3]
    return render(
        request,
        'single_pages/home.html',
        {
            'recent_items': recent_items,
        }
    )

def company(request):
    return render(request, 'single_pages/company.html')