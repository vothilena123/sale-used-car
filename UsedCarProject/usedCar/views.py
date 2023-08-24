from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import UserProfile, PostSell, PostSellImages, LikePost, Follow, Thread
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.contrib.messages.api import add_message
import joblib
from flask import Flask, jsonify
from flask_cors import CORS
import pickle
import pandas as pd
import numpy as np
import os
from itertools import chain

app=Flask(__name__)
cors=CORS(app)
model=joblib.load(os.path.join('LinearRegressionModelForCar3.pkl'))
car=pd.read_csv('new_cars_list5.csv')



@login_required(login_url='login')
def index(request):    
    user_object = User.objects.get(username=request.user.username)
    user_profile = UserProfile.objects.get(user = user_object)
    # post_sale = PostSell.objects.get(user = user_object)
    posts = PostSell.objects.all()
    # post_images = PostSellImages.objects.filter(post_id= post_sale)

    # if request.method == 'POST':
    #     search_car_name = request.POST['search-car-name']
    #     print(search_car_name)
    #     if search_car_name:
    #         car_searched = PostSell.objects.filter(carName = search_car_name)
    #         return render(request, 'pages/carSearched.html', {'carSearched': car_searched})
    #     else:
    #         add_message(request, messages.SUCCESS, 'There is no car found')
    #         return render(request,'pages/home.html')


    return render(request,'pages/home.html' , {'user_profile': user_profile ,  'posts': posts})



@login_required(login_url='login')
def predict(request):

    user_object = User.objects.get(username=request.user.username)
    user_profile = UserProfile.objects.get(user = user_object)

   
    manufacturer_names=sorted(car['manufacturer_name'].unique())
    model_names=sorted(car['model_name'].unique())
   

    return render(request,'pages/predict.html' , {'user_profile': user_profile, 'manufacturer_names':manufacturer_names, 'model_names':model_names })


def predictResult(request):

    user_object = User.objects.get(username=request.user.username)
    user_profile = UserProfile.objects.get(user = user_object)
    
    if request.method == 'POST':
        manufacturer_name = request.POST['manufacturer_name']
        model_name = request.POST['model_name']
        transmission = request.POST['transmission']
        color = request.POST['color']
        odometer_value = request.POST['odometer_value']
        year_produced = request.POST['year_produced']
        engine_type = request.POST['engine_type']
        body_type = request.POST['body_type']
        

        dataFrame = pd.DataFrame(columns=['manufacturer_name', 'model_name', 'transmission', 'color', 'odometer_value', 'year_produced', 'engine_type', 'body_type'],
                        data=np.array([manufacturer_name,model_name,transmission,color,odometer_value,year_produced,engine_type,body_type]).reshape(1, 8))

        print(dataFrame)
        print(model)
        

        predictExpectation = model.predict(dataFrame)

        prediction = str(np.round(predictExpectation[0],2))
        print(prediction)
        

        # return jsonify({'prediction': prediction})
        

    return render(request,'pages/predictResult.html', {'user_profile': user_profile,'prediction': prediction, 'manufacturer_name':manufacturer_name, 'model_name': model_name, 'transmission':transmission, 'color': color, 'odometer_value': odometer_value, 'year_produced': year_produced, 'engine_type': engine_type, 'body_type': body_type})



