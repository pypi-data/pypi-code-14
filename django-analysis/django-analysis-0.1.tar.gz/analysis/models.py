from django.db import models


class Request(models.Model):
    view_func_path = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    method = models.CharField(max_length=10)
    date = models.DateTimeField()
    sql_times = models.IntegerField()
    sql_used = models.DecimalField(max_digits=5, decimal_places=2)
    request_used = models.DecimalField(max_digits=5, decimal_places=2)


class SQLEntry(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    db = models.CharField(max_length=50)
    sql = models.TextField()
    time = models.DecimalField(max_digits=5, decimal_places=2)

    def as_json(self):
        return {
            'request_id': self.request_id,
            'db': self.db,
            'time': str(self.time),
            'sql': self.sql
        }
