import math
from decouple import config
from django.shortcuts import render
import http.client
import json
from .forms import LeaguesForm, TeamsForm, ContactForm
import datetime
from django.core.mail import send_mail
from django.conf import settings
# defined time

actual_date = datetime.datetime.today()
actual_year = actual_date.strftime("%Y")
time_range = actual_date - datetime.timedelta(weeks=6)
time_range = time_range.strftime('%Y-%m-%d')


# list teams of first chosen league
teams1 = []
# list teams of second chosen league
teams2 = []
# list teams of one league if first league is equal to second league
teams = []
# list id of chosen leagues
chosen_leagues_id = []


def index(request):
    return render(request, 'PoissonApp/index.html', )


def about(request):
    return render(request, 'PoissonApp/about.html', )


def calculate(request):

    conn = http.client.HTTPSConnection("v3.football.api-sports.io")
    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': config('X_RAPIDAPI_KEY'),
    }
    if request.method == "GET":
        form = LeaguesForm()
        return render(request, 'PoissonApp/calculate.html', {'form': form})

    if request.method == "POST" and 'btnform1' in request.POST:
        form = LeaguesForm(request.POST)
        if form.is_valid():
            first_league_id = form.cleaned_data['first_league']
            second_league_id = form.cleaned_data['second_league']
            chosen_leagues_id.append(first_league_id)
            chosen_leagues_id.append(second_league_id)

            # If User chose two same leagues, only one request to the api to get the list of teams
            if first_league_id == second_league_id:
                conn.request("GET", f"/teams?league={first_league_id}&season=2021", headers=headers)
                res = conn.getresponse()
                data = res.read()
                first_league_teams = json.loads(data.decode('utf-8'))
                if len(first_league_teams['errors']) >= 1:
                    error_api = '''Sorry, the maximum number of the requests reach the day limit...
                     Try again tommorow or send me some money to upgrade the plan ;) '''
                    return render(request, 'PoissonApp/calculate.html', {'error_api': error_api})

                teams.clear()
                for i, x in enumerate(first_league_teams['response']):
                    teams.append([int(first_league_teams['response'][i]['team']['id']),
                                  first_league_teams['response'][i]['team']['name']])
                # creating new form and added choices
                new_form = TeamsForm()
                teams_copy = teams.copy()
                new_form.fields['first_team'].choices = teams_copy
                new_form.fields['second_team'].choices = teams_copy
            else:
                conn.request("GET", f"/teams?league={first_league_id}&season={actual_year}", headers=headers)
                res = conn.getresponse()
                data = res.read()
                first_league_teams = json.loads(data.decode('utf-8'))
                conn.request("GET", f"/teams?league={second_league_id}&season={actual_year}", headers=headers)
                res2 = conn.getresponse()
                data2 = res2.read()
                second_league_teams = json.loads(data2.decode('utf-8'))
                if len(first_league_teams['errors']) >= 1:
                    error_api = '''Sorry, the maximum number of the requests reach the day limit...
                     Try again tommorow or send me some money to upgrade the plan ;) '''
                    return render(request, 'PoissonApp/calculate.html', {'error_api': error_api})
                teams1.clear()
                teams2.clear()
                for i, x in enumerate(first_league_teams['response']):
                    teams1.append([int(first_league_teams['response'][i]['team']['id']),
                                   first_league_teams['response'][i]['team']['name']])
                for i, x in enumerate(second_league_teams['response']):
                    teams2.append([int(second_league_teams['response'][i]['team']['id']),
                                   second_league_teams['response'][i]['team']['name']])
                new_form = TeamsForm()
                teams1_copy = teams1.copy()
                teams2_copy = teams2.copy()
                new_form.fields['first_team'].choices = teams1_copy
                new_form.fields['second_team'].choices = teams2_copy
            return render(request, 'PoissonApp/calculate.html', {'form2': new_form, })

    if request.method == "POST" and 'btnform2' in request.POST:
        copy_chosen_leagues_id = chosen_leagues_id.copy()
        new_form = TeamsForm(request.POST)
        # When user chose leagues
        if len(copy_chosen_leagues_id) >= 2:
            # When leagues are the same, defined new choices
            if copy_chosen_leagues_id[-1] == copy_chosen_leagues_id[-2]:
                new_form.fields['first_team'].choices = teams
                new_form.fields['second_team'].choices = teams
            else:
                new_form.fields['first_team'].choices = teams1
                new_form.fields['second_team'].choices = teams2

            chosen_leagues_id.clear()
            if new_form.is_valid():
                # defined time
                # actual_date = datetime.datetime.today()
                # actual_year = actual_date.strftime("%Y")
                # time_range = actual_date - datetime.timedelta(weeks=5)
                # time_range = time_range.strftime('%Y-%m-%d')
                first_team = new_form.cleaned_data['first_team']
                second_team = new_form.cleaned_data['second_team']
                if first_team == second_team:
                    conn.request("GET",
                                 f"https://v3.football.api-sports.io/teams/statistics?league={copy_chosen_leagues_id[-1]}&team={first_team}&season={actual_year}",
                                 headers=headers)
                    res = conn.getresponse()
                    data = res.read()
                    first_team_information_all_season = json.loads(data.decode('utf-8'))
                    second_team_information_all_season = json.loads(data.decode('utf-8'))
                    conn.request("GET",
                                 f"https://v3.football.api-sports.io/teams/statistics?league={copy_chosen_leagues_id[-1]}&team={second_team}&season={actual_year}&date={time_range}",
                                 headers=headers)
                    res = conn.getresponse()
                    data = res.read()
                    first_team_information_to_date = json.loads(data.decode('utf-8'))
                    second_team_information_to_date = json.loads(data.decode('utf-8'))
                else:
                    conn.request("GET",
                                 f"https://v3.football.api-sports.io/teams/statistics?league={copy_chosen_leagues_id[-2]}&team={first_team}&season={actual_year}&date={time_range}",
                                 headers=headers)
                    res = conn.getresponse()
                    data = res.read()
                    first_team_information_to_date = json.loads(data.decode('utf-8'))
                    conn.request("GET",
                                 f"https://v3.football.api-sports.io/teams/statistics?league={copy_chosen_leagues_id[-2]}&team={first_team}&season={actual_year}",
                                 headers=headers)
                    res = conn.getresponse()
                    data = res.read()
                    first_team_information_all_season = json.loads(data.decode('utf-8'))
                    conn.request("GET",
                                 f"https://v3.football.api-sports.io/teams/statistics?league={copy_chosen_leagues_id[-1]}&team={second_team}&season={actual_year}&date={time_range}",
                                 headers=headers)
                    res = conn.getresponse()
                    data = res.read()
                    second_team_information_to_date = json.loads(data.decode('utf-8'))
                    conn.request("GET",
                                 f"https://v3.football.api-sports.io/teams/statistics?league={copy_chosen_leagues_id[-1]}&team={second_team}&season={actual_year}",
                                 headers=headers)
                    res = conn.getresponse()
                    data = res.read()
                    second_team_information_all_season = json.loads(data.decode('utf-8'))

                print(first_team_information_all_season['response'])
                print('**************************')
                print(second_team_information_all_season['response'])
                print('&&&&&&&&&&&&&&&&&&')
                print(first_team_information_all_season)
                print('**************************')
                print(second_team_information_all_season)
                if len(first_team_information_all_season['error']) >= 1 or len(second_team_information_all_season['errors']) >=1 :
                    return render(request, 'PoissonApp/calculate.html', {
                        'error_api': '''Sorry, the maximum number of the requests reach the day limit...
                        Try again tomorrow or send me some money to upgrade the plan ;) ''', })

                if first_team_information_all_season['response']['goals']['for']['total']['home'] == 0 or second_team_information_all_season['response']['goals']['for']['total']['away'] == 0:
                    return render(request, 'PoissonApp/calculate.html', {'error_api': """Sorry, 
                    the teams that you chose have not enough information for this season...""", })

                first_team_information = {
                    'league': first_team_information_all_season['response']['league']['name'],
                    'league_logo': first_team_information_all_season['response']['league']['logo'],
                    'country': first_team_information_all_season['response']['league']['country'],
                    'country_flag': first_team_information_all_season['response']['league']['flag'],
                    'team': first_team_information_all_season['response']['team']['name'],
                    'team_logo': first_team_information_all_season['response']['team']['logo'],
                }
                second_team_information = {
                    'league': second_team_information_all_season['response']['league']['name'],
                    'league_logo': second_team_information_all_season['response']['league']['logo'],
                    'country': second_team_information_all_season['response']['league']['country'],
                    'country_flag': second_team_information_all_season['response']['league']['flag'],
                    'team': second_team_information_all_season['response']['team']['name'],
                    'team_logo': second_team_information_all_season['response']['team']['logo'],
                }

                # first team all goals
                first_team_information_goals_all_season = first_team_information_all_season['response']['goals']['for']['total']['total']
                first_team_information_goals_to_date = first_team_information_to_date['response']['goals']['for']['total']['total']
                first_team_information_goals_from_to_date = first_team_information_goals_all_season - first_team_information_goals_to_date
                first_team_information_goals_all_season_home = first_team_information_all_season['response']['goals']['for']['total']['home']
                # first team all matches played
                first_team_information_matches_all_season = first_team_information_all_season['response']['fixtures']['played']['total']
                first_team_information_matches_all_season_home = first_team_information_all_season['response']['fixtures']['played']['home']
                first_team_information_matches_to_date = first_team_information_to_date['response']['fixtures']['played']['total']
                first_team_information_matches_from_to_date = first_team_information_matches_all_season - first_team_information_matches_to_date
                # first team average
                first_team_information_average_all_season = first_team_information_goals_all_season / first_team_information_matches_all_season
                first_team_information_average_all_season_home = first_team_information_goals_all_season_home/first_team_information_matches_all_season_home
                first_team_information_average_from_to_date = first_team_information_goals_from_to_date / first_team_information_matches_from_to_date
                # second team all goals
                second_team_information_goals_all_season = second_team_information_all_season['response']['goals']['for']['total']['total']
                second_team_information_goals_to_date = second_team_information_to_date['response']['goals']['for']['total']['total']
                second_team_information_goals_from_to_date = second_team_information_goals_all_season - second_team_information_goals_to_date
                second_team_information_goals_all_season_away = second_team_information_all_season['response']['goals']['for']['total']['away']
                # second team all matches played
                second_team_information_matches_all_season = second_team_information_all_season['response']['fixtures']['played']['total']
                second_team_information_matches_all_season_away = second_team_information_all_season['response']['fixtures']['played']['away']
                second_team_information_matches_to_date = second_team_information_to_date['response']['fixtures']['played']['total']
                second_team_information_matches_from_to_date = second_team_information_matches_all_season - second_team_information_matches_to_date
                # second team average
                second_team_information_average_all_season = second_team_information_goals_all_season / second_team_information_matches_all_season
                second_team_information_average_from_to_date = second_team_information_goals_from_to_date / second_team_information_matches_from_to_date
                second_team_information_average_all_season_away = second_team_information_goals_all_season_away/second_team_information_matches_all_season_away

                #Poisson Distribution - calculate
                #events - 5 goals in match
                k_elements = [0, 1, 2, 3, 4, 5]
                e_value = 2.718
                first_team_poisson_results_all_season = []
                second_team_poisson_results_all_season = []
                first_team_poisson_results_from_to_date = []
                second_team_poisson_results_from_to_date = []
                first_team_poisson_results_all_season_home = []
                second_team_poisson_results_all_season_home = []
                first_team_all = 0
                first_team_date = 0
                first_team_home = 0
                second_team_all = 0
                second_team_date = 0
                second_team_home = 0
                for k in k_elements:
                        result_first_team = ((pow(first_team_information_average_all_season,k) * pow(e_value, -first_team_information_average_all_season))/math.factorial(k))*100
                        first_team_poisson_results_all_season.append(result_first_team)
                        result_first_team_from_to_date = ((pow(first_team_information_average_from_to_date,k) * pow(e_value, -first_team_information_average_from_to_date))/math.factorial(k))*100
                        first_team_poisson_results_from_to_date.append(result_first_team_from_to_date)
                        result_first_team_home = ((pow(first_team_information_average_all_season_home, k) * pow(e_value, -first_team_information_average_all_season_home)) / math.factorial(k)) * 100
                        first_team_poisson_results_all_season_home.append(result_first_team_home)
                        result_second_team = ((pow(second_team_information_average_all_season,k) * pow(e_value, -second_team_information_average_all_season))/math.factorial(k))*100
                        second_team_poisson_results_all_season.append(result_second_team)
                        result_second_team_from_to_date = ((pow(second_team_information_average_from_to_date, k) * pow(e_value, -second_team_information_average_from_to_date)) / math.factorial(k)) * 100
                        second_team_poisson_results_from_to_date.append(result_second_team_from_to_date)
                        result_second_team_home = ((pow(second_team_information_average_all_season_away, k) * pow(e_value, -second_team_information_average_all_season_away)) / math.factorial(k)) * 100
                        second_team_poisson_results_all_season_home.append(result_second_team_home)
                        first_team_all += result_first_team
                        first_team_date += result_first_team_from_to_date
                        first_team_home += result_first_team_home
                        second_team_all += result_second_team
                        second_team_date += result_second_team_from_to_date
                        second_team_home += result_second_team_home
                print(f'{first_team_all}')
                print(f'{first_team_date}')
                print(f'{first_team_home}')
                print(f'{second_team_all}')
                print(f'{second_team_date}')
                print(f'{second_team_home}')
                # Poisson distribution - calculate result of the match dependent on team condition /at home and at away
                # Percent chance for Home Team / Draw / Away Team
                if len(first_team_poisson_results_all_season_home) == 6 and len(second_team_poisson_results_all_season_home) == 6:
                    draw = 0
                    home_win = 0
                    against_win = 0

                    # Calculate probabilities for all result in match Max 5 goals
                    for i, x in enumerate(first_team_poisson_results_all_season_home):
                        draw += first_team_poisson_results_all_season_home[i] * second_team_poisson_results_all_season_home[i]
                        if i == 0:
                            for element in range(5):
                                home_win += first_team_poisson_results_all_season_home[element + 1] * second_team_poisson_results_all_season_home[0]
                                against_win += second_team_poisson_results_all_season_home[element + 1] * first_team_poisson_results_all_season_home[0]
                        elif i == 1:
                            for element in range(4):
                                home_win += first_team_poisson_results_all_season_home[element + 2] * second_team_poisson_results_all_season_home[1]
                                against_win += second_team_poisson_results_all_season_home[element + 2] * first_team_poisson_results_all_season_home[1]
                        elif i == 2:
                            for element in range(3):
                                home_win += first_team_poisson_results_all_season_home[element + 3] * second_team_poisson_results_all_season_home[2]
                                against_win += second_team_poisson_results_all_season_home[element + 3] * first_team_poisson_results_all_season_home[2]
                        elif i == 3:
                            for element in range(2):
                                home_win += first_team_poisson_results_all_season_home[element + 4] * second_team_poisson_results_all_season_home[3]
                                against_win += second_team_poisson_results_all_season_home[element + 4] * first_team_poisson_results_all_season_home[3]
                        elif i == 4:
                            for element in range(1):
                                home_win += first_team_poisson_results_all_season_home[element + 5] * second_team_poisson_results_all_season_home[4]
                                against_win += second_team_poisson_results_all_season_home[element + 5] * first_team_poisson_results_all_season_home[4]
                    draw = format(draw/100, '.1f')
                    home_win = format(home_win/100, '.1f')
                    against_win = format(against_win/100, '.1f')

                return render(request, 'PoissonApp/calculate2.html', context={
                    'first_team': first_team_poisson_results_all_season,
                    'second_team': second_team_poisson_results_all_season,
                    'first_team_from_to': first_team_poisson_results_from_to_date,
                    'second_team_from_to': second_team_poisson_results_from_to_date,
                    'k_elements': k_elements,
                    'first_team_information': first_team_information,
                    'second_team_information': second_team_information,
                    'draw': draw,
                    'home_win': home_win,
                    'against_win': against_win,
                })
        # if user didn't chose leagues ( or simply click back button ), we create new form and render template
        form = LeaguesForm()
        return render(request, 'PoissonApp/calculate.html', context={'form': form, })


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            message_subject = form.cleaned_data['subject']
            message_email = form.cleaned_data['mail']
            message_name = form.cleaned_data['name']

            mail_message = f"""
               From:{message_name}
               Email: {message_email}
               Message: {message}
               """
            # send an email
            send_mail(
                message_subject,  # subject
                mail_message,  # message
                message_email,  # from email
                [settings.EMAIL_HOST_USER],  # to email
            )
            return render(request, 'PoissonApp/contact.html', {'message_name': message_name})
    else:
        form = ContactForm()
    return render(request, 'PoissonApp/contact.html', context={'form': form, })
