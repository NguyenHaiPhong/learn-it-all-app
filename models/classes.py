from mongoengine import *
from datetime import datetime

class User(Document):
    name = StringField()
    sign_in = StringField()
    password = StringField()
    email = StringField()
    profile_pic = StringField()
    phone_number = StringField()
    is_activating = BooleanField(default=False)
    is_admin = BooleanField(default=False)

class Category(Document):
    name = StringField()
    thumbnail = StringField()
    is_activating = BooleanField(default=True)

class Lesson(Document):
    name = StringField()
    link = StringField()
    is_activating = BooleanField(default=True)

class Course(Document):
    name = StringField(required=True)
    level = StringField()
    fee = IntField(required=True)
    thumbnail = StringField()
    description = StringField()
    duration = StringField()
    is_activating = BooleanField(default=True)
    category_id = ReferenceField(Category)
    lesson_id = ListField(ReferenceField(Lesson))

class Lecturer(Document):
    name = StringField()
    email = StringField()
    profile_pic = StringField()
    height = IntField()
    weight = IntField()
    body_fat = IntField()
    phone_number = StringField()
    description = ListField()
    is_activating = BooleanField(default=True)
    category_id = ReferenceField(Category)
    course_id = ListField(ReferenceField(Course))

class Order(Document):
    order_time = DateTimeField(default=datetime.now())
    is_purchased = BooleanField(default=False)
    customer_id = ReferenceField(User)
    course_id = ReferenceField(Course)
