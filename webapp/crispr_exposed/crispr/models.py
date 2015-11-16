from django.db import models
from django.template.defaultfilters import slugify

class Strain(models.Model):

    ASSEMBLY_LEVEL = (
        ('COMP', 'Complete Genome'),
        ('CHRO', 'Chromosome'),
        ('SCAF', 'Scaffolds'),
        ('CONT', 'Contigs')
    )

    # Note: max_length values estimated from csv file

    refseq_id = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    organism_name = models.CharField(max_length=100)
    strain = models.CharField(max_length=100, null=True, blank=True)
    clade_id = models.IntegerField(null=True, blank=True) 
    bio_sample = models.CharField(max_length=13, null=True, blank=True) # SAMNxxxxxxxx
    bio_project = models.CharField(max_length=13, null=True, blank=True) # PRJNAxxxxxx
    group = models.CharField(max_length=50) # phyla name
    sub_group = models.CharField(max_length=50) # class name
    assembly = models.CharField(max_length=20) # GCA_0000XXXXX.X 
    size = models.CharField(max_length=10) # 6.18186 (Mb) (should be integer?)
    gc_content = models.CharField(max_length=10) # 64.7171 (%) (should be float?)
    replicons = models.CharField(max_length=2000,
                                 null=True, blank=True) # replicons should be split (long list)
    wgs = models.CharField(max_length=10, null=True, blank=True)
    scaffolds = models.IntegerField(null=True, blank=True)
    genes = models.IntegerField(null=True, blank=True)
    proteins = models.IntegerField(null=True, blank=True)
    release_date = models.DateField()
    modification_date = models.DateField()
    level = models.CharField(max_length=4, choices=ASSEMBLY_LEVEL)
    refseq_ftp = models.URLField(null=True, blank=True)
    genbank_ftp = models.URLField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Strain, self).save(*args, **kwargs)

    def __str__(self):
        return "refseq: %s\norganism name: %s" % (self.refseq_id, self.organism_name)


class CrisprArray(models.Model):
    handle = models.ForeignKey(Strain)
    array_id = models.IntegerField()

    def __str__(self):
        return self.handle.handle

class CrisprEntry(models.Model):
    array = models.ForeignKey(CrisprArray)
    position = models.IntegerField()
    length_repeat = models.IntegerField(null=True)
    length_spacer = models.IntegerField(null=True)
    repeat = models.CharField(max_length=100)
    spacer = models.CharField(max_length=100)

    def __str__(self):
        return self.spacer
