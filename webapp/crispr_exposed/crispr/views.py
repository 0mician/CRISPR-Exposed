from django.shortcuts import render
from django.http import HttpResponse

from .models import Strain, CrisprEntry, CrisprArray

from crispr.tasks import blastn,crt

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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
        
        ## from tasks.py
        blast_result = blastn.delay(FASTA)
        
        ## check if the result is ready
        #while not(blast_result.ready()):pass    ## and not(blast_result.successful()) ... OR sleep(time) OR retry i times
        try:
            blast_result.get(timeout = 2, interval = 1)    ## set timeout = 300 seconds and wait time = 1 sec
        except:
            return HttpResponse("Request timeout! please try again.")
        if blast_result.ready():
            if blast_result.successful():
                return render(request, "crispr/blast_result.html", {'FASTA' : FASTA, 'Blast_result' : blast_result.result})
            else:
                if isinstance(blast_result.result, Exception):
                    print("task failed due to an exception")
                    raise result.result
                else:
                    print("task was failed without raising an exception")
        else:
            print ("task has not yet run")
        
    else:
        return HttpResponse("Please submit a FASTA sequence")
        

def crispr_finder(request):
    return render(request, "crispr/crt.html")

def crt_result(request):
    if request.POST['input_seq']:
        FASTA = request.POST.get('input_seq')
        
        ## from tasks.py
        crt_result = crt.delay(FASTA)
        
        try:
            crt_result.get(timeout = 20, interval = 1)    ## set timeout = 300 seconds and wait time = 1 sec
        except:
            return HttpResponse("Request timeout! please try again.")
        if crt_result.ready():
            if crt_result.successful():
                return render(request, "crispr/crt_result.html", {'FASTA' : FASTA, 'crt_result' : crt_result.result})
            else:
                if isinstance(crt_result.result, Exception):
                    print("task failed due to an exception")
                    raise result.result
                else:
                    print("task was failed without raising an exception")
        else:
            print ("task has not yet run")
        
    else:
        return HttpResponse("Please submit a FASTA sequence")