@login_required(login_url='login')
def postSale(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = UserProfile.objects.get(user = user_object)

    if request.method == 'POST':
        user = request.user.username
        carName = request.POST['car_name']
        image1 = request.FILES.get('picture')
        carImages = request.FILES.getlist("file[]")
        yearOfManufacture = request.POST['year']
        carStatus = request.POST['car_status']
        transmission = request.POST['transmission']
        fuel = request.POST['fuel']
        color = request.POST['color']
        kilimetersRun = request.POST['km_run']
        locationSell = request.POST['location_sell']
        carPrice = request.POST['car_price']
        description = request.POST['description']


        new_post = PostSell.objects.create(user=user, carName=carName, image1 = image1, yearOfManufacture = yearOfManufacture, carStatus = carStatus, transmission = transmission, fuel = fuel, color = color, kilimetersRun = kilimetersRun, locationSell = locationSell, carPrice = carPrice, description = description)
        new_post.save()

        # list = []

        for img in carImages:
            fs=FileSystemStorage()
            file_path=fs.save(img.name, img)
            # list.append(file_path)
            new_post_imgs = PostSellImages.objects.create(post_id = new_post, carImage = file_path)
            new_post_imgs.save()

        return redirect('/')

    
    else:
        return render(request,'pages/sale.html' , {'user_profile': user_profile})


def updatePost(request, id):
    postCurrent = PostSell.objects.get(id = id)
    # with open(postCurrent.image1.url, 'r') as f:
    #     file_content = f.read()
    postCurrentImage = PostSellImages.objects.filter(post_id = postCurrent)

    context = {
        'postCurrent' : postCurrent,
        'postCurrentImage': postCurrentImage,
        # 'file_content' : file_content
    }



    return render(request,'pages/updatePost.html', context)



def updated(request, id): 

    postUpdated = PostSell.objects.get(id = id)
    imagesUpdated = PostSellImages.objects.filter(post_id = postUpdated)

    if request.method == 'POST':
        user = request.user.username
        carName = request.POST.get("car_name")
        image1 = request.FILES.get('picture')
        # carImages = request.FILES.getlist("file[]")
        yearOfManufacture = request.POST.get("year")
        carStatus = request.POST.get("car_status")
        transmission = request.POST.get("transmission")
        fuel = request.POST.get("fuel")
        color = request.POST.get("color")
        kilimetersRun = request.POST.get("km_run")
        locationSell = request.POST.get("location_sell")
        carPrice = request.POST.get("car_price")
        description = request.POST.get("description")

        # update_post = PostSell.objects.create(user=user, carName=carName, image1 = image1, yearOfManufacture = yearOfManufacture, carStatus = carStatus, transmission = transmission, fuel = fuel, color = color, kilimetersRun = kilimetersRun, locationSell = locationSell, carPrice = carPrice, description = description)
        # update_post.save()

        postUpdated.user = user
        postUpdated.carName = carName
        postUpdated.image1 = image1
        postUpdated.yearOfManufacture = yearOfManufacture
        postUpdated.carStatus = carStatus
        postUpdated.transmission = transmission
        postUpdated.fuel = fuel
        postUpdated.color = color
        postUpdated.kilimetersRun = kilimetersRun
        postUpdated.locationSell = locationSell
        postUpdated.carPrice = carPrice
        postUpdated.description = description

        postUpdated.save()

        return redirect('/')



        # for img in carImages:
        #     fs=FileSystemStorage()
        #     file_path=fs.save(img.name, img)
        #     # list.append(file_path)

        #     imagesUpdated.post_id = file_path
        #     imagesUpdated.save()

    return render(request,'pages/home.html')




def deletePost(request, id):
    deletedPost = PostSell.objects.filter(id = id)
    deletedPost.delete()
    return redirect('/')


def blog(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = UserProfile.objects.get(user = user_object)
    return render(request,'pages/blog.html' , {'user_profile': user_profile})

def msearch(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = UserProfile.objects.get(user = user_object)
    return render(request,'pages/mSearch.html' , {'user_profile': user_profile})

def about(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = UserProfile.objects.get(user = user_object)
    return render(request,'pages/about.html' , {'user_profile': user_profile})

def register(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        repeatedPassword = request.POST['repeatedPassword']

        if password == repeatedPassword:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Used')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'User Name Used')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                # Login user and redirect to account setting page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)
               
                # Create profile obj for the user just create
                user_model = User.objects.get(username=username)
                new_profile = UserProfile.objects.create(user=user_model, userID=user_model.id)
                new_profile.save()
                return redirect('accountSettings')

        else:
            messages.info(request, 'Password Does Not Match')
            return redirect('register')

    else:
        return render(request,'pages/register.html')

def login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Login Information Is Incorrect')
            return redirect('login')
    else:
        return render(request,'pages/login.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')


@login_required(login_url='login')
def accountSettings(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        
        if request.FILES.get('image') == None:
            image = user_profile.profileImage 
            backgroundImage = request.FILES.get('backgroundImage')
            about = request.POST['about']
            location = request.POST['location']
            detailAdress = request.POST['detailAdress']
            phoneNumber = request.POST['phoneNumber']

            user_profile.profileImage = image
            user_profile.backgroundImage = backgroundImage
            user_profile.about = about
            user_profile.location = location
            user_profile.detailAdress = detailAdress
            user_profile.phoneNumber = phoneNumber
            user_profile.save()

        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            backgroundImage = request.FILES.get('backgroundImage')
            about = request.POST['about']
            location = request.POST['location']
            detailAdress = request.POST['detailAdress']
            phoneNumber = request.POST['phoneNumber']

            user_profile.profileImage = image
            user_profile.backgroundImage = backgroundImage
            user_profile.about = about
            user_profile.location = location
            user_profile.detailAdress = detailAdress
            user_profile.phoneNumber = phoneNumber
            user_profile.save()

        return redirect('/')


    return render(request,'pages/accountSettings.html', {'user_profile': user_profile})

@login_required(login_url='login')
def carDetail(request,id):
    postDetail = PostSell.objects.get(id = id)
    postOwner = User.objects.get(username = postDetail)
    postOwnerProfile = UserProfile.objects.get(user = postOwner)
    postImages = PostSellImages.objects.filter(post_id = postDetail)
    user_object = User.objects.get(username=request.user.username)
    user_profile = UserProfile.objects.get(user = user_object)

    context = {
        
        'postDetail': postDetail,
        'postOwner': postOwner,
        'postOwnerProfile': postOwnerProfile,
        'postImages': postImages,
        'user_object' : user_object,
        'user_profile': user_profile,
        # 'postSell' : postSell,
    }

    return render(request,'pages/carDetail.html', context)



@login_required(login_url='login')
def likePost(request):
    username = request.user.username
    post_liked_id = request.GET.get('post_liked_id')
    print(username)
    print(post_liked_id)
    
    post_liked = PostSell.objects.get(id=post_liked_id)
    print(post_liked)
    

    like_filter = LikePost.objects.filter(post_liked_id=post_liked_id, username=username).first()

    if like_filter == None:
        new_like = LikePost.objects.create(post_liked_id=post_liked_id, username=username)
        new_like.save()
        post_liked.numberOfLike = post_liked.numberOfLike+1
        post_liked.save()
        return redirect('/')
    else:
        like_filter.delete()
        post_liked.numberOfLike = post_liked.numberOfLike-1
        post_liked.save()
        return redirect('/')



def follow(request):

    if request.method == 'POST':
        
        follower = request.POST['follower']
        user = request.POST['user']

        if Follow.objects.filter(follower = follower, user = user).first():
            delete_follower = Follow.objects.get(follower = follower, user = user)
            delete_follower.delete()
            return redirect('/profile/'+user)

        else:
            new_follower = Follow.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/'+user)
    else:
        return redirect('/')


@login_required(login_url='login')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = UserProfile.objects.get(user=user_object)
    user_posts = PostSell.objects.filter(user = pk)
    user_post_long = len(user_posts)
    

    follower = request.user.username
    user = pk

    if Follow.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    followers = len(Follow.objects.filter(user=pk))
    following = len(Follow.objects.filter(follower=pk))

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_long': user_post_long,
        'button_text': button_text,
        'followers': followers,
        'following': following,
    }
    
    return render(request, 'pages/profile.html', context)


@login_required(login_url='login')
def contact(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = UserProfile.objects.get(user=user_object)

    threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread').order_by('timestamp')
    context = {
        'user_profile': user_profile,
        'Threads': threads,
    }

    return render(request, 'pages/contact.html', context)

def carSearched(request):
    user_object = User.objects.get(username=request.user.username)
    post = PostSell.objects.filter(user=user_object)

    if request.method == 'POST':
        search_car_name = request.POST['search-car-name']
        carSearched = PostSell.objects.filter(carName__icontains=search_car_name)

        car_name_searched = []
        car_name_searched_list = []

        for name in carSearched:
            car_name_searched.append(name.id)
        
        for ids in car_name_searched:
            car_list = PostSell.objects.filter(id = ids)
            car_name_searched_list.append(car_list)
        
        car_name_searched_list = list(chain(*car_name_searched_list))

    return render(request, 'pages/carSearched.html', {'post': post, 'car_name_searched_list': car_name_searched_list })