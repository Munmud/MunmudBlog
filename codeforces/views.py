from django.shortcuts import render 
from django.http import JsonResponse
from django.core.validators import validate_email
from blog.views import SideBarWork
from .models import Handle
from django.contrib import messages
import os
# Create your views here.

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


def formView(request):
    context ={}

    if request.is_ajax():
        first_name = request.POST.get('first_name', None)
        last_name = request.POST.get('last_name', None)
        codeforces_handle = request.POST.get('codeforces_handle', None)
        email_address = request.POST.get('email_address', None)

        try :
            validate_email(email_address)
            assert(len(first_name)>0)
            assert(len(last_name)>0)
            assert(len(codeforces_handle)>0)
            # print(first_name,last_name,email_address,codeforces_handle)


            obj = Handle(firstName = first_name,lastName=last_name,email = email_address,handle = codeforces_handle)
            obj.save()

            from django.template.loader import render_to_string
            from django.utils.html import strip_tags
            
            datatuple = []
            mp = {
                'uid' : obj.uid,
                'domain': os.environ.get('ALLOWED_HOSTS').split(',')[1],
            }
            subject = "Moontasir's Blog"
            html_message = render_to_string('mail/emailVerification.html', mp)
            plain_message = strip_tags(html_message)
            from_email = str(os.environ.get('EMAIL__VerifyEmail_HOST_USER'))
            tple = (subject,plain_message,html_message,from_email,[email_address])
            datatuple.append(tple)
            
            send_mass_html_mail(datatuple,
                    user = str(os.environ.get('EMAIL__VerifyEmail_HOST_USER')),
                    password=str(os.environ.get('EMAIL__VerifyEmail_HOST_PASSWORD'))
                )
            
            response = {
                'success': "We have sent a confirmation email. Please login to your email account to verify",
            }
            return JsonResponse(response)
        except Exception as e:
            response = {
                'msg': "Form data not valid, " + str(e),
            }
            return JsonResponse(response)

    context.update(SideBarWork())
    return render(request, 'codeforces/form.html' , context)


def confirmMail(request,uid):
    try :
        obj = Handle.objects.get(uid = uid)
        obj.isVerified = True
        obj.save()
        messages.success(request,'Your Email is verified')
    except :
        messages.error(request,'Invalid url')
    context = {}
    context.update(SideBarWork())
    return render(request,'blog/blogHome.html', context)


def unSubscribeCF(request, uid):
    try:
        handle = Handle.objects.get(uid = uid)
        handle.isActive = False
        handle.save()
        messages.success(request, 'Sorry to see you leave. To subscrive again you habe to refill the form from our website')
    except:
        messages.error(request, 'Invalid Url')
    context={}
    context.update(SideBarWork())
    return render(request , 'blog/blogHome.html' , context)

    pass