from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from user_agents import parse
from short.helpers import get_user_locations, get_client_ip
from short.models import Urls, StatsUrl
import uuid
import csv
from django.contrib.auth.hashers import make_password


class ShortUrlService:
    def make_short(self, url_short_form):
        urls = Urls(original_url=url_short_form.data['original_url'] ,url_key=str(uuid.uuid4())[:8])
        if url_short_form.data['password']:
            urls.password = make_password(url_short_form.data['password'])
        urls.save()
        return urls


class UrlStatsService:
    def save_stats(self, request: WSGIRequest, urls: Urls):
        stats_urls_fields = {**self.__get_user_agent_fields(request), **self.__get_user_locations_data(request), **{
            'url': urls,
            'url_key': urls.url_key
        }}
        stats_url = StatsUrl(**stats_urls_fields)
        stats_url.save()
        return stats_url

    def export_stats(self,url_key):
        opts = StatsUrl._meta
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment;filename=url_stats.csv'
        writer = csv.writer(response)
        field_names = [field.name for field in opts.fields]
        writer.writerow(field_names)
        for obj in StatsUrl.objects.filter(url_key=url_key).order_by('-id'):
            writer.writerow([getattr(obj, field) for field in field_names])
        return response

    def __get_user_locations_data(self, request):
        ip_data = get_user_locations(get_client_ip(request))
        return {item: ip_data.all[item] for item in ip_data.all if hasattr(StatsUrl, item)}

    def __get_user_agent_fields(self, request):
        user_agent = parse(request.META['HTTP_USER_AGENT'])
        return {
            'browser': user_agent.get_browser(),
            'os': user_agent.get_os(),
            'device': user_agent.get_device(),
            'is_bot': user_agent.is_bot,
            'is_email_client': user_agent.is_email_client,
            'is_pc': user_agent.is_pc,
            'is_tablet': user_agent.is_tablet,
            'is_mobile': user_agent.is_mobile,
            'is_touch_capable': user_agent.is_touch_capable
        }

url_stats_service = UrlStatsService()
short_url_service = ShortUrlService()
