from django.views import generic
from django.urls import reverse_lazy, reverse
from main.models import House, Comment, Evaluation
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404,redirect
from django.views.generic.edit import FormView
from main.forms.CommentForm import CommentForm
from main.forms.EvaluationForm import EvaluationForm
from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponseForbidden, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.db.models import Count, Avg

import json

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#Use UsersPassTestMixin a la place de dispatch
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# -----------------------------------------------------------------------------
#                                    HOUSES
# -----------------------------------------------------------------------------

class UserHouseListView(generic.ListView):
    """ Houses List by User """
    model = House
    paginate_by = 6
    name = 'profile-house-list'

    def get_queryset(self):
        query_houses = House.objects.filter(user__username = self.kwargs['slug']).prefetch_related('user')

        # if not query_user.count():
        #     raise Http404("No User matches the given query.")

        return query_houses

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.kwargs['slug']
        return context


class HouseListView(generic.ListView):
    """ Houses List ordered by date """
    model = House
    paginate_by = 6

    def get_queryset(self):
        return House.objects.select_related('user').order_by('-pub_date').all()

class HouseDetailView(generic.DetailView):
    """ House Detail Page"""
    model = House
    slug_field = 'slug_name'

    def get_queryset(self):
        return House.objects.select_related('user').prefetch_related('comment_set', 'comment_set__user').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Evaluations about this house
        evaluations = self.object.evaluation_set.all()

        # Evaluations containing this user
        context['evaluation'] = evaluations.filter(user__id=self.request.user.pk).first()  # Evaluation.objects.filter(house__id=self.object.pk, user__id=self.request.user.pk).first()
        # Forms
        context['formComments'] = CommentForm()
        context['formEvaluation'] = EvaluationForm()
        # Vote Count
        context['vote_count'] = evaluations.count()
        # Average
        context['average_evaluation'] = self.object.evaluation_set.aggregate(stars=Avg('stars'))

        return context

class HouseCreateView(LoginRequiredMixin, generic.CreateView):
    """ Houses Creation Page """
    model = House
    fields = ['name', 'country', 'city', 'street_name', 'street_number', 'description', 'room_quantity', 'person_quantity', 'price', 'image']
    success_url = reverse_lazy('house-list')
    name = 'new-house'

    def get_success_url(self):
        return reverse('house-detail', kwargs={'slug': self.object.slug_name})

    def form_valid(self, form):
        house = form.save(commit = False)
        house.user = self.request.user
        house.save()
        return super().form_valid(form)

class HouseUpdateView(UserPassesTestMixin, generic.UpdateView):
    """ House Update Page """
    model = House
    slug_field = 'slug_name'
    fields = ['name', 'country', 'city', 'street_name', 'street_number', 'description', 'room_quantity', 'person_quantity', 'price', 'image']
    name = 'update-house'

    def get_success_url(self):
        return reverse('house-detail', kwargs={'slug': self.object.slug_name})

    def test_func(self):
        self.object = self.get_object()
        return self.object.user.username == self.request.user.username


class HouseDeleteView(UserPassesTestMixin, generic.DeleteView):
    """ House Delete Page"""
    model = House
    slug_field = 'slug_name'
    success_url = reverse_lazy('house-list')

    def test_func(self):
        self.object = self.get_object()
        return self.object.user.username == self.request.user.username


# -----------------------------------------------------------------------------
#                            COMMENTS ON HOUSES
# -----------------------------------------------------------------------------

class HouseCommentCreateView(LoginRequiredMixin, SingleObjectMixin, FormView):
    """ Comment Creation on House """
    template_name = 'main/house_detail.html'
    slug_field = 'slug_name'
    form_class = CommentForm
    model = House

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        form = self.get_form()

        # Form validation
        if form.is_valid():
            # Comment creation and completion
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
    """ Comment Update Page """
    model = Comment
    fields = ['body']

    def get_success_url(self):
        return reverse('house-detail', kwargs={'slug': self.object.house.slug_name})

    def test_func(self):
        self.object = self.get_object()
        return self.object.user.username == self.request.user.username


class CommentDeleteView(UserPassesTestMixin, generic.DeleteView):
    """ Comment Delete Page """
    model = Comment

    def get_success_url(self):
        return reverse('house-detail', kwargs={'slug': self.object.house.slug_name})

    def test_func(self):
        self.object = self.get_object()
        return self.object.user.username == self.request.user.username

# -----------------------------------------------------------------------------
#                               SEARCH HOUSES
# -----------------------------------------------------------------------------

class SearchHouseView(generic.ListView):
    """ Search Houses """
    template_name = 'main/house_list.html'
    model = House
    paginate_by = 3

    def get_queryset(self):
        try:
            name = self.request.GET.get('name')
        except:
            name = ''
        if (name != ''):
            object_list = self.model.objects.filter(name__icontains = name)
        else:
            object_list = []
        return object_list

# -----------------------------------------------------------------------------
#                               EVALUATIONS
# -----------------------------------------------------------------------------

def update_rating(request):
    if request.method == 'POST':
        # Get info transmitted
        house_id = request.POST['house_id']
        house_slug = request.POST['house_slug']
        stars = int(request.POST['stars'])

        house = House.objects.filter(pk=house_id).first()

        # Get evaluation from auth user and house from the page
        evaluation = Evaluation.objects.filter(house__id=house_id, user__id=request.user.pk).first()

        # Create a new eval if there's not one yet
        if not evaluation:
            evaluation = Evaluation()

        change_validated = False
        # To be sure to receive a correct amount of stars
        if(stars <= 5 and stars >= 1):
            evaluation.stars = stars
            evaluation.user = request.user
            evaluation.house = house
            evaluation.save()
            change_validated = True

        # Ajax response with validation state, new average stars and number of votes for this house
        response = {
            'change_validated' : change_validated,
            'average_evaluation' : list(Evaluation.objects.filter(house__id=house_id).aggregate(stars=Avg('stars')).values())[0],
            'vote_count' : Evaluation.objects.filter(house__id=house_id).count()
        }

        return HttpResponse(json.dumps(response), content_type='application/json')
