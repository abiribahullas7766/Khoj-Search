from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from .models import *
from .serializers import ClientSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


#login page
def loginPage(request):
    
    if request.method == 'POST':
        user = request.POST.get('username')
        password = request.POST.get('pass')
        #validating the user login inputs
        user = auth.authenticate(username=user,password=password)
        if user is None:
            messages.info(request,"Invalid password or username")
            return redirect('/')
        else:
            auth.login(request,user)
            return redirect('search')

    context = {'title':'login'}
    return render(request,'login.html',context)

#registration page
def registerPage(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password')
        pass2 = request.POST.get('re_password')

        if pass1 == pass2:
            #validating the given user information
            if not(User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
                user = User.objects.create_user(username=username,password=pass1,first_name=firstname,last_name=lastname)
                user.save()
                return redirect('/')
            else:
                messages.info(request,"email or username already exists")
                return redirect('register')
        else:
            messages.info(request,"your re-entered password didn't match")
            return redirect('register')

    context = {'title':'register'}
    return render(request,'register.html',context)

#search page
@login_required(login_url='/')
def searchPage(request):
    if request.method == 'POST':
        values = request.POST.get('inputvalues')
        search = request.POST.get('searchvalues')
        #checking for valid inputs
        try:
            #sorting the given list and removing all the spaces
            val = sorted([int(i) for i in values.replace(" ","").split(',')],reverse=True)
            check = int(search)
            flag = False
            #for showing the result label
            msg = 'show' 
            #checking if the value is in the given list
            if check in val:
                flag = True 
            
            #saving the inputs in database
            info = ClientAPI(status=flag,inputvalues=val)
            info.save()

            context = {'title':'search','flag':flag,'msg':msg}
        except:
            messages.info(request,"Invalid input")
            return redirect('search')
    else:
        context = {'title':'search'}
    
    return render(request,'search.html',context)

#API View
@api_view(['GET'])
def clientDetail(request,pk):
    details = ClientAPI.objects.get(id=pk)
    serializer = ClientSerializer(details,many=False)
    return Response(serializer.data)

#API List
@api_view(['GET'])
def clientDetailList(request):
    list = ClientAPI.objects.all().order_by('-id')
    serializer = ClientSerializer(list,many=True)
    return Response(serializer.data)
#API View
@api_view(['DELETE'])
def clientDelete(request,pk):
    client = ClientAPI.objects.get(id=pk)
    client.delete()  # or something your code.
    return Response({
        "message": "Client was deleted."
    },status=status.HTTP_204_NO_CONTENT)


#logout page
def logoutPage(request):
    auth.logout(request)
    return redirect('/')