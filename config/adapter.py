from allauth.account.adapter import DefaultAccountAdapter
from environs import Env


class NoNewUsersAccountAdapter(DefaultAccountAdapter):
    """
    Adapter to disable allauth new signups
    Used at equilang/settings.py with key ACCOUNT_ADAPTER

    https://django-allauth.readthedocs.io/en/latest/advanced.html#custom-redirects"""

    def is_open_for_signup(self, request):
        env = Env()
        env.read_env()
        """
        Checks whether or not the site is open for signups.

        Next to simply returning True/False you can also intervene the
        regular flow by raising an ImmediateHttpResponse
        """
        return env.bool("DJANGO_SIGNUP_OPEN", True)
