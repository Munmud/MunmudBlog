import uuid
from django.db import models
from ckeditor.fields import RichTextField
from django.template.defaultfilters import slugify
from taggit.managers import TaggableManager

#Category Model
class Category(models.Model):
    title = models.CharField(max_length=100)
    cat_id = models.AutoField(primary_key=True)
    slug = models.SlugField(max_length=255, unique=True, null=False, blank=False)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

#Post Model
post_status = [("pending","Pending"),("approaved","Approaved")]
class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    content = RichTextField(blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, null=False, blank=False)
    cat = models.ForeignKey(Category,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post/')
    imageAltText = models.CharField(default='image', max_length=200,null=True, blank=True)
    add_date = models.DateTimeField(auto_now_add=True)
    visitorCount = models.IntegerField(default=0,null=True, blank=True)
    status = models.CharField(max_length=250,choices=post_status, default="pending")
    tags = TaggableManager()


    class Meta:
        ordering = ['-add_date']

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.imageAltText:
            self.imageAltText = self.title
        return super().save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=False, blank=False)
    email = models.EmailField(null=False,blank=False)
    body = RichTextField(blank=False, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date_added']
    
    def __str__(self):
        return self.name
    
    
class EmailSubscriber(models.Model):
    email=models.EmailField(null=False,blank=False,unique=True)
    is_active= models.BooleanField(default=True)
    uuid = models.CharField(max_length=250)

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = str(uuid.uuid4())[:249]
        
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.email


class Image(models.Model):
    image = models.ImageField(upload_to='postContent/')
    imageAltText = models.CharField(default='image', max_length=200,null=True, blank=True)


# from django.db.models.signals import pre_save
# from django.dispatch import receiver
# @receiver(pre_save, sender=Post)
# def sendMail(sender, instance,*args, **kwargs):

#     if instance.post_id is None: # new object will be created
#         pass 
#     else:
#         previous = sender.objects.get(post_id=instance.post_id)
#         if previous.status == 'pending' and instance.status == 'approaved': # field is updated