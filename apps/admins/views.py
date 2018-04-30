from rest_framework.views import APIView
from rest_framework.response import Response


from .models import (Admins, Departments, Positions,
                     Permissions, PermissionToDepartment, PermissionToPosition)
from .serializers import (AdminSerializer,)
from apps.members.models import Members


class AdminLogin(APIView):
    """
       管理平台登录接口(POST)
       Request: {
           'id': <学生证号>,
           'password': <密码>
       }
       Response: {
           'detail': <状态码>
       }
       """

    def post(self, request, format=None):
        id = request.data.get('id', None)
        password = request.data.get('password')
        try:
            user = Members.objects.get(id=id)
            if user.check_password(password):
                request.session['id'] = user.id
                request.session['admin'] = True
                request.session.set_expiry(86400)
                if user.is_active:
                    if user.is_auth:
                        if user.is_admin:
                            return Response({'detail': 0})
                        else:
                            return Response({'detail': 15})
                    else:
                        return Response({'detail': 15})
                else:
                    return Response({'detail': 15})
            else:
                # 密码错误
                return Response({"detail": 2})
        except Exception as e:
            # 未注册
            return Response({"detail": 2})


class AdminLogout(APIView):
    """
    管理平台注销接口(POST)
    Request: {}
    Response: {
        'detail': 0
    }
    """

    def post(self, request, format=None):
        try:
            del request.session['id']
            del request.session['admin']
        except KeyError:
            pass
        return Response({'detail': 0})
