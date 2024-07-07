class BaseException(Exception):
    pass


class ProblemsException(BaseException):
    pass


class ProblemsNotFoundException(ProblemsException):
    pass


class SubmissionException(BaseException):
    pass


class SubmissionNotFoundException(SubmissionException):
    pass