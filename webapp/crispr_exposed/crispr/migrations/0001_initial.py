# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Strain',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('refseq_id', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
                ('organism_name', models.CharField(max_length=100)),
                ('strain', models.CharField(max_length=100, blank=True, null=True)),
                ('clade_id', models.IntegerField(blank=True, null=True)),
                ('bio_sample', models.CharField(max_length=13, blank=True, null=True)),
                ('bio_project', models.CharField(max_length=13, blank=True, null=True)),
                ('group', models.CharField(max_length=50)),
                ('sub_group', models.CharField(max_length=50)),
                ('assembly', models.CharField(max_length=20)),
                ('size', models.CharField(max_length=10)),
                ('gc_content', models.CharField(max_length=10)),
                ('replicons', models.CharField(max_length=2000, blank=True, null=True)),
                ('wgs', models.CharField(max_length=10, blank=True, null=True)),
                ('scaffolds', models.IntegerField(blank=True, null=True)),
                ('genes', models.IntegerField(blank=True, null=True)),
                ('proteins', models.IntegerField(blank=True, null=True)),
                ('release_date', models.DateField()),
                ('modification_date', models.DateField()),
                ('level', models.CharField(max_length=4, choices=[('COMP', 'Complete Genome'), ('CHRO', 'Chromosome'), ('SCAF', 'Scaffolds'), ('CONT', 'Contigs')])),
                ('refseq_ftp', models.URLField(blank=True, null=True)),
                ('genbank_ftp', models.URLField(blank=True, null=True)),
            ],
        ),
    ]
