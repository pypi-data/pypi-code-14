# -*- coding: utf-8 -*-


import models
import arch
import tasks
import git
import targets

ALL = [
    models.ui.view.ModelsView,
    arch.ui.view.FilesView,
    tasks.ui.view.TasksView,
    git.ui.view.GitView,
    targets.ui.view.TargetsView,
    ]

INDEX = dict([(x.name, x) for x in ALL])
