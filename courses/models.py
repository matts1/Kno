from auth.models import User
from common import models
from common.functions import genunique

YEARS = tuple(enumerate(
    ['K'] +
    list(range(1, 13))
#    ['1st Year University', '2nd Year University', '3rd Year University', '4th Year University']
))

SUBJECTS = tuple(enumerate(['Other'] + sorted((
    'Maths',
    'English',
    'Science',
    'Commerce',
    'Dance',
    'Design And Technology',
    'Food Tech',
    'Geography',
    'History',
    'Industrial Technology',
    'Information And Software Technology',
    'Languages',
    'Music',
    'PDHPE',
    'Textiles',
    'Art',
    'Metalwork',
    'Software Design And Development',
    'Multimedia',
    'Information And Processing Technology',
    'Engineering Studies',
))))

class Course(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    code = models.CharField(max_length=20, null=True, blank=True)

    teacher = models.ForeignKey(User, related_name='taught')
    students = models.ManyToManyField(User, related_name='courses')

    year = models.IntegerField(choices=YEARS)
    subject = models.IntegerField(choices = SUBJECTS, default=0)

    @classmethod
    def create(cls, teacher, name, private, subject, year):
        code = genunique(Course, 'code', 16) if private else None
        cls(teacher=teacher, name=name, code=code, year=year, subject=subject).save()
