from django.conf.urls import url,include
from basic_app import views #can also say from . import views

#TEMPLATE URLS!
app_name = 'basic_app'#need to set up the app_name variable

urlpatterns = [
    url(r'^register/$',views.register, name = 'register'),
    url(r'^user_login/$',views.user_login, name='user_login')
]
