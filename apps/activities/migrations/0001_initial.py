# Generated by Django 2.0.4 on 2018-04-24 08:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='编号')),
                ('name', models.CharField(max_length=20, verbose_name='名称')),
                ('reg_start', models.DateTimeField(verbose_name='报名开始时间')),
                ('reg_end', models.DateTimeField(verbose_name='报名结束时间')),
                ('time', models.DateTimeField(verbose_name='活动开始时间')),
                ('place', models.CharField(max_length=50, verbose_name='地点')),
                ('status', models.SmallIntegerField(default=-1, verbose_name='状态')),
            ],
            options={
                'verbose_name': '活动',
                'verbose_name_plural': '活动',
                'db_table': 'activities',
            },
        ),
        migrations.CreateModel(
            name='ActivitySignup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remark', models.CharField(blank=True, max_length=100, null=True, verbose_name='备注')),
                ('status', models.SmallIntegerField(default=-1, verbose_name='状态')),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activities.Activities', verbose_name='活动')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='成员')),
            ],
            options={
                'verbose_name': '活动报名情况',
                'verbose_name_plural': '活动报名情况',
                'db_table': 'activity_signup',
            },
        ),
        migrations.AlterUniqueTogether(
            name='activitysignup',
            unique_together={('activity', 'member')},
        ),
    ]
