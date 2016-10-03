__author__ = 'marcoantonioalberoalbero'

import logging
import uuid
import os


class Log:

    config = None
    consolidate_only = None

    def __init__(self):
        self.default_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    def setup(self, config, task_id, build_id=None, log_dir=None, log_file=None, with_console=True):
        """
        Setup the default logger for the task_id in question
        :param config: config environment
        :param task_id: id of the task whose logger is going to be configured
        :param log_dir: the dir where the files are kept (None is config default)
        :param log_file: the log file (None is config default)
        :return:
        """
        Log.config = config
        Log.consolidate_only = True if config.get('global', 'log_consolidate_only') == "True" else False
        level = (logging.DEBUG if 'debug' in config.get('global', 'log_level') else logging.INFO)
        log_format = (config.get('global', 'log_format')
                      if config.get('global', 'log_format')
                      else self.default_format)
        logger = logging.getLogger(config.get('global', 'program') + '.' + task_id)
        logger.setLevel(level)
        ld = (log_dir if log_dir else config.get('global', 'log_dir'))
        lf = (log_file if log_file else config.get('global', 'log_file'))
        if build_id:
            if not os.path.exists(ld+'/'+build_id):
                os.makedirs(ld+'/'+build_id)
            fh = logging.FileHandler(ld+'/'+build_id+'/'+lf)
        else:
            fh = logging.FileHandler(ld+'/'+lf)
        formatter = logging.Formatter(log_format)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        if with_console:
            ch = logging.StreamHandler()
            ch.setFormatter(formatter)
            logger.addHandler(ch)
        return logger

    @staticmethod
    def id_log(logger=None, msg=None, level=logging.INFO):
        """
        Log with a uuid for track the log of the task/command
        :param logger: logger who's going to log
        :param msg: message to log
        :param level: level to log
        :return:
        """
        if logger and msg and level == logging.INFO:
            logger.info(str(uuid.uuid1()) + " - " + msg)
        if logger and msg and level == logging.DEBUG:
            logger.debug(str(uuid.uuid1()) + " - " + msg)

    @staticmethod
    def set_log(task, l_dir=None, l_file=None, consolidate_only=True, with_console=True):
        """
        Adds the logger with logger_id new loggers to log with
        :param task: the task to configure the log for
        :param l_dir: log directory
        :param l_file: log file
        :param consolidate_only: if only consolidate the log or not
        :return:
        """
        if consolidate_only:
            # log to the consolidated file (here it breaks with its own logger, it's not part of the logger hierarchy)
            # so it only logs in this l_file.
            tid = 'consolidated.' + task.id
        else:
            # add a new child logger (because it's part of the logger hierarchy)
            tid = task.id
        task.log = Log().setup(config=Log.config,
                               task_id=tid,
                               build_id=task.build_id,
                               log_dir=l_dir,
                               log_file=l_file,
                               with_console=with_console)

    @staticmethod
    def consolidate_log(task, hierarchy_node=None):
        """
        Consolidate the log of the task to every task ancestor
        :param task: task whose log is going to be consolidated
        :param hierarchy_node: ancestor
        :return:
        """
        if not Log.consolidate_only:
            if hierarchy_node:
                Log.set_log(task, consolidate_only=False, l_file=hierarchy_node.log_file, with_console=False)
                if hierarchy_node.parent:
                    Log.consolidate_log(task, hierarchy_node=hierarchy_node.parent)
