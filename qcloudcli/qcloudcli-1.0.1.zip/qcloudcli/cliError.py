import json
import result
class error:
    def printInFormat(self, errorCode, errorMsg):
        content = {'Code':errorCode, 'Message':errorMsg}
        result.display_result("error", content, "json")
        pass

