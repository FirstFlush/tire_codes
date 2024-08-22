from typing import Any
from tire_codes.enums import TireCodeFormat, TireSpecsEnum
from tire_codes.exc import TireCodeParsingError
from tire_codes.parsing_methods import MetricParser, OffRoadParser
from tire_codes.regex import TireCodeRegex
from tire_codes.tire_specs import TireSpecs



class TireCodeParser:
    """
    A class to parse tire codes using regular expressions.

    Parameters:
    ----------
    tire_code : str
        Pass in the tire code you want to parse. 
        This can be in either metric `LT305/30ZR20 103Y` or off-road `35X12.50R17LT 121Q` format. 
    """

    def __init__(
            self,
            tire_code: str,
    ):
        self.tire_code = tire_code.upper().strip()
        self.format_enum = self._format_enum()


    def parse(self) -> TireSpecs:
        # '295/70R18 129/126Q'
        # '305/30ZR20 103Y'
        # '315/35R20 110W'
        # 'LT315/35R20 110W'
        # '35X12.50R17LT 121Q'
        # '40X15.5R20LT 128/125Q'

        match self.format_enum:
            case TireCodeFormat.METRIC:
                
                metric_parser = MetricParser(self.tire_code)
                width, aspect_ratio = metric_parser.width_and_aspect_ratio()
                speed_rating = metric_parser.speed_rating()
                construction = metric_parser.construction()
                wheel_diameter = metric_parser.wheel_diameter(construction)
                load_index = metric_parser.load_index()
                load_index_dual = metric_parser.load_index_dual()
                service_type = metric_parser.service_type(construction=construction, wheel_diameter=wheel_diameter)
                overall_diameter = None

            case TireCodeFormat.OFF_ROAD:
                offroad_parser = OffRoadParser(self.tire_code)
                overall_diameter, width = offroad_parser.overall_diamater_and_width()
                diameter_width_string = 'X'.join([overall_diameter, width])
                construction = offroad_parser.construction(diameter_width_string)
                wheel_diameter = offroad_parser.wheel_diameter(diameter_width_string, construction)
                service_type = offroad_parser.service_type()
                load_index = offroad_parser.load_index()
                load_index_dual = offroad_parser.load_index_dual()
                speed_rating = offroad_parser.speed_rating()
                aspect_ratio = None


        return TireSpecs(
            FORMAT=self.format_enum,
            WIDTH=width,
            SERVICE_TYPE=service_type,
            ASPECT_RATIO=aspect_ratio,
            OVERALL_DIAMETER=overall_diameter,
            CONSTRUCTION=construction,
            WHEEL_DIAMETER=wheel_diameter,
            LOAD_INDEX=load_index,
            LOAD_INDEX_DUAL=load_index_dual,
            SPEED_RATING=speed_rating,
        )


    def _speed_rating(self) -> str | None:
        speed_rating = ''
        for char in self.tire_code[::-1]:
            if char.isalpha():
                speed_rating += char
            else:
                break
        return ''.join([char for char in speed_rating[::-1]]) if speed_rating else None


    def _format_enum(self) -> TireCodeFormat:
        if TireCodeRegex.format_metric.search(self.tire_code):
            return TireCodeFormat.METRIC
        elif TireCodeRegex.format_off_road.search(self.tire_code):
            return TireCodeFormat.OFF_ROAD
        else:
            raise TireCodeParsingError(f"Could not parse tire code format for tire code `{self.tire_code}`")
        



if __name__ == '__main__':
    from tests.sample_codes import sample_codes 
   

    for code in sample_codes:
        if 'X' not in code:
            try:
                parser = TireCodeParser(code)
            except TireCodeParsingError as e:
                print('ERROR', code)
            else:
                # specs = parser.parse()
                # print(specs)
                # print(parser.tire_code)
                # print()
                ...