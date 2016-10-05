import os
import shutil


class BuildResult(object):
  def __init__(self, artifacts):
    self.artifacts = artifacts

  def copy_to(self, destDir):
    os.makedirs(destDir, exist_ok=True)
    for artifact in self.artifacts:
      artifact.copy_to(destDir)


class StepResult(object):
  def __init__(self, artifacts):
    self.artifacts = artifacts

  def copy_to(self, destDir):
    os.makedirs(destDir, exist_ok=True)
    for artifact in self.artifacts:
      artifact.copy_to(destDir)


class Artifact(object):
  def __init__(self, name):
    self.name = name


class FileArtifact(Artifact):
  def __init__(self, name, srcFile, dstFile=None):
    super().__init__(name)
    self.srcFile = srcFile
    self.dstFile = dstFile

  def __str__(self):
    return '"{}" at {}'.format(self.name, self.srcFile)

  def copy_to(self, destDir):
    if not self.dstFile:
      return
    copyLocation = os.path.join(destDir, self.dstFile)
    copyDir = os.path.dirname(copyLocation)
    os.makedirs(copyDir, exist_ok=True)
    print('Copying file artifact {} to {}'.format(self, copyLocation))
    return shutil.copyfile(self.srcFile, copyLocation)


class DirArtifact(Artifact):
  def __init__(self, name, srcDir, dstDir=None):
    super().__init__(name)
    self.srcDir = srcDir
    self.dstDir = dstDir

  def __str__(self):
    return '"{}" at {}'.format(self.name, self.srcDir)

  def copy_to(self, destDir):
    if not self.dstDir:
      return
    copyDir = os.path.join(destDir, self.dstDir)
    print('Copying directory artifact {} to {}'.format(self, copyDir))
    return shutil.copytree(self.srcDir, copyDir)
