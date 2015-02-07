from django.db import models
from django.contrib.auth.models import User


class TicketStatus(models.Model):
    name = models.CharField(max_length=25, default='unassigned')


class TicketRegister(models.Model):
    created_on = models.DateTimeField()
    created_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='created_by')
    system_id = models.CharField(max_length=45)
    ipaddress = models.CharField(max_length=20, blank=True, null=True)
    complaints = models.TextField()
    priority = models.CharField(max_length=10, blank=True, null=True)
    email_msg_id = models.TextField(blank=True, null=True)
    status = models.ForeignKey(TicketStatus, blank=True, null=True, on_delete=models.SET_NULL)
    assigned_to = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='assigned_to')
    resolved_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='resolved_by')

    class Meta:
        default_permissions = []
        permissions = (
            ("can_assign_ticket", "Can Assign Ticket"),
            ("self_assign_ticket", "Self Assign Ticket"),
            ("view_ticket_tracker", "View Ticket Tracker"),
        )
        # permissions = (
        # ("can_assign_task", "Admin can assign new task to any engineer"),
        # ("can_self_assign_task", "Engineer can assign task to self only"),
        # ("can_only_view", "User can only view and change status of the issue"),
        # )
 

class TicketComment(models.Model):
    complaints = models.ForeignKey(TicketRegister, blank=True, null=True, on_delete=models.SET_NULL)
    created_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    created_on = models.DateTimeField()
    # should be comment not comments
    comment = models.TextField()
    resolved_flag = models.BooleanField(default=False)