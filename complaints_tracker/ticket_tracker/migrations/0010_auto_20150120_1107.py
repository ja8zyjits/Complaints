# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ticket_tracker', '0009_auto_20150119_1833'),
    ]

    operations = [
        migrations.CreateModel(
            name='TicketComments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField()),
                ('comments', models.TextField()),
                ('resolved_flag', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TicketRegister',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField()),
                ('created_by', models.CharField(max_length=25)),
                ('system_id', models.CharField(max_length=45)),
                ('ipaddress', models.CharField(max_length=20, null=True, blank=True)),
                ('complaints', models.TextField()),
                ('priority', models.CharField(max_length=10, null=True, blank=True)),
                ('email_msg_id', models.TextField(null=True, blank=True)),
                ('assigned_to', models.ForeignKey(related_name='assigned_to', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('resolved_by', models.ForeignKey(related_name='resolved_by', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'permissions': (('can_assign_task', 'Admin can assign new task to any engineer'), ('can_self_assign_task', 'Engineer can assign task to self only'), ('can_only_view', 'User can only view and change status of the issue')),
            },
            bases=(models.Model,),
        ),
        migrations.RenameModel(
            old_name='Status',
            new_name='TicketStatus',
        ),
        migrations.RemoveField(
            model_name='comments',
            name='complaints',
        ),
        migrations.RemoveField(
            model_name='comments',
            name='created_by',
        ),
        migrations.DeleteModel(
            name='Comments',
        ),
        migrations.RemoveField(
            model_name='complaintsregister',
            name='assigned_to',
        ),
        migrations.RemoveField(
            model_name='complaintsregister',
            name='resolved_by',
        ),
        migrations.RemoveField(
            model_name='complaintsregister',
            name='status',
        ),
        migrations.DeleteModel(
            name='ComplaintsRegister',
        ),
        migrations.AddField(
            model_name='ticketregister',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='ticket_tracker.TicketStatus', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ticketcomments',
            name='complaints',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='ticket_tracker.TicketRegister', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ticketcomments',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
