import codeforces_api
from codeforces.models import Contest, Rank, Handle
from django.conf import settings
from blog.models import Post
from django.db.models import Count
from django.core.mail import get_connection, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import os

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


def sendMail(contest):

    datatuple=[]
    popularPosts = Post.objects.annotate(num_items=Count('comments')).order_by('-visitorCount','-num_items')[:4]
    try :
        for obj in Handle.objects.filter(isVerified=True, isActive = True):
            email = obj.email
            handle = obj.handle
            try :
                rank = Rank.objects.get(contest = contest , handle = handle)

                context = {
                    'firstName' : obj.firstName,
                    'lastName' : obj.lastName,
                    'handle' : handle,
                    'contest' : contest.name,
                    'globalRank' : rank.globalRank,
                    'country' : rank.country,
                    'organization' : rank.organization,
                    'domain' : os.environ.get('ALLOWED_HOSTS').split(',')[1],
                    'unSubscribeId' : obj.uid,
                    'Popular_Posts' : popularPosts,
                    'MEDIA_URL' : settings.MEDIA_URL
                }

                if rank.countryRank == None and rank.organizationRank == None :
                    context['addMessage'] = 'Please add your Country and Organization in https://codeforces.com/settings/social'
                elif rank.countryRank == None :
                    context['addMessage'] = 'Please add your Country in https://codeforces.com/settings/social'
                    context['organizationRank'] = rank.organizationRank
                elif rank.organizationRank == None :
                    context['addMessage'] = 'Please add your Organization in https://codeforces.com/settings/social'
                    context['countryRank'] = rank.countryRank
                else :
                    context['organizationRank'] = rank.organizationRank
                    context['countryRank'] = rank.countryRank
                    context['addMessage'] = ''

                subject = "Codeforces Rank for " + str(contest.name) 
                html_message = render_to_string('mail/cfRank.html', context)
                plain_message = strip_tags(html_message)
                from_email = 'CF Rank by Moontasir <' + str(os.environ.get('EMAIL_HOST_USER')) + '>'
                tple = (subject,plain_message,html_message,from_email,[email])
                datatuple.append(tple)
                print(handle)
            except Exception as e: 
                # print(handle, " -> didn't participated")
                pass
        
        send_mass_html_mail(datatuple)
        contest.isSend = True 
        contest.save()
    except Exception as e :
        print(e)
            

def getContestStanding(contest_id):
    try :
        ls = []
        r = codeforces_api.CodeforcesApi().contest_standings(contest_id=contest_id)
        for xx in r['rows']:
            for x in xx.party.members:
                han = str(x.handle)
                ls.append(han)
        return ls
    except :
        return []


def requestCodeforcesToGetDetailsOfHandles(handles):
    if len(handles) ==0 : return None
    res = []
    try:
        r = codeforces_api.CodeforcesApi().user_info(handles=handles)
        for x in r:
            temp ={}
            temp['handle'] = x.handle
            temp['country'] = x.country
            temp['organization'] = x.organization
            res.append(temp)
        return res

    except Exception as e:
        if len(handles) != 1 : 
            half = len(handles)//2
            first = handles[:half]
            second = handles[half:]
            first = requestCodeforcesToGetDetailsOfHandles( first )
            second = requestCodeforcesToGetDetailsOfHandles( second )

            if first != None : res+= first
            if second != None : res+= second
            return res
        else :
            try:
                r = codeforces_api.CodeforcesApi().user_info(handles=handles)
                for x in r:
                    temp ={}
                    temp['handle'] = x.handle
                    temp['country'] = x.country
                    temp['organization'] = x.organization
                    res.append(temp)
                return res
            except: 
                return None


def saveRankToDatabase(contest_id, contest_ranking):
    if (len(contest_ranking)) == 0 : return

    contest = Contest.objects.get(id=contest_id)
    
    countryCount = {}
    organizationCount = {}
    try :
        for globalRank, handle_details in enumerate( contest_ranking ) :
            handle = handle_details['handle']
            country = handle_details['country']
            organization = handle_details['organization']
            countryRank = None
            organizationRank = None

            if country== None : country = ''
            if organization== None : organization = ''

            if country != '' :
                if country in countryCount:
                    countryCount[country]+=1
                else : 
                    countryCount[country] = 1
                countryRank = countryCount[country]

            if organization != '' :
                if organization in organizationCount:
                    organizationCount[organization]+=1
                else : 
                    organizationCount[organization] = 1
                organizationRank = organizationCount[organization]

            rank = Rank(
                handle = handle, 
                country = country, 
                countryRank = countryRank,
                organization = organization,
                organizationRank = organizationRank, 
                contest = contest ,
                globalRank = globalRank+1
            )
            rank.save()
        
    except Exception as e:
        print(e)


def saveContestToDatabase(contest):
    try :
        for rank in Rank.objects.filter(contest = contest):
            rank.delete()
        contest.isSend = False
        contest.isParsed = False
        contest.save()
        standing= getContestStanding(contest_id = contest.id)
        assert(len(standing) != 0)
        print('Cf Standing Count = ', len(standing))
        handleDetails = requestCodeforcesToGetDetailsOfHandles(standing)
        print('Cf Parse handle-details Count = ', len(handleDetails))
        assert(len(handleDetails) != 0)
        if contest.tryCount <=10 :
            assert(len(handleDetails) == len(standing))
        saveRankToDatabase(contest_id = contest.id, contest_ranking = handleDetails)
        assert(len(Rank.objects.filter(contest = contest)) != 0)
        contest.isParsed = True
        contest.save()
        print('successfully Parsed')
    except Exception as e :
        print(e)
        contest.tryCount = contest.tryCount+1
        contest.save()
