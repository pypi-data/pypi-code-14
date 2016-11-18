from processors.postgres_processor import PostgresProcessor
from models import Model, Col
from main import Snek

db = Snek("postgres", host="mysql.ludd.ltu.se", database="swag", user="swag", password="swag123")

class User(Model):
    id = Col.Id(primary = True)
    username = Col.Text()
#User.register()

class Tag(Model):
    id = Col.Id(primary = True)
    name = Col.Text()
    user_key = Col.ForeignKey(User)

    def _read_swag(self):
        return "<%s> %s" % (self.id, self.name)
    swag = property(_read_swag)
#Tag.register()

tag = Tag.get(name="#swag")
print(tag)
tag.user.username = "yolo"
print(tag)
tag.save()

user = User.get(id=tag.user_key)
print(user)
