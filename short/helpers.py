import ipinfo
from django.conf import settings


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_user_locations(ip_address=None):
    ip_info_token = getattr(settings, "IPINFO_TOKEN", None)
    ip_info_settings = getattr(settings, "IPINFO_SETTINGS", {})
    ip_data = ipinfo.getHandler(ip_info_token, **ip_info_settings)
    ip_data = ip_data.getDetails(ip_address)
    return ip_data
