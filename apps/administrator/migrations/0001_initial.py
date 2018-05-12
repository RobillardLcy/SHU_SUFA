# Generated by Django 2.0.4 on 2018-05-12 21:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('member', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Administrator',
            fields=[
                ('member', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='成员')),
                ('status', models.BooleanField(default=True, verbose_name='状态')),
            ],
            options={
                'verbose_name': '社团骨干',
                'verbose_name_plural': '社团骨干',
                'db_table': 'administrator',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='编号')),
                ('name', models.CharField(max_length=10, verbose_name='名称')),
                ('description', models.CharField(max_length=200, verbose_name='简介')),
            ],
            options={
                'verbose_name': '部门',
                'verbose_name_plural': '部门',
                'db_table': 'department',
            },
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='编号')),
                ('name', models.CharField(max_length=20, verbose_name='名称')),
                ('description', models.CharField(max_length=50, verbose_name='描述')),
            ],
            options={
                'verbose_name': '权限',
                'verbose_name_plural': '权限',
                'db_table': 'permission',
            },
        ),
        migrations.CreateModel(
            name='PermissionToDepartment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrator.Department', verbose_name='部门')),
                ('permission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrator.Permission', verbose_name='权限')),
            ],
            options={
                'verbose_name': '部门权限',
                'verbose_name_plural': '部门权限',
                'db_table': 'permission_to_department',
            },
        ),
        migrations.CreateModel(
            name='PermissionToPosition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrator.Permission', verbose_name='权限')),
            ],
            options={
                'verbose_name': '职位权限',
                'verbose_name_plural': '职位权限',
                'db_table': 'permission_to_position',
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='编号')),
                ('name', models.CharField(max_length=10, verbose_name='名称')),
                ('remind', models.CharField(blank=True, max_length=200, verbose_name='提醒事项')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrator.Department', verbose_name='所属部门')),
                ('permission', models.ManyToManyField(through='administrator.PermissionToPosition', to='administrator.Permission', verbose_name='职位权限')),
            ],
            options={
                'verbose_name': '职位',
                'verbose_name_plural': '职位',
                'db_table': 'position',
            },
        ),
        migrations.AddField(
            model_name='permissiontoposition',
            name='position',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrator.Position', verbose_name='职位'),
        ),
        migrations.AddField(
            model_name='department',
            name='permission',
            field=models.ManyToManyField(through='administrator.PermissionToDepartment', to='administrator.Permission', verbose_name='部门权限'),
        ),
        migrations.AddField(
            model_name='administrator',
            name='position',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='administrator.Position', verbose_name='职位'),
        ),
        migrations.AlterUniqueTogether(
            name='permissiontoposition',
            unique_together={('permission', 'position')},
        ),
        migrations.AlterUniqueTogether(
            name='permissiontodepartment',
            unique_together={('permission', 'department')},
        ),
    ]
