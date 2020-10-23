class ErrorMessage(Exception):
    def __init__(self, filed, msg):
        if msg == None:
            self.msg = 'Please prvoide a valid {}'.format(filed)
        else:
            self.msg = msg
        self.filed = filed