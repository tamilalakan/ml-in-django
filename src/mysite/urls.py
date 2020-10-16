"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path


from personal.views import (
	home_screen_view,
)
from account.views import (
    registration_view,
    logout_view,
    login_view,
    account_view,
    project_view,
    project_sum,
    result_view,
    url_view,
    result_url,
    upload,
    result_file,

)
urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),
    path('', home_screen_view, name="home"),
    path('register/', registration_view, name="register"),
    path('logout/', logout_view, name="logout"),
    path('login/', login_view, name="login"),
    path('account/', account_view, name="account"),
    path('project/', project_view, name="project"),
    path('project_summerize/', project_sum, name="project_summerize"),
    path('project_summerize/result_view', result_view, name="result_view"),
    path('url_summerize/', url_view, name="url_summerize"),
    path('url_summerize/result_url', result_url, name="result_url"),
    path('upload/', upload, name="upload"),
    path('upload/result_file', result_file, name="result_file"),

]
