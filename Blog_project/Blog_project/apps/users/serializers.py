import re
from datetime import datetime

from django_redis import get_redis_connection
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from users.models import User, Blog

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UserSerializer(serializers.ModelSerializer):
    allow = serializers.CharField(label='同意协议', write_only=True)
    password2 = serializers.CharField(label="同意协议", write_only=True)
    sms_code = serializers.CharField(label="短信验证吗", write_only=True)
    token = serializers.CharField(label="JWT_token", read_only=True)
    # username = serializers.CharField(label="用户姓名")

    class Meta:
        model = User
        fields = ["username", "mobile", "password", "allow", "password2", "sms_code", "token"]
        extra_kwargs = {
            "username": {
                "required": False
            },

            "password": {
                "write_only": True
            }
        }

    def validate_mobile(self, value):
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError("手机号格式错误")
        return value

    def validate_allow(self, value):
        if value != "true":
            raise serializers.ValidationError("请同意用户协议")
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs["password"]:
            raise serializers.ValidationError("两次密码不一致")
        redis_conn = get_redis_connection("verify_codes")
        mobile = attrs["mobile"]
        real_sms_code = redis_conn.get("sms_%s" % mobile)
        if real_sms_code:
            real_sms_code = real_sms_code.decode()
        if attrs["sms_code"] == real_sms_code:
            return attrs
        else:
            raise serializers.ValidationError("短信验证码错误或无效")

    def create(self, validated_data):
        del validated_data["password2"]
        del validated_data["sms_code"]
        del validated_data["allow"]
        user = super().create(validated_data)
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        if not user.username:
            user.username = validated_data["mobile"]
        user.token = token
        return user


class BlogSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(label='ID', read_only=True)

    class Meta:
        blog = Blog
        fields = "__all__"
        extra_kwargs = {

        }
        read_only_fields = ()


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详细信息序列化器
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'mobile')

