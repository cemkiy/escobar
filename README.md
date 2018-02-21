
![alt tag](https://d13yacurqjgara.cloudfront.net/users/322905/screenshots/2273155/pablo_v7.gif)

# Escobar
Escobar is a crypto coin statics helper. It's purpose is determine the accuracy of your functions.

  - Light Weight
  - Yo Notifications
  - No Requirements Databases
  - Uses Coin Market Cap datas
  - Escobar wise every time
  - Python 3.x

# Environment
Please set up your environment variables.

    coin_name=bitcoin
    currency=USD
    notify_high_yo_api_key=<api_key>
    notify_constant_yo_api_key=<api_key>
    notify_fall_yo_api_key=<api_key>

# How does it work
Escobar assigns a value to each function. The sum of these values does not exceed 100. That is, each function has a percentage of accuracy. These values are recalculated according to the results they give. And escobar is more intelligent in every work.

You can run the escort at any interval.

    python escobar.py

# Write Your Own Functions

 1. Write your own function to forecast.py. The functions can only return 0,1 or -1.
 0 is will be ignored. 1 is rises and -1 is falls . Example func:
 ```python
def trend_by_weekdays(self):
        weekno = datetime.datetime.today().weekday()
        if weekno < 5:
            # weekday
            return 0
        else:
            # weekend
            return -1
```

2. Register the functions you want to run in escobar.py.
 ```python
functions_to_be_run = {
    'trend_by_perc': Forecast.trend_by_perc,
    'trend_by_weekdays': Forecast.trend_by_weekdays
}
```

Done. You can now run and view the results.

# Yo
Yo sends only yo. Escobar script is use this features for send notification about results.
