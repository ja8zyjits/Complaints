__author__ = 'jitesh.nair'
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import email.utils
from django.contrib.auth.models import User, Group
import sys

"""
MERGE ALL THE FUNCTION TO HAVE A SINGLE MAIL FUNCTION AND THE REST SHOULD BE TO CHANGE THE TEXT ONLY

PLEASE REDESIGN THIS CODE TO NOT REPEAT ANYTHING MORE THAN ONCE
"""


def send_mail_old(query_object):
    try:
        fromaddr = "jitesh.nair@gmail.com"
        to_list = User.objects.filter(groups__name='engineers')
        toaddr = [i.username + '@gmail.com' for i in to_list]
        toaddr.append(query_object.created_by + '@gmail.com')
        print toaddr
        msg = MIMEMultipart('alternative')
        myid = email.utils.make_msgid()
        msg['From'] = fromaddr
        msg['To'] = ', '.join(toaddr)
        msg['Subject'] = 'ticket Id: [%s]%s' % (query_object.id, query_object.created_by)
        text_body = "A new issue has been created with ticket number:%s\r\nComplaint: %s" % (
            query_object.id, query_object.complaints)
        msg.attach(MIMEText(text_body, 'plain'))
        html_body = """\
        <html>
            <head><title>New Ticket</title>
            </head>
            <body>
                 A new issue has arrived kindly look into the tickets dashboard for further details
                <br/>
                <br/>
                <br/>
                <table style="border-collapse:collapse; width:100%; text-align:left; border:2px solid black; word-wrap:break-word; padding:5px;">
                    <tr style="border:2px solid black; word-wrap:break-word; padding:5px;">
                        <th style="border:2px solid black; word-wrap:break-word; padding:5px;">Ticket No.</th>
                        <td style="border:2px solid black; word-wrap:break-word; padding:5px;">{id}</td>
                    </tr>
                    <tr style="border:2px solid black; word-wrap:break-word; padding:5px;">
                        <th style="border:2px solid black; word-wrap:break-word; padding:5px;">Issue Date</th>
                        <td style="border:2px solid black; word-wrap:break-word; padding:5px;">{created_on}</td>
                    </tr>
                    <tr style="border:2px solid black; word-wrap:break-word; padding:5px;">
                        <th style="border:2px solid black; word-wrap:break-word; padding:5px;">Issue By</th>
                        <td style="border:2px solid black; word-wrap:break-word; padding:5px;">{created_by}</td>
                    </tr>
                    <tr style="border:2px solid black; word-wrap:break-word; padding:5px;">
                        <th style="border:2px solid black; word-wrap:break-word; padding:5px;">System ID</th>
                        <td style="border:2px solid black; word-wrap:break-word; padding:5px;">{system_id}</td>
                    </tr>
                    <tr style="border:2px solid black; word-wrap:break-word; padding:5px;">
                        <th style="border:2px solid black; word-wrap:break-word; padding:5px;">Issue</th>
                        <td style="border:2px solid black; word-wrap:break-word; padding:5px;">{complaints}</td>
                    </tr>
                    <tr style="border:2px solid black; word-wrap:break-word; padding:5px;">
                        <th style="border:2px solid black; word-wrap:break-word; padding:5px;">System IP</th>
                        <td style="border:2px solid black; word-wrap:break-word; padding:5px;">{ipaddress}</td>
                    </tr>
                </table>
                <br/>
                <br/>Thank you
            </body>
        </html>
        """.format(
            id=query_object.id,
            created_on=query_object.created_on.strftime('%b %d, %Y %I:%M %p'),
            created_by=query_object.created_by,
            system_id=query_object.system_id,
            complaints=query_object.complaints,
            ipaddress=query_object.ipaddress
        )
        msg.attach(MIMEText(html_body, 'html'))
        msg.add_header("Message-ID", myid)
        server = smtplib.SMTP('10.17.0.10', 25)
        server.ehlo()
        server.starttls()
        server.ehlo()
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        return myid
    except Exception, e:
        print e.args


