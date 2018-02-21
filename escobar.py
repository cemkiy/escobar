from forecast import Forecast
from real_environment import real_environment
import yopy
import json
import utils

def update_weights():

# environment
renv = real_environment.RealEnvironment()

# register your func
functions_to_be_run = {
    'trend_by_perc': Forecast.trend_by_perc,
    'trend_by_weekdays': Forecast.trend_by_weekdays
}

try:
    weight = utils.read_file(
        'weight_' + renv.get_env_or_default("coin_name", "bitcoin") + '.json')
except FileNotFoundError:
    weight = {}
    for key, value in functions_to_be_run.items():
        weight[key]=100/len(functions_to_be_run)
    utils.write_file(
        'weight_' + renv.get_env_or_default("coin_name", "bitcoin") + '.json', weight)

try:
    prophecy = utils.read_file(
        'prophecy_' + renv.get_env_or_default("coin_name", "bitcoin") + '.json')
    successful_funcs = []
    unsuccessful = []
    for key, value in functions_to_be_run.items():
        if prophecy["price"] > Forecast.ticker[renv.get_env_or_default("currency", "USD").lower()]: #falls
            if prophecy[key] == -1:
                successful_funcs.append(key)
            else:
                unsuccessful.append(key)
        elif prophecy["price"] == Forecast.ticker[renv.get_env_or_default("currency", "USD").lower()]: #static
            if prophecy[key] == 0:
                successful_funcs.append(key)
            else:
                unsuccessful.append(key)
        elif prophecy["price"] < Forecast.ticker[renv.get_env_or_default("currency", "USD").lower()]: #rises
            if prophecy[key] == 1:
                successful_funcs.append(key)
            else:
                unsuccessful.append(key)
    new_weight = {}
    will_give_points_per_func = (len(unsuccessful)*2)/len(successful_funcs)
    for f in successful_funcs:
        new_weight[f] = weight[f]+will_give_points
    for f in unsuccessful:
        new_weight[f] = weight[f]-2
except:
    prophecy={}


forecast = {"price":Forecast.ticker[renv.get_env_or_default("currency", "USD").lower()]}
score = 0
for key, value in functions_to_be_run.items():
    forecast[key] = functions_to_be_run[key]()
    score += forecast[key]*weight[key]

if score > 0:
    forecast["desicion"]=1
    yo_high = yopy.Yo(renv.get_env_or_default("notify_high_yo_api_key", ""))
elif score == 0:
    forecast["desicion"]=0
    yo_constant = yopy.Yo(renv.get_env_or_default("notify_constant_yo_api_key", ""))
else:
    forecast["desicion"]=-1
    yo_fall = yopy.Yo(renv.get_env_or_default("notify_fall_yo_api_key", ""))

utils.write_file(
    'prophecy_' + renv.get_env_or_default("coin_name", "bitcoin") + '.json', forecast)
