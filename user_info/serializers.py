from django.contrib.auth.models import User
from rest_framework import serializers


class UserDescSerializer(serializers.ModelSerializer):
    """文章列别中应用的嵌套序列器"""

    class Meta:
        model = User
        fields = ['id','username','last_login','date_joined']