from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def hello(request):
    # return HttpResponse('Hello World')
    return render(request=request,
                  template_name='hello.html',
                  context={'name' : 'Rishabh', 'emotion':'bad'}
                  )
