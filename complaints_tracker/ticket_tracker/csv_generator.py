__author__ = 'jitesh.nair'
import csv
from django.http import HttpResponse


def generate_csv(ticket_list):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ComplaintsRegister.csv"'

    writer = csv.writer(response)
    writer.writerow(
        ['Ticket No', 'Issued Date', 'Issued by', 'System id', 'Ip Address', 'Complaint', 'Priority', 'Assigned To',
         'Resolved By', 'Current Status'])
    for ticket in ticket_list:
        ticket_assigned_to = ticket.assigned_to.username if ticket.assigned_to_id else "User Resolved"
        ticket_resolved_by = ticket.resolved_by.username if ticket.resolved_by_id else ""  # not required

        # if ticket.engineers_id:
        # ticket_assigned_to = ticket.assigned_to.username
        # else:
        # ticket_assigned_to = ''
        #
        # if ticket.resolved_by_id:
        # ticket_resolved_by = ticket.resolved_by.username
        # else:
        #     ticket_resolved_by = ''

        writer.writerow(
            [ticket.id, ticket.created_on.strftime('%b. %d, %Y, %I:%M %p'), ticket.created_by.username,
             ticket.system_id, ticket.ipaddress, ticket.complaints.encode("utf-8").strip(), ticket.priority,
             ticket_assigned_to, ticket_resolved_by, ticket.status.name])

    return response