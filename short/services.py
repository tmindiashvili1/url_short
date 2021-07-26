from django.core.handlers.wsgi import WSGIRequest
from user_agents import parse
from short.helpers import get_user_locations, get_client_ip
from short.models import Urls, StatsUrl
import uuid


class ShortUrlService:
    def make_short(self, original_url):
        urls = Urls(original_url=original_url, url_key=str(uuid.uuid4())[:8])
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
