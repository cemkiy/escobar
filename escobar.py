from stats import Stats
import utils
from real_environment import real_environment
import yopy
import json


def update_weights(weight, stats):
    renv = real_environment.RealEnvironment()
    try:
        prophecy = utils.read_file(
            'prophecy_' + renv.get_env_or_default("coin_symbol", "") + '.json')
    except:
        print("No found prophecy data.")
        return

    try:
        ticker = utils.read_file(
            'ticker_' + renv.get_env_or_default("coin_symbol", "") + '.json')
    except:
        print("No found prophecy ticker.")
        return

    wrong_weights = []

    if stats.ticker["last_price"] >= ticker["last_price"]:
        # high
        if prophecy["volume"] == -1:
            weight["volume"] -= 2
            wrong_weights.append("volume")
        if prophecy["ftbttt"] == -1:
            weight["ftbttt"] -= 2
            wrong_weights.append("ftbttt")
        if prophecy["week"] == -1:
            weight["week"] -= 2
            wrong_weights.append("week")
    elif stats.ticker["last_price"] < ticker["last_price"]:
        # low
        if prophecy["volume"] == 1:
            weight["volume"] -= 2
            wrong_weights.append("volume")
        if prophecy["ftbttt"] == 1:
            weight["ftbttt"] -= 2
            wrong_weights.append("ftbttt")
        if prophecy["week"] == 1:
            weight["week"] -= 2
            wrong_weights.append("week")

    will_be_distributed_points_per_weight = (
        len(wrong_weights) * 2) / (3 - len(wrong_weights))

    if "volume" not in wrong_weights:
        weight["volume"] += will_be_distributed_points_per_weight
    if "ftbttt" not in wrong_weights:
        weight["ftbttt"] += will_be_distributed_points_per_weight
    if "week" not in wrong_weights:
        weight["week"] += will_be_distributed_points_per_weight

    utils.write_file(
        'weight_' + renv.get_env_or_default("coin_symbol", "") + '.json', weight)


def escobar():
    renv = real_environment.RealEnvironment()
    yo_high = yopy.Yo(renv.get_env_or_default("notify_high_yo_api_key", ""))
    yo_low = yopy.Yo(renv.get_env_or_default("notify_low_yo_api_key", ""))
    stats = Stats()

    utils.write_file(
        'ticker_' + renv.get_env_or_default("coin_symbol", "") + '.json', stats.ticker)

    weight = {}
    try:
        weight = utils.read_file(
            'weight_' + renv.get_env_or_default("coin_symbol", "") + '.json')
    except FileNotFoundError:
        data = {}
        data["volume"] = 100 / 3
        data["ftbttt"] = 100 / 3
        data["week"] = 100 / 3
        utils.write_file(
            'weight_' + renv.get_env_or_default("coin_symbol", "") + '.json', data)

    update_weights(weight, stats)

    prophecy = {}
    prophecy["volume"] = stats.process_volume_stats()
    prophecy["ftbttt"] = stats.process_from_the_bottom_to_the_top()
    prophecy["week"] = stats.process_week()

    utils.write_file(
        'prophecy_' + renv.get_env_or_default("coin_symbol", "") + '.json', prophecy)

    result_turn = prophecy["volume"] * weight["volume"] + \
        prophecy["ftbttt"] * weight["ftbttt"] + \
        prophecy["week"] * weight["week"]

    if result_turn >= 0:
        yo_high.youser(renv.get_env_or_default("notify_yo_username", ""))
    elif result_turn < 0:
        yo_low.youser(renv.get_env_or_default("notify_yo_username", ""))


escobar()
