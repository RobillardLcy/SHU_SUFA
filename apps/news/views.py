import datetime
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import (NewsPosition, News, NewsContent, NewsReview)
from .serializers import (NewsPositionSerializer, NewsSerializer, NewsReviewSerializer)
from apps.member.permissions import (MemberPermission, MemberAuthPermission)


class NewsRecentlyListAPI(APIView):
    """
    近期新闻列表接口
    (GET)
    Response(array): {
        'id': <新闻编号>,
        'title': <标题>,
        'writer_name': <作者姓名>,
        'datetime': <创作时间>,
        'position_id': <板块编号>,
        'thumb_up': <点赞次数>
    }
    """

    def get(self, request, format=None):
        now = datetime.datetime.now()
        start = now - datetime.timedelta(weeks=4)
        news = News.objects.all().filter(datetime__gte=start)
        news_list = NewsSerializer(news, many=True).data
        return Response(news_list)


class NewsAllListAPI(APIView):
    """
    所有新闻列表接口
    (GET)
    Response(array): {
        'id': <新闻编号>,
        'title': <标题>,
        'writer_name': <作者姓名>,
        'datetime': <创作时间>,
        'position_id': <板块编号>,
        'thumb_up': <点赞次数>
    }
    """

    def get(self, request, format=None):
        news = News.objects.all()
        news_list = NewsSerializer(news, many=True).data
        return Response(news_list)


class NewsContentAPI(APIView):
    """
    新闻内容接口
    (GET)
    Response: {
        'content': <内容>
    }
    """

    def get(self, request, news_id, format=None):
        try:
            news_content = NewsContent.objects.get(news__id=news_id)
            return Response({'content': news_content.content})
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class NewsReviewListAPI(APIView):
    """
    新闻评论列表接口
    (GET)
    Response(array): {
        'member_name': <成员姓名>,
        'content': <评论内容>
    }
    """

    def get(self, request, news_id, format=None):
        news_review = NewsReview.objects.all().filter(news__id=news_id)
        news_review_list = NewsReviewSerializer(news_review, many=True).data
        return Response(news_review_list)


class NewsReviewPublishAPI(APIView):
    """
    新闻评论发表接口
    (POST)
    Request: {
        'news': <新闻编号>,
        'content': <内容>
    }
    Response: {
        'detail': <状态码>
    }
    """

    permission_classes = (MemberPermission,)

    def post(self, request, format=None):
        member_id = request.session.get('id')
        news_id = request.data.get('news')
        content = request.data.get('content')
        news_review = NewsReview.objects.create(member__id=member_id, news__id=news_id, content=content)
        if news_review:
            return Response({'detail': 0})
        else:
            # TODO: Add Error Tag
            return Response({'detail': ...})
