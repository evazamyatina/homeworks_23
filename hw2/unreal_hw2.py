"""Provides UNREAL :) types and functions for solving task_2."""

from datetime import datetime

import const
import pandas as pd


def aggregate_users_stats(input_path: str, output_path: str, _now: datetime = None) -> None:
    """Read user stats from input_path, aggregate them and write to output_path.

    See docs for hw2.aggregate_users_stats()

    Args:
        input_path: path to a json file containing user stats
        output_path: path to an output file. json aggregate stats will be written there.
    """
    now = datetime.now() if _now is None else _now  # for tests
    df = pd.read_json(input_path, orient='index', convert_dates=['last_login'])
    time_since_login = now - df.get('last_login', pd.Series())
    ages = df.get('age', pd.Series())
    pd.Series({
        const.LESS_TWO_DAYS: ages[time_since_login < pd.Timedelta('2 days')].mean(),
        const.LESS_WEEK: ages[time_since_login < pd.Timedelta('7 days')].mean(),
        const.LESS_MONTH: ages[time_since_login < pd.Timedelta('30 days')].mean(),
        const.LESS_HALFYEAR: ages[time_since_login < pd.Timedelta('180 days')].mean(),
        const.GREATER_HALFYEAR: ages[time_since_login > pd.Timedelta('180 days')].mean(),

        const.AGE_MAX: ages.max(),
        const.AGE_MIN: ages.min(),
        const.AGE_AVERAGE: ages.mean(),
        const.AGE_MEDIAN: ages.median(),
    }).fillna(0).round(const.ROUND_UPTO).to_json(output_path)
