from django.shortcuts import render, HttpResponse, redirect
from .models import Contact
from django.contrib import messages
from blog.models import Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
# Create your views here.

def home(request):
    return render(request, 'home/home.html')
    # return HttpResponse("this is Home")

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']

        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request, "Please fill form correctly!!!")
        else:
            contact = Contact(name= name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, "Your message has been successfully send")

    return render(request, 'home/contact.html')

def about(request):
    return render(request, 'home/about.html')

def search(request):
    # allPosts = Post.objects.all()
    query = request.GET['query']
    if len(query)>150:
        allPosts = Posts.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent)
    
    if allPosts.count() == 0:
        messages.warning(request, "No Search results found please refine your query")
    params = {'allPosts': allPosts, 'query':query}
    return render(request, 'home/search.html', params)


def handleSignup(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        #Check for error Inputes
        # Username should contain less than 10 characters
        if len(username)> 10:
            messages.error(request,"Your username must be under 10 characters")
            return redirect('home')

        #username should be alphaNumeric
        if not username.isalnum():
            messages.error(request,"Your username should only contain letters and numbers")
            return redirect('home')
        # Paassword should match
        if password1 != password2:
            messages.error(request, "Password do not matched")
            return redirect('home')



        #Create User
        myuser = User.objects.create_user(username, email, password1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your account successfully created")
        return redirect('home')
    else:
        return HttpResponse('404 - Not Found')

def handleLogin(request):
    if request.method == "POST":
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username= loginusername, password= loginpassword)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully loged in")
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials, Please try again")
            return redirect('home')

    return HttpResponse("this is login page")

def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully loged Out")
    return redirect('home')

