def get_input():
    command = input(": ").split()
    verb_word = command[0]
    if verb_word in verb_dict:
        verb = verb_dict[verb_word]
    else:
        print("Palabra desconocida {}".format(verb_word))
        return

    if len(command) >= 2:
        noun_word = command[1]
        print(verb(noun_word))
    else:
        print(verb(" "))

def diga(noun):
    return "Usted dijo {}".format(noun)

verb_dict = {"diga":diga,}

class GameObject:
    class_name=""
    desc=""
    objects={}

    def __init__(self,name):
        self.name=name
        GameObject.objects[self.class_name] = self

    def get_desc(self):
        return self.class_name+"\n"+self.desc

class Goblin(GameObject):
    def __init__(self,name):
        self.class_name="duende"
        self.health=3
        self._desc="Una criatura sucia"
        super().__init__(name)

    @property
    def desc(self):
        if self.health >= 3:
            return self._desc
        elif self.health == 2:
            health_line = "Tiene una herida en su rodilla"
        elif self.health == 1:
            health_line = "Su brazo izquierdo ha sido cortado"
        elif self.health <= 0:
            health_line = "Está muerto"
        return self._desc+"\n"+health_line

    @desc.setter
    def desc(self,value):
        self._desc=value
    

duende = Goblin("Duende Verde")

def examinar(noun):
    if noun in GameObject.objects:
        return GameObject.objects[noun].get_desc()
    else:
        return "No existe {} aqui".format(noun)

def golpear(noun):
    if noun in GameObject.objects:
        thing = GameObject.objects[noun]
        if type(thing) == Goblin:
            thing.health = thing.health -1
            if thing.health <= 0:
                msg = "Mataste al duende"
            else:
                msg = "Golpeaste al {}".format(thing.class_name)
    else:
        msg = "No existe {} aquí".format(noun)
    return msg
verb_dict["examinar"]=examinar
verb_dict["golpear"]=golpear

for i in range(8):
    get_input()    
