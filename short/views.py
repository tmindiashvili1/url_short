from django.shortcuts import render
from django.views import View
from .forms import UrlShortForm
from .models import Urls,StatsUrl
from .services import short_url_service, url_stats_service
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import ListView

class ShortUrlView(View):
    def get(self, request):
        return render(request, 'short/index.html', {
            'url_short_form': UrlShortForm()
        })

    def post(self, request):
        url_short_form = UrlShortForm(request.POST)

        if url_short_form.is_valid():
            urls = short_url_service.make_short(url_short_form.data['original_url'])
            return render(request, 'short/index.html', {
                'url_short_form': url_short_form,
                'urls': urls
            })

        return render(request, 'short/index.html', {
            'url_short_form': url_short_form
        })


class RedirectUrlView(View):
    def get(self, request, key):
        urls = get_object_or_404(Urls, url_key=key)
        url_stats_service.save_stats(request, urls)
        return HttpResponseRedirect(urls.original_url)


class StatsUrlView(ListView):
    template_name = 'short/stats.html'
    model = StatsUrl
    paginate_by = 10
    context_object_name = 'url_stats'

    def get_queryset(self):
        base_query = super().get_queryset()
        data = base_query.order_by('-id')
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_key'] = self.request.GET.get('url_key','')
        return context
