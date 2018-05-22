import os
import random
import ConfigParser
from urllib.parse import urlencode
from sufa.settings import BASE_DIR
from yunpian_python_sdk.model import constant as YC
from yunpian_python_sdk.ypclient import YunpianClient


def send_mobile_verification_code(mobile, request):
    code = random.randint(100000, 999999)
    request.session['mobile_code'] = code
    request.session.set_expire(300)

    config_file = os.path.join(BASE_DIR, "sufa.cnf")
    cf = ConfigParser.ConfigParser()
    cf.read(config_file)

    apikey = cf.get("yunpian", "apikey")
    tpl_value = {'#code#': str(code)}
    param = {YC.MOBILE: mobile, YC.TPL_ID: 1, YC.TPL_VALUE: urlencode(tpl_value)}
    client = YunpianClient(apikey=apikey)
    r = client.sms().single_send(param)
    if r.code():
        return True
    else:
        return False
