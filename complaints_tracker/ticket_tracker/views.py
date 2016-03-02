import subprocess
import sys

from django.contrib.auth.views import login
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from models import TicketRegister, TicketStatus
from ticket_tracker.send_mail import send_mail
from csv_generator import generate_csv


def ticket_register(request):
    try:
        username = request.GET.get('username')
        username_exixts = User.objects.get_by_natural_key(username=username)  # need to check this with ldap
        if not username_exixts:
            raise ObjectDoesNotExist('No such user exists')
        system_id = request.GET.get('system_id')
        bashcommand = "nslookup " + system_id + " |grep 'Address: '"
        p = subprocess.Popen(bashcommand, shell=True, stdout=subprocess.PIPE)
        p = p.communicate()[0]
        if not p:
            raise ObjectDoesNotExist('Wrong system id')
        p = p.split()
        ipaddress = p[-1]
        user_complaints = request.GET.get('complaints').strip()
        registered_date = timezone.now()
        status_id = TicketStatus.objects.get(name="unassigned").id
        # print request.GET
        queryset = TicketRegister(created_on=registered_date, created_by=username_exixts,
                                  ipaddress=ipaddress, system_id=system_id, status_id=status_id, priority='medium',
                                  complaints=user_complaints)
        queryset.save()
        email_msg_id = send_mail(queryset, 'new_issue')
        queryset.email_msg_id = email_msg_id
        queryset.save()
        return HttpResponse(
            "The issue has been raised please login to tickets dashboard for tracking you issue.Thank you %s Your "
            "Ticket_id is %s" % (username, queryset.id))
    except ObjectDoesNotExist as e:
        return HttpResponse(e)
    except Exception, e:
        print(e.args)
        return HttpResponse("server Unavailable")


def custom_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('pending_ticket'))
    else:
        return login(request, template_name='login.html')


