from django.shortcuts import render
from main.models import House, Comment, Evaluation
from django.db.models import Count, Avg

def index(request):
    context = {}

    # Recent houses
    qs = House.objects.order_by('-pub_date')[:3]
    context['recent_houses'] = qs

    # Random houses
    qs = House.objects.order_by('?')[:3]
    context['random_houses'] = qs

    # Best rated Houses
    qs = House.objects.annotate(average_stars=Avg('evaluation__stars')).order_by('-average_stars')[:3]
    context['best_rated_houses'] = qs

    # Most commented Houses
    qs = House.objects.annotate(num_comments=Count('comments')).order_by('-num_comments')[:3]
    context['most_commented_houses'] = qs

    return render(request, 'index.html', context)
