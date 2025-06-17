from django.shortcuts import render
from django.http import HttpResponse
from myapp.models import *
from django.forms.models import model_to_dict

def search_list(request):
    if 'cName' in request.GET:
        cName = request.GET["cName"]
        print(cName)
        #resultList = students.objects.filter(cName=cName)
        resultList = students.objects.filter(cName__contains=cName)
    else:
        resultList = students.objects.all()

    errorMessage=""
    if not resultList:
        errorMessage="無此資料"


    #resultList = students.objects.all()

    # for data in resultList:   #-->檢查是否db有資料
    #     print(model_to_dict(data))

    # return HttpResponse("hello!")
    return render(request,"search_list.html",locals())
from django.db.models import Q
from django.core.paginator import Paginator
def index(request):
    if 'site_search' in request.GET:
        site_search = request.GET["site_search"]
        site_search = site_search.strip() #去除前後空白
        print(site_search)
        #一個關鍵字搜尋一個欄位
        #resultList = students.objects.filter(cName__contains=site_search)
        
        #一個關鍵字搜尋多個欄位
        # resultList = students.objects.filter(
        #     Q(cName__contains=site_search)|
        #     Q(cBirthday__contains=site_search)|
        #     Q(cEmail__contains=site_search)|
        #     Q(cPhone__contains=site_search)|
        #     Q(cAddr__contains=site_search)              
        # )
        
        #多個關鍵字搜尋多個欄位
        keyworks = site_search.split() #切割
        print(keyworks)
        #resultList = []
        q_object = Q()
        for keywork in keyworks:
            q_object.add(Q(cName__contains=keywork),Q.OR)
            q_object.add(Q(cBirthday__contains=keywork),Q.OR)
            q_object.add(Q(cEmail__contains=keywork),Q.OR)
            q_object.add(Q(cPhone__contains=keywork),Q.OR)
            q_object.add(Q(cAddr__contains=keywork),Q.OR)
        resultList = students.objects.filter(q_object)

    else:
        resultList = students.objects.all().order_by("cID")
    dataCount = len(resultList)
    #print(dataCount)
    status = True
    errormessage = ''
    if not resultList:
        status = False
        errormessage="無此資料"
    #分頁設定，每頁顯示3筆
    paginator = Paginator(resultList,3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number) #根據page_number，得到對應頁數的資料
    #page_obj 包含該頁資料的物件
    #page_obj.object_list: 該頁的資料
    #page_obj.has_next, page_obj.has_previous:是否有下一頁、上一頁
    #page-obj.next_page_number, page-obj.previous_page_number:下一頁、上一頁
    #page_obj.number 目前的頁碼
    #page_obj.paginator.num_pages:總頁數

    #return HttpResponse("hello!")
    return render(request,"index.html",locals())

from django.shortcuts import redirect
def post(request):
    if request.method == "POST":
        cName = request.POST["cName"]
        cSex = request.POST["cSex"]
        cBirthday = request.POST["cBirthday"]
        cEmail = request.POST["cEmail"]
        cPhone = request.POST["cPhone"]
        cAddr= request.POST["cAddr"]
        print(f"cName={cName},cSex={cSex},cBirthday={cBirthday},cEmail={cEmail},cPhone={cPhone},cAddr={cAddr}")
        # orm
        add = students(cName=cName,cSex=cSex,cBirthday=cBirthday,cEmail=cEmail,cPhone=cPhone,cAddr=cAddr)
        add.save()
        #return HttpResponse("hello!")
        return redirect('/index/')
    else:
        return render(request,"post.html",locals())

def edit(request,id=None):
    print(f"id={id}")
    if request.method == "POST":
        cName = request.POST["cName"]
        cSex = request.POST["cSex"]
        cBirthday = request.POST["cBirthday"]
        cEmail = request.POST["cEmail"]
        cPhone = request.POST["cPhone"]
        cAddr= request.POST["cAddr"]
        print(f"cName={cName},cSex={cSex},cBirthday={cBirthday},cEmail={cEmail},cPhone={cPhone},cAddr={cAddr}")
        #orm
        update = students.objects.get(cID=id)
        update.cName = cName
        update.cSex = cSex
        update.cBirthday = cBirthday
        update.cEmail = cEmail
        update.cPhone = cPhone
        update.cAddr = cAddr
        update.save()
        #return HttpResponse("hello!")
        return redirect('/index/')
    else:
        obj_data = students.objects.get(cID=id)
        print(model_to_dict(obj_data)) #檢視用
        return render(request,"edit.html",locals())

