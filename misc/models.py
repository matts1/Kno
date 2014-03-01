from auth.models import User
from common import models
from courses.models import Course
from tasks.modeldir.base import Task

tables = (User, Course, Task)


class Search(models.Model):
    word = models.CharField(max_length=200)
    table_id = models.IntegerField()
    table = models.IntegerField()
    weight = models.IntegerField()

    @classmethod
    def add_words(cls, line:str, key:int, table):
        for word in line.lower().split():
            # len(word) means common words like 'and' will have less weight because they're short
            weight = 1000 * len(word) / len(line)  # scale factor so I can use int instead of float
            cls(word=word, table_id=key, table=tables.index(table), weight=weight).save()

    @classmethod
    def search(cls, line:str, user:User) -> list:
        count = {}
        for word in line.lower().split():
            for result in cls.objects.filter(word=word):
                key = (result.table, result.table_id)
                count[key] = count.get(key, 0) + result.weight
        values = []
        for (table, key) in sorted(count, key=count.get, reverse=True):
            table = tables[table]
            row = table.objects.get(id=key)
            if user.can_see(row, table):
                values.append(row)
        return values

    @classmethod
    def rename_words(cls, line:str, key:int, table):
        # for each record, there's only going to be one 'line' indexed
        cls.delete_words(key, table)
        cls.add_words(line, key, table)

    @classmethod
    def delete_words(cls, key:int, table):
        cls.objects.filter(table_id=key, table=table).delete()
