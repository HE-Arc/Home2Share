from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.contrib.auth.models import User
from main.forms.SignupForm import SignupForm
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from main.tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.mixins import LoginRequiredMixin ,UserPassesTestMixin


def account_activation_sent(request):
    context = {}
    return render(request, 'registration/account_activation_sent.html', context)


def activate(request, uidb64, token):
    try:
        #get the uid based on the token
        uid = urlsafe_base64_decode(uidb64)
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    #test if the user is valid and activate his account
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('index')
    else:
        return render(request, 'registration/account_activation_invalid.html',context)

class UserCreateView(generic.CreateView):
    """User Creation Page"""
    name = "create"
    model = User
    form_class = SignupForm
    success_url = '/account_activation_sent'
    template_name = 'registration/user_form.html'

    #form validation and mail sending for the account activation
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        subject = 'Activate Your Home2Share Account'
        message = render_to_string('registration/account_activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': force_text(urlsafe_base64_encode(force_bytes(user.pk))),
            'token': account_activation_token.make_token(user),
        })
        user.email_user(subject, message,from_email='Webmaster@Home2Share.com')
        return super().form_valid(form)


class ProfileView(generic.DetailView):
    """User profile page"""
    model = User
    slug_field = 'username'
    template_name = 'registration/user_detail.html'


class UpdateUserView(UserPassesTestMixin, LoginRequiredMixin, generic.UpdateView):
    """User information update page"""
    model = User
    name= "update"
    fields = ['username', 'email']
    slug_field = 'username'
    success_url = '/'
    template_name = 'registration/user_form.html'

    #test if the user try to update the informations of another user
    def test_func(self):
        self.object = self.get_object()
        return self.object.username == self.request.user.username


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')
