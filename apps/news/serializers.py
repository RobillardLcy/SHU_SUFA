from rest_framework import serializers
from .models import (NewsPosition, News, NewsContent, NewsReview)


# 管理新闻板块位置使用
class NewsPositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = NewsPosition
        fields = ('id', 'name', 'description', 'status')


# 新闻
class NewsSerializer(serializers.ModelSerializer):
    writer_name = serializers.ReadOnlyField(source='writer.name')
    position_id = serializers.ReadOnlyField(source='position.id')

    class Meta:
        model = News
        fields = ('id', 'title', 'writer_name', 'position_id', 'datetime', 'thumb_up')


# 新闻评论
class NewsReviewSerializer(serializers.ModelSerializer):
    member_name = serializers.ReadOnlyField(source='member.name')

    class Meta:
        model = NewsReview
        fields = ('member_name', 'content')
