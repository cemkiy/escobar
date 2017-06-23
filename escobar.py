from stats import Stats
from real_environment import real_environment
import yopy
import json


def update_weights(weight):
    try:
        with open('prophecy_' + renv.get_env_or_default("coin_symbol", "") +
                  '.json') as data_file:
            prophecy = json.load(data_file)

        try:
            with open('ticker_' + renv.get_env_or_default("coin_symbol", "") +
                      '.json') as data_file:
                ticker = json.load(data_file)
                if stats.ticker["last_price"] >= ticker["last_price"]:
                    # high
                    # TODO: update weight
                elif:
                    # low
                    # TODO: update weight
        except:
            print("No found prophecy data.")
    except:
        print("No found prophecy data.")


def escobar():
    renv = real_environment.RealEnvironment()
    yo_high = yopy.Yo(renv.get_env_or_default("notify_high_yo_api_key", ""))
    yo_low = yopy.Yo(renv.get_env_or_default("notify_low_yo_api_key", ""))
    stats = Stats()

    weight = {}
    try:
        with open('weight_' + renv.get_env_or_default("coin_symbol", "") +
                  '.json') as data_file:
            weight = json.load(data_file)
    except FileNotFoundError:
        with open('weight_' + renv.get_env_or_default("coin_symbol", "") +
                  '.json', 'w') as outfile:
            data = {}
            data["volume"] = 100 / 3
            data["ftbttt"] = 100 / 3
            data["week"] = 100 / 3
            json.dump(data, outfile)

    update_weights(weight)

    prophecy = {}
    prophecy["volume"] = stats.process_volume_stats()
    prophecy["ftbttt"] = stats.process_from_the_bottom_to_the_top()
    prophecy["week"] = stats.process_week()

    result_turn = prophecy["volume"] * weight["volume"] + \
        prophecy["ftbttt"] * weight["ftbttt"] + \
        prophecy["week"] * weight["week"]

    if result_turn >= 0:
        yo_high.youser(renv.get_env_or_default("notify_yo_username", ""))
    elif result_turn < 0:
        yo_low.youser(renv.get_env_or_default("notify_yo_username", ""))
