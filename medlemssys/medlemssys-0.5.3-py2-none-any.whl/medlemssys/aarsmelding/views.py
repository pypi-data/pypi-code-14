# Create your views here.
import datetime
from django.shortcuts import render, get_object_or_404
from medlem.models import Lokallag

def index(request):
    return render(request, 'aarsmelding/index.html', {})

def single(request, lokallag_slug):
    lokallag = get_object_or_404(Lokallag, slug=lokallag_slug)
    year = datetime.date.today().year - 1
    previous_year = year - 1

    teljande = lokallag.medlem_set.teljande(year)
    previous_teljande = lokallag.medlem_set.teljande(previous_year)

    betalande = lokallag.medlem_set.betalande(year)
    previous_betalande = lokallag.medlem_set.betalande(previous_year)

    nye = lokallag.medlem_set.nye(year)
    previous_nye = lokallag.medlem_set.nye(previous_year)

    teljande_nye = lokallag.medlem_set.teljande_nye(year)
    previous_teljande_nye = lokallag.medlem_set.teljande_nye(previous_year)
    return render(request, 'aarsmelding/single.html', {
        'lokallag': lokallag,
        'teljande': teljande,
        'previous_teljande': previous_teljande,
        'betalande': betalande,
        'previous_betalande': previous_betalande,
        'nye': nye,
        'previous_nye': previous_nye,
        'teljande_nye': teljande_nye,
        'previous_teljande_nye': previous_teljande_nye,
        'year': year,
        'previous_year': previous_year,
    })
