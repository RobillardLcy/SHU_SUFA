from rest_framework import serializers
from .models import (NewsPosition, News, NewsContent, NewsReview)


# 管理新闻板块位置使用
class NewsPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsPosition
        fields = ('id', 'name', 'description', 'status')


# 新闻
class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('id', 'title', 'writer', 'position', 'thumb_up', 'status')


# 新闻内容
class NewsContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsContent
        fields = ('news', 'content')


# 新闻评论
class NewsReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsReview
        fields = ('id', 'member', 'news', 'content')
