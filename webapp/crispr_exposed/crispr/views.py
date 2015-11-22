from django.shortcuts import render
from django.http import HttpResponse

from .models import Strain, CrisprEntry, CrisprArray

def index(request):
    return render(request, "crispr/index.html")

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
