"""A module that includes the functions for working with json files."""

import json
import os
from datetime import datetime, timedelta

import config


def update_online_stats(online_stats: dict, time_online: timedelta) -> None:
    """Update online statistics.

    Args:
        online_stats (dict): Dictionary with statistics of being online for different periods.
        time_online (timedelta): The period when the user is online.
    """
    thresholds = {
        config.LT_TWO_DAYS: timedelta(days=2),
        config.LT_WEEK: timedelta(days=7),
        config.LT_MONTH: timedelta(days=config.MONTH),
        config.LT_SIX_MONTHS: timedelta(days=config.SIX_MONTHS),
        config.GT_SIX_MONTHS: timedelta.max,
    }
    for stat_key, threshold in thresholds.items():
        if time_online < threshold:
            online_stats[stat_key] += 1
            break


def onl(usr_data: dict) -> dict:
    """Make online statistics.

    Args:
        usr_data (dict): User information.

    Returns:
        dict: Dictionary with statistics of being online for different periods.
    """
    online_stats = {
        config.LT_TWO_DAYS: 0,
        config.LT_WEEK: 0,
        config.LT_MONTH: 0,
        config.LT_SIX_MONTHS: 0,
        config.GT_SIX_MONTHS: 0,
    }
    for user_info in usr_data.values():
        user_info = {details.lower(): _ for details, _ in user_info.items()}
        if user_info.get('registered') and user_info.get('last_login'):
            registr = datetime.strptime(user_info.get('registered'), '%Y-%m-%d')
            last_log = datetime.strptime(user_info.get('last_login'), '%Y-%m-%d')
            time_online = (last_log - registr)
            update_online_stats(online_stats, time_online)
    return online_stats


def geo(usr_data: dict) -> dict:
    """Make geographical statistics.

    Args:
        usr_data (dict): User information.

    Returns:
        dict: Dictionary with statistics on the distribution of users by city.
    """
    city_stats = {}
    for user_info in usr_data.values():
        region = user_info.get('region')
        if region:
            if region not in city_stats:
                city_stats[region] = 0
            city_stats[region] += 1
    return city_stats


def slash(path: str) -> None:
    """Create and change directories and return file name in this path.

    Args:
        path (str): Path to json file.
    """
    if not os.path.exists(path[:path.rindex(config.SLASH)]):
        os.makedirs(path[:path.rindex(config.SLASH)])
    os.chdir(path[:path.rindex(config.SLASH)])
    output_file = path[path.rindex(config.SLASH) + 1:]
    with open(output_file, 'w') as out_f:
        json.dump(
            {
                'geo_distribution': 0, 'online_stats': 0,
            },
            out_f, indent=4,
        )


def process_data(data_file: str, output_file: str) -> None:
    """Make other statistics as a percentage.

    Args:
        data_file (str): Path to input json file with user data.
        output_file (str): Path to output json file.
    """
    if os.path.exists(data_file):
        with open(data_file, 'rt') as inp_f:
            usr_data = json.load(inp_f)
            geo_distrb = {city: num / len(usr_data) for city, num in geo(usr_data).items()}
            onl_sts = {period: num / len(usr_data) for period, num in onl(usr_data).items()}
            geo_distrb = {city: round(num, 2) for city, num in geo_distrb.items()}
            onl_sts = {period: round(num, 2) for period, num in onl_sts.items()}
    else:
        geo_distrb = 0
        onl_sts = 0
    if config.SLASH in output_file:
        slash(output_file)
    else:
        with open(output_file, 'w') as out_f:
            json.dump(
                {
                    'geo_distribution': geo_distrb, 'online_stats': onl_sts,
                },
                out_f, indent=4,
            )