# Emailer Docs
The email function is kept in the apogee1 folder under utils, this small function has a few key differences
between the default sendmail function. Primarily it allows for HTML rendered emails that are references in templates/emails/\*.html

## python implementation 
```python
from apogee1.utils.email import emailer
# email.email (Email_Subject,             From_Email,                Array or To_Emails,    email templates to render,   email data context for template to render)
emailer.email('Test Email - Apogee Dev', 'devteam@mail.granite.gg', ['rafael@granite.gg'], 'event_reminder_email.html', {"creator" : "rafael"})

```

## html implementation in templates/emails
All emails are draw from this folder, just reference the email you would like to render and pass it the proper context to render
```html
{% extends 'emails/base_email.html' %}

{% block title %}
    {{ block.super }} Email Html Title
{% endblock title %}

{% block content %}
	<h1>Welcome to Granite!</h1>
	<p>Thanks for signing up {{ username }}, if this email was sent to you by mistake or you did not sign up for Granite please disregard.</p>
{% endblock content %}

```

# Testing Emails
An endpoint exists here at /test_email/ to use locally or on your private heroku servers, by default it is disabled
but you can activate it via setting DISABLE_TEST_EMAILS=FALSE in your enviorment settings. It's important that you 
disable this setting after using it, as it allows people to send email as us.

http://localhost:8000/test_email/

application/json
```

{
        "email_to_send" : "creation_email.html",
        "to_address": "rafael@granite.gg",
        "email_data" : { "creator": "rafael" }

}

```

Above is a scaffold that will render and send data to the email of your choice
* email_to_send - a string that references the template you would like to render
* to_address - where email will be sent
* email_data - a json object containing the data needed for your email
