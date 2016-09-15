# vim:fileencoding=utf-8:noet
import string
from subprocess import PIPE, Popen

from powerline.segments import Segment, with_docstring
from powerline.theme import requires_segment_info


@requires_segment_info
class TaskwarriorBaseSegment(Segment):
    def execute(self, pl, command):
        pl.debug('Executing command: %s' % ' '.join(command))

        proc = Popen(command, stdout=PIPE, stderr=PIPE)
        out, err = [item.decode('utf-8') for item in proc.communicate()]

        if out:
            pl.debug('Command output: %s' % out.strip(string.whitespace))
        if err:
            pl.debug('Command errors: %s' % err.strip(string.whitespace))

        return out.splitlines(), err.splitlines()

    def build_segments(self, pl, task_alias):
        pl.debug('Nothing to do')
        return []

    def __call__(self, pl, segment_info, task_alias='task'):
        pl.debug('Running Taskwarrior: ' + task_alias)

        if not task_alias:
            return

        return self.build_segments(pl, task_alias)


class ContextSegment(TaskwarriorBaseSegment):
    def build_segments(self, pl, task_alias):
        pl.debug('Build Context segment')

        context_name, err = self.execute(pl, [task_alias, '_get', 'rc.context'])

        if not err and context_name:
            context_name = context_name.pop(0)
            if context_name:
                return [{
                    'contents': context_name,
                    'highlight_groups': ['information:regular'],
                }]

        return []


class ActiveTaskSegment(TaskwarriorBaseSegment):
    description = None
    task_id = None

    def __call__(self, pl, segment_info, task_alias='task', description_length=40):
        pl.debug('Running Taskwarrior: ' + task_alias)

        if not task_alias:
            return

        return self.build_segments(pl, task_alias, description_length)

    def build_segments(self, pl, task_alias, description_length=0):
        pl.debug('Build ActiveTask segment')

        # Command below shows only ID and description sorted by urgency
        # task rc.verbose: rc.report.next.columns:id,description rc.report.next.labels:1,2 +ACTIVE
        command_parts = [
            task_alias,
            'rc.verbose:',
            'rc.report.next.columns:id,description',
            'rc.report.next.labels:1,2', '+ACTIVE'
        ]
        id_and_description, err = self.execute(pl, command_parts)

        if not err and id_and_description:
            self.task_id, self.description = id_and_description.pop(0).split(' ', 1)

            return [{
                'name': 'active_task_id',
                'contents': self.task_id,
                'highlight_groups': ['critical:failure'],
            }, {
                'name': 'active_task_description',
                'contents': self.cut_description(self.description, description_length),
                'highlight_groups': ['critical:success'],
            }]
        else:
            return []

    def truncate(self, pl, amount, segment, description_length=0, **kwargs):
        if segment['name'] == 'active_task_id':
            return segment['contents']

        length = segment['_len'] - amount
        if description_length and description_length < length:
            length = description_length
        return self.cut_description(self.description, length)

    @staticmethod
    def cut_description(description, length):
        if length and len(description) > length:
            parts = []
            for part in description.split():
                if len(' '.join(parts + [part])) < length - 1:
                    parts.append(part)
                else:
                    return ' '.join(parts) + '…'
        else:
            return description


class TaskwarriorSegment(TaskwarriorBaseSegment):
    def build_segments(self, pl, task_alias):
        pl.debug('Build ActiveTask + Context segment')
        return ActiveTaskSegment()(pl, task_alias) + ContextSegment()(pl, task_alias)


taskwarrior = with_docstring(
    TaskwarriorSegment(),
    '''Return information from Taskwarrior task manager.

    It will show current context and active task (first by urgency order).

    Highlight groups used: ``critical:failure``, ``critical:success``, ``information:regular``
    ''')

context = with_docstring(
    ContextSegment(),
    '''Return information from Taskwarrior task manager.

    It will show current context.

    Highlight groups used: ``information:regular``
    ''')

active_task = with_docstring(
    ActiveTaskSegment(),
    '''Return information from Taskwarrior task manager.

    It will show active task (first by urgency order).

    Highlight groups used: ``critical:failure``, ``critical:success``
    ''')
