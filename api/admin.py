from django.contrib import admin
from . models import User, Hostel, Block, Room, Student

admin.site.register([User, Hostel, Block, Room, Student])
