from rest_framework import serializers
from .models import (NewsPosition, News, NewsContent, NewsReviews)


# 管理新闻板块位置使用
class NewsPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsPosition
        fields = ('id', 'name', 'description', 'status')


# 新闻管理
class NewsAdminSerializer(serializers.Serializer):
    pass


# 发表新闻
class NewsSerializer(serializers.Serializer):
    pass


# 浏览新闻列表
class NewsListSerializer(serializers.Serializer):
    pass


# 浏览新闻内容
class NewsContentSerializer(serializers.Serializer):
    pass


# 浏览及发表新闻评论
class NewsReviewSerializer(serializers.Serializer):
    pass
