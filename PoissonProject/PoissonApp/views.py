from django.shortcuts import render, redirect
import http.client
import json

from django.urls import reverse

from .forms import LeaguesForm, TeamsForm


# Create your views here.


def index(request):
    return render(request, 'PoissonApp/index.html', )


def about(request):
    return render(request, 'PoissonApp/about.html', )


def calculate(request):
    if request.method == "GET":
        form = LeaguesForm()
        new_form = TeamsForm()
        return render(request, 'PoissonApp/calculate.html', {'form': form})

    if request.method == "POST" and 'btnform1' in request.POST:
        conn = http.client.HTTPSConnection("v3.football.api-sports.io")
        headers = {
            'x-rapidapi-host': "v3.football.api-sports.io",
            'x-rapidapi-key': "your key"
        }

        form = LeaguesForm(request.POST)
        if form.is_valid():
            first_league_id = form.cleaned_data['first_league']
            second_league_id = form.cleaned_data['second_league']
            print(f"Liga 1 ID : {first_league_id}")
            print(f"Liga 2 ID : {second_league_id}")

            # If User chose two same leagues, only one request to the api
            if first_league_id == second_league_id:
                conn.request("GET", f"/teams?league={first_league_id}&season=2021", headers=headers)
                res = conn.getresponse()
                data = res.read()
                first_league_teams = json.loads(data.decode('utf-8'))
                teams = []
                for i, x in enumerate(first_league_teams['response']):
                    teams.append([first_league_teams['response'][i]['team']['id'],
                                  first_league_teams['response'][i]['team']['name']])
                # creating new form and added choices
                new_form = TeamsForm()
                new_form.fields['first_team'].choices = teams
                new_form.fields['second_team'].choices = teams
            else:
                print("Przypadek jeśli dwie ligi są różne działa !")
                conn.request("GET", f"/teams?league={first_league_id}&season=2021", headers=headers)
                res = conn.getresponse()
                data = res.read()
                first_league_teams = json.loads(data.decode('utf-8'))
                conn.request("GET", f"/teams?league={second_league_id}&season=2021", headers=headers)
                res2 = conn.getresponse()
                data2 = res2.read()
                second_league_teams = json.loads(data2.decode('utf-8'))
                teams1 = []
                teams2 = []
                for i, x in enumerate(first_league_teams['response']):
                    teams1.append([int(first_league_teams['response'][i]['team']['id']),
                                   first_league_teams['response'][i]['team']['name']])
                for i, x in enumerate(second_league_teams['response']):
                    teams2.append([int(second_league_teams['response'][i]['team']['id']),
                                   second_league_teams['response'][i]['team']['name']])
                new_form = TeamsForm()
                print(type(teams1[0][0]))
                new_form.fields['first_team'].choices = teams1
                new_form.fields['second_team'].choices = teams2
                print(teams1)
                print(teams2)
            return render(request, 'PoissonApp/calculate.html', {'form2': new_form})

    if request.method == "POST" and 'btnform2' in request.POST:
        new_form = TeamsForm(request.POST)
        print("test dla różnych opcji lig")
        print(new_form)
        if new_form.is_valid():
            first_team = new_form.cleaned_data['first_team']
            second_team = new_form.cleaned_data['second_team']
            print("test2")
            print(f"Pierwsza drużyna : {first_team}")
            print(f"Druga drużyna : {second_team}")
            return render(request, 'PoissonApp/index.html')
        return render(request, 'PoissonApp/about.html')


# def calculate2(request):
#
#     if request.method == "GET":
#         return render(request, 'PoissonApp/calculate2.html')
#
#     if request.method == "POST":
#         new_form2 = TeamsForm(request.POST)
#         print("test dla różnych opcji lig")
#         print(new_form2)
#         if new_form2.is_valid():
#             first_team = new_form2.cleaned_data['first_team']
#             second_team = new_form2.cleaned_data['second_team']
#             print("test2")
#             print(f"Pierwsza drużyna : {first_team}")
#             print(f"Druga drużyna : {second_team}")
#             return render(request, 'PoissonApp/index.html')
#
#         return render(request,'PoissonApp/contact.html')

        # form = LeaguesForm(request.POST)
        # if form.is_valid():
        #     print('działa0')
        #     first_league = form.cleaned_data['first_league']
        #     second_league = form.cleaned_data['second_league']
        #     if first_league == second_league:
        #         print('działa1')
        #         conn.request("GET", f"/teams?league={first_league}&season=2021", headers=headers)
        #         res = conn.getresponse()
        #         data = res.read()
        #         data_first_teams = json.loads(data.decode('utf-8'))
        #         teams1 = []
        #         for i, x in enumerate(data_first_teams['response']):
        #             teams1.append([data_first_teams['response'][i]['team']['id'],
        #                            data_first_teams['response'][i]['team']['name']])
        #
        #         # new_form = LeaguesForm()
        #         new_form = TeamsForm()
        #         new_form.fields['first_team'].choices = teams1
        #         new_form.fields['second_team'].choices = teams1
        #     else:
        #         print('działa2')
        #         conn.request("GET", f"/teams?league={first_league}&season=2021", headers=headers)
        #         res1 = conn.getresponse()
        #         data = res1.read()
        #         data_first_teams = json.loads(data.decode('utf-8'))
        #         conn.request("GET", f"/teams?league={second_league}&season=2021", headers=headers)
        #         res2 = conn.getresponse()
        #         data = res2.read()
        #         data_second_teams = json.loads(data.decode('utf-8'))
        #         teams1 = []
        #         teams2 = []
        #         for i, x in enumerate(data_first_teams['response']):
        #             teams1.append([data_first_teams['response'][i]['team']['id'],
        #                            data_first_teams['response'][i]['team']['name']])
        #         for i, x in enumerate(data_second_teams['response']):
        #             teams2.append([data_second_teams['response'][i]['team']['id'],
        #                            data_second_teams['response'][i]['team']['name']])
        #         # new_form = LeaguesForm()
        #         new_form = TeamsForm()
        #         new_form.fields['first_team'].choices = teams1
        #         new_form.fields['second_team'].choices = teams2
        #         # print(data_first_teams)
        #         # new_form.fields['first_league'].label = "First team"
        #         # new_form.fields['second_league'].label = "Second team"
        #         if request.method == "POST":
        #             # form = LeaguesForm(request.POST)
        #             form = TeamsForm(request.POST)
        #             print('działa3')
        #             print(form)
        #             if form.is_valid():
        #                 print('działa4')
        #                 print(first_league)
        #                 print(second_league)
        #                 first_team = form.cleaned_data['first_team']
        #                 second_team = form.cleaned_data['second_team']
        #                 conn.request("GET", f"/teams?id={first_team}", headers=headers)
        #                 response = conn.getresponse()
        #                 data = response.read()
        #                 first_team_information = json.loads(data.decode('utf-8'))
        #                 conn.request("GET", f"/teams?id={second_team}", headers=headers)
        #                 response = conn.getresponse()
        #                 data = response.read()
        #                 second_team_information = json.loads(data.decode('utf-8'))
        #                 # Działa id drużyn są pobrane :)
        #                 # Teraz zamiast druzyn trzeba pobrać ich statystyki,
        #                 # get("https://v3.football.api-sports.io/teams/statistics?league=39&team=33&season=2019");
        #                 print(first_team_information['response'], second_team_information['response'])
        #
        #     return render(request, 'PoissonApp/calculate.html', {'form2': new_form})
        # else:
        #     return render(request,'PoissonApp/index.html')
