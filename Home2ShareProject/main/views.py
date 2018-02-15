from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, SignupForm
from django.views import generic, View
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from.models import House

def index(request):
    context = {}
    return render(request, 'index.html', context)

class UserCreateView(generic.CreateView):
    model = User
    form_class = SignupForm
    success_url = '/'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        login(self.request, user)
        return super().form_valid(form)

class LoginView(generic.FormView):
    template_name = 'auth/login.html'
    form_class = LoginForm
    success_url = '/'


    def form_valid(self, form):
        username=form.cleaned_data['username']
        password=form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            # the password verified for the user
            if user.is_active:
                print("User is valid, active and authenticated")
                login(self.request, user)
            else:
                print("The password is valid, but the account has been disabled!")
        else:
            # the authentication system was unable to verify the username and password
            print("The username and password were incorrect.")
        return super().form_valid(form)

class ProfileView(generic.DetailView):
    model = User
    slug_field = 'username'

class UpdateUserView(generic.UpdateView):
    model = User
    fields = ['username', 'email']
    slug_field = 'username'

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


class HouseListView(generic.ListView):
    model = House
    paginate_by = 2

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
