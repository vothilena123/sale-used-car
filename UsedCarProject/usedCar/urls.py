from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accountSettings', views.accountSettings, name='accountSettings'),
    path('predict', views.predict, name='predict'),
    path('predictResult', views.predictResult, name='predictResult'),
    path('msearch', views.predict, name='msearch'),
    path('sale', views.postSale, name='sale'),
    path('blog', views.blog, name='blog'),
    path('register', views.register, name='register'), 
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('about', views.about, name='about'),
    path('carDetail/<uuid:id>', views.carDetail, name='carDetail'),
    path('likePost', views.likePost, name='likePost'),
    path('follow', views.follow, name='follow'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('contact', views.contact, name='contact'),
    path('carSearched', views.carSearched, name='carSearched'),
    path('updatePost/<uuid:id>', views.updatePost, name='updatePost'),
    path('deletePost/<uuid:id>', views.deletePost, name='deletePost'),
    path('updated/<uuid:id>', views.updated, name='updated'),


]