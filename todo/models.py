from django.db import models
from django.contrib.auth.models import User

PRIORITY = (
	('1','Low'),
    ('2','Medium'),
    ('3','Normal'),
    ('4','Severe'),
    ('5','High'),
)

STATE = (
	('Done','Done'),
    ('Doing','Doing'),
    ('Todo','Todo'),
)


class Todo(models.Model):
	user = models.ForeignKey(User)
	name = models.CharField(max_length = 25, unique = True)
	description = models.TextField(null = True, blank= True)
	priority = models.CharField(max_length=50, choices = PRIORITY)
	state = models.CharField(max_length=50, default='Todo', choices=STATE)
	task_date = models.DateTimeField()
	created_date = models.DateTimeField(auto_now_add = True)

	def __unicode__(self):
		return self.name
	


	


