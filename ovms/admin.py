from django.contrib import admin

# Register your models here.

from .models import EC_Employee, EC_login, Voter, Constituency, Candidate, Vote, Party


admin.site.register(EC_Employee)
admin.site.register(EC_login)
admin.site.register(Voter)
admin.site.register(Constituency)
admin.site.register(Candidate)

admin.site.register(Party)
