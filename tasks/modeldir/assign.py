from tasks.modeldir.base import Task, Submission


class AssignTask(Task):
    class Meta:
        app_label = 'tasks'

class AssignSubmission(Submission):
    class Meta:
        app_label = 'tasks'

    def on_submit(self, bonus):
        return 'Submitted'
