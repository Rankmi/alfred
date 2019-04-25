class AlfredConfig:
    def __init__(self,
                 user=None,
                 password=None,
                 bucket=None,
                 youtrack_token=None,
                 youtrack_username=None,
                 youtrack_url="https://youtrack.rankmi.com",
                 github_username=None,
                 github_password=None,
                 github_token=None):
        self.user = user
        self.password = password
        self.bucket = bucket
        self.youtrack_token = youtrack_token
        self.youtrack_username = youtrack_username
        self.youtrack_url = youtrack_url
        self.github_username = github_username
        self.github_password = github_password
        self.github_token = github_token
