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

    @property
    def tire_code_no_spaces(self) -> str:
        return ''.join([char for char in self.tire_code.split() if char != ' '])

    @property
    def tire_code_remove_leading_alpha(self) -> str:
        if self.tire_code[0].isalpha():
            for i, char in enumerate(self.tire_code):
                if not char.isalpha():
                    return self.tire_code[i:]
        return self.tire_code

    def __init__(
            self,
            tire_code: str,
    ):
        self.tire_code = tire_code.upper().strip()
        self.regex = TireCodeRegex
        self.format_enum = self._format_enum()
        # self.parse()


    def parse(self) -> TireSpecs:
        # '295/70R18 129/126Q'
        # '305/30ZR20 103Y'
        # '315/35R20 110W'
        # 'LT315/35R20 110W'
        # '35X12.50R17LT 121Q'
        # '40X15.5R20LT 128/125Q'

        match self.format_enum:
            case TireCodeFormat.METRIC:
                width, aspect_ratio = self._width_and_aspect_ratio_metric()
                
                print(MetricParser(self.tire_code).speed_rating())

                speed_rating = self._speed_rating()
                construction = self._construction()
                wheel_diameter = self._wheel_diameter(construction)
                load_index = self._load_index(construction, wheel_diameter)
                load_index_dual = self._load_index_dual()
                service_type = self._service_type(construction, wheel_diameter)
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
                # overall_diameter, width = self._overall_diamater_and_width()
                # diameter_width_string = 'X'.join([overall_diameter, width])
                # construction = self._construction_off_road(diameter_width_string)
                # wheel_diameter = self._wheel_diameter_off_road(diameter_width_string, construction)
                # service_type = self._service_type_offroad()
                # load_index = self._load_index_offroad()
                # load_index_dual = self._load_index_dual_offroad()
                # speed_rating = self._speed_rating()
                # aspect_ratio = None

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


    def _load_index_offroad(self) -> str | None:
        load_index = ''
        split_string = self.tire_code.split(' ')[-1]
        for char in split_string:
            if char.isdigit():
                load_index += char
            else:
                break
        return load_index if load_index else None


    def _load_index_dual_offroad(self) -> str | None:
        load_index_dual = ''
        split_string = self.tire_code.split(' ')[-1]
        dual_string = split_string.split('/')[-1]

        if split_string != dual_string:
            for char in dual_string:
                if char.isdigit():
                    load_index_dual += char
                else:
                    break
        return load_index_dual if load_index_dual else None


    def _service_type_offroad(self) -> str | None:
        service_type = ''
        for char in self.tire_code.split(' ')[0][::-1]:
            if char.isalpha():
                service_type += char
            else: break
        if service_type:
            return ''.join([char for char in service_type[::-1]])



    def _slice_tire_code(self, substring:str) -> str:
        return self.tire_code[self.tire_code.find(substring) + len(substring):]


    def _wheel_diameter_off_road(self, diameter_width_string:str, construction:str) -> str:
        s = diameter_width_string+construction
        sliced_tire_code = self._slice_tire_code(s)
        wheel_diameter = ''
        for char in sliced_tire_code:
            if char.isdigit():
                wheel_diameter += char
            else:
                break
        if not wheel_diameter:
            raise TireCodeParsingError(f"Could not parse wheel diameter for tire code `{self.tire_code}`")
        return wheel_diameter


    def _construction_off_road(self, diameter_width_string:str) -> str:
        construction = ''
        sliced_tire_code = self._slice_tire_code(diameter_width_string)
        for char in sliced_tire_code:
            if char.isalpha():
                construction += char
            else:
                break
        if not construction:
            raise TireCodeParsingError(f"Could not parse construction type for tire code `{self.tire_code}`")

        return construction





    def _service_type_start(self) -> str | None:
        """If the service type is at the start of the string"""
        service_type = ''
        if self.tire_code != self.tire_code_remove_leading_alpha:

            for char in self.tire_code:
                if char.isalpha():
                    service_type += char
                else:
                    break

        return service_type if service_type else None


    def _service_type(self, construction:str, wheel_diameter:str) -> str | None:

        service_type = self._service_type_start()
        if not service_type:
            service_type = ''
            substring = construction + wheel_diameter
            tire_code_slice = self.tire_code[self.tire_code.find(substring) + len(substring):]
            for char in tire_code_slice:
                if char.isalpha():
                    service_type += char
                else:
                    break

        return service_type if service_type else None


    def _load_index_dual(self) -> str | None:
        load_index_dual = ''
        is_dual = False
        for char in self.tire_code[::-1]:
            if char.isdigit():
                load_index_dual += char
            elif char == '/':
                is_dual = True
                break
            elif char == ' ':
                break
        if load_index_dual and is_dual:
            return load_index_dual[::-1]
        return None

    def _load_index(self, construction:str, wheel_diameter:str) -> str | None:
        load_index = ''
        substring = construction+wheel_diameter
        sliced_code = self.tire_code[self.tire_code.find(substring) + len(substring):]
        for char in sliced_code:
            if char.isdigit():
                load_index += char
            elif char == '/':
                break
        return load_index if load_index else None


    def _construction(self) -> str:
        match = self.regex.metric_construction.search(self.tire_code)
        if match:
            return match.group(0)
        else:
            raise TireCodeParsingError(f"Could not parse construction type for tire code `{self.tire_code}`")


    def _wheel_diameter(self, construction:str) -> str:

        wheel_diameter = ''
        tire_code = self.tire_code_remove_leading_alpha
        sliced_tire_code = tire_code[tire_code.find(construction):].replace(construction, '', 1)

        for char in sliced_tire_code:
            if char.isdigit():
                wheel_diameter += char
            else:
                break
        if not wheel_diameter:
            raise TireCodeParsingError(f"Could not parse wheel diameter for tire code `{self.tire_code}`, `{sliced_tire_code}`")
        return wheel_diameter



    def _overall_diamater_and_width(self) -> tuple[str, str]:
        width_aspect_string = ''
        for char in self.tire_code:
            if char.isdigit() or char == '.' or char == 'X':
                width_aspect_string += char
            else:
                break
        width_aspect_list = width_aspect_string.split('X')
        if len(width_aspect_list) != 2:
            raise TireCodeParsingError(f"Could not parse width and/or aspect ratio for tire code `{self.tire_code}`")

        return tuple(width_aspect_list)


    def _width_and_aspect_ratio_metric(self) -> tuple[str, str|None]:
        match = self.regex.metric_width_aspect_ratio.search(self.tire_code_no_spaces)
        if match:
            try:
                return match.group(1), match.group(2)
            except (IndexError):
                pass
        raise TireCodeParsingError(f"Could not parse width and/or aspect ratio for tire code `{self.tire_code}`")


    def _format_enum(self) -> TireCodeFormat:
        if self.regex.format_metric.search(self.tire_code):
            return TireCodeFormat.METRIC
        elif self.regex.format_off_road.search(self.tire_code):
            return TireCodeFormat.OFF_ROAD
        else:
            raise TireCodeParsingError(f"Could not parse tire code format for tire code `{self.tire_code}`")
        



if __name__ == '__main__':
    from tests.sample_codes import sample_codes 
   

    for code in sample_codes:
        if 'X' in code:
            try:
                parser = TireCodeParser(code)
            except TireCodeParsingError as e:
                print('ERROR', code)
            else:
                specs = parser.parse()
                print(specs)
                print(parser.tire_code)
                print()