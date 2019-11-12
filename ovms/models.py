from django.db import models

# Create your models here.


class EC_login(models.Model):
    login_id = models.PositiveIntegerField(primary_key=True)
    Username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)


class EC_Employee(models.Model):
    Emp_id = models.PositiveIntegerField(primary_key=True)
    Emp_Name = models.CharField(max_length=50)
    Ec_Email = models.EmailField()
    login_id = models.ForeignKey(EC_login, on_delete=models.CASCADE, null=True)

    class Meta:
        unique_together = (('Emp_id', 'login_id'),)


class Constituency(models.Model):
    Constituency_id = models.PositiveIntegerField(primary_key=True)
    Constituency_name = models.CharField(max_length=50)
    City = models.CharField(max_length=50)
    District = models.CharField(max_length=50)

    class Meta:
        unique_together = (('Constituency_id', 'Constituency_name'),)


class Voter(models.Model):
    Voter_id = models.PositiveIntegerField(primary_key=True)
    Voter_name = models.CharField(max_length=50)
    Voter_Phn_no = models.PositiveIntegerField(
        help_text='Enter a 10 digit number')
    Age = models.PositiveIntegerField()
    Voter_email = models.EmailField()
    Address = models.TextField()
    Voter_Username = models.CharField(max_length=50, null=True)
    Voter_password = models.CharField(max_length=50, null=True)
    ConstituencyID = models.ForeignKey(Constituency, on_delete=models.CASCADE)
    Has_voted = models.BooleanField(default=False)

    class Meta:
        unique_together = (('Voter_id', 'ConstituencyID',
                            'Voter_Username', 'Voter_password'),)


class Party(models.Model):
    Party_id = models.PositiveIntegerField(primary_key=True)
    Party_name = models.CharField(max_length=50)
    Party_symbol = models.CharField(max_length=20)


class Candidate(models.Model):
    Candidate_id = models.PositiveIntegerField(primary_key=True)
    Candidate_name = models.CharField(max_length=50)
    Party_id = models.ForeignKey(Party, on_delete=models.CASCADE, null=True)
    ConstituencyID = models.ForeignKey(Constituency, on_delete=models.CASCADE)
    Address = models.CharField(max_length=150)
    Candidate_Email = models.EmailField()
    Candidate_phn_no = models.PositiveIntegerField()
    No_of_votes = models.PositiveIntegerField(null=True)

    class Meta:
        unique_together = (('Candidate_id', 'Party_id', 'ConstituencyID'),)


class Vote(models.Model):
    Vote_id = models.PositiveIntegerField(primary_key=True)
    CandidateID = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    Voter_id = models.ForeignKey(Voter, on_delete=models.CASCADE, null=True)
