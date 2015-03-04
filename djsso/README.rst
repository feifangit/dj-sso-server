SSO server side app.

SSO provider: apps with this application installed
SSO client: 3rd party apps with djssoclient installed

Installation
- Dependency: djapiauth



Recommended SSO client app
djssoclient


Sample applications:
2 heroku applications, one run as SSO provider, another as SSO client.
source code: ???




SSO login
login may detect existing login status, and provide option to login with another account.
SSO login requested from 3rd party app will not affect existing logged-in users on SSO provider app.


API key for SSO
Create an api key in admin console. All SSO related APIs will assigned to this API Key.
Of course, you can assign extra APIs for this API key if your SSO

Work flow
...


Customize SSO login page
by default, Django
create a `templates` folder, and add the folder in <settings.py>
create `djsso/ssologin.html` under the `templates` folder


Security
all underneath communications are protected by djapiauth module.
