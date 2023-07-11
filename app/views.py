import json
import plistlib
from zipfile import ZipFile
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import File
import uuid
from mobileprovision import MobileProvisionModel
from pyaxmlparser import APK
import xml.etree.ElementTree as ET

@csrf_exempt
def index(request):
    if request.method =="POST":
        file = request.FILES.get('file_uploaded')
        file_name = file.name.split('.')[0]
        extention = file.name.split('.')[-1]
        if extention =='ipa':
            unique_file_name = str(uuid.uuid4())+'.'+extention
            with open(f"static/{unique_file_name}", 'wb+') as destination: #for image
                for chunk in file.chunks(): #for image
                    destination.write(chunk)
            zip_path=destination.name
            print(">>>>>>>>>>>>>", destination.name)
            file_=File(name=file_name,unique_name=unique_file_name,)
            file_.save()
            with ZipFile(zip_path, 'r') as zObject:
                zObject.extractall(path="D:\projects\diawi\diawi\static/temp/"+unique_file_name)
            plist_dict = plist_to_dict("D:\projects\diawi\diawi\static/temp/"+unique_file_name+"/Payload/savvyMobile.app/Info.plist")
            info_data={}
            info_data['BundleIdentifier'] = plist_dict['CFBundleIdentifier']
            info_data['MinimumiOSVersion'] = plist_dict['MinimumOSVersion']
            for i in plist_dict['UIDeviceFamily']:
                if i ==1:
                    info_data['Device Family'] = "iPhone"
                else:
                    info_data['Device Family']="android"
            info_data['Required Device Capabilities'] = plist_dict['UIRequiredDeviceCapabilities']
            info_data['Supported architecture'] = plist_dict['UIRequiredDeviceCapabilities']
            print(info_data)
            mp_file_path = "D:\projects\diawi\diawi\static/temp/Payload/savvyMobile.app/embedded.mobileprovision"
            mp_model = MobileProvisionModel(mp_file_path)
            info_data['Provisioned Device']=mp_model['ProvisionedDevices']
            info_data['Profile expiration']=str(mp_model['ExpirationDate'])
            info_data['Profile type']=mp_model['Entitlements']['aps-environment']
            info_data['app_name']= plist_dict['CFBundleDisplayName']
            info_data['app_version']= plist_dict['CFBundleShortVersionString']
            info_data['app build'] = plist_dict['CFBundleVersion']
            print(mp_model)
            
            return HttpResponse(json.dumps(info_data))
            # return HttpResponse("Uploaded")
        elif extention=='apk':
            unique_file_name = str(uuid.uuid4())+'.'+extention
            with open(f"static/{unique_file_name}", 'wb+') as destination: #for image
                for chunk in file.chunks(): #for image
                    destination.write(chunk)
            zip_path=destination.name
            print(">>>>>>>>>>>>>", destination.name)
            file_=File(name=file_name,unique_name=unique_file_name,)
            file_.save()
            with ZipFile(zip_path, 'r') as zObject:
                zObject.extractall(path="D:\projects\diawi\diawi\static/temp/android")
            apk = APK('D:\projects\diawi\diawi/'+zip_path)
            
            f=open('D:\projects\diawi\diawi\static/temp/android/AndroidManifest.xml',encoding='UTF-8')
            tree = ET.parse(f)
            print(ET.dump(tree))            # mytree = ET.parse('D:\projects\diawi\diawi\static/temp/android/AndroidManifest.xml')
            # myroot = mytree.getroot()
            # print(myroot[0].tag)
            print(apk.package)
            print(apk.version_name)
            print(apk.version_code)
            print(apk.icon_info)
            print(apk.application)

            # Display the data
            return HttpResponse("Apk Uploaded")
        else:
            return HttpResponse("Uploaded file is not .ipa or .apk")
        

def plist_to_dict(file_path):
    with open(file_path, 'rb') as file:
        plist_data = plistlib.load(file)
        # Convert plist data to a dictionary
        plist_dict = dict(plist_data)
    return plist_dict

def write_manifest(url,bundleId,bundleversion,appname):
    f = open('manifest.plist', 'w+')
    f.write("")

def get_and_write_manifest(request,filename):
    if request.method == 'GET':
        file = request.GET(filename)
        # file_=File(name=file_name,unique_name=unique_file_name,)
        #     file.save()
        #     with ZipFile(zip_path, 'r') as zObject:
        #         zObject.extractall(path="D:\projects\diawi\diawi\static/temp")
        #     plist_dict = plist_to_dict("D:\projects\diawi\diawi\static/temp/Payload/savvyMobile.app/Info.plist")
        #     info_data={}
        #     info_data['BundleIdentifier'] = plist_dict['CFBundleIdentifier']
        #     info_data['MinimumiOSVersion'] = plist_dict['MinimumOSVersion']
        #     for i in plist_dict['UIDeviceFamily']:
        #         if i ==1:
        #             info_data['Device Family'] = "iPhone"
        #         else:
        #             info_data['Device Family']="android"
        #     info_data['Required Device Capabilities'] = plist_dict['UIRequiredDeviceCapabilities']
        #     info_data['Supported architecture'] = plist_dict['UIRequiredDeviceCapabilities']
        #     print(info_data)
        #     mp_file_path = "D:\projects\diawi\diawi\static/temp/Payload/savvyMobile.app/embedded.mobileprovision"
        #     mp_model = MobileProvisionModel(mp_file_path)
        #     info_data['Provisioned Device']=mp_model['ProvisionedDevices']
        #     info_data['Profile expiration']=str(mp_model['ExpirationDate'])
        #     info_data['Profile type']=mp_model['Entitlements']['aps-environment']
        #     info_data['app_name']= plist_dict['CFBundleDisplayName']
        #     info_data['app_version']= plist_dict['CFBundleShortVersionString']
        #     info_data['app build'] = plist_dict['CFBundleVersion']
        #     print(mp_model)
            
        #     return HttpResponse(json.dumps(info_data))
        return HttpResponse(file)
    