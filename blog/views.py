from django.shortcuts import get_object_or_404, render
from .models import Post, Category, Comment, EmailSubscriber
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import JsonResponse
from django.core.validators import validate_email
from django.contrib import messages
from taggit.models import Tag
from better_profanity import profanity

def SideBarWork():
    context={}
    context['categorys'] = Category.objects.all()
    context['Popular_Posts'] = Post.objects.annotate(num_items=Count('comments')).order_by('-visitorCount','-num_items')[:4]
    return context

# Create your views here.
def BlogHome(request):
    context = {}

    #setup Paginator
    p = Paginator(Post.objects.all(),8)
    page = request.GET.get('page')
    posts = p.get_page(page)

    context['posts'] = posts
    context.update(SideBarWork())
    return render(request,'blogHome.html',context)


def BlogPost(request, slug):
    context = {}
    post = Post.objects.get(slug=slug)

    if request.is_ajax():
        name = request.POST.get('commentName', None)
        email = request.POST.get('commentEmail', None)
        message = request.POST.get('commentMessage', None)

        try :
            validate_email(email)
            assert(len(name)>0)
            assert(len(message)>0)
            name = profanity.censor(name)
            message = profanity.censor(message)
            comment = Comment(name=name,email=email,body=message, post=post)
            comment.save()
            response = {
            }
            return JsonResponse(response)
        except Exception as e:
            response = {
                'msg': "Comment data not valid, " + str(e),
            }
            return JsonResponse(response)

    post.visitorCount+=1
    post.save()

    context['post'] = post
    # context['form'] = form

    posts = Post.objects.all()
    if post.post_id != 1 :
        context['previousPost'] = Post.objects.get(post_id=post.post_id-1)
        # print(context['previousPost'])
    if (post.post_id != len(posts)):
        context['nextPost'] = Post.objects.get(post_id=post.post_id+1)
        # print(context['nextPost'])
    

    context.update(SideBarWork())

    return render(request,'blogPost.html',context)

def CategoryView(request,slug):
    context = {}
    cat = Category.objects.get(slug=slug)
    posts = Post.objects.filter(cat = cat)


    #setup Paginator
    p = Paginator(Post.objects.filter(cat = cat),8)
    page = request.GET.get('page')
    posts = p.get_page(page)

    context['posts'] = posts
    context.update(SideBarWork())
    return render(request,'blogHome.html',context)

def searchPost(request):
    if 'searchPost' in request.GET:
        value = request.GET['searchPost']
        pp = Post.objects.filter(content__contains=value)

        context = {}

        #setup Paginator
        p = Paginator(pp,8)
        page = request.GET.get('page')
        posts = p.get_page(page)

        context['posts'] = posts
        context.update(SideBarWork())
        return render(request,'blogHome.html',context)
    pass

def TagView(request, slug):
    tag = get_object_or_404(Tag, slug = slug)
    posts = Post.objects.filter(tags = tag)
    context = {}

    #setup Paginator
    p = Paginator(Post.objects.filter(tags = tag),8)
    page = request.GET.get('page')
    posts = p.get_page(page)

    context['posts'] = posts
    context.update(SideBarWork())
    return render(request,'blogHome.html',context)

def emailSubscription(request):
    if request.is_ajax():
        email = request.POST.get('email', None) # getting data from email input 

        try :
            validate_email(email) #cheking if email and last_name have value
            try:
                obj = EmailSubscriber.objects.get(email=email)
                obj.is_active = True
                obj.save()
            except :
                e = EmailSubscriber(email=email)
                e.save()
            response = {
                'msg': 'Your email has been saved successfully'
            }
            return JsonResponse(response) # return response as JSON
        except Exception as e :
            response = {
                'msg': str(e),
            }
            return JsonResponse(response)
    pass

def unsubscribeEmail(request,pk):
    try :
        email = EmailSubscriber.objects.get(uuid = pk)
        email.is_active = False
        email.save()
        messages.success(request, 'Successfully Unsubscribed')
        
        context = {}
        context.update(SideBarWork())
        return render(request,'blogHome.html',context)

    except :
        messages.error(request, 'Not valid Link')
        
        context = {}
        context.update(SideBarWork())
        return render(request,'blogHome.html',context)

    pass
