from django.conf import settings
from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.forms import ModelForm
from .models import Video


class DetailView(generic.DetailView):
    model =  Video

class ListView(generic.ListView):
    model=  Video

