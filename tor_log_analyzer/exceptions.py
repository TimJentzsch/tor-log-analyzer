from praw.models import Submission
from praw.models import Comment
from tor_log_analyzer.data.done_data import DoneData


class SubmissionNotFoundException(RuntimeError):
    "The submission could not be found for the given 'done'."

    def __init__(self, done_data: DoneData):
        super().__init__()
        self.done_data = done_data


class TranscriptionNotFoundException(RuntimeError):
    "The transcription could not be found for the given submission."

    def __init__(self, submission: Submission):
        super().__init__()
        self.submission = submission


class TranscriptionFormatException(RuntimeError):
    "The transcription has broken formatting."

    def __init__(self, comment: Comment):
        super().__init__()
        self.comment = comment
