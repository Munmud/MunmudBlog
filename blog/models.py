import uuid
from django.db import models
from ckeditor.fields import RichTextField
from django.template.defaultfilters import slugify
import os

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
    uuid = models.CharField(max_length=10)

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = str(uuid.uuid4())[:9]
        
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.email


from django.core.mail import get_connection, EmailMultiAlternatives
def send_mass_html_mail(datatuple, fail_silently=False, user=None, password=None, 
                        connection=None):
    """
    Given a datatuple of (subject, text_content, html_content, from_email,
    recipient_list), sends each message to each recipient list. Returns the
    number of emails sent.

    If from_email is None, the DEFAULT_FROM_EMAIL setting is used.
    If auth_user and auth_password are set, they're used to log in.
    If auth_user is None, the EMAIL_HOST_USER setting is used.
    If auth_password is None, the EMAIL_HOST_PASSWORD setting is used.

    """
    connection = connection or get_connection( username=user, password=password, fail_silently=fail_silently)
    messages = []
    for subject, text, html, from_email, recipient in datatuple:
        message = EmailMultiAlternatives(subject, text, from_email, recipient)
        message.attach_alternative(html, 'text/html')
        messages.append(message)
    return connection.send_messages(messages)


from django.db.models.signals import pre_save
from django.dispatch import receiver
@receiver(pre_save, sender=Post)
def sendMail(sender, instance,*args, **kwargs):

    if instance.post_id is None: # new object will be created
        pass 
    else:
        previous = sender.objects.get(post_id=instance.post_id)
        if previous.status == 'pending' and instance.status == 'approaved': # field is updated

            datatuple = []
            for x in EmailSubscriber.objects.all():
                if x.is_active:
                    email = x.email
                    mp = {}
                    mp['title'] = instance.title
                    mp['slug'] = instance.slug
                    mp['id'] = x.uuid
                    mp['domain'] = os.environ.get('ALLOWED_HOSTS').split(',')[1]

                    from django.template.loader import render_to_string
                    from django.utils.html import strip_tags

                    subject = "Moontasir's Blog"
                    html_message = render_to_string('mail/newPost.html', mp)
                    plain_message = strip_tags(html_message)
                    from_email = str(os.environ.get('EMAIL__new_post'))
                    tple = (subject,plain_message,html_message,from_email,[email])
                    datatuple.append(tple)
            
            send_mass_html_mail(datatuple,
                    user = str(os.environ.get('EMAIL__new_post_HOST_USER')),
                    password=str(os.environ.get('EMAIL__new_post_HOST_PASSWORD'))
                )
            

    pass  