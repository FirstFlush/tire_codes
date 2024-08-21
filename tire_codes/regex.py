import re


class TireCodeRegex:
    format_metric = re.compile(r'\d+\s*/')
    format_off_road = re.compile(r'\d+\s*X')
    # service_type_start = re.compile(r'^[A-Za-z]+')

    metric_width_aspect_ratio = re.compile(r'(\d+)/(\d+)')
    metric_speed_rating = re.compile(r'(?<!\s)([A-Za-z]+)\b')
    # metric_construction = re.compile(r'(?<=\d)[A-Za-z]+(?=\d)') # untested