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
        if country not in countries and country != 'World':
            countries.append(country)
items = []

for i, country in enumerate(countries):

    items.append([country,[]])
    for index, league in enumerate(leagues):
        if leagues[league]['country'] == country:
            items[i][1].append([leagues[league]['id'], leagues[league]['name'],])


class LeaguesForm(forms.Form):
    first_league = forms.ChoiceField(choices=items, widget=forms.Select(attrs={'class': 'form-select',}))
    second_league = forms.ChoiceField(choices=items, widget=forms.Select(attrs={'class': 'form-select',}))


class TeamsForm(forms.Form):
    first_team = forms.TypedChoiceField(coerce=int, widget=forms.Select(attrs={'class': 'form-select',}))
    second_team = forms.TypedChoiceField(coerce=int, widget=forms.Select(attrs={'class': 'form-select',}))


class ContactForm(forms.Form):
    name = forms.CharField(label='Your name', max_length=128, widget=forms.TextInput(attrs={'class': 'text-input',
                                                                                            'placeholder': 'Enter Your Name',
                                                                                            }), )
    mail = forms.EmailField(label='Your Email', max_length=256, widget=forms.EmailInput(attrs={'class': 'text-input',
                                                                                    'placeholder': 'Enter Your Email',
                                                                                                        }), )
    subject = forms.CharField(label='Subject', max_length=128, widget=forms.TextInput(attrs={'class': 'text-input',
                                                                                             'placeholder': 'Subject',
                                                                                                      }), )
    message = forms.CharField(label='Message',
                              widget=forms.Textarea(attrs={'class': 'text-input', 'rows': 10,
                                                           'placeholder': 'Type a message...', }), )
