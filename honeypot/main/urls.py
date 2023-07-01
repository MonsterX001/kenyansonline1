from django.urls import path
from . import views

app_name = 'main'


urlpatterns = [
    path('', views.index, name='index'),
    path('podcast/', views.podcast, name='podcast'),
    path('blog/', views.blog, name='blog'),
    path('register', views.register, name='register'),
    path('share/', views.share_view, name='share'),
    path('recommended', views.Recommended, name='recommended'),
    path('trending', views.trending_posts, name='trending'),
    path('signin', views.signin, name='signin'),
    path('account/<str:pk>', views.account, name='account'),
    path('acc-profile/', views.acc, name='acc'),
    path('logout', views.logout, name='logout'),
    path('Houseupload', views.Houseupload, name='Houseupload'),
    path('search', views.search, name='search'),
    path('profile-search', views.profilesearch, name='profile-search'),
    path('Shot', views.Shot, name='Shot'),
    path('shotss', views.shotss, name='shotss'),
    path('livechat', views.livechat, name='livechat'),
    path('terms-policy', views.terms_policy, name='terms-policy'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('hookup', views.hookup, name='hookup'),
    path('socialbook/<str:agentname>/', views.socialbook, name='socialbook'),
    path('video_play/<str:id>', views.video_play, name='video_play'),
    path('forgotpassword', views.forgotpassword, name='forgotpassword'),
    path('changepassword/<token>/', views.changepassword, name='changepassword'),
    path('follow', views.follow, name='follow'),
]