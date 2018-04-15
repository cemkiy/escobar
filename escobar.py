from forecast import Forecast
from real_environment import real_environment
import yopy
import json
import utils

# environment
renv = real_environment.RealEnvironment()

# forecast 
forecast = Forecast()

# register your func
functions_to_be_run = {
    'trend_by_perc': forecast.trend_by_perc,
    'trend_by_weekdays': forecast.trend_by_weekdays
}

# read weight json file. if not exist, redefine all weights
try:
    weight = utils.read_file(
        'weight_' + renv.get_env_or_default("coin_name", "bitcoin") + '.json')
except FileNotFoundError:
    weight = {}
    for key, value in functions_to_be_run.items():
        weight[key]=100/len(functions_to_be_run) # give a percantage value
    utils.write_file(
        'weight_' + renv.get_env_or_default("coin_name", "bitcoin") + '.json', weight)

# prophecy is old forecast. read prophecy data and update weights. escobar will smarter.
try:
    prophecy = utils.read_file(
        'prophecy_' + renv.get_env_or_default("coin_name", "bitcoin") + '.json')
    successful_funcs = []
    unsuccessful_funcs = []
    for key, value in functions_to_be_run.items():
        # coin price falls
        if prophecy["price"] > forecast.ticker["price_" + renv.get_env_or_default("currency", "USD").lower()]:
            if prophecy[key] == -1:
                successful_funcs.append(key)
            else:
                unsuccessful_funcs.append(key)
        # coin price constant
        elif prophecy["price"] == forecast.ticker["price_" + renv.get_env_or_default("currency", "USD").lower()]:
            if prophecy[key] == 0:
                successful_funcs.append(key)
            else:
                unsuccessful_funcs.append(key)
        # coin price rises
        elif prophecy["price"] < forecast.ticker["price_" + renv.get_env_or_default("currency", "USD").lower()]: #rises
            if prophecy[key] == 1:
                successful_funcs.append(key)
            else:
                unsuccessful_funcs.append(key)

    # write new weights
    new_weight = {}
    will_give_points_per_func = (len(unsuccessful_funcs)*2)/len(successful_funcs)
    for f in successful_funcs:
        new_weight[f] = weight[f]+will_give_points_per_func
    for f in unsuccessful_funcs:
        new_weight[f] = weight[f]-2

    utils.write_file(
        'weight_' + renv.get_env_or_default("coin_name", "bitcoin") + '.json', new_weight)
except:
    prophecy={}


forecast = {
    # save price data for next turn
    "price":forecast.ticker["price_" + renv.get_env_or_default("currency", "USD").lower()]
    }

score = 0 # score is result all functions.

for key, value in functions_to_be_run.items():
    forecast[key] = functions_to_be_run[key]()
    score += forecast[key]*weight[key]

if score > 0: # coin will rise
    forecast["desicion"]=1
    yo_high = yopy.Yo(renv.get_env_or_default("notify_high_yo_api_key", ""))
elif score == 0: # coin will constant
    forecast["desicion"]=0
    yo_constant = yopy.Yo(renv.get_env_or_default("notify_constant_yo_api_key", ""))
else: # coin will falls
    forecast["desicion"]=-1
    yo_fall = yopy.Yo(renv.get_env_or_default("notify_fall_yo_api_key", ""))

# write prophecy for next turn
utils.write_file(
    'prophecy_' + renv.get_env_or_default("coin_name", "bitcoin") + '.json', forecast)
