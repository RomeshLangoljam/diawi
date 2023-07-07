import json
import plistlib
from zipfile import ZipFile
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import File
import uuid


@csrf_exempt
def index(request):
    if request.method =="POST":
        file = request.FILES.get('file_uploaded')
        file_name = file.name.split('.')[0]
        extention = file.name.split('.')[-1]
        if extention in ['ipa','apk']:
            unique_file_name = str(uuid.uuid4())+'.'+extention
            with open(f"static/{unique_file_name}", 'wb+') as destination: #for image
                for chunk in file.chunks(): #for image
                    destination.write(chunk)
            zip_path=destination.name
            file_=File(name=file_name,unique_name=unique_file_name,)
            file_.save()
            with ZipFile(zip_path, 'r') as zObject:
                zObject.extractall(path="/Users/romesh/projects/diawi/diawi_pro/static/temp")
            
            return HttpResponse("Uploaded")
        else:
            return HttpResponse("Uploaded file is not .ipa or .apk")
        

# def read_ipa(request,id):

#     if request.method == "GET":

