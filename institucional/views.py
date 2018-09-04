# Create your views here.
from django.shortcuts import render
from galerias.models import FotoGaleria
import random

def sobre(request):
    fotos = list(FotoGaleria.objects.get_fotos_pousada())

    if len(fotos) < 4:
        fotos = list(FotoGaleria.objects.get_fotos())

    if len(fotos) >= 4:
        fotos = random.sample(fotos, 4)

    return render(request, 'sobre.html', {'fotos': fotos})