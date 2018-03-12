from django.views import generic
from django.urls import reverse_lazy, reverse
from main.models import House, Comment
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404,redirect
from django.views.generic.edit import FormView
from main.forms.CommentForm import CommentForm
from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#Use UsersPassTestMixin a la place de dispatch
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# -------------------------------------------
# USER
# -------------------------------------------

class UserHouseListView(UserPassesTestMixin, generic.ListView):
    model = House
    paginate_by = 3
    name = 'profile-house-list'

    def get_queryset(self):
        query_houses = House.objects.filter(user__username = self.kwargs['slug']).prefetch_related('user')

        # if not query_user.count():
        #     raise Http404("No User matches the given query.")

        return query_houses

    def test_func(self):
        return self.kwargs['slug'] == self.request.user.username

    # def dispatch(self, request, *args, **kwargs):
    #     if self.kwargs['slug'] == request.user.username:
    #         return super(UserHouseListView, self).dispatch(request, *args, **kwargs)
    #     else:
    #         return redirect('/')


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(house__id=self.object.pk).prefetch_related('user')
        context['form'] = CommentForm()
        return context

class HouseCreateView(LoginRequiredMixin, generic.CreateView):
    model = House
    fields = ['name', 'country', 'city', 'street_name', 'street_number', 'description', 'room_quantity', 'person_quantity', 'price', 'image']
    success_url = reverse_lazy('house-list')
    name = 'new-house'

    def form_valid(self, form):
        house = form.save(commit = False)
        house.user = self.request.user
        house.save()
        return super().form_valid(form)

class HouseUpdateView(UserPassesTestMixin, generic.UpdateView):
    model = House
    slug_field = 'slug_name'
    fields = ['name', 'country', 'city', 'street_name', 'street_number', 'description', 'room_quantity', 'person_quantity', 'price', 'image']
    success_url = reverse_lazy('house-list')
    name = 'update-house'

    def test_func(self):
        self.object = self.get_object()
        return self.object.user.username == self.request.user.username

    # def dispatch(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     if self.object.user.username == request.user.username:
    #         return super(HouseUpdateView, self).dispatch(request, *args, **kwargs)
    #     else:
    #         return redirect('/')

class HouseDeleteView(UserPassesTestMixin, generic.DeleteView):
    model = House
    slug_field = 'slug_name'
    success_url = reverse_lazy('house-list')

    def test_func(self):
        self.object = self.get_object()
        return self.object.user.username == self.request.user.username

    # def dispatch(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     if self.object.user.username == request.user.username:
    #         return super(HouseDeleteView, self).dispatch(request, *args, **kwargs)
    #     else:
    #         return redirect('/')


class HouseCommentCreateView(LoginRequiredMixin, SingleObjectMixin, FormView):
    template_name = 'main/house_detail.html'
    slug_field = 'slug_name'
    form_class = CommentForm
    model = House

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            comment = Comment()
            comment.body = form.cleaned_data['body']
            comment.user = request.user
            comment.house = self.object
            comment.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('house-detail', kwargs={'slug': self.object.slug_name})

class CommentUpdateView(UserPassesTestMixin, generic.UpdateView):
    model = Comment
    fields = ['body']

    def get_success_url(self):
        return reverse('house-detail', kwargs={'slug': self.object.house.slug_name})

    def test_func(self):
        self.object = self.get_object()
        return self.object.user.username == self.request.user.username

    # def dispatch(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     if self.object.user.username == request.user.username:
    #         return super(CommentUpdateView, self).dispatch(request, *args, **kwargs)
    #     else:
    #         return redirect('/')

class CommentDeleteView(UserPassesTestMixin, generic.DeleteView):
    model = Comment
    def get_success_url(self):
        return reverse('house-detail', kwargs={'slug': self.object.house.slug_name})

    def test_func(self):
        self.object = self.get_object()
        return self.object.user.username == self.request.user.username

    # def dispatch(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     if self.object.user.username == request.user.username:
    #         return super(CommentDeleteView, self).dispatch(request, *args, **kwargs)
    #     else:
    #         return redirect('/')
