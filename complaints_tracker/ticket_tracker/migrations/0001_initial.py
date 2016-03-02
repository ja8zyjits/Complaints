# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_of_posted_comment', models.DateTimeField()),
                ('comments', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ComplaintsRegister',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('complaints_registered_date', models.DateTimeField()),
                ('user_name', models.CharField(max_length=25)),
                ('system_id', models.CharField(max_length=15)),
                ('complaints', models.TextField()),
                ('priority', models.CharField(max_length=10, null=True, blank=True)),
                ('engineers', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'permissions': (('can_assign_task', 'Admin can assign new task to any engineer'), ('can_self_assign_task', 'Engineer can assign task to self only'), ('can_only_view', 'User can only view and change status of the issue')),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'unassigned', max_length=25)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='complaintsregister',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='ticket_tracker.Status', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comments',
            name='complaints',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='ticket_tracker.ComplaintsRegister', null=True),
            preserve_default=True,
        ),
    ]
