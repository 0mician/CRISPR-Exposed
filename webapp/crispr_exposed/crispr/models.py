from django.db import models
from django.template.defaultfilters import slugify

class Strain(models.Model):

    ASSEMBLY_LEVEL = (
        ('COMP', 'Complete Genome'),
        ('CHRO', 'Chromosome'),
        ('SCAF', 'Scaffolds'),
        ('CONT', 'Contigs')
    )

    refseq_id = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    organism_name = models.CharField(max_length=100)
    strain = models.CharField(max_length=100)
    clade_id = models.IntegerField() 
    bio_sample = models.CharField(max_length=13) # SAMNxxxxxxxx
    bio_project = models.CharField(max_length=13) # PRJNAxxxxxx
    group = models.CharField(max_length=50) # phyla name
    sub_group = models.CharField(max_length=50) # class name
    assembly = models.CharField(max_length=20) # GCA_0000XXXXX.X 
    size = models.CharField(max_length=10) # 6.18186 (Mb) (should be integer?)
    gc_content = models.CharField(max_length=10) # 64.7171 (%) (should be float?)
    replicons = models.CharField(max_length=2000) # replicons should be split (long list)
    wgs = models.CharField(max_length=10)
    scaffolds = models.IntegerField()
    genes = models.IntegerField()
    proteins = models.IntegerField()
    release_date = models.DateField()
    modification_date = models.DateField()
    level = models.CharField(max_length=4,choices=ASSEMBLY_LEVEL)
    refseq_ftp = models.URLField()
    genbank_ftp = models.URLField()
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Strain, self).save(*args, **kwargs)

    def __str__(self):
        return "refseq: %s\norganism name: %s" % (self.refseq_id, self.organism_name)
