from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
from django.contrib.auth.models import User


class Courses(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="creater")
    users_enrolled = models.ManyToManyField(User, blank=True)
    course_name=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()
    def __str__(self):
    	return self.course_name
    

class EnrollRequest(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="from_user")
    related_course = models.ForeignKey(Courses, on_delete=models.CASCADE,related_name="related_course")
    objects=models.Manager()
    def __str__(self):
    	return f'request from {self.from_user} for enrolling into {self.related_course} course created by {self.related_course.user}'
 
 
#def course_directory_path(instance, filename):
  
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
 #   return 'user_{0}/{1}'.format(instance.course.course_name, filename)   	
    	
class Assignment(models.Model):
    def upload_file_name(self, filename):
        return f'Assignment/stuff/{self.title}/{filename}'
    title = models.CharField(max_length=255)
    related_course = models.ForeignKey(Courses,on_delete=models.CASCADE,related_name='assignments')
    uploadfile = models.FileField(upload_to=upload_file_name, unique=True)
    totalmarks = models.IntegerField()
    objects=models.Manager()
    def str(self):
	    return self.title
	
#class Grades(models.Model):
#	assignment=models.

class Submission(models.Model):
    def upload_file_name(self, filename):
        return f'Assignment/answers/{self.assignme}/{self.id}/{filename}'
    submitter = models.ForeignKey(User,on_delete=models.CASCADE,related_name='submitter')
    assignme = models.ForeignKey(Assignment,on_delete=models.CASCADE,related_name='assignme')
    marksgot = models.IntegerField(null=True)
    ansfile = models.FileField(upload_to=upload_file_name, unique=True)
    feedback = models.TextField(blank=True)
    objects=models.Manager()

