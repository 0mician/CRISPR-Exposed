# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crispr', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CrisprArray',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('array_id', models.IntegerField()),
                ('start', models.IntegerField()),
                ('end', models.IntegerField()),
                ('refseq_id', models.ForeignKey(to='crispr.Strain')),
            ],
        ),
        migrations.CreateModel(
            name='CrisprEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position', models.IntegerField()),
                ('repeat', models.CharField(max_length=100)),
                ('spacer', models.CharField(max_length=100)),
                ('length_repeat', models.IntegerField(null=True)),
                ('length_spacer', models.IntegerField(null=True)),
                ('array', models.ForeignKey(to='crispr.CrisprArray')),
            ],
        ),
    ]
