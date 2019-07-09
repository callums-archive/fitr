class DBError(Exception):
    def __init__(self, message):

        # Call the base class constructor with the parameters it needs
        super(DBError, self).__init__(message)

        # save message
        self.message = message

    def __str__(self):
        return self.message