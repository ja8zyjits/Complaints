# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket_tracker', '0008_comments_resolved_flag'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comments',
            old_name='commentor',
            new_name='created_by',
        ),
        migrations.RenameField(
            model_name='comments',
            old_name='date_of_posted_comment',
            new_name='created_on',
        ),
        migrations.RenameField(
            model_name='complaintsregister',
            old_name='engineers',
            new_name='assigned_to',
        ),
        migrations.RenameField(
            model_name='complaintsregister',
            old_name='user_name',
            new_name='created_by',
        ),
        migrations.RenameField(
            model_name='complaintsregister',
            old_name='complaints_registered_date',
            new_name='created_on',
        ),
    ]
