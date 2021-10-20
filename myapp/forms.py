from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import fields
from .models import Assignment,Courses,Submission
class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30,required=False)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','email','password1', 'password2','first_name','last_name']

class courseForm(forms.Form):
    course_name = forms.CharField(label='coursename', max_length=255,required=True)
    class Meta:
        model = Courses
        fields = ['course_name']
        
class UploadAssignmentForm(forms.Form):
	title = forms.CharField(max_length=255)
	uploadfile = forms.FileField(label='Select a file',help_text='max. 42 megabytes')
	totalmarks = forms.IntegerField()
	#class Meta:
	#	model = Assignment
	#	fields = [ 'title', 'uploadfile', 'totalmarks']
	# this works when you only need to save forms and no other modifications on model object.
	
class editForm(forms.Form):
    newfirstname=forms.CharField(max_length=30,label='new_firstname')
    newemail = forms.EmailField(label='new_email')
    newlastname=forms.CharField(max_length=30,label='new_lastname')
    class Meta:
        model = User
        fields = ['newfirstname','newlastname','newemail']

class UploadSubmissionForm(forms.Form):
	ansfile = forms.FileField(label='Select a file',help_text='max. 42 megabytes')
	
