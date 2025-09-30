from django.shortcuts import render, redirect, get_object_or_404
from .models import Petition
from django.contrib.auth.decorators import login_required

def index(request):
    petitions = Petition.objects.all()
    template_data = {}
    template_data['petitions'] = petitions
    return render(request, 'petition/index.html',
                  {'template_data': template_data})

@login_required
def create_petition(request):
    if request.method == 'POST' and request.POST['comment'] != '':
        petition = Petition()
        petition.movie = request.POST['movie']
        petition.comment = request.POST['comment']
        petition.date = request.POST
        petition.user = request.user
        petition.save()
        return redirect('petition.index')
    else:
        return redirect('petition.index')
    
@login_required
def delete_petition(request, id):
    petition = get_object_or_404(Petition, id=id)
    petition.delete()
    return redirect('petition.index')

@login_required
def vote_petition(request, id):
    petition = get_object_or_404(Petition, id=id)
    petition.votes += 1
    petition.voters.add(request.user)
    petition.save()
    return redirect('petition.index')