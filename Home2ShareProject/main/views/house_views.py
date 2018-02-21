from django.views import generic
from django.urls import reverse_lazy
from main.models import House

class HouseListView(generic.ListView):
    model = House
    paginate_by = 3

    def get_queryset(self):
        return House.objects.all()

class HouseDetailView(generic.DetailView):
    model = House
    slug_field = 'slug_name'
    # query_pk_and_slug = True

class HouseCreateView(generic.CreateView):
    model = House
    fields = ['name', 'country', 'city', 'street_name', 'street_number', 'description', 'room_quantity', 'person_quantity', 'price', 'image']
    success_url = reverse_lazy('house-list')

class HouseUpdateView(generic.UpdateView):
    model = House
    slug_field = 'slug_name'
    fields = ['name', 'country', 'city', 'street_name', 'street_number', 'description', 'room_quantity', 'person_quantity', 'price', 'image']
    success_url = reverse_lazy('house-list')

class HouseDeleteView(generic.DeleteView):
    model = House
    slug_field = 'slug_name'
    success_url = reverse_lazy('house-list')
