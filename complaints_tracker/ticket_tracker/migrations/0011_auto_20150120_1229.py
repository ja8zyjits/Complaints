# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ticket_tracker', '0010_auto_20150120_1107'),
    ]

    operations = [
        migrations.CreateModel(
            name='TicketComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField()),
                ('comments', models.TextField()),
                ('resolved_flag', models.BooleanField(default=False)),
                ('complaints', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='ticket_tracker.TicketRegister', null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='ticketcomments',
            name='complaints',
        ),
        migrations.RemoveField(
            model_name='ticketcomments',
            name='created_by',
        ),
        migrations.DeleteModel(
            name='TicketComments',
        ),
    ]
