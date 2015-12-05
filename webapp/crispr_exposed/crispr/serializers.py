from .models import Strain, CrisprArray, CrisprEntry

from rest_framework import serializers

class StrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Strain
        fields = ('refseq_id', 'organism_name', 'strain',
                  'clade_id', 'group', 'sub_group', 'bio_sample', 
                  'bio_project', 'assembly', 'size', 'gc_content',
                  'replicons', 'wgs', 'scaffolds', 'genes', 
                  'proteins', 'release_date', 'modification_date',
                  'level', 'refseq_ftp', 'genbank_ftp')

class CrisprArraySerializer(serializers.ModelSerializer):
    class Meta:
        model = CrisprArray
        fields = ('refseq_id', 'array_id', 'start', 'end')

class CrisprEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = CrisprEntry
        fields = ('array', 'position', 'repeat', 
                  'spacer', 'length_repeat', 'length_spacer')
