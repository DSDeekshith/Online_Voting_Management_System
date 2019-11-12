from django.shortcuts import render, redirect
from django.db import connection
from .forms import AddVoter, EC_login_Form, AddEmployee1, AddEmployee2, AddCandidate, Vote_login_form, Vote_form, Result_form
from django.contrib import messages
from django.http import HttpResponse
from .models import EC_login, Candidate, Voter, Party

# from .models import voter

# Create your views here.

c = connection.cursor()


def baseView(request):
    return render(request, 'base.html', {})


def AddVoterView(request):
    form = AddVoter(request.POST or None)
    if form.is_valid():
        form.save()
        form = AddVoter()
        messages.success(request, 'Form submission successful')
        return render(request, "EC_home.html", {})
    context = {
        'form': form
    }
    return render(request, "Add_Voter.html", context)


def AddCandidateView(request):
    form = AddCandidate(request.POST or None)
    if form.is_valid():
        form.save()
        form = AddCandidate()
        messages.success(request, 'Form submission successful')
        return render(request, "EC_home.html", {})
    context = {
        'form': form
    }
    return render(request, "Add_Candidate.html", context)


def AddEmployeeView(request):
    emp_form1 = AddEmployee1(request.POST or None)
    emp_form2 = AddEmployee2(request.POST or None)
    if emp_form1.is_valid() and emp_form2.is_valid():
        empID = emp_form1.cleaned_data['Emp_id']
        emp_form1.save()
        loginID = emp_form2.cleaned_data['login_id']
        emp_form2.save()
        c.execute("update ovms_ec_employee set login_id_id = %s where Emp_id = %s", [
                  loginID, empID])
        emp_form1 = AddEmployee1()
        emp_form2 = AddEmployee2()
        messages.success(request, 'Form submission successful')
    context = {
        'emp_form1': emp_form1,
        'emp_form2': emp_form2
    }
    return render(request, "Add_Employee.html", context)


def Home(request):
    return render(request, "Home.html")


def EC_Login(request):
    ec_login_form = EC_login_Form(request.POST or None)
    if ec_login_form.is_valid():
        user = ec_login_form.cleaned_data['username']
        passw = ec_login_form.cleaned_data['password']
        c.execute(
            "select Username,password from ovms_ec_login where Username=%s;", [user])
        name = c.fetchall()
        if name:
            if name[0][0]:
                if passw == name[0][1]:
                    return render(request, "EC_home.html", {})
        else:
            messages.error(request, 'User Not Found')
    context = {
        'ec_login_form': ec_login_form
    }
    return render(request, "EC_Login.html", context)


def EC_Signup(request):
    return render(request, "EC_Signup.html")


def success(request):
    return render(request, "success.html", {})


def VotersView(request):
    vot_list = Voter.objects.raw('select * from ovms_voter')
    return render(request, "View_Voters.html", {"vot_list": vot_list})


def CandidatesView(request):
    cand_list = Candidate.objects.raw(
        'select Candidate_id,Candidate_name,Party_id_id,Address,Candidate_Email,Candidate_phn_no,No_of_votes from ovms_candidate')
    return render(request, "View_Candidates.html", {"cand_list": cand_list})


def VoteLoginView(request):
    vote_login_form = Vote_login_form(request.POST or None)
    if vote_login_form.is_valid():
        user = vote_login_form.cleaned_data['voter_user']
        passw = vote_login_form.cleaned_data['voter_pass']
        c.execute(
            "select Has_Voted from ovms_voter where Voter_Username=%s;", [user])
        flag = c.fetchone()
        if flag[0] == 0:
            c.execute(
                "select Voter_Username,Voter_password from ovms_voter where Voter_Username=%s;", [user])
            name = c.fetchall()
            if name[0][0]:
                if passw == name[0][1]:
                    c.execute(
                        "select Voter_id,ConstituencyID_id from ovms_voter where Voter_Username = %s;", [user])
                    i = c.fetchone()
                    id = i[0]
                    vid = i[1]
                    request.session['id'] = id
                    request.session['vid'] = vid
                    return redirect('Vote')
        else:
            messages.error(request, "Voter has already casted his Vote")
            return redirect('Vote_Login')
    context = {
        'vote_login_form': vote_login_form
    }
    return render(request, "Vote_Login.html", context)


def VoteView(request):
    C_ID = request.session.get('id')
    V_ID = request.session.get('vid')
    all_list = Candidate.objects.select_related('Party_id')
    #party_list = Party.objects.values_list('Party_id', 'Party_name')
    #all_list = cand_list.union(party_list)
    vote_form = Vote_form(request.POST or None)
    if vote_form.is_valid():
        cand_id = vote_form.cleaned_data['Choose_Candidate_ID']
        flag1 = 0
        for r in all_list:
            if r.ConstituencyID_id == C_ID:
                if r.Candidate_id == cand_id:
                    flag1 = 1
                    c.execute(
                        "update ovms_candidate set No_of_votes = No_of_votes+1 where Candidate_id = %s", [cand_id])
                    c.execute(
                        "update ovms_voter set Has_Voted = 1 where Voter_id = %s", [V_ID])
                    return redirect('Vote_Login')
        if flag1 == 0:
            messages.error(request, "Entered Candidate ID doesn't exist")
            return redirect('Vote')
    context = {
        "all_list": all_list,
        "C_ID": C_ID,
        "vote_form": vote_form
    }
    return render(request, "Vote.html", context)


def ResultsView(request):
    res_form = Result_form(request.POST or None)
    all_list = Candidate.objects.select_related('Party_id')
    cand_list = Candidate.objects.raw(
        "select * from ovms_candidate order by No_of_votes DESC")
    if res_form.is_valid():
        C_ID = res_form.cleaned_data['Enter_Constituency_ID']
        for r in all_list:
            if r.ConstituencyID_id == C_ID:
                cand_list = Candidate.objects.raw(
                    'select Candidate_id,Candidate_name,Party_id_id,No_of_votes from ovms_candidate where ConstituencyID_id = %s order by No_of_votes DESC', [C_ID])
                res_form = Result_form(request.POST or None)
                context2 = {
                    "cand_list": cand_list,
                    "res_form": res_form
                }
                return render(request, "Results.html", context2)
                if not cand_list:
                    messages.error(request, "No results to display")
                    return render(request, "EC_home.html", {})
            else:
                messages.error(request, "Entered Constituency ID doesn't exist")
                return redirect('Results')
    context = {
        "all_list": all_list,
        "res_form": res_form
    }
    return render(request, "Results.html", context)

# def add(request):

#   val1 = int(request.POST["num1"])
#   val2 = int(request.POST["num2"])
#   res = val1 + val2

#   return render(request, "result.html", {'result':res})


# def voters_list(request):
#   # voters = voter.objects.all()
#   # context = {
#   # 'voters_list' : voters
#   # }
#   return render(request, "voters.html")

# # def voters_detail(request, id):
# #     voter = voter.objects.get(id=id)
# #     context = {
# #         'voter' : voter
# #     }
# #     return render(request, "ovms/voters_detail.html", context)
