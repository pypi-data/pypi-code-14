#!/usr/local/bin/python
# encoding: utf-8
"""
*Add template files and folders into new Gollum wiki projects and directories*

:Author:
    David Young

:Date Created:
    June  3, 2016
"""
################# GLOBAL IMPORTS ####################
import sys
import os
import re
import shutil
os.environ['TERM'] = 'vt100'
from frankenstein import electric
from fundamentals import tools


class templates():
    """
    *Add template files and folders into new Gollum wiki projects and directories*

    **Key Arguments:**
        - ``log`` -- logger
        - ``settings`` -- the settings dictionary

    **Usage:**

        .. code-block:: python

            from bilbo import templates
            templates(
                log=log,
                settings=settings
            ).get()

    """
    # Initialisation

    def __init__(
            self,
            log,
            settings=False,

    ):
        self.log = log
        log.debug("instansiating a new 'templates' object")
        self.settings = settings
        # xt-self-arg-tmpx

        # Initial Actions

        return None

    def get(self):
        """
        *populate the wiki with template content*
        """
        self.log.info('starting the ``get`` method')

        pathToTemplateStandard = os.path.dirname(
            __file__) + "/resources/standard-template"
        pathToWorkflowTemplate = os.path.dirname(
            __file__) + "/resources/workflow-template"
        pathToProjectTemplate = os.path.dirname(
            __file__) + "/resources/project-template"

        # FOR EACH WIKI IN THE SETTINGS FILE ...
        for name, wiki in self.settings["wikis"].iteritems():
            projectDir = wiki["root"] + "/projects"
            self._add_project_template(
                directoryPath=wiki["root"],
                wikiRoot=wiki["root"],
                pathToTemplate=pathToTemplateStandard,
                foldersPathsToAvoid=["/workflows", "/projects"]
            )

            self._add_project_template(
                directoryPath=wiki["root"] + "/workflows",
                wikiRoot=wiki["root"],
                pathToTemplate=pathToWorkflowTemplate
            )

            self._add_project_template(
                directoryPath=wiki["root"] + "/projects",
                wikiRoot=wiki["root"],
                pathToTemplate=pathToProjectTemplate
            )

            self._add_workflow_listsings(
                pathToWorkflowRoot=wiki["root"] + "/workflows"
            )

            self.remove_non_wiki_templates(
                pathToWorkspaceRoot=wiki["root"]
            )

        self.log.info('completed the ``get`` method')
        return templates

    def _add_project_template(
            self,
            directoryPath,
            pathToTemplate,
            wikiRoot="",
            foldersPathsToAvoid=[]):
        """*Populate new projects in wiki with template files and folders*

        **Key Arguments:**
            - ``directoryPath`` -- path to the folder to populate with the tmeplate.
            - ``pathToTemplate`` -- path to the template to be used to populated the folder.
            - ``foldersPathsToAvoid`` -- extra paths to folders to avoid
            - ``wikiRoot`` -- path to the root of the wiki
        """
        self.log.info('starting the ``_add_project_template`` method')

        self.log.debug(
            'path to the destination folder to populate: %(directoryPath)s' % locals())

        # FOR EVERY DIRECTORY IN PROJECT ROOT
        exists = os.path.exists(directoryPath)
        if not exists:
            return
        for d in os.listdir(directoryPath):
            if os.path.isdir(os.path.join(directoryPath, d)):

                # FOLDERS TO AVOID
                matched = False
                for avoid in self.settings["template parameters"]["folder avoid regex"]:
                    matchObject = re.search(
                        r"%(avoid)s" % locals(), d, re.S)
                    if matchObject:
                        matched = True
                if matched or os.path.exists(os.path.join(directoryPath, d + "/.non-wiki")):
                    continue

                # AVOID THE EXTRA FOLDERS
                moveOn = False
                for fpath in foldersPathsToAvoid:
                    if os.path.join(directoryPath, d).lower().replace(wikiRoot.lower(), "") == fpath.lower():
                        moveOn = True
                if moveOn:
                    continue

                # REMOVE SPACES FROM PROJECT FOLDERS
                if " " in d:
                    newD = d.replace(" ", "-")
                    source = os.path.join(directoryPath, d)
                    destination = os.path.join(directoryPath, newD)
                    exists = os.path.exists(destination)
                    if not exists:
                        try:
                            self.log.debug("attempting to rename file %s to %s" %
                                           (source, destination))
                            shutil.move(source, destination)
                        except Exception, e:
                            self.log.error("could not rename file %s to %s - failed with this error: %s " %
                                           (source, destination, str(e),))
                            sys.exit(0)
                    d = newD

                pathToDestination = os.path.join(directoryPath, d)
                self.settings["template parameters"]["fixed placeholders"][
                    "project_name"] = d.replace(" ", "-")
                # DUPLICATE SETTINGS INTO FRANKENSTEIN KEY
                self.settings["frankenstein"] = self.settings[
                    "template parameters"]

                if "conflicted-copy" in pathToDestination:
                    try:
                        shutil.rmtree(pathToDestination)
                    except:
                        pass
                    continue

                # USE FRANKENSTEIN ELECTRIC TO POPULATE THE FOLDERS IN THE WIKI
                if "@" != d[0]:
                    electric(
                        log=self.log,
                        pathToTemplate=pathToTemplate,
                        pathToDestination=pathToDestination,
                        settings=self.settings,
                        ignoreExisting=True
                    ).get()

                # NOW WALK THROUGH SUB-FOLDERS
                self._add_project_template(
                    directoryPath=pathToDestination,
                    pathToTemplate=pathToTemplate,
                    wikiRoot=wikiRoot,
                    foldersPathsToAvoid=foldersPathsToAvoid
                )

        self.log.info('completed the ``_add_project_template`` method')
        return None

    def _add_workflow_listsings(
            self,
            pathToWorkflowRoot):
        """*add workflow listsings*

        **Key Arguments:**
            - ``pathToWorkflowRoot`` -- path to the root of the workflow directory.

        **Return:**
            - None
        """
        self.log.info('starting the ``_add_workflow_listsings`` method')

        # Recursively create missing directories
        if not os.path.exists(pathToWorkflowRoot):
            os.makedirs(pathToWorkflowRoot)

        # FOR EVERY DIRECTORY IN WORKFLOW ROOT
        thisDir = pathToWorkflowRoot.split("/")[-1]
        indexFile = pathToWorkflowRoot + "/%(thisDir)s.md" % locals()
        exists = os.path.exists(indexFile)

        if not exists:
            return

        if exists:
            import codecs
            pathToReadFile = indexFile
            try:
                self.log.debug("attempting to open the file %s" %
                               (pathToReadFile,))
                readFile = codecs.open(
                    pathToReadFile, encoding='utf-8', mode='r')
                thisData = readFile.read()
                oldData = thisData
                readFile.close()
            except IOError, e:
                message = 'could not open the file %s' % (pathToReadFile,)
                self.log.critical(message)
                raise IOError(message)

            skip = False
            if ":--" not in thisData:
                self.log.warning(
                    "No table found in workflow %(indexFile)s " % locals())
                skip = True
            else:
                matchObject = re.search(r"\|\s?\:-+.*", thisData)
                tableRow = matchObject.group().replace(":", " ").replace("-", " ")
                columnNumber = len(tableRow.split("|")) - 2
            readFile.close()

        for d in os.listdir(pathToWorkflowRoot):
            # FOLDERS TO AVOID
            matched = False
            for avoid in self.settings["template parameters"]["folder avoid regex"]:
                matchObject = re.search(
                    r"%(avoid)s" % locals(), d, re.S)
                if matchObject:
                    matched = True
            if matched:
                continue

            if os.path.isdir(os.path.join(pathToWorkflowRoot, d)) and not skip:
                link = '[%(d)s](./%(d)s/%(d)s.md)' % locals()

                if link not in thisData:
                    regex = re.compile(r"(\|\s?\:-+.*)")
                    row = "| " + link + " | " + \
                        ("|").join(tableRow.split("|")[2:])
                    thisData = regex.sub("\g<1>\n%(row)s" %
                                         locals(), thisData, count=1)
            if thisData != oldData:
                pathToWriteFile = indexFile
                try:
                    self.log.debug("attempting to open the file %s" %
                                   (pathToWriteFile,))
                    writeFile = codecs.open(
                        pathToWriteFile, encoding='utf-8', mode='w')
                except IOError, e:
                    message = 'could not open the file %s' % (pathToWriteFile,)
                    self.log.critical(message)
                    raise IOError(message)

                writeFile.write(thisData)
                writeFile.close()

            if os.path.isdir(os.path.join(pathToWorkflowRoot, d)):
                self._add_workflow_listsings(
                    pathToWorkflowRoot=os.path.join(pathToWorkflowRoot, d)
                )

        self.log.info('completed the ``_add_workflow_listsings`` method')
        return None

    def remove_non_wiki_templates(
            self,
            pathToWorkspaceRoot,
            parentTrigger=False):
        """*remove non wiki templates*

        **Key Arguments:**
            - ``pathToWorkspaceRoot`` -- path to the root of the workspace directory
            - ``parentTrigger`` -- removal triggered from a parent folder. Default *False*

        **Return:**
            - None

        **Usage:**
            ..  todo::

                - add usage info
                - create a sublime snippet for usage
                - update package tutorial if needed

            .. code-block:: python 

                usage code 
        """
        self.log.info('starting the ``remove_non_wiki_templates`` method')

        # FOR EVERY DIRECTORY IN PROJECT ROOT
        exists = os.path.exists(pathToWorkspaceRoot + "/.non-wiki")
        if exists or parentTrigger:
            filename = pathToWorkspaceRoot.split("/")[-1]
            try:
                os.remove(pathToWorkspaceRoot + "/" + filename + ".taskpaper")
            except:
                pass
        if exists:
            parentTrigger = True

        for d in os.listdir(pathToWorkspaceRoot):
            if os.path.isdir(os.path.join(pathToWorkspaceRoot, d)):
                self.remove_non_wiki_templates(
                    pathToWorkspaceRoot=os.path.join(pathToWorkspaceRoot, d),
                    parentTrigger=parentTrigger
                )

        self.log.info('completed the ``remove_non_wiki_templates`` method')
        return None

    # use the tab-trigger below for new method
    # xt-class-method
