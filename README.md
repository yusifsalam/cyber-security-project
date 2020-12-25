# Cyber security project

The aim of this project is to create a webapp that is unsecure by design. The app should contain at least five flaws from the OWASP top ten list.
The project is done as part of the course [Cyber Security Base 2020](https://cybersecuritybase.mooc.fi/).

## Installation

You need python 3 with pip installed. Clone the repository, cd to the cloned repository and create a new virtual environment `python3 -m venv venv`. Now activate the newly installed venv `source venv/bin/activate`. Note that the venv activation command will depend on your OS and shell. With the venv activated, run `pip install -r requirements.txt` to install the needed requirements.

The app can be started with `python manage.py runserver`.

## Vulnerabilities

These are the vulnerabilities present in the app:

1. Injection
1. Broken authentication
1. Broken access control
1. Cross-site scripting XSS
1. Cross-site request forgery CSRF (Security Misconfiguration)
1. Insufficient logging and monitoring

### FLAW 1: Injection

The injection flaw is present in the app, namely SQL injection.
The app allows users to change their usernames. To do that, users navigate to the change username page and input their desired new username. Unfortunately, the way it's implemented in the backend leaves the database exposed to SQL injection, since the user input isn't sanitized and is executed directly as SQL statements. This means that a malicious user could try to inject SQL to reveal sensitive information from the entire database. Luckily the username change input is the only place in the app where unsanitized SQL is used, and the user passwords are salted by default thanks to Django, so plain text passwords will not be revealed to the hackers.

To fix this issue, the developer needs to either sanitize the input or simply stop directly executing SQL statements and instead leave the job to Django.

### FLAW 2: Broken authentication

By default Django starter app includes settings that prevent users from using passwords that are too weak. By removing password validators, we open the app to the risk of broken authentication where the passwords are too easy to guess.

To fix this issue, password validators need to be added in the settings.

### FLAW 3: Broken access control

The app allows users to upload files and download and remove them. However, access control has not been implemented for the files. This means that any logged-in user can navigate to '/download/${filename}' and download the file that some other user uploaded. Even more, any logged-in user can remove other users' files.

To fix this issue, ownership checking needs to be added to the methods that deal with the files. If the owner of the file matches the logged-in user, the method are allowed, otherwise they redirect the user to the homepage.

### FLAW 4: XSS

The app allows users to send messages to each other called chirps. However, the message input field is prone to XSS attacks. One possible attack vector would be to include malicious code in the message with the use of \<script> tags, for example \<script>alert('I can do anything') \</scirpt>. When the user opens the message, an alert window will pop up with the text "I can do anything". Obviously, a more malicious attacker would be able to execute more harmful code.

To prevent this specific attack, the message input field needs to be sanitized properly. There is a number of libraries for input sanitization, so any of those can be used. One of the working principles of XSS prevention is to remove brackets from the input field for example, so that the script tag would be stripped of the opening and closing brackets and, as a result, never get executed.

### FLAW 5: CSRF

Cross-site request forgery or CSRF for short is also present in the app. The developers removed the CsrfViewMiddleware middleware from the app, which provides protection against CSRF. Unfortunately, the developers also forgot to put \{% csrf_token %\} in the registration form. This means that a possible attacker could hijack the registration form and thus direct all the input to a machine that they control, thus getting a hold of the unsuspecting user's username and password. The attacker could then register on the actual service, so the user would not suspect a thing, since everything would work normally, but in reality the hackers already know the username and password.

To prevent this kind of attack, the easiest solution is to enable the CsrfMiddleware that comes preinstalled in the Django starter app. Another option would be to manually add {% csrf_token %\} to every form.

### FLAW 6: Insufficient logging and monitoring

While the app is set to DEBUG mode, there is virtually no logging or monitoring. As a result, system maintainers will not be able to quickly react to possible attacks, since they will be completely oblivious of anything happening. This means that the app is free real estate for malicious attackers and the above five flaws can be abused freely without reprecussions.

To fix this issue, proper monitoring needs to be set up. This can be achieved through the use of middleware, for example logging middleware could be used. Another possibility is to enable and configure LogEntry via the Django admin file. Finally, there are paid solutions for this very problem: a quick search reveals Loggly as one of them.
