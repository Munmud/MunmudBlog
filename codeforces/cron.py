from django_cron import CronJobBase, Schedule
import codeforces_api
from codeforces.models import Contest
from django.conf import settings
from datetime import datetime
import pytz
from .helper import saveContestToDatabase, sendMail


class CheckNewContest(CronJobBase):
    RUN_EVERY_MINS = 5 # every 2 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'CheckNewContest'    # a unique code



    def do(self):
        print('Cron is running')
        try :

            #Refresh ContestList
            for x in codeforces_api.CodeforcesApi().contest_list():
                if (x.phase == 'FINISHED' ):
                    # print(x.id , x.name)
                    try : 
                        contest = Contest.objects.get(id = x.id)
                    except :
                        try:
                            date = datetime.utcfromtimestamp(x.start_time_seconds).replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
                            contest = Contest(id = x.id , name = str(x.name)[:254] , date = date)
                            contest.save()
                        except Exception as e:
                            print(e)
                    
            #Add one more contest details to database
            obj = Contest.objects.filter(isParsed = False).order_by('tryCount','-date')[:1][0]
            date = obj.date
            now = datetime.now().replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
            delta = now-date
            if (delta.days <=3):
                print("Initiating...",obj.id,obj.name)
                saveContestToDatabase(obj.id)


            #send Latest Contest Mail
            obj = Contest.objects.filter(isSend = False).order_by('-date')[:1][0]
            now = datetime.now().replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
            date = obj.date
            delta = now-date
            if (delta.days <=2):
                print('Sending Mail...' , obj.name)
                sendMail(obj)
                pass
        except Exception as e :
            print(e)
            pass

        pass    # do your thing here