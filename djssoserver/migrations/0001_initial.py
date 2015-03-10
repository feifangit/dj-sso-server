# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djapiauth', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='SSO',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('host', models.CharField(unique=True, max_length=100)),
                ('note', models.CharField(max_length=80, null=True, blank=True)),
                ('credential', models.ForeignKey(to='djapiauth.APIKeys')),
            ],
            options={
                'verbose_name': 'SSO credential',
            },
            bases=(models.Model,),
        ),
    ]
