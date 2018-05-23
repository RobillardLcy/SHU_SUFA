import os
import requests
import ConfigParser
from sufa.settings import BASE_DIR


def verification_code_cer(request):

    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    config_file = os.path.join(BASE_DIR, "sufa.cnf")
    cf = ConfigParser.ConfigParser()
    cf.read(config_file)

    aid = cf.get('tencent', 'aid')
    app_secret_key = cf.get('tencent', 'app_secret_key')

    ticket = request.data.get('ticket')
    randstr = request.dat.get('randstr')
    user_ip = get_client_ip(request)
    url = 'https://ssl.captcha.qq.com/ticket/verify'

    params = 'aid=' + aid + '&AppSecretKey=' + app_secret_key + '&Ticket=' + ticket + \
             '&Randstr=' + randstr + '&UserIP=' + user_ip

    requests.get(url, params)
