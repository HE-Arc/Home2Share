from django.shortcuts import render
from django.views import generic, View

from.models import House

def index(request):
    context = {}
    return render(request, 'main/index.html', context)

class HouseListView(generic.ListView):
    model = House

    def get_queryset(self):
        return House.objects.all()

class HouseDetailView(generic.DetailView):
    model = House