def registration(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        error = ""
        print username, password
        # ###check if user exists in ldap some queries ()
        # ###if no then send an error

        # ###if exists then check if a user with same name exists here?
        # ###if yes prompt a duplicate error
        # ###else create a user
        try:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            error = "Your id was success successfully created please login"
            group = Group.objects.get(name='user')
            user.groups.add(group)
            # ##also send a mail to the admin to assign the group.
            return render(request, "login.html", {'error': error})

        except Exception as e:
            print(e.args)
            error = "Duplicate entry: This username already exists"
            return render(request, "registration.html", {'error': error})
    else:
        return render(request, "registration.html")


@login_required()
def pending_ticket(request):
    try:
        priority = ['low', 'medium', 'high']
        user_list = User.objects.all()
        engineer_list = User.objects.filter(groups__name='engineer')
        status_list = TicketStatus.objects.all()
        status_required = TicketStatus.objects.get(name="unassigned").id
        inprogress_status = TicketStatus.objects.get(name="inprocess").id
        ticket_list = ""
        if request.user.has_perm('ticket_tracker.can_assign_ticket'):
            ticket_list = TicketRegister.objects.all().order_by('-created_on')

        elif request.user.has_perm('ticket_tracker.self_assign_ticket'):
            ticket_list = TicketRegister.objects.filter(
                Q(status_id=status_required) | Q(status_id=inprogress_status) | Q(
                    assigned_to_id=int(request.user.id))).order_by('-created_on')
        elif request.user.has_perm('ticket_tracker.view_ticket_tracker'):
            ticket_list = TicketRegister.objects.filter(created_by=request.user).order_by(
                '-created_on')
        return render(request, 'dashboard.html', {
            'priority': priority,
            'user_list': user_list,
            'engineer_list': engineer_list,
            'ticket_list': ticket_list,
            'status_list': status_list,
        })
    except Exception, e:
        return render(request, '404.html', {'error': e})


@login_required()
def resolved_ticket(request):
    try:
        # priority = ['low', 'medium', 'high']
        # user_list = User.objects.all()
        # engineer_list = User.objects.filter(groups__name='engineer')
        # status_list = TicketStatus.objects.all()
        status_required = TicketStatus.objects.get(name="resolved").id
        ticket_list = ""

        if request.user.has_perm('ticket_tracker.can_assign_ticket'):
            ticket_list = TicketRegister.objects.filter(status_id=status_required).order_by(
                '-created_on')
        elif request.user.has_perm('ticket_tracker.self_assign_ticket'):
            # ticket_list = TicketRegister.objects.filter(Q(status_id=status_required), (
            # Q(assigned_to_id=int(request.user.id)) | Q(resolved_by_id=int(request.user.id)) | Q(
            # created_by=request.user))).order_by('-created_on')
            ticket_list = TicketRegister.objects.filter(status_id=status_required).order_by('-created_on')
        elif request.user.has_perm('ticket_tracker.view_ticket_tracker'):
            ticket_list = TicketRegister.objects.filter(Q(created_by=request.user),
                                                        Q(status_id=status_required)).order_by('-created_on')

        # ###--->>ajax filters
        if request.method == "POST":
            try:
                # assigned_to_me = request.POST.get('assigned_to_me', '')
                # select_engineer = request.POST.get('select_an_engineer', '')
                # select_user = request.POST.get('select_a_user', '')
                start_date = request.POST.get('start_date', '')
                end_date = request.POST.get('end_date', '')
                download_csv = request.POST.get('download', '')
                # if assigned_to_me != '':
                # ticket_list = TicketRegister.objects.filter(Q(assigned_to_id=int(request.user.id)),
                # Q(status_id=status_required)).order_by(
                # '-created_on')
                # if select_engineer != '':
                # ticket_list = TicketRegister.objects.filter(Q(assigned_to_id=int(select_engineer)),
                # Q(status_id=status_required)).order_by(
                # '-created_on')
                # if select_user != '':
                # if request.user.has_perm('ticket_tracker.can_assign_ticket'):
                # ticket_list = TicketRegister.objects.filter(Q(created_by=select_user),
                # Q(status_id=status_required)).order_by(
                # '-created_on')
                # elif request.user.has_perm('ticket_tracker.self_assign_ticket'):
                # ticket_list = TicketRegister.objects.filter(Q(created_by=select_user),
                # Q(status_id=status_required),
                # Q(assigned_to_id=int(request.user.id))).order_by(
                # '-created_on')
                if start_date != '' and end_date != '':
                    if request.user.has_perm('ticket_tracker.can_assign_ticket'):
                        ticket_list = TicketRegister.objects.filter(status_id=status_required, created_on__range=(
                            start_date, end_date)).order_by('-created_on')
                    elif request.user.has_perm('ticket_tracker.self_assign_ticket'):
                        ticket_list = TicketRegister.objects.filter(Q(created_on__range=(start_date, end_date)),
                                                                    Q(status_id=status_required),
                                                                    Q(assigned_to_id=int(request.user.id))).order_by(
                            '-created_on')
                    elif request.user.has_perm('ticket_tracker.view_ticket_tracker'):
                        ticket_list = TicketRegister.objects.filter(Q(created_on__range=(start_date, end_date)),
                                                                    Q(status_id=status_required),
                                                                    Q(created_by=request.user)).order_by(
                            '-created_on')
                if download_csv != '':
                    print 'in'
                    ticket_list = TicketRegister.objects.filter(status_id=status_required)
                    response = generate_csv(ticket_list)
                    return response
            except Exception, e:
                print 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)
                print e.args
        # ###--->>
        # paginator = Paginator(ticket_list, 10)
        # page_no = request.GET.get('page')
        # try:
        # resolved_issues = paginator.page(page_no)
        # except PageNotAnInteger:
        # resolved_issues = paginator.page(1)
        # except EmptyPage:
        # resolved_issues = paginator.page(paginator.num_pages)
        # ticket_list = resolved_issues
        return render(request, 'resolved_dashboard.html', {
            # 'priority': priority,
            # 'user_list': user_list,
            # 'engineer_list': engineer_list,
            'ticket_list': ticket_list,
            # 'status_list': status_list,
        })
    except Exception, e:
        return render(request, '404.html', {'error': e})


