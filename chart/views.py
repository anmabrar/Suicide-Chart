from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Country, Year, SuicideCase


# Create your views here.
class Index(generic.ListView):
    model = Country
    template_name = 'index.html'


class SuicideByCountry(generic.View):
    def get(self, *args, **kwargs):
        country = get_object_or_404(Country, name=kwargs.get('name'))
        qs = list(SuicideCase.objects.filter(country= country).values_list("year__name","cases"))
        context = {
            'country': country,
            'qs': qs
        }
        return render(self.request, 'chart.html', context)
