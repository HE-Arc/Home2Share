from django.views import generic
from django.urls import reverse_lazy
from main.models import House
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

# -------------------------------------------
# USER
# -------------------------------------------

class UserHouseListView(generic.ListView):
    model = House
    paginate_by = 3
    template_name = 'main/user_house_list.html'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs['slug'])
        return House.objects.filter(user=user.pk)


# -------------------------------------------
# PUBLIC
# -------------------------------------------
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

    def form_valid(self, form):
        house = form.save(commit = False)
        house.user = self.request.user
        house.save()
        return super().form_valid(form)

class HouseUpdateView(generic.UpdateView):
    model = House
    slug_field = 'slug_name'
    fields = ['name', 'country', 'city', 'street_name', 'street_number', 'description', 'room_quantity', 'person_quantity', 'price', 'image']
    success_url = reverse_lazy('house-list')

class HouseDeleteView(generic.DeleteView):
    model = House
    slug_field = 'slug_name'
    success_url = reverse_lazy('house-list')