# @login_required()
# def update_ticket(request):
# if request.is_ajax():
# try:
# data = json.loads(request.POST['data'])
# engineer_assigned = data.get('engineer_name', '')
# ticket = TicketRegister.objects.get(id=data['ticket_id'])
# # ticket_count_for_resolved_section = TicketRegister.objects.filter(
# # status_id=TicketStatus.objects.get(name='resolved').id).count
# mark_resolved = data.get('mark_resolved', '')
# status_id_for_resolved = TicketStatus.objects.get(name='resolved').id
# comments_received = data.get('comment', '')
# status_id_for_inprocess = TicketStatus.objects.get(name='inprocess').id
# priority = data.get('priority', '')
# # TicketStatus = data.get('TicketStatus', '')
# engineer_to_change = data.get('engineer', '')
# comment_popup = data.get('comment_popup', '')
# action = ""
# now = datetime.now()
# time_of_action = "%s%s" % (now.strftime('%b. %d, %Y, %I:%M'), now.strftime('%p.').lower())
# user_performing_the_act = request.user.username
# user_id = User.objects.get(username=user_performing_the_act).id
# if priority != '':
# ticket.priority = priority.lower()
# action = 'updated priority to %s' % priority
# # elif TicketStatus != '':
# # ticket.status_id = int(TicketStatus)
# # action = 'updated TicketStatus to %s' % data['status_text']
# # if data['status_text'].lower() == 'resolved':
# # ticket.save()
# # # send_resolved_mail(ticket)
# # elif data['status_text'].lower() == 'inprocess':
# # ticket.save()
#             # # send_re_assigned_mail(ticket)
#             elif engineer_to_change != '':
#                 if ticket.status.name == 'unassigned':
#                     ticket.status_id = status_id_for_inprocess
#                     ticket.assigned_to_id = engineer_to_change
#                     ticket.save()
#                     # send_assigned_mail(ticket)
#                 else:
#                     ticket.assigned_to_id = engineer_to_change
#                 if engineer_assigned == "Assign to me":
#                     engineer_assigned = user_performing_the_act
#                 action = 'updated engineer assigned to %s' % engineer_assigned
#             elif mark_resolved != '' and comments_received != '':
#                 ticket = TicketRegister.objects.get(id=data['ticket_id'])
#                 ticket.resolved_by = request.user
#                 ticket.status_id = status_id_for_resolved
#
#                 comment = TicketComment.objects.create(created_on=timezone.now(),
#                                                        comment=comments_received,
#                                                        complaints_id=data['ticket_id'], created_by_id=user_id,
#                                                        resolved_flag=True)
#                 comment.save()
#                 action = 'resolved by %s' % request.user
#                 # send_resolved_mail(ticket)
#             elif comment_popup != '' and data['ticket_id'] != '':
#                 comments = TicketComment.objects.filter(complaints_id=data['ticket_id'])
#                 comment = []
#                 for i in comments:
#                     action = i.comment
#                     now = i.created_on
#                     time_of_action = "%s%s" % (now.strftime('%b. %d, %Y, %I:%M'), now.strftime('%p.').lower())
#                     user_performing_the_act = i.created_by.username
#                     resolved = i.resolved_flag
#                     comment.append({'action': action, 'time_of_action': time_of_action,
#                                     'user_performing_the_act': user_performing_the_act, 'resolved': resolved})
#
#                 comment.append({'complaints': ticket.complaints})
#                 return HttpResponse(json.dumps(comment), content_type="application/json")
#
#             comments = TicketComment.objects.create(created_on=timezone.now(), comment=action,
#                                                     complaints_id=data['ticket_id'], created_by_id=user_id)
#             comments.save()
#             ticket.save()
#             # comment = [action, time_of_action, user_performing_the_act]
#             # print comment
#             return HttpResponse(json.dumps({'action': action, 'time_of_action': time_of_action,
#                                             'user_performing_the_act': user_performing_the_act}),
#                                 content_type="application/json")
#         except Exception, e:
#             print 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)
#             print e.args
#             return HttpResponseBadRequest(e)
#
#
# @login_required()
# def update_comment(request):
#     if request.is_ajax():
#         try:
#             data = json.loads(request.POST['data'])
#             ticket_id = data['ticket_id']
#             comments_received = data['comment']
#             print data
#             user_id = User.objects.get(username=request.user).id
#             now = datetime.now()
#             time_of_action = "%s%s" % (now.strftime('%b. %d, %Y, %I:%M'), now.strftime('%p.').lower())
#             comment = TicketComment.objects.create(created_on=timezone.now(), comment=comments_received,
#                                                    complaints_id=ticket_id, created_by_id=user_id)
#             comment.save()
#             return HttpResponse(json.dumps({'action': comments_received, 'time_of_action': time_of_action,
#                                             'user_performing_the_act': request.user.username}),
#                                 content_type="application/json")
#         except Exception, e:
#             print e.args
#             return HttpResponseBadRequest(e)
