from django.urls import path
from . import views
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('',views.home, name='home'),
    path('register/',views.register,name='register'),
    path('profile/',views.profile,name='profile'),
    path('createdcourses/', views.createdcourses, name='createdcourses'),
    path('courseslist/', views.courseslist,name = 'courseslist'),
    path('enrolledcourses/',views.enrolledcourses,name = "enrolledcourses"),
    path('courseinfo/<int:course_id>',views.courseinfo,name="courseinfo"),
    path('courseinfocreated/<int:course_id>',views.courseinfocreated,name="courseinfocreated"),
    path('login/',auth_view.LoginView.as_view(template_name='myapp/login.html'),name="login"),
    path('sendaddrequest/<int:course_id>',views.sendaddrequest,name = 'sendaddrequest'),
    path('acceptaddrequest/<int:request_id>', views.acceptaddrequest, name = 'acceptaddrequest'),
    path('logout/',auth_view.LogoutView.as_view(template_name='myapp/logout.html'),name="logout"),
    path('addassignment/<int:course_id>',views.upload_assignment,name='addassignment'),
    path('createnewcourse/',views.createnewcourse,name = "createnewcourse"),
    path('viewAssignment/<int:assignment_id>',views.viewAssignment,name='viewAssignment'),
    path('editprofile/',views.editprofile,name='editprofile'),
    path('addsubmission/<int:assignment_id>',views.addsubmission,name = 'addsubmission'),
    path('changepassword/',views.changepassword,name = 'changepassword'),
    path('uploadcsv/<int:assignment_id>',views.uploadcsv,name = 'uploadcsv'),
]
