# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket_tracker', '0012_auto_20150120_1451'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ticketcomment',
            old_name='comments',
            new_name='comment',
        ),
    ]
