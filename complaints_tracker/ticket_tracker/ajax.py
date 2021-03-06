import json
from datetime import datetime
import sys

from django.http.response import HttpResponseBadRequest
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core import serializers

from models import TicketRegister, TicketComment, TicketStatus
from ticket_tracker.send_mail import send_mail
from utils import broadcast


@login_required()
def update_ticket(request):
    if request.is_ajax():
        try:
            data = json.loads(request.POST['data'])
            engineer_assigned = data.get('engineer_name', '')
            ticket = TicketRegister.objects.get(id=data['ticket_id'])
            mark_resolved = data.get('mark_resolved', '')
            status_id_for_resolved = TicketStatus.objects.get(name='resolved').id
            comments_received = data.get('comment', '')
            status_id_for_inprocess = TicketStatus.objects.get(name='inprocess').id
            priority = data.get('priority', '')
            # TicketStatus = data.get('TicketStatus', '')
            engineer_to_change = data.get('engineer', '')
            comment_popup = data.get('comment_popup', '')
            action = ""
            now = datetime.now()
            time_of_action = "%s%s" % (now.strftime('%b. %d, %Y, %I:%M'), now.strftime('%p.').lower())
            user_performing_the_act = request.user
            user_id = User.objects.get(username=user_performing_the_act).id
            if priority != '':
                ticket.priority = priority.lower()
                action = 'updated priority to %s' % priority
            elif engineer_to_change != '':
                if ticket.status.name == 'unassigned':
                    ticket.status_id = status_id_for_inprocess
                    ticket.assigned_to_id = engineer_to_change
                    ticket.save()
                    send_mail(ticket, 'assigned')
                else:
                    ticket.assigned_to_id = engineer_to_change
                if engineer_assigned == "Assign to me":
                    engineer_assigned = user_performing_the_act
                action = 'updated engineer assigned to %s' % engineer_assigned
                broadcast(ticket_id=data['ticket_id'], engineer_id=engineer_to_change, engineer_name=engineer_assigned,
                          function='change_row', user=request.user.username)
            elif mark_resolved != '' and comments_received != '':
                ticket = TicketRegister.objects.get(id=data['ticket_id'])
                ticket.resolved_by = request.user
                ticket.status_id = status_id_for_resolved
                comment = TicketComment.objects.create(created_on=timezone.now(),
                                                       comment=comments_received,
                                                       complaints_id=data['ticket_id'], created_by_id=user_id,
                                                       resolved_flag=True)
                comment.save()
                action = 'resolved by %s' % request.user
                send_mail(ticket, 'resolved')
                ticket.save()
                ticket_object = TicketRegister.objects.filter(id=data['ticket_id'])
                data = serializers.serialize('json', ticket_object)
                ticket_object = json.loads(data)
                ticket_object = ticket_object[0]['fields']
                ticket_object['ticket_id'] = data['ticket_id']
                ticket_object['function'] = 'add_resolved_row'
                ticket_object['created_by_name'] = ticket_object[0].created_by.username
                ticket_object['function'] = 'add_resolved_row'
                ticket_object['function'] = 'add_resolved_row'
                broadcast(ticket_id=data['ticket_id'], function='delete_resolved_row', user=request.user.username)
            elif comment_popup != '' and data['ticket_id'] != '':
                comments = TicketComment.objects.filter(complaints_id=data['ticket_id'])
                comment = []
                for i in comments:
                    action = i.comment
                    now = i.created_on
                    time_of_action = "%s%s" % (now.strftime('%b. %d, %Y, %I:%M'), now.strftime('%p.').lower())
                    user_performing_the_act = i.created_by.username
                    resolved = i.resolved_flag
                    comment.append({'action': action, 'time_of_action': time_of_action,
                                    'user_performing_the_act': user_performing_the_act, 'resolved': resolved})

                comment.append({'complaints': ticket.complaints})
                return HttpResponse(json.dumps(comment), content_type="application/json")

            comments = TicketComment.objects.create(created_on=timezone.now(), comment=action,
                                                    complaints_id=data['ticket_id'], created_by_id=user_id)
            comments.save()
            ticket.save()
            return HttpResponse(json.dumps({'action': action, 'time_of_action': time_of_action,
                                            'user_performing_the_act': user_performing_the_act.username}),
                                content_type="application/json")
        except Exception, e:
            print 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)
            print e.args
            return HttpResponseBadRequest(e)


@login_required()
def update_comment(request):
    if request.is_ajax():
        try:
            data = json.loads(request.POST['data'])
            ticket_id = data['ticket_id']
            comments_received = data['comment']
            user_id = User.objects.get(username=request.user).id
            now = datetime.now()
            time_of_action = "%s%s" % (now.strftime('%b. %d, %Y, %I:%M'), now.strftime('%p.').lower())
            comment = TicketComment.objects.create(created_on=timezone.now(), comment=comments_received,
                                                   complaints_id=ticket_id, created_by_id=user_id)
            comment.save()
            return HttpResponse(json.dumps({'action': comments_received, 'time_of_action': time_of_action,
                                            'user_performing_the_act': request.user.username}),
                                content_type="application/json")
        except Exception, e:
            print 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)
            print e.args
            return HttpResponseBadRequest(e)
