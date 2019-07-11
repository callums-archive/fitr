from flask import (
    request
)

class Base():
    def __init__(self):
        super(Base, self).__init__()
        self.request = request
