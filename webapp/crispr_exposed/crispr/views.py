from django.shortcuts import render
from django.http import HttpResponse

from .models import Strain, CrisprEntry, CrisprArray

import os

def index(request):
    return render(request, "crispr/index.html")

def about(request):
    return render(request, "crispr/about.html")

def search_result(request):
    if 'organism_name_q' in request.POST and request.POST['organism_name_q']:
        organism_name_q = request.POST['organism_name_q']
        query = organism_name_q
        if 'refseq_id_q' in request.POST and request.POST['refseq_id_q']:
            refseq_id_q = request.POST['refseq_id_q']        
            strain_result = Strain.objects.filter(organism_name__icontains=organism_name_q, refseq_id__icontains=refseq_id_q)
            query += refseq_id_q
        else:
            strain_result = Strain.objects.filter(organism_name__icontains=organism_name_q)
        return render(request, 'crispr/search_result.html', {'strain_result' : strain_result, 'query' : query})
    else:
        return HttpResponse("Please  submit a search Term")

def crispr_details(request, slug):
    context_dict = {}
    try:
        strain = Strain.objects.get(slug=slug)
        context_dict['strain'] = strain
        crispr_array = CrisprArray.objects.filter(refseq_id=strain)
        context_dict['crispr_array'] = crispr_array

    except Strain.DoesNotExist:
        pass
    return render(request, 'crispr/details.html', context_dict)

def blast(request):
    return render(request, "crispr/blast.html")
    
def blast_result(request):
    ## File Browse
    #if request.POST['FASTA_file']:
        #FASTA_file = request.POST.get('FASTA_file')
        #return render(request, "crispr/blast_result.html", {'FASTA_file' : FASTA_file})
        #return HttpResponse(request, "File selected")
    ## FASTA input from text field.
    if request.POST['input_seq']:
        FASTA = request.POST.get('input_seq')
        
        ## save input FASTA to a temp file.
        fasta_file = open("crispr/blast/input.fasta" ,'w')
        fasta_file.writelines(">input\n"+FASTA)
        fasta_file.close()
        
        ## blastn command
        os.system("blastn -query crispr/blast/input.fasta -db crispr/blast/db/spacers.fasta -out crispr/blast/blast_result.txt")
        
        ## loop until file is generated
        while(True):
            try:
                blast_result_file = open("crispr/blast/blast_result.txt", 'r')
                if(blast_result_file):
                    ## reading blast result file into memory
                    blast_result_txt = blast_result_file.read()
                    blast_result_file.close()
                    
                    ## removing temp files
                    os.system("rm crispr/blast/input.fasta crispr/blast/blast_result.txt")
                    break
            except File.DoesNotExist:
                pass

        return render(request, "crispr/blast_result.html", {'FASTA' : FASTA, 'Blast_result' : blast_result_txt})
    else:
        return HttpResponse("Please submit a FASTA sequence")
