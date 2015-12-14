from django.shortcuts import render
from django.http import HttpResponse

from rest_framework import viewsets
from .serializers import StrainSerializer, CrisprArraySerializer, CrisprEntrySerializer

from .models import Strain, CrisprEntry, CrisprArray
from crispr.tasks import blastn, crt

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def index(request):
    ## querying the db for all organism names
    strain_list = Strain.objects.values('organism_name').order_by('organism_name')
    
    ## generate a uniq list of organism names
    genus_list = []
    for item in strain_list:
        genus_list.append(item['organism_name'].split()[0])# + ' ' + item['organism_name'].split()[1])
    genus_list = sorted(set(genus_list))
    
    return render(request, "crispr/index.html", {'genus_list' : genus_list})

def about(request):
    return render(request, "crispr/about.html")

def visualization(request):
    return render(request, "crispr/dataviz.html")

def search_result(request):
    ## search by refseq
    if 'refseq_id' in request.POST and request.POST['refseq_id']:
        refseq_id = request.POST['refseq_id']
        strain_result = Strain.objects.filter(refseq_id__icontains=refseq_id)
        query = refseq_id
        return render(request, 'crispr/search_result.html', {'strain_result' : strain_result, 'query' : query})

    ## search by selected organism and filter
    elif 'organism_name' in request.POST and request.POST['organism_name']:     ## remove?
        organism_name = request.POST['organism_name']
        query = organism_name

        ## applying the filter if entered
        if 'org_name_filter' in request.POST and request.POST['org_name_filter']:
            org_name_filter = request.POST['org_name_filter']
            strain_result = Strain.objects.filter(organism_name__icontains=organism_name, organism_name__contains=org_name_filter)
            query = org_name_filter
        
        else:
            strain_result = Strain.objects.filter(organism_name__icontains=organism_name)
            
        return render(request, 'crispr/search_result.html', {'strain_result' : strain_result, 'query' : query})
    
    ## no entry --remove?
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
    if request.FILES:
        FASTA_file = request.FILES["file"]
        FASTA = FASTA_file.read()
        FASTA = FASTA.decode(encoding='UTF-8')
        
    ## FASTA input from text field.
    elif request.POST['input_seq']:
        FASTA = request.POST.get('input_seq')
        
    else:
        return HttpResponse("Please submit a FASTA sequence")
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

def crispr_finder(request):
    return render(request, "crispr/crt.html")

def crt_result(request):
    if request.POST['input_seq']:
        FASTA = request.POST.get('input_seq')
        
        ## retrieving CRT parameters from POST request
        parameters = {}
        parameters['para1'] = request.POST.get('para1')
        parameters['para2'] = request.POST.get('para2')
        parameters['para3'] = request.POST.get('para3')
        parameters['para4'] = request.POST.get('para4')
        parameters['para5'] = request.POST.get('para5')
        parameters['para6'] = request.POST.get('para6')
        
        ## from tasks.py
        crt_result = crt.delay(FASTA, parameters)
        
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

# Rest ViewSets (django rest framework)

class StrainViewSet(viewsets.ModelViewSet):
    queryset = Strain.objects.all()
    serializer_class = StrainSerializer
    http_method_names = ['get', 'head']

class CrisprArrayViewSet(viewsets.ModelViewSet):
    queryset = CrisprArray.objects.all()
    serializer_class = CrisprArraySerializer
    http_method_names = ['get', 'head']

class CrisprEntryViewSet(viewsets.ModelViewSet):
    queryset = CrisprEntry.objects.all()
    serializer_class = CrisprEntrySerializer
    http_method_names = ['get', 'head']
