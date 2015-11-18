from django.contrib import admin

from crispr.models import Strain, CrisprArray, CrisprEntry

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

class CrisprArrayAdmin(admin.ModelAdmin):
    list_display = ['refseq_id', 'array_id', 'start', 'end']
    fieldsets = (
        ('Information', {
            'fields' : ('refseq_id', 'array_id', 'start', 'end')
        }),
    )

class CrisprEntryAdmin(admin.ModelAdmin):
    list_display = ['array', 'position', 'repeat', 'spacer']
    fieldsets = (
        ('Information', {
            'fields' : ('refseq_id', 'position', 'repeat', 'spacer',
                        'length_repeat', 'length_spacer')
        }),
    )

admin.site.register(Strain, StrainAdmin)
admin.site.register(CrisprArray, CrisprArrayAdmin)
admin.site.register(CrisprEntry, CrisprEntryAdmin)