def send_assigned_mail(query_object):
    try:
        fromaddr = "jitesh.nair@gmail.com"
        to_list = User.objects.filter(groups__name='admin')
        toaddr = [i.username + '@gmail.com' for i in to_list]
        toaddr.append(query_object.created_by + '@gmail.com')
        toaddr.append(query_object.assigned_to.username + '@gmail.com')
        print toaddr
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = ', '.join(toaddr)
        msg['Subject'] = 'ticket Id: [%s]%s' % (query_object.id, query_object.created_by)
        body = "The ticket with ticket number:%s has been ASSIGNED to %s kindly check the dashboard for further " \
               "details" % (query_object.id, query_object.assigned_to.username)
        msg.add_header("Message-ID", query_object.email_msg_id)
        msg.add_header("In-Reply-To", query_object.email_msg_id)
        msg.add_header("References", query_object.email_msg_id)
        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP('10.17.0.10', 25)
        server.ehlo()
        server.starttls()
        server.ehlo()
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
    except Exception, e:
        print e.args


def send_resolved_mail(query_object):
    try:
        fromaddr = "jitesh.nair@gmail.com"
        to_list = User.objects.filter(groups__name='admin')
        toaddr = [i.username + '@gmail.com' for i in to_list]
        toaddr.append(query_object.created_by + '@gmail.com')
        toaddr.append(query_object.assigned_to.username + '@gmail.com')
        toaddr.append(query_object.resoved_by.username + '@gmail.com')
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = ', '.join(toaddr)
        msg['Subject'] = 'ticket Id: [%s]%s' % (query_object.id, query_object.created_by)
        body = "The ticket with ticket number:%s has been RESOLVED by %s kindly check the dashboard for further " \
               "details" % (query_object.id, query_object.resoved_by.username)
        msg.add_header("Message-ID", query_object.email_msg_id)
        msg.add_header("In-Reply-To", query_object.email_msg_id)
        msg.add_header("References", query_object.email_msg_id)
        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP('10.17.0.10', 25)
        server.ehlo()
        server.starttls()
        server.ehlo()
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
    except Exception, e:
        print e.args


def send_re_assigned_mail(query_object):
    try:
        fromaddr = "jitesh.nair@gmail.com"
        to_list = User.objects.filter(groups__name='admin')
        toaddr = [i.username + '@gmail.com' for i in to_list]
        toaddr.append(query_object.created_by + '@gmail.com')
        toaddr.append(query_object.assigned_to.username + '@gmail.com')
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = ', '.join(toaddr)
        msg['Subject'] = 'ticket Id: [%s]%s' % (query_object.id, query_object.created_by)
        body = "The ticket with ticket number:%s has been REOCCURED by %s kindly check the dashboard for further " \
               "details" % (query_object.id, query_object.assigned_to.username)
        msg.add_header("Message-ID", query_object.email_msg_id)
        msg.add_header("In-Reply-To", query_object.email_msg_id)
        msg.add_header("References", query_object.email_msg_id)
        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP('10.17.0.10', 25)
        server.ehlo()
        server.starttls()
        server.ehlo()
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
    except Exception, e:
        print e.args


def send_mail1(query_object, action):
    pass


