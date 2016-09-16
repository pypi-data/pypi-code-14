from nodeconductor.core import tasks, executors


class ProjectCreateExecutor(executors.CreateExecutor):

    @classmethod
    def get_task_signature(cls, project, serialized_project, **kwargs):
        return tasks.BackendMethodTask().si(
            serialized_project, 'create_project', state_transition='begin_creating')


class ProjectUpdateExecutor(executors.UpdateExecutor):

    @classmethod
    def get_task_signature(cls, project, serialized_project, **kwargs):
        return tasks.BackendMethodTask().si(
            serialized_project, 'update_project', state_transition='begin_updating')


class ProjectImportExecutor(executors.UpdateExecutor):

    @classmethod
    def get_task_signature(cls, project, serialized_project, **kwargs):
        return tasks.BackendMethodTask().si(
            serialized_project, 'import_project_issues', state_transition='begin_updating')


class ProjectDeleteExecutor(executors.DeleteExecutor):

    @classmethod
    def get_task_signature(cls, project, serialized_project, **kwargs):
        if project.backend_id:
            return tasks.BackendMethodTask().si(
                serialized_project, 'delete_project', state_transition='begin_deleting')
        else:
            return tasks.StateTransitionTask().si(serialized_project, state_transition='begin_deleting')


class IssueCreateExecutor(executors.CreateExecutor):

    @classmethod
    def get_task_signature(cls, issue, serialized_issue, **kwargs):
        return tasks.BackendMethodTask().si(
            serialized_issue, 'create_issue', state_transition='begin_creating')


class IssueUpdateExecutor(executors.UpdateExecutor):

    @classmethod
    def get_task_signature(cls, issue, serialized_issue, **kwargs):
        return tasks.BackendMethodTask().si(
            serialized_issue, 'update_issue', state_transition='begin_updating')


class IssueDeleteExecutor(executors.DeleteExecutor):

    @classmethod
    def get_task_signature(cls, issue, serialized_issue, **kwargs):
        if issue.backend_id:
            return tasks.BackendMethodTask().si(
                serialized_issue, 'delete_issue', state_transition='begin_deleting')
        else:
            return tasks.StateTransitionTask().si(serialized_issue, state_transition='begin_deleting')


class CommentCreateExecutor(executors.CreateExecutor):

    @classmethod
    def get_task_signature(cls, comment, serialized_comment, **kwargs):
        return tasks.BackendMethodTask().si(
            serialized_comment, 'create_comment', state_transition='begin_creating')


class CommentUpdateExecutor(executors.UpdateExecutor):

    @classmethod
    def get_task_signature(cls, comment, serialized_comment, **kwargs):
        return tasks.BackendMethodTask().si(
            serialized_comment, 'update_comment', state_transition='begin_updating')


class CommentDeleteExecutor(executors.DeleteExecutor):

    @classmethod
    def get_task_signature(cls, comment, serialized_comment, **kwargs):
        if comment.backend_id:
            return tasks.BackendMethodTask().si(
                serialized_comment, 'delete_comment', state_transition='begin_deleting')
        else:
            return tasks.StateTransitionTask().si(serialized_comment, state_transition='begin_deleting')


class AttachmentCreateExecutor(executors.CreateExecutor):

    @classmethod
    def get_task_signature(cls, attachment, serialized_attachment, **kwargs):
        return tasks.BackendMethodTask().si(
            serialized_attachment, 'add_attachment', state_transition='begin_creating')


class AttachmentDeleteExecutor(executors.DeleteExecutor):

    @classmethod
    def get_task_signature(cls, attachment, serialized_attachment, **kwargs):
        if attachment.backend_id:
            return tasks.BackendMethodTask().si(
                serialized_attachment, 'remove_attachment', state_transition='begin_deleting')
        else:
            return tasks.StateTransitionTask().si(serialized_attachment, state_transition='begin_deleting')
