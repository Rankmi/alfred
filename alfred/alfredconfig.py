class AlfredConfig:
    def __init__(self,
                 user=None,
                 password=None,
                 bucket=None,
                 youtrack_token=None,
                 youtrack_username=None,
                 github_username=None,
                 github_password=None):
        self.user = user
        self.password = password
        self.bucket = bucket
        self.youtrack_token = youtrack_token
        self.youtrack_username = youtrack_username
        self.github_username = github_username
        self.github_password = github_password