def send_mail(query_object, action):
    try:
        fromaddr = "jitesh.nair@gmail.com"
        to_list = User.objects.filter(groups__name='engineers')
        toaddr = [i.username + '@gmail.com' for i in to_list]
        toaddr.append(query_object.created_by + '@gmail.com')
        if action == 'new_issue':
            group_object = Group.objects.get_by_natural_key('engineers')
            user_list = User.objects.filter(groups=group_object)
            for i in user_list:
                toaddr.append(i.username + '@gmail.com')
        elif action == 'assigned':
            toaddr.append(query_object.assigned_to.username + '@gmail.com')
        elif action == 'resolved':
            toaddr.append(query_object.assigned_to.username + '@gmail.com')
            toaddr.append(query_object.resolved_by.username + '@gmail.com')
        print toaddr
        msg = MIMEMultipart('alternative')
        if query_object.email_msg_id == '':
            myid = email.utils.make_msgid()
        else:
            myid = query_object.email_msg_id
        msg['From'] = fromaddr
        msg['To'] = ', '.join(toaddr)
        msg['Subject'] = 'Ticket Id: [%s]%s' % (query_object.id, query_object.created_by)
        if action == 'new_issue':
            text_body = "A new issue has been created with ticket number:%s\r\nComplaint: %s" % (
                query_object.id, query_object.complaints)
            msg.attach(MIMEText(text_body, 'plain'))
            html_body = """\
                <html>
                    <head><title>New Ticket</title>
                    </head>
                    <body>
                         A new issue has arrived kindly look into the tickets dashboard for further details
                        <br/>
                        <br/>
                        <br/>
                        <table style="border-collapse:collapse; width:100%; text-align:left; border:2px solid black; word-wrap:break-word; padding:5px;">
                            <tr style="border:2px solid black; word-wrap:break-word; padding:5px;">
                                <th style="border:2px solid black; word-wrap:break-word; padding:5px;">Ticket No.</th>
                                <td style="border:2px solid black; word-wrap:break-word; padding:5px;">{id}</td>
                            </tr>
                            <tr style="border:2px solid black; word-wrap:break-word; padding:5px;">
                                <th style="border:2px solid black; word-wrap:break-word; padding:5px;">Issue Date</th>
                                <td style="border:2px solid black; word-wrap:break-word; padding:5px;">{created_on}</td>
                            </tr>
                            <tr style="border:2px solid black; word-wrap:break-word; padding:5px;">
                                <th style="border:2px solid black; word-wrap:break-word; padding:5px;">Issue By</th>
                                <td style="border:2px solid black; word-wrap:break-word; padding:5px;">{created_by}</td>
                            </tr>
                            <tr style="border:2px solid black; word-wrap:break-word; padding:5px;">
                                <th style="border:2px solid black; word-wrap:break-word; padding:5px;">System ID</th>
                                <td style="border:2px solid black; word-wrap:break-word; padding:5px;">{system_id}</td>
                            </tr>
                            <tr style="border:2px solid black; word-wrap:break-word; padding:5px;">
                                <th style="border:2px solid black; word-wrap:break-word; padding:5px;">Issue</th>
                                <td style="border:2px solid black; word-wrap:break-word; padding:5px;">{complaints}</td>
                            </tr>
                            <tr style="border:2px solid black; word-wrap:break-word; padding:5px;">
                                <th style="border:2px solid black; word-wrap:break-word; padding:5px;">System IP</th>
                                <td style="border:2px solid black; word-wrap:break-word; padding:5px;">{ipaddress}</td>
                            </tr>
                        </table>
                        <br/>
                        <br/>Thank you
                    </body>
                </html>
                """.format(
                id=query_object.id,
                created_on=query_object.created_on.strftime('%b %d, %Y %I:%M %p'),
                created_by=query_object.created_by,
                system_id=query_object.system_id,
                complaints=query_object.complaints,
                ipaddress=query_object.ipaddress
            )
            msg.attach(MIMEText(html_body, 'html'))
            msg.add_header("Message-ID", myid)
        elif action == 'assigned':
            body = "The ticket with ticket number:%s has been ASSIGNED to %s kindly check the dashboard for further " \
                   "details" % (query_object.id, query_object.assigned_to.username)
            msg.add_header("Message-ID", query_object.email_msg_id)
            msg.add_header("In-Reply-To", query_object.email_msg_id)
            msg.add_header("References", query_object.email_msg_id)
            msg.attach(MIMEText(body, 'plain'))
        elif action == 'resolved':
            body = "The ticket with ticket number:%s has been RESOLVED by %s kindly check the dashboard for further " \
                   "details" % (query_object.id, query_object.resolved_by.username)
            msg.add_header("Message-ID", query_object.email_msg_id)
            msg.add_header("In-Reply-To", query_object.email_msg_id)
            msg.add_header("References", query_object.email_msg_id)
            msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP('10.17.0.10', 25)
        server.ehlo()
        server.starttls()
        server.ehlo()
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        return myid

    except Exception, e:
        print 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)
        print e.args
