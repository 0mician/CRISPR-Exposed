from django.contrib import admin

from crispr.models import Strain

class StrainAdmin(admin.ModelAdmin):
    list_display = ['refseq_id', 'organism_name', 'group', 'sub_group']
    fieldsets = (
        ('General information', {
            'fields' : ('refseq_id','organism_name', 'group', 'sub_group',
                        'strain', 'clade_id')
            }),
        ('Assembly information', {
            'fields' : ('assembly', 'level', 'scaffolds', 'refseq_ftp', 
                        'genbank_ftp', 'bio_sample', 'bio_project', 'wgs')
            }),
        ('Other information', {
            'fields' : ('size', 'gc_content', 'genes', 'proteins', 'release_date', 
                        'modification_date', 'replicons')
        })
    )

admin.site.register(Strain, StrainAdmin)
