from .regex import TireCodeRegex


class TireCodeParsingError(Exception):
    """Raised when the tire code can not be successfully parsed."""
    pass


class TireSpecs:

    def __init__(self):
        self.SERVICE_TYPE        = None
        self.TIRE_WIDTH          = None
        self.ASPECT_RATIO        = None
        self.WHEEL_DIAMETER      = None
        self.OVERALL_DIAMETER    = None
        self.LOAD_INDEX          = None
        self.LOAD_INDEX_DUAL     = None
        self.SPEED_RATING        = None


class TireCodeParser:


    @property
    def specs_dict(self) -> dict:
        """If you prefer to have the specs as a dictionary instead of a different class."""
        d = {}
        for key, value in self.specs.__dict__.items():
            d[key] = value
        return d

    def __init__(self, tire_code:str):
        self.tire_code = tire_code
        self.regex = TireCodeRegex
        self.specs = TireSpecs()
        self._get_specs()


    def _get_specs(self):
        """Populates the TireSpecs class with the data found in the tire code"""
        tire_code = self.tire_code.upper().strip().replace('(','').replace(')','')
        if tire_code[0].isalpha():
            if tire_code[1].isalpha():
                service_type = tire_code[:2]
                tire_code = tire_code[2:]
            else:
                service_type = tire_code[0]
                tire_code = tire_code[1:]
        else:
            service_type = None

        match = self.regex.tire_code.match(tire_code)
        if match:
            print('match: ', match)
            self.specs.SERVICE_TYPE = service_type
            self.specs.TIRE_WIDTH = match.group(1)
            self.specs.ASPECT_RATIO = match.group(2)
            self.specs.WHEEL_DIAMETER = match.group(3)
            self.specs.LOAD_INDEX = match.group(4)
            self.specs.LOAD_INDEX_DUAL = match.group(5)
            self.specs.SPEED_RATING = match.group(6)
        else:
            match = self.regex.tire_code_2.match(tire_code)
            if match:
                print('match2: ', match)
                self.specs.TIRE_WIDTH = match.group(1)
                self.specs.ASPECT_RATIO = None
                self.specs.WHEEL_DIAMETER = match.group(3)
                self.specs.SERVICE_TYPE = match.group(4)
                self.specs.LOAD_INDEX = match.group(5)
                self.specs.LOAD_INDEX_DUAL = match.group(6)
                self.specs.SPEED_RATING = match.group(7)
            else:
                match = self.regex.tire_code_3.match(tire_code)
                if match:
                    print('match3: ', match)
                    self.specs.TIRE_WIDTH = match.group(1)
                    self.specs.ASPECT_RATIO = match.group(2)
                    self.specs.WHEEL_DIAMETER = match.group(3)
                    self.specs.SERVICE_TYPE = match.group(4)
                    self.specs.LOAD_INDEX = match.group(5)
                    self.specs.LOAD_INDEX_DUAL = match.group(6)
                    self.specs.SPEED_RATING = match.group(7)
                else:
                    match = self.regex.tire_code_offroad.match(tire_code)
                    if match:
                        print('match4: ', match)
                        width_inches = float(match.group(2))
                        self.specs.OVERALL_DIAMETER = match.group(1)
                        self.specs.ASPECT_RATIO = None
                        self.specs.TIRE_WIDTH = str(self.inch_to_mm(width_inches)) if width_inches <= 50 else str(width_inches)
                        self.specs.WHEEL_DIAMETER = match.group(4)
                        self.specs.SERVICE_TYPE = match.group(5)
                        self.specs.LOAD_INDEX = match.group(6)
                        self.specs.SPEED_RATING = match.group(7)
                    else:
                        match = self.regex.tire_code_reinf.match(tire_code)
                        if match:
                            print('match5: ', match)
                            self.specs.SERVICE_TYPE = service_type
                            self.specs.TIRE_WIDTH = match.group(1)
                            self.specs.ASPECT_RATIO = match.group(2)
                            self.specs.WHEEL_DIAMETER = match.group(3)
                            self.specs.LOAD_INDEX = None
                            self.specs. SPEED_RATING = None
                        else:
                            raise TireCodeParsingError(f"Can't parse tire code: '{tire_code}'")
        
