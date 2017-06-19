from django.shortcuts import render
from basic_app.forms import UserForm,UserProfileInfoForm

from django.contrib.auth import authenticate, login, logout
    #this will do a lot of the heavy lifting for what we want
from django.http import HttpResponseRedirect, HttpResponse
    #simple shit for now
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
#if you ever want a view to require the user to log in
#use this login_required decorator!


# Create your views here.
def index(request):
    return render(request,'basic_app/index.html')

@login_required
def special(request):
    return HttpResponse("You are logged in, nice!")

#decorator always has to be one line above!
#With this decorator we can make sure that only a user who has logged in can log out
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):

    registered = False   #name of this variable must link up to our HTML in registration.html

    if request.method == 'POST':
        user_form = UserForm(data = request.POST)
        profile_form = UserProfileInfoForm(data = request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save() #we're grabbing the user forms, saving it to the database
            user.set_password(user.password) #hashing the password according to setting using set_password
            user.save() #and then save hashed password to the database

            #now we want to deal with our extra information: portfolio link and profile pic

            profile = profile_form.save(commit=False) #don't want to save to database yet
                                                      #avoids errors where it overrides our prevous user
            profile.user = user #sets 1 to 1 relationship according to our models (confirms our model thing in views)

            if 'profile_pic' in request.FILES: #will be located here since it's an actual FILE
                profile.profile_pic = request.FILES['profile_pic'] #FILES is a dictionary, Key is based on definition in models

                profile.save()

                registered = True
        else:
            print(user_form.errors,profile_form.errors) #print errors in case something goes wrong, as tuple pretty much

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request,'basic_app/registration.html', #context dict according to our html page
                            {'user_form': user_form,
                             'profile_form':profile_form,
                             'registered':registered})
                              #v common to have keys and value match up in context dict!


def user_login(request):
    #sometimes django will complain if you call something with 'login', especially
    #if youre importing login above (since you don't want to overwrite it in views)
    #so make sure the view doesn't share a name with your imports

    if request.method == 'POST': #is user has filled out login information
        username = request.POST.get('username')
            #we use the .get method because in our login.html file, we're just
            #using simple HTML, and we gave the Username input field a name='username
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)
            #use django's built-in authentication (make sure to always set the parameters)
            #will automatically authenticate the user for you
        if user:
            if user.is_active:
                #check if account is active
                login(request,user) #simple django login command
                return HttpResponseRedirect(reverse('index'))
                    #send the user somewhere once they've logged in
                    #if they login and it's successful, and their account is active,
                    #it will reverse them and redirect them back to the homepage
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            print("Someone tried to login and failed")
                #print something for us in the console
            print("Username: {} and password {}".format(username,password))
            return HttpResponse("invalid login details supplied")

    else:
        return render(request,'basic_app/login.html',{})
            #if request was not posted
