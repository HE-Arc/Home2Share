from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.views import generic, View
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .forms import SignupForm
from .models import House

def index(request):
    context = {}
    return render(request, 'index.html', context)

class UserCreateView(generic.CreateView):
    model = User
    form_class = SignupForm
    success_url = '/'
    template_name = 'registration/user_form.html'

    def form_valid(self, form):
        user = form.save(commit=True)
        login(self.request, user)
        return super().form_valid(form)


class ProfileView(generic.DetailView):
    model = User
    slug_field = 'username'
    template_name = 'registration/user_detail.html'

class UpdateUserView(generic.UpdateView):
    model = User
    fields = ['username', 'email']
    slug_field = 'username'
    success_url = '/'
    template_name = 'registration/user_form.html'

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


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
