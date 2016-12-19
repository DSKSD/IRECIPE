from django.conf.urls import url
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^$', views.index, name = 'index'), # 최초화면 / 타임라인!
    url(r'^chat/$', views.chat, name = 'chat'),
    url(r'^message/$', views.reply, name='reply'),
    url(r'^feedback/$', views.recomfeedback, name='feedback'), # 챗 상에서 피드백 주기
    url(r'^recipe/(?P<pk>\d+)/$', views.recipeDetail, name='recipe_detail'), # 로그 상에서 레시피 보기
    url(r'^seeDetail/$', views.seeDetail, name='see_detail'), # 챗 상에서 레시피 보기
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^accounts/register/$', views.register, name='register'), # 회원가입 POST 요청
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'), # 로그인 POST 요청
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',{'next_page': '/'}, name='logout'), # 로그아웃 요청
    url(r'^loginForm/$', TemplateView.as_view(template_name='login.html'), name='loginForm'), # 로그인 페이지 이동
    url(r'^userInfo/$', views.userInform, name='userinform')
   # url(r'^register/$', views.register, name = 'register'),
    #url(r'^logout/$',views.logout_view, name="logout"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)