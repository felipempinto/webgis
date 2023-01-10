from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

users_page = [
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='main/password_reset.html'),name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='main/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='main/password_reset_complete.html'),name='password_reset_complete'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='main/password_reset_done.html'),name='password_reset_done')
    ]

app_name = 'main'

urlpatterns = [
    path('',views.homepage,name='homepage'),
    path('login/',views.login_request,name='login'),
    path('logout/',views.logout_request,name='logout'),
    path("user/",views.user,name='user'),
    path("download/",views.download_page,name='download'),
    path("map/",views.map,name='map'),
    path("createdata/",views.createdata,name='createdata'),
    path("deletedata/<str:source>/<int:dataid>/",views.deletedata,name='deletedata'),
    path("deleteview/<str:source>/<int:dataid>/",views.deleteview,name='deleteview'),
    path("upload-data/<source>/",views.uploaddata,name='uploaddata'),
    
]+ users_page



#+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)