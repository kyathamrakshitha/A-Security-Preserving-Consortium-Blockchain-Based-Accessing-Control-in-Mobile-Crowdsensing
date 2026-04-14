from django.urls import path

from . import views

urlpatterns = [path("index.html", views.index, name="index"),
	       path('MobileLogin', views.MobileLogin, name="MobileLogin"),
	       path('MobileLoginAction', views.MobileLoginAction, name="MobileLoginAction"),
	       path('StakeLogin', views.StakeLogin, name="StakeLogin"),
	       path('StakeLoginAction', views.StakeLoginAction, name="StakeLoginAction"),	   
	       path('Register', views.Register, name="Register"),
	       path('RegisterAction', views.RegisterAction, name="RegisterAction"),
	       path('GenerateTask', views.GenerateTask, name="GenerateTask"),
	       path('GenerateTaskAction', views.GenerateTaskAction, name="GenerateTaskAction"),
	       path('DownloadData', views.DownloadData, name="DownloadData"),
	       path('DownloadDataAction', views.DownloadDataAction, name="DownloadDataAction"),
	       path('Graph', views.Graph, name="Graph"),
	       path('CacheGraph', views.CacheGraph, name="CacheGraph"),

	       path('UploadData', views.UploadData, name="UploadData"),
	       path('UploadDataAction', views.UploadDataAction, name="UploadDataAction"),
	       path('Download', views.Download, name="Download"),
	       path('ViewTask', views.ViewTask, name="ViewTask"),
]