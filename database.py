from time import time
from peewee import *


db = SqliteDatabase('data/arithmetic_tester.db')


class BaseModel(Model):
    class Meta:
        database = db
        

class User(BaseModel):
    chat_id = IntegerField(primary_key=True)
    name = CharField()
    
    @property
    def last_command(self):
        return self.last_command_q.get()
        
    @property
    def last_test(self):
        return self.last_test_q.get()
    
        
class Test(BaseModel):
    n_samples = IntegerField()
    name = CharField(unique=True)
        
    
class LastTestInfo(BaseModel):
    user = ForeignKeyField(User, backref='last_test_q', unique=True)
    test = ForeignKeyField(Test, null=True)
    questions = IntegerField(null=True)
    correct_answers = IntegerField(null=True)
    start_time = FloatField(null=True)
    last_answer = FloatField(null=True)
    
    def get_percentage(self):
        return self.correct_answers / self.questions
        
    def get_elapsed_time(self):
        return time() - self.start_time
        
        
class LastCommand(BaseModel):
    user = ForeignKeyField(User, backref='last_command_q', unique=True)
    command = CharField()
    edit_test_id = IntegerField(null=True)
    question_ids = CharField(null=True)
    test_name = CharField(null=True)
    
class Question(BaseModel):
    test = ForeignKeyField(Test, backref='questions')
    question_id = IntegerField()
        

class Achievement(BaseModel):
    user = ForeignKeyField(User, backref='achievments')
    test = ForeignKeyField(Test)
    correct_answers = IntegerField()
    elapsed_time = FloatField()

    
User.create_table()
Test.create_table()
LastTestInfo.create_table()
LastCommand.create_table()
Question.create_table()
Achievement.create_table()
print('Users:')
for user in User.select():
    print(user.chat_id, user.name, user.last_command.command)
print('Tests:')
for test in Test.select():
    questions = [question.question_id for question in test.questions]
    print(test.name, questions)
for achievement in Achievement.select():
    print(achievement.user.name, achievement.test.name, achievement.test.n_samples, achievement.correct_answers, achievement.elapsed_time)
