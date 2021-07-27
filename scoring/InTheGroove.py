def rate(offset: int, judge: dict[int, str]) -> str:
    """
    rates a single hit based on a judge
    :param offset: the hit
    :param judge: the scoring system
    :return: the rate
    """
    delta = abs(offset)
    result = ""
    for window in reversed(judge):
        if delta <= window:
            result = judge[window]
            continue
    return result


def calc_dp(tally: dict[str, int]) -> int:
    """
    calculates the dance points based on itg scoring
    :param tally: the current tally
    :return: dance points
    """
    points = tally["MA"] * 5
    points += tally["PF"] * 4
    points += tally["GR"] * 2
    points += tally["GD"] * 0
    points -= tally["BA"] * 6
    points -= tally["MISS"] * 12
    return points


def max_dp(hit_count: int, misses: int) -> int:
    """
    calculates the maximum amount of dance points (if all hits were MA)
    :param hit_count: the number of hits so far
    :param misses: the number of misses so far
    :return: current maximum dance points
    """
    return (hit_count + misses) * 5


def get_hit_count(tally: dict[str, int]) -> int:
    """
    gets the hit count from a tally
    :param tally: the tally
    :return: the hit count
    """
    return tally["MA"] + tally["PF"] + tally["GR"] + tally["GD"] + tally["BA"]


def get_acc(tally: dict[str, int]) -> float:
    """
    calculates accuracy based on the current tally
    :param tally: the tally
    :return: the accuracy
    """
    if get_hit_count(tally) == 0:
        return 0
    else:
        return (calc_dp(tally) / max_dp(get_hit_count(tally), tally["MISS"])) * 100
