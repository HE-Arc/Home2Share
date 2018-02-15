from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, SignupForm
from django.views import generic, View
from django.contrib.auth.models import User

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
