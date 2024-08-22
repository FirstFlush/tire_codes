from tire_codes.exc import TireCodeParsingError

class BaseParsingMethods:

    def __init__(self, tire_code:str):
        self.tire_code = tire_code

    @staticmethod
    def extract_alpha(s:str,reverse: bool = False) -> str:
        """Extracts a contiguous sequence of alphabetic characters from the start of a string."""
        if reverse:
            s = s[::-1]
        alpha_str = ''
        for char in s:
            if char.isalpha():
                alpha_str += char
            else:
                break
        return alpha_str[::-1] if reverse else alpha_str

    @staticmethod
    def extract_digits(s:str, reverse: bool = False) -> str:
        """Extracts a contiguous sequence of digits from the start of a string."""
        if reverse:
            s = s[::-1]
        digit_str = ''
        for char in s:
            if char.isdigit():
                digit_str += char
            else:
                break
        return digit_str[::-1] if reverse else digit_str
    

    @staticmethod
    def slice_after_substring(s:str, substring: str) -> str:
        """Returns the portion of the string after a given substring."""
        return s[s.find(substring) + len(substring):]
    

    def speed_rating(self) -> str | None:

        s = self.tire_code.replace('REINF', '').strip()
        speed_rating = self.extract_alpha(s, reverse=True)
        return speed_rating if speed_rating else None




class MetricParser(BaseParsingMethods):

    ...



class OffRoadParser(BaseParsingMethods):

    def overall_diamater_and_width(self) -> tuple[str, str]:
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


    def wheel_diameter(self, diameter_width_string:str, construction:str) -> str:
        """Param diameter_width_string will be in the format of '37x13.5'"""
        substring = diameter_width_string+construction
        sliced_tire_code = self.slice_after_substring(self.tire_code, substring)
        wheel_diameter = self.extract_digits(sliced_tire_code)
        if not wheel_diameter:
            raise TireCodeParsingError(f"Could not parse wheel diameter for tire code `{self.tire_code}`")
        return wheel_diameter


    def construction(self, diameter_width_string:str) -> str:

        sliced_tire_code = self.slice_after_substring(s=self.tire_code, substring=diameter_width_string)
        construction = self.extract_alpha(s=sliced_tire_code)
        if not construction:
            raise TireCodeParsingError(f"Could not parse construction type for tire code `{self.tire_code}`")

        return construction



    def load_index(self) -> str | None:
        split_string = self.tire_code.split(' ')[-1]
        load_index = self.extract_digits(s=split_string)
        return load_index if load_index else None



    def load_index_dual(self) -> str | None:
        load_index_dual = None
        split_string = self.tire_code.split(' ')[-1]
        dual_string = split_string.split('/')[-1]
        if split_string != dual_string:
            load_index_dual = self.extract_digits(dual_string)
        return load_index_dual


    def service_type(self) -> str | None:
        service_type = ''
        for char in self.tire_code.split(' ')[0][::-1]:
            if char.isalpha():
                service_type += char
            else: break
        if service_type:
            return ''.join([char for char in service_type[::-1]])


