from django.db import models
from ckeditor.fields import RichTextField
from django.template.defaultfilters import slugify

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
        if not self.imageAltText:
            self.imageAltText = self.title
        return super().save(*args, **kwargs)

#Post Model
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
    
    