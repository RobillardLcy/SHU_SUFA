from django.db import models
from django.conf import settings


class NewsPosition(models.Model):
    """
    新闻版块
    """
    id = models.PositiveSmallIntegerField(primary_key=True, verbose_name='编号')
    name = models.CharField(max_length=10, verbose_name='名称')
    description = models.CharField(max_length=100, verbose_name='描述')
    status = models.BooleanField(default=True, verbose_name='状态')

    class Meta:
        db_table = 'news_position'
        verbose_name = '新闻板块位置'
        verbose_name_plural = verbose_name


class News(models.Model):
    """
    新闻信息
    """
    id = models.PositiveIntegerField(primary_key=True, verbose_name='编号')
    title = models.CharField(max_length=20, verbose_name='标题')
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='作者')
    position = models.ForeignKey(NewsPosition, on_delete=models.SET_NULL, null=True, default=None, verbose_name='板块')
    thumb_up = models.PositiveSmallIntegerField(default=0, verbose_name='好评')
    status = models.SmallIntegerField(default=-1, verbose_name='状态')

    class Meta:
        db_table = 'news'
        verbose_name = '新闻'
        verbose_name_plural = verbose_name


class NewsContent(models.Model):
    """
    新闻内容
    """
    news = models.OneToOneField(News, on_delete=models.CASCADE, primary_key=True, verbose_name='新闻')
    content = models.CharField(max_length=2000, verbose_name='内容')

    class Meta:
        db_table = 'news_content'
        verbose_name = '新闻内容'
        verbose_name_plural = verbose_name


class NewsReviews(models.Model):
    """
    新闻评论
    """
    id = models.PositiveIntegerField(primary_key=True, verbose_name='编号')
    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='评论者')
    news = models.ForeignKey(News, on_delete=models.CASCADE, verbose_name='新闻')
    content = models.CharField(max_length=200, verbose_name='评论')

    class Meta:
        db_table = 'news_reviews'
        verbose_name = '新闻评论'
        verbose_name_plural = verbose_name
