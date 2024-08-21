from tire_codes.enums import CodeFormat
from tire_codes.regex import TireCodeRegex
from tire_codes.tire_specs import TireSpecs


class TireCodeParsingError(Exception):
    """Raised when the tire code can not be successfully parsed."""
    pass


class TireCodeParser:
    """
    A class to parse tire codes using regular expressions.

    Parameters:
    ----------
    use_search : bool
        If True, use `re.Pattern.search()` instead of `re.Pattern.match()` for regex matching. Default is False.
    raise_exc : bool
        If True, raises an exception when no tire-code data is found by any of the regex patterns. Default is False.
    *args/**kwargs : 
        Optional parameters to pass to `re.Pattern.match()` or `re.Pattern.search()` methods.
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

        self.parse()



    def parse(self) -> TireSpecs:
        # '295/70R18 129/126Q'
        # '305/30ZR20 103Y'
        # '315/35R20 110W'
        # 'LT315/35R20 110W'
        # '35X12.50R17LT 121Q'
        width, aspect_ratio = self._width_and_aspect_ratio()
        speed_rating = self._speed_rating()
        construction = self._construction()
        wheel_diameter = self._wheel_diameter(construction)
        load_index = self._load_index(construction, wheel_diameter)
        load_index_dual = self._load_index_dual()
        service_type = self._service_type(construction, wheel_diameter)
        # print(service_type)

        if self.format_enum == CodeFormat.METRIC:

            TireSpecs(
                WIDTH=width,
                ASPECT_RATIO=aspect_ratio,
                CONSTRUCTION=construction,
                WHEEL_DIAMETER=wheel_diameter,
                LOAD_INDEX=load_index,
                LOAD_INDEX_DUAL=load_index_dual,
                SPEED_RATING=speed_rating,
                SERVICE_TYPE=service_type
            )




    def _service_type_start(self) -> str | None:
        service_type = ''
        removed_leading_alpha = self.tire_code_remove_leading_alpha
        if self.tire_code != removed_leading_alpha:
            for char in self.tire_code:
                if char.isalpha():
                    service_type += char
                else:
                    break
        return service_type

    def _service_type(self, construction:str, wheel_diameter:str) -> str | None:
        #TODO this function doesnt work yet
        service_type = self._service_type_start()
        if not service_type:
            substring = construction+wheel_diameter
            tire_code_slice = self.tire_code[self.tire_code.find(substring) + len(substring):]

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

    def _speed_rating(self) -> str | None:
        match = self.regex.metric_speed_rating.search(self.tire_code_remove_leading_alpha)
        if match:
            return match.group(0)


    def _construction(self) -> str:
        tire_code = self.tire_code_remove_leading_alpha
        start = None
        construction = None
        for i, char in enumerate(tire_code):
            if char.isdigit():
                if start is not None:
                    construction = tire_code[start:i]
                start = None
            elif char.isalpha():
                if start is None:
                    start = i
                    
        if not construction:
            raise TireCodeParsingError(f"Could not parse construction type for tire code `{self.tire_code}`")
        return construction

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




    def _width_and_aspect_ratio(self) -> tuple[str, str|None]:
        match self.format_enum:
            case CodeFormat.METRIC:
                match = self.regex.metric_width_aspect_ratio.search(self.tire_code_no_spaces)
            case CodeFormat.OFF_ROAD:
                match = None
        if match:
            return match.group(1), match.group(2)
        else:
            raise TireCodeParsingError(f"Could not parse width and/or aspect ratio for tire code `{self.tire_code}`")


    def _clean_split(self, sep:str, **kwargs) -> list[str]:
        return [code.strip() for code in self.tire_code.split(sep=sep **kwargs)]


    def _format_enum(self) -> CodeFormat:
        if self.regex.format_metric.search(self.tire_code):
            return CodeFormat.METRIC
        elif self.regex.format_off_road:
            return CodeFormat.OFF_ROAD
        else:
            raise TireCodeParsingError(f"Tire code{self.tire_code} can not be parsed")
        




if __name__ == '__main__':
    from tests.sample_codes import sample_codes 
   
    for code in sample_codes:
        if TireCodeRegex.format_metric.match(code):
            TireCodeParser(code)

    # parser = TireCodeParser('LT215/65R17 99T')