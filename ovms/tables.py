import django_tables2 as tables
from .models import Voter

class VoterTable(tables.Table):
    class Meta:
        model = Voter
        template_name = "django_tables2/bootstrap4.html"
        fields = ("Voter_id","Voter_name","Voter_Phn_no","Age","Voter_email","Address","ConstituencyID","Has_voted", )
