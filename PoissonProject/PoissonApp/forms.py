from django import forms
import json
leagues = {}
file_location = "all_leagues.json"
countries = []
with open(file_location) as data_file:
    data = json.load(data_file)

    for i, element in enumerate(data['response']):
        name = element['league']['name']
        logo = element['league']['logo']
        id = element['league']['id']
        country = element['country']['name']
        country_flag = element['country']['flag']
        leagues[i] = {'name': name, 'logo': logo, 'id': id, 'country': country, 'country_flag': country_flag, }
        if country not in countries:
            countries.append(country)
items = []

for i,country in enumerate(countries):
    items.append([country,[]])
    for index, league in enumerate(leagues):
        if leagues[league]['country'] == country:
            items[i][1].append([leagues[league]['id'],leagues[league]['name'],])


class LeaguesForm(forms.Form):
    first_league = forms.ChoiceField(choices=items, widget=forms.Select(attrs={'class': 'form-select',}))
    second_league = forms.ChoiceField(choices=items, widget=forms.Select(attrs={'class': 'form-select',}))


class TeamsForm(forms.Form):
    first_team = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-select',}))
    second_team = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-select',}))