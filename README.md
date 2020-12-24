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

### 1. Injection

### 2. Broken authentication

By default Django starter app includes settings that prevent users from using passwords that are too weak. By removing password validators, we open the app to the risk of broken authentication where the passwords are too easy to guess.

To fix this issue, password validators need to be added in the settings.

### 3. Broken access control

The app allows users to upload files and download and remove them. However, access control has not been implemented for the files. This means that any logged-in user can navigate to '/download/${filename}' and download the file that some other user uploaded. Even more, any logged-in user can remove other users' files.

To fix this issue, ownership checking needs to be added to the methods that deal with the files. If the owner of the file matches the logged-in user, the method are allowed, otherwise they redirect the user to the homepage.

### 4. XSS

The app allows users to send messages to each other called chirps. However, the message input field is prone to XSS attacks. One possible attack vector would be to include malicious code in the message with the use of \<script> tags, for example \<script>alert('I can do anything') \</scirpt>. When the user opens the message, an alert window will pop up with the text "I can do anything". Obviously, a more malicious attacker would be able to execute more harmful code.

To prevent this specific attack, the message input field needs to be sanitized properly. There is a number of libraries for input sanitization, so any of those can be used. One of the working principles of XSS prevention is to remove brackets from the input field for example, so that the script tag would be stripped of the opening and closing brackets and, as a result, never get executed.

### 5. CSRF
