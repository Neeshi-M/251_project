from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from django.views.decorators.csrf import csrf_exempt
from .forms import UserRegisterForm, UploadAssignmentForm,editForm,UploadSubmissionForm,courseForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Courses,EnrollRequest,Assignment,Submission
from django.contrib.auth import get_user_model
from django.contrib.auth import update_session_auth_hash

def home(request):
    return render(request, 'myapp/home.html')

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hi {username}, your account was created successfully')
            return redirect('home')
    else:
        form = UserRegisterForm()

    return render(request, 'myapp/register.html', {'form': form})

@login_required()
def createdcourses(request):
    data = Courses.objects.filter(user=request.user)
    return render(request,'myapp/createdcourses.html', {'data' : data})


@login_required()   
def profile(request):
    return render(request, 'myapp/profile.html')
# Create your views here.
@login_required
def sendaddrequest(request, course_id):
    from_user = request.user
    related_course = Courses.objects.get(id = course_id)
    add_request , created = EnrollRequest.objects.get_or_create(from_user=from_user,related_course=related_course)
    user_in_courses=Courses.objects.filter(users_enrolled__in = [request.user.id])	
    if created:
        messages.success(request, f'Hi {request.user.username}, your request is sent')
    else:
        messages.success(request, f'Hi {request.user.username},add_request already sent')
    course = Courses.objects.get(id = course_id)
    all_add_requests = EnrollRequest.objects.filter(related_course=course)
    return render(request, 'myapp/courseinfo.html',{'all_add_requests' : all_add_requests ,'course' : course})

@login_required
def acceptaddrequest(request, request_id):
    add_request = EnrollRequest.objects.get(id = request_id)
    course = Courses.objects.get(id = add_request.related_course.id)
    course.users_enrolled.add(add_request.from_user)
    messages.success(request,f'Added Successfully')
    add_request.delete()
    all_add_requests = EnrollRequest.objects.filter(related_course=course)
    return render(request, 'myapp/courseinfocreated.html',{'all_add_requests' : all_add_requests,'course' : course})

@login_required
def courseinfo(request,course_id):
    course = Courses.objects.get(id = course_id)
    assignments= Assignment.objects.filter(related_course = course)
    return render(request, 'myapp/courseinfo.html',{'course' : course, 'assignments': assignments })

@login_required
def courseinfocreated(request,course_id):
    course = Courses.objects.get(id = course_id)
    all_add_requests = EnrollRequest.objects.filter(related_course=course)
    assignments= Assignment.objects.filter(related_course = course)
    #assignments = course.assignments.all()
    return render(request, 'myapp/courseinfocreated.html',{'all_add_requests' : all_add_requests,'course' : course, 'assignments': assignments })
   
   
@login_required
def viewAssignment(request,assignment_id):
    assignment = Assignment.objects.get( id=assignment_id)
    assignment_creater = assignment.related_course.user
    if request.user == assignment_creater:
        submissions = Submission.objects.filter(assignme=assignment)
    else:
        submissions = Submission.objects.filter(submitter=request.user,assignme=assignment)
    return render(request,'myapp/assignment.html',{'assignment':assignment, 'submissions':submissions})

@login_required
def createnewcourse(request):
    if request.method == "POST":
        form = courseForm(request.POST)
        if form.is_valid():
            name = request.POST.get('course_name')
            course = Courses.objects.create(course_name = name, user = request.user)
            course.users_enrolled.add(request.user)
            data = Courses.objects.filter(user=request.user)
            messages.success(request,f'Added Successfully')
            return redirect('createdcourses')
    else:
        form = courseForm()
    return render(request,'myapp/createnewcourse.html',{'form': form})

@login_required
def courseslist(request):
    courses = Courses.objects.all()
    return render(request,"myapp/courseslist.html",{'courses' : courses})

@login_required
def enrolledcourses(request):
    data = Courses.objects.filter(users_enrolled__in = [request.user.id])
    return render(request, 'myapp/enrolledcourses.html', {'data' : data})

@login_required
def upload_assignment(request,course_id):
	if request.method=='POST':
		form = UploadAssignmentForm(request.POST,request.FILES)
		#messages.success(request, f'Hi, your request is sent')
		if form.is_valid():
			#messages.success(request, f'your request is sent')
			instance = Assignment(uploadfile = request.FILES['uploadfile'])
			instance.related_course=Courses.objects.get(id=course_id)
			instance.title=form.cleaned_data.get('title')
			instance.totalmarks=form.cleaned_data.get('totalmarks')
			instance.save()
			return redirect('courseinfocreated',course_id=course_id)
	else:
		form=UploadAssignmentForm()
		
	return render(request,'myapp/addassignment.html',{'form':form })
		
@login_required
def addsubmission(request,assignment_id):
    if request.method == 'POST':
        form = UploadSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            instance = Submission(ansfile = request.FILES['ansfile'])
            instance.assignme = Assignment.objects.get(id=assignment_id)
            instance.submitter = request.user
            instance.save()
            return redirect('viewAssignment',assignment_id=assignment_id)
    else:
        form = UploadSubmissionForm()
    return render(request,'myapp/addsubmission.html',{'form':form })
 
@login_required
def editprofile(request):
    if request.method == "POST":
        form = editForm(request.POST)
        if form.is_valid():
            newfirstname = form.cleaned_data.get('newfirstname')
            newlastname = form.cleaned_data.get('newlastname')
            newemail = form.cleaned_data.get('newemail')
            request.user.first_name = newfirstname
            request.user.last_name = newlastname
            request.user.email = newemail
            request.user.save()
            messages.success(request,f'Updated Successfully')
            return redirect('home')
    else:
        form = editForm()
    return render(request,'myapp/editprofile.html',{'form': form})
    	
@login_required    
def changepassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'myapp/changepassword.html', {
        'form': form
    })
    
def uploadcsv(request,assignment_id):
	if "GET" == request.method:
    		return render(request, "myapp/uploadcsvfile.html")
# if not GET, then proceed
	csv_file = request.FILES["csv_file"]
	if not csv_file.name.endswith('.csv'):
         	messages.error(request,'File is not CSV type')
         	return HttpResponseRedirect(reverse("myapp:uploadcsvfile"))
         file_data = csv_file.read().decode("utf-8")
         lines = file_data.split("\n")
         req_assignment = Assignment.objects.get(id=assignment_id)
    	
    #loop over the lines and save them in db. If error , store as string and then display
    	for line in lines:
    	    fields = line.split(",")
    	    submission=Submission.objects.get(assignme = req_assignment, submitter=fields[0])
    	    submission.marksgot = fields[1]
    	    submission.feedback = fields[2]
    	return HttpResponseRedirect(reverse("myapp:uploadcsvfile"))
	#return HttpResponseRedirect(reverse("myapp:uploadcsvfile"))
		
	
	   
    
    
    
    
    
    
    
    
