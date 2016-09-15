import os
from PyQt5.QtWidgets import QMessageBox #type: ignore
from kryptal.gui.controller.CreateDirectoryYesNoController import CreateDirectoryYesNoController
from kryptal.gui.view.dialogs.CreateFilesystemDialog import CreateFilesystemDialog
from kryptal.pluginmanager.IFilesystem import FilesystemCreateException
from kryptal.services.FilesystemCreatorService import FilesystemCreatorService


class CreateFilesystemController(object):
    def __init__(self, filesystemCreatorService: FilesystemCreatorService) -> None:
        self._filesystemCreatorService = filesystemCreatorService
        self._dlg = CreateFilesystemDialog()
        self._dlg.setAcceptHandler(self._acceptHandler)

    def create(self) -> None:
        self._dlg.exec_()

    def _acceptHandler(self, name: str, ciphertextDir: str, plaintextDir: str, password1: str, password2: str) -> bool:
        if not self._validatePasswords(password1, password2):
            return False

        if not self._validateDirExists('ciphertext directory', ciphertextDir):
            return False

        if not self._validateDirExists('plaintext directory', plaintextDir):
            return False

        return self._createFilesystem(name=name, fstype="CryFS", ciphertextDir=ciphertextDir, plaintextDir=plaintextDir, password=password1)

    def _validatePasswords(self, password1: str, password2: str) -> bool:
        if password1 == password2:
            return True
        QMessageBox.warning(self._dlg, "Passwords don't match",
                            "Passwords don't match. Please enter the same password in both fields.")
        self._dlg.clearPasswordFields()
        return False

    def _validateDirExists(self, name: str, path: str) -> bool:
        if os.path.isdir(path):
            return True
        return CreateDirectoryYesNoController(self._dlg).askYesNoAndCreateDir(name, path)

    def _createFilesystem(self, name: str, fstype: str, ciphertextDir: str, plaintextDir: str, password: str) -> bool:
        try:
            self._filesystemCreatorService.create(name=name, fstype=fstype, ciphertextDirectory=ciphertextDir, plaintextDirectory=plaintextDir, password=password.encode(encoding='UTF-8'))
            return True
        except FilesystemCreateException as e:
            QMessageBox.critical(self._dlg, "Error creating file system", e.message())