def delete(request,id=None):
    print(f"id={id}")
    if request.method == "POST":
        delete_data = students.objects.get(cID=id)
        delete_data.delete()
        #return HttpResponse("hello!")
        return redirect('/index/')
    else: 
        obj_data = students.objects.get(cID=id)
        print(model_to_dict(obj_data)) #檢視用      
        return render(request,"delete.html",locals())
    
###########################
#web api

from django.http import JsonResponse
def getallitems(request):
    resultListobject = students.objects.all().order_by("cID")
    # for data in resultListobject:
    #     print(model_to_dict(data))
    #queerySet->object轉成list-->dict
    resultListDict = list(resultListobject.values())
    print(resultListDict)
    #return HttpResponse("hello!")
    return JsonResponse(resultListDict, safe=False)

def getitem(request, id=None):
    print(f"id={id}")
    resultListObject = students.objects.filter(cID=id)
    if not resultListObject.exists():
        return JsonResponse ({"message":"無資料"}, safe=False)
    resultListDict = list(resultListObject.values())
    print(resultListDict)
    #return HttpResponse("hello!")
    return JsonResponse(resultListDict, safe=False)

#使用postman

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def createItem(request):
    try:
        if request.method == "GET":
            cName = request.GET["cName"]
            cSex = request.GET["cSex"]
            cBirthday = request.GET["cBirthday"]
            cEmail = request.GET["cEmail"]
            cPhone = request.GET["cPhone"]
            cAddr= request.GET["cAddr"]
            print("GET...................................")
            print(f"cName={cName},cSex={cSex},cBirthday={cBirthday},"+
                f"cEmail={cEmail},cPhone={cPhone},cAddr={cAddr}")
        elif request.method == "POST":
            cName = request.POST["cName"]
            cSex = request.POST["cSex"]
            cBirthday = request.POST["cBirthday"]
            cEmail = request.POST["cEmail"]
            cPhone = request.POST["cPhone"]
            cAddr= request.POST["cAddr"]
            print("POST...................................")
            print(f"cName={cName},cSex={cSex},cBirthday={cBirthday},"+
                f"cEmail={cEmail},cPhone={cPhone},cAddr={cAddr}")
    except:
        return JsonResponse({"message":"缺少資料"}, safe=False)
    
    try:
        add = students(cName=cName,cSex=cSex,cBirthday=cBirthday,cEmail=cEmail,cPhone=cPhone,cAddr=cAddr)
        add.save()
        return JsonResponse({"message":"新增成功"}, safe=False)
    except:
        return JsonResponse({"message":"新增失敗"}, safe=False)

        
    #return HttpResponse("hello!")

@csrf_exempt
def updateItem(request,id=None): 
    print(id)
    try:
        if request.method == "GET":
            cName = request.GET["cName"]
            cSex = request.GET["cSex"]
            cBirthday = request.GET["cBirthday"]
            cEmail = request.GET["cEmail"]
            cPhone = request.GET["cPhone"]
            cAddr= request.GET["cAddr"]
            print("GET...................................")
            print(f"cName={cName},cSex={cSex},cBirthday={cBirthday},"+
                f"cEmail={cEmail},cPhone={cPhone},cAddr={cAddr}")
        elif request.method == "POST":
            cName = request.POST["cName"]
            cSex = request.POST["cSex"]
            cBirthday = request.POST["cBirthday"]
            cEmail = request.POST["cEmail"]
            cPhone = request.POST["cPhone"]
            cAddr= request.POST["cAddr"]
            print("POST...................................")
            print(f"cName={cName},cSex={cSex},cBirthday={cBirthday},"+
                f"cEmail={cEmail},cPhone={cPhone},cAddr={cAddr}")
    except:
        return JsonResponse({"message":"缺少資料"}, safe=False)
    try:
        #orm
        update = students.objects.get(cID=id)
        update.cName = cName
        update.cSex = cSex
        update.cBirthday = cBirthday
        update.cEmail = cEmail
        update.cPhone = cPhone
        update.cAddr = cAddr
        update.save()
        return JsonResponse({"message":"更新成功"}, safe=False)
    except:
        return JsonResponse({"message":"更新失敗"}, safe=False)
    #return HttpResponse("Hello!")

@csrf_exempt
def deleteItem(request,id=None):
    print(id)
    try:
        delete_data = students.objects.get(cID=id)
        delete_data.delete()
        return JsonResponse({"message":"刪除成功"}, safe=False)
    except:
        return JsonResponse({"message":"刪除失敗"}, safe=False)
    #return HttpResponse("Hello!")



    



    
    
