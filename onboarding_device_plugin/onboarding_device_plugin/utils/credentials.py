
"""User credentials helper module for device onboarding."""

class Credentials:
    """Class used to hide user's credentials in RQ worker and Django."""

    def __init__(self, username=None, password=None, secret=None):
        """Create a Credentials instance."""
        self.username = username
        self.password = password
        self.secret = secret

    def __repr__(self):
        """Return string representation of a Credentials object."""
        return "*Credentials argument hidden*"
