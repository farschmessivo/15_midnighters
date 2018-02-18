import requests
import pytz
import datetime
from collections import Counter


def load_api_data(page_number):
    params = {'page': page_number}
    raw_data_response = requests.get(
        'http://devman.org/api/challenges/solution_attempts/',
        params
    )
    json_data = raw_data_response.json()
    return json_data


def load_solution_attempts(data_loader):
    page = 1
    while True:
        json_data = data_loader(page)
        for attempt in json_data['records']:
            yield attempt
        page += 1
        if page > json_data['number_of_pages']:
            break


def get_midnighters_top_list(midnight_attempts_usernames):
    midnighters_top_list = Counter(midnight_attempts_usernames).most_common()
    return midnighters_top_list


def is_midnight_attempt(attempt, night_start, night_end):
    local_timezone = pytz.timezone(attempt['timezone'])
    attempt_localized_datetime = datetime.datetime.fromtimestamp(
        attempt['timestamp'],
        local_timezone
    )
    local_time = attempt_localized_datetime.time()

    return night_start <= local_time.hour < night_end


def get_filtered_attempts_usernames(solution_attempts, filter_by_time_range):
    filtered_usernames = [
        attempt['username'] for attempt in solution_attempts
        if filter_by_time_range(attempt, 0, 4)
    ]
    return filtered_usernames


def print_to_console(midnighters_top_list):
    print('Midnighters Top List:')
    for index, (username, num_of_midnight_attempts) in enumerate(
            midnighters_top_list, 1):
        print('{}. {} made {} midnight attempts.'.format(
            index,
            username,
            num_of_midnight_attempts)
        )


if __name__ == '__main__':
    solution_attempts_list = load_solution_attempts(load_api_data)
    midnight_attempts_usernames = get_filtered_attempts_usernames(
        solution_attempts_list, is_midnight_attempt)
    midnighters_top_list = get_midnighters_top_list(
        midnight_attempts_usernames)
    print_to_console(midnighters_top_list)
