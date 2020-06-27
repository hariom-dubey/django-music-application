import requests

country = 'India'

url = 'https://corona.lmao.ninja/v2/historical/' + country + '?lastdays=1'

url2 = "https://api.covidindiatracker.com/state_data.json"


def get_percentage(how_much, out_of):
    per = (how_much / out_of) * 100
    temp_lst = str(per).split('.')
    lst_per = list(temp_lst[1])
    if int(lst_per[2]) > 5:
        lst_per[1] = str(int(lst_per[1]) + 1)
    temp_per = ''
    for i in range(0, 2):
        temp_per += lst_per[i]
    per = temp_lst[0] + '.' + temp_per
    return per


response = requests.get(url)

india_confirmed = list(response.json()['timeline']['cases'].values())[0]
# temp_date = list(response.json()['timeline']['cases'].keys())[0]
india_deaths = list(response.json()['timeline']['deaths'].values())[0]
india_recover = list(response.json()['timeline']['recovered'].values())[0]
india_active = india_confirmed - india_deaths - india_recover

response2 = requests.get(url2)

maha_recovered = response2.json()[0]['recovered']
maha_confirmed = response2.json()[0]['confirmed']
mumbai_confirmed = response2.json()[0]['districtData'][0]['confirmed']


india_per_active = get_percentage(india_active, india_confirmed)
india_per_recover = get_percentage(india_recover, india_confirmed)
india_per_deaths = get_percentage(india_deaths, india_confirmed)
maha_per_recover = get_percentage(maha_recovered, maha_confirmed)
mum_per_india = get_percentage(mumbai_confirmed, india_confirmed)

