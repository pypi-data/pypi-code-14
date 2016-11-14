# Copyright (c) 2016, Formation Data Systems, Inc. All Rights Reserved.
#
from enum import Enum, unique

@unique
class CompletionStatus(Enum):
    unknown   = 0
    initiated = 1
    running   = 2
    failed    = 3
    done      = 4

    def __str__(self):
        if self.value == CompletionStatus.running.value:
            return "in_progress"
        return self.name
