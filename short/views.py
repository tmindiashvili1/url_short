from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from django.views import View
from .forms import UrlShortForm
from .models import Urls, StatsUrl
from .services import short_url_service, url_stats_service
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import ListView
from django.urls import reverse


class ShortUrlView(View):
    def get(self, request):
        return render(request, 'short/index.html', {
            'url_short_form': UrlShortForm()
        })

    def post(self, request):
        url_short_form = UrlShortForm(request.POST)

        if url_short_form.is_valid():
            urls = short_url_service.make_short(url_short_form)
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
        if urls.password:
            return redirect('url:redirect-url-password-check', key=key)
        url_stats_service.save_stats(request, urls)
        return HttpResponseRedirect(urls.original_url)


class RedirectPasswordCheckView(View):
    def get(self, request, key):
        return render(request, 'short/url-password-check.html', {
            'url_key': key
        })

    def post(self, request, key):
        urls = get_object_or_404(Urls, url_key=key)
        if check_password(request.POST.get('password'),urls.password) is not True:
            return redirect('url:redirect-url-password-check', key=key)

        url_stats_service.save_stats(request, urls)
        return HttpResponseRedirect(urls.original_url)


class StatsUrlExportView(View):
    def post(self, request, key):
        return url_stats_service.export_stats(key)


class StatsUrlView(ListView):
    template_name = 'short/stats.html'
    model = StatsUrl
    paginate_by = 10
    context_object_name = 'url_stats'

    def get_queryset(self):
        base_query = super().get_queryset()
        data = base_query.filter(url_key=self.request.GET.get('url_key', None)).order_by('-id')
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_key'] = self.request.GET.get('url_key', '')
        return context
