class AlfredConfig:
    user: str
    password: str
    bucket: str

    def __init__(self, user, password, bucket):
        self.user = user
        self.password = password
        self.bucket = bucket

