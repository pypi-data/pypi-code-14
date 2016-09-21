import subprocess, atexit, time
from py4j.java_gateway import JavaGateway

class JavaClient(object):
  JAR_PATH = "./J4Py.jar"


  def __init__(self):
    self._gateway = None
    self._process = None
    cmd = ["java", "-jar", self.JAR_PATH]
    self._process = subprocess
    print("JVM started: " + str(self._process.pid))
    atexit.register(self.kill)
    time.sleep(1)
    self._gateway = JavaGateway()

  def kill(self):
    if self._gateway != None:
      self._gateway.shutdown()
      self._gateway = None
    if self._process != None:
      self._process.kill()
      print("JVM killed: " + str(self._process.pid))
      self._process = None

  def read_pdf(self, file, password=None):
    pdf_document = self._gateway.jvm.org.apache.pdfbox.pdmodel.PDDocument()
    doc = pdf_document.load(file)
    pdf_document.close()
    return doc

  def make_pages(self, pages):
    l = self._gateway.jvm.java.util.ArrayList()
    for page in pages:
      l.add(self._gateway.jvm.java.lang.Integer, page)

    return l

  def make_area(self, area=None, pages=None, page_size=None):
