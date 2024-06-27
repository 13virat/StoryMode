from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_comment_notification(comment):
    subject = f'New comment on your story "{comment.story.title}"'
    html_message = render_to_string('emails/new_comment.html', {'comment': comment})
    plain_message = strip_tags(html_message)
    from_email = settings.DEFAULT_FROM_EMAIL
    to = comment.story.author.email

    send_mail(subject, plain_message, from_email, [to], html_message=html_message)