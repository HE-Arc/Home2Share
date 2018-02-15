from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.views import generic, View
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .forms import SignupForm
from .models import House
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site

def index(request):
    context = {}
    return render(request, 'index.html', context)

def account_activation_sent(request):
    context = {}
    return render(request, 'registration/account_activation_sent.html', context)

def activate(request, uidb64, token):
    context={'id' : uidb64[2:-1]}
    try:
        # pour enlever ce b''
        uidb64 = uidb64[2:-1]
        uid = urlsafe_base64_decode(uidb64)
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None


    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('index')
    else:
        return render(request, 'registration/account_activation_invalid.html',context)

class UserCreateView(generic.CreateView):
    model = User
    form_class = SignupForm
    success_url = '/account_activation_sent'
    template_name = 'registration/user_form.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        subject = 'Activate Your Home2Share Account'
        message = render_to_string('registration/account_activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        print(urlsafe_base64_encode(user.pk))
        user.email_user(subject, message)
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
