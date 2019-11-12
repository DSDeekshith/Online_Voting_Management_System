from django import forms
from .models import Voter, EC_Employee, EC_login, Candidate
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


class AddVoter(forms.ModelForm):
    class Meta:
        model = Voter
        fields = [
            'Voter_id',
            'Voter_name',
            'Voter_Phn_no',
            'Age',
            'Voter_email',
            'Voter_Username',
            'Voter_password',
            'ConstituencyID',
            'Address',
        ]


class AddCandidate(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = [
            'Candidate_id',
            'Candidate_name',
            'Party_id',
            'ConstituencyID',
            'Candidate_Email',
            'Address',
            'Candidate_phn_no',



        ]


class AddEmployee1(forms.ModelForm):
    class Meta:
        model = EC_Employee
        fields = [
            'Emp_id',
            'Emp_Name',
            'Ec_Email',
        ]


class AddEmployee2(forms.ModelForm):
    class Meta:
        model = EC_login
        fields = [
            'login_id',
            'Username',
            'password'
        ]


class EC_login_Form(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)


class Vote_login_form(forms.Form):
    voter_user = forms.CharField(max_length=50)
    voter_pass = forms.CharField(widget=forms.PasswordInput)


class Vote_form(forms.Form):
    Choose_Candidate_ID = forms.IntegerField()


class Result_form(forms.Form):
    Enter_Constituency_ID = forms.IntegerField()
