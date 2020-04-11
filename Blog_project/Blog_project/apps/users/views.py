import re
import random
from django.shortcuts import render
# Create your views here.
from django.views.generic.base import View
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ViewSet

from Blog_project.utils.SMS import sendSMS
from users.serializers import UserSerializer, UserDetailSerializer, BlogSerializer
from django_redis import get_redis_connection
SMS = sendSMS.SMS(SIGN_NAME='速诺科技')


class SendSMSView(APIView):
    def get(self, request):
        params = request.query_params.dict()
        mobile = params.get("mobile")
        print(mobile)
        if not re.match(r'1[3-9]\d{9}$', mobile):
            return Response({"code": -1, "msg": "手机号格式错误"})
        else:
            sms_code = "%06d" % random.randint(0, 999999)
            print(sms_code)
            # if SMS.send_sms(mobile, "SMS_91850019", sms_code):
            redis_conn = get_redis_connection("verify_codes")
            redis_conn.setex("sms_%s" % mobile, 300, sms_code)
            return Response("ok")


class UserView(CreateAPIView):
    serializer_class = UserSerializer


class UserDetailInfoView(RetrieveAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        print(self.request.user)
        return self.request.user


class UserBlogView(ModelViewSet):
    serializer_class = BlogSerializer


class UserCommrntView(RetrieveAPIView):
    pass
