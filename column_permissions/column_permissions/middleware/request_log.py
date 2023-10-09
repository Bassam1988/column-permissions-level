
"""
Middleware to log `*/api/*` requests and responses.
"""
import socket
import time
import json
import logging
from datetime import datetime

#from easy_timezones.utils import get_ip_address_from_request, is_valid_ip, is_local_ip

request_logger = logging.getLogger(__name__)

"""
import geocoder

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
        ip_location = geocoder.ip(f"{ip}")
        ip_location = geocoder.ip("me")
        print(ip_location.city)
        # you can get city such as "New York"
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip




def get_ip_address_from_request(request):
    ip = get_ip_address_from_request(request)
    try:
        if is_valid_ip(ip):
            geoip_record = IpRange.objects.by_ip(ip)
    except IpRange.DoesNotExist:
        return None
   
    PRIVATE_IPS_PREFIX = ('10.', '172.', '192.', '127.')
    ip_address = ''
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', '')
    if x_forwarded_for and ',' not in x_forwarded_for:
        if not x_forwarded_for.startswith(PRIVATE_IPS_PREFIX) and is_valid_ip(x_forwarded_for):
            ip_address = x_forwarded_for.strip()
    else:
        ips = [ip.strip() for ip in x_forwarded_for.split(',')]
        for ip in ips:
            if ip.startswith(PRIVATE_IPS_PREFIX):
                continue
            elif not is_valid_ip(ip):
                continue
            else:
                ip_address = ip
                break
    if not ip_address:
        x_real_ip = request.META.get('HTTP_X_REAL_IP', '')
        if x_real_ip:
            if not x_real_ip.startswith(PRIVATE_IPS_PREFIX) and is_valid_ip(x_real_ip):
                ip_address = x_real_ip.strip()
    if not ip_address:
        remote_addr = request.META.get('REMOTE_ADDR', '')
        if remote_addr:
            if not remote_addr.startswith(PRIVATE_IPS_PREFIX) and is_valid_ip(remote_addr):
                ip_address = remote_addr.strip()
    if not ip_address:
        ip_address = '127.0.0.1'
    return ip_address
"""


class RequestLogMiddleware:
    """Request Logging Middleware."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.monotonic()
        created_time = datetime.now()
        log_data = {
            "remote_address": request.META["REMOTE_ADDR"],
            "server_hostname": socket.gethostname(),
            "request_method": request.method,
            "request_path": request.get_full_path(),
        }
        log_data["created_time"] = created_time

        # Only logging "*/api/*" patterns
        if "/api/" in str(request.get_full_path()):
            req_body = json.loads(request.body.decode(
                "utf-8")) if request.body else {}
            if "password" in req_body.keys():
                req_body.pop("password")

            log_data["request_body"] = req_body
        
        #api_class=self.process_view(request)
        # api_class=request.view
        #log_data["api_class"] =request.content_type


        # request passes on to controller
        response = self.get_response(request)

        # add runtime to our log_data
        if response and response["content-type"] == "application/json":
            response_body = json.loads(response.content.decode("utf-8"))
            log_data["response_body"] = response_body
        end_time = time.monotonic()
        log_data["run_time"] = end_time - start_time

        request_logger.info(msg=log_data)

        return response

    #Log unhandled exceptions as well
    # def process_exception(self, request, exception):
        
    #     request_logger.exception("Unhandled Exception: " + str(exception))
    #     raise exception
