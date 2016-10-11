#!/usr/local/bin/python
# encoding: utf-8
"""
*send PDF and web-articles to your kindle and/or kindle apps*

:Author:
    David Young

:Date Created:
    September 30, 2016
"""
################# GLOBAL IMPORTS ####################
import sys
import os
os.environ['TERM'] = 'vt100'
from fundamentals import tools

import shutil
import getpass
import optparse
import os
import smtplib
import sys
import traceback
from StringIO import StringIO
from email import encoders
from email.MIMEBase import MIMEBase
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.generator import Generator
from fundamentals.mysql import readquery, writequery
from fundamentals.files import recursive_directory_listing
from subprocess import Popen, PIPE, STDOUT
from polyglot import htmlCleaner
import codecs


class sendToKindle():
    """
    The worker class for the sendToKindle module

    **Key Arguments:**
        - ``dbConn`` -- mysql database connection
        - ``log`` -- logger
        - ``settings`` -- the settings dictionary

    **Usage:**
        ..todo::

            add usage info
            create a sublime snippet for usage

        .. code-block:: python

            usage code

    """
    # Initialisation

    def __init__(
            self,
            log,
            dbConn=False,
            settings=False,

    ):
        self.log = log
        log.debug("instansiating a new 'sendToKindle' object")
        self.dbConn = dbConn
        self.settings = settings
        self.pdfs = []
        # xt-self-arg-tmpx

        # Initial Actions

        return None

    def send(self):
        """send the sendToKindle object

        **Return:**
            - ``sendToKindle``

        ..todo::

            - @review: when complete, clean send method
            - @review: when complete add logging
        """
        self.log.info('starting the ``send`` method')

        # self.send_pdfs()
        self.send_webarticles()

        self.log.info('completed the ``send`` method')
        return None

    def _get_data_to_send(
            self,
            docType):
        """*Select the rows from the reading-list table in the database containing webarticles or PDFs that need sent to kindle device and/or apps*

        **Key Arguments:**
            - ``docType`` -- either PDFs of webpages. [pdf|web]

        **Return:**
            - ``data`` -- a list of dictionaries giving details of the data to send to kindle
        """
        self.log.info('starting the ``_get_data_to_send`` method')

        if docType == "pdf":
            sqlQuery = u"""
                select * from `reading-list` where  kind = "imported-pdf" and sentToKindle =0 and workflowStage = "reading"  order by dateCreated limit 5 
            """ % locals()
        elif docType == "web":
            sqlQuery = u"""
                select * from `reading-list` where  kind = "webpage" and sentToKindle =0 and workflowStage = "reading" order by dateCreated limit 5 
            """ % locals()

        data = readquery(
            log=self.log,
            sqlQuery=sqlQuery,
            dbConn=self.dbConn,
            quiet=False
        )

        self.log.info('completed the ``_get_data_to_send`` method')
        return data

    def update_database_for_sent_item(
            self,
            primaryId):
        """*update the database to indicate that the PDFs have been sent to kindle(s)*

        **Key Arguments:**
            - ``primaryId`` -- unique ID of database entry to update.

        **Return:**
            - None

        **Usage:**
            ..  todo::

                add usage info
                create a sublime snippet for usage

            .. code-block:: python

                usage code

        .. todo::

            - @review: when complete, clean methodName method
            - @review: when complete add logging
        """
        self.log.info('starting the ``update_database_for_sent_item`` method')

        sqlQuery = u"""
            update `reading-list` set sentToKindle = 1 where primaryId = %(primaryId)s
        """ % locals()
        writequery(
            log=self.log,
            sqlQuery=sqlQuery,
            dbConn=self.dbConn
        )

        self.log.info('completed the ``update_database_for_sent_item`` method')
        return None

    def get_pdf_paths(
            self):
        """*generate a dictionary of pdf-names and their paths*

        **Key Arguments:**
            # -

        **Return:**
            - ``pdfDict`` -- the dictionary of pdf paths (keys are pdf names)

        **Usage:**
            ..  todo::

                add usage info
                create a sublime snippet for usage

            .. code-block:: python

                usage code

        .. todo::

            - @review: when complete, clean methodName method
            - @review: when complete add logging
        """
        self.log.info('starting the ``get_pdf_paths`` method')

        fileList = recursive_directory_listing(
            log=self.log,
            baseFolderPath=self.settings["read"]["reading_list_root_path"],
            whatToList="files"  # all | files | dirs
        )
        pdfDict = {}
        for f in fileList:
            if f.split(".")[-1].lower() == "pdf":
                pdfDict[os.path.basename(f)] = f

        self.log.info('completed the ``get_pdf_paths`` method')
        return pdfDict

    def trigger_mobi_generation(
            self,
            pdfPath):
        """*Add a `.hj` file into the file system beside the PDF file to trigger mobi book creation*

        **Key Arguments:**
            - ``pdfPath`` -- path to the input PDF file

        **Return:**
            - None

        **Usage:**
            ..  todo::

                add usage info
                create a sublime snippet for usage

            .. code-block:: python

                usage code

        .. todo::

            - @review: when complete, clean methodName method
            - @review: when complete add logging
        """
        self.log.info('starting the ``trigger_mobi_generation`` method')

        basename = os.path.basename(pdfPath)

        hjPath = pdfPath.replace(".pdf", ".hj")

        # INITIAL EXISTENCE TEST
        try:
            with open(hjPath):
                pass
        except IOError:
            fileExists = False
            writeFile = codecs.open(hjPath, encoding='utf-8', mode='w')
            writeFile.close()

        try:
            with open(hjPath):
                pass
            fileExists = True
        except IOError:
            fileExists = False

        if fileExists:
            sqlQuery = """update `reading-list` set mobi = "waiting" where pdfName = "%(basename)s"  """ % locals(
            )
            writequery(
                log=self.log,
                sqlQuery=sqlQuery,
                dbConn=self.dbConn,
            )

        self.log.info('completed the ``trigger_mobi_generation`` method')
        return None

    def send_pdfs(
            self):
        """*send pdfs*

        **Key Arguments:**
            # -

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
        self.log.info('starting the ``send_pdfs`` method')

        pdfsToSend = self._get_data_to_send(docType="pdf")
        pdfDict = self.get_pdf_paths()

        for pdf in pdfsToSend:
            print self.settings["read"]
            if pdf["kind"] == "imported-pdf":
                # TEST IF REFLOW REQUIRED
                if pdf["pdfName"] in pdfDict and "mobiConvert" in self.settings["read"] and self.settings["read"]["mobiConvert"] == True and pdf["mobi"] == None:

                    self.trigger_mobi_generation(pdfDict[pdf["pdfName"]])
                elif pdf["mobi"] == "waiting":
                    continue
                elif pdf["pdfName"] in pdfDict:
                    if "mobiConvert" in self.settings["read"] and self.settings["read"]["mobiConvert"] == True and pdf["mobi"] == 1:
                        sendFile = pdfDict[pdf["pdfName"]].split("/")
                        sendFile = (
                            "/").join(sendFile[:-1]) + "/OCR_" + sendFile[-1]
                        fileSize = os.path.getsize(sendFile) / 1000000
                        if fileSize > 25:
                            print "Need to reduce the size of the file `%(sendFile)s` before sending it to Kindle" % locals()
                            continue
                        sendTmp = "/tmp/" + os.path.basename(sendFile)
                        sendTmp = sendTmp.replace("/OCR_", "/")
                        shutil.copyfile(
                            sendFile, sendTmp)
                        sent = self.send_mail(pdfPath=sendTmp)
                    if sent == True:
                        try:
                            self.log.debug("attempting to rename file %s to %s" %
                                           (sendFile, sendFile.replace(
                                               "OCR_", "SENT_")))
                            os.rename(sendFile, sendFile.replace(
                                "OCR_", "SENT_"))
                            os.remove(sendTmp)
                        except Exception, e:
                            self.log.error("could not rename file %s to %s - failed with this error: %s " % (
                                sendFile, sendFile.replace(
                                    "OCR_", "SENT_"), str(e),))
                            sys.exit(0)
                        self.update_database_for_sent_item(pdf["primaryId"])

        self.log.info('completed the ``send_pdfs`` method')
        return None

    def send_webarticles(
            self):
        """*send webarticles*

        **Key Arguments:**
            # -

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
        self.log.info('starting the ``send_webarticles`` method')

        articlesToSend = self._get_data_to_send(docType="web")

        for article in articlesToSend:

            articleId = article["primaryId"]
            original = article["url"]
            footer = """%(articleId)s""" % locals(
            )

            from polyglot import kindle
            sender = kindle(
                log=self.log,
                settings=self.settings,
                urlOrPath=article["url"],
                title=article["pdfName"].replace(".pdf", ""),
                header=footer,
                footer=footer
            )
            success = sender.send()

            if success == True:
                self.update_database_for_sent_item(article["primaryId"])

        self.log.info('completed the ``send_webarticles`` method')
        return None

    # use the tab-trigger below for new method
    def create_workflow_links_html(
            self,
            id,
            databaseTable):
        """*Create an HTML page of workflow links to be added to the end of the ebook*

        **Key Arguments:**
            - ``id`` -- the item database id
            - ``databaseTable`` -- the database table the item is hosted by

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
        self.log.info('starting the ``create_workflow_links_html`` method')

        url = "http://www.thespacedoctor.co.uk"

        content = """

<hr>
<div style="text-align: center">
<a href="%(url)s">ARCHIVE</a> | <a href="%(url)s">SEARCH FOR ORIGINAL</a> | <a href="%(url)s">DELETE</a>
</div>
<hr>

""" % locals()

        pathToWriteFile = "/tmp/%(id)s_%(databaseTable)s.html" % locals()
        try:
            self.log.debug("attempting to open the file %s" %
                           (pathToWriteFile,))
            writeFile = codecs.open(
                pathToWriteFile, encoding='utf-8', mode='w')
        except IOError, e:
            message = 'could not open the file %s' % (pathToWriteFile,)
            self.log.critical(message)
            raise IOError(message)
        writeFile.write(content)
        writeFile.close()

        self.log.info('completed the ``create_workflow_links_html`` method')
        return pathToWriteFile

    # use the tab-trigger below for new method
    # xt-class-method
