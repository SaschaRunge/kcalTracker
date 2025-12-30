import datetime

class Parser():
    @staticmethod
    def clean_string(string):
        if not string:
            return "0" #TODO probably should return None with subsequent clean up
        return string.translate(str.maketrans(',', '.', ' "!@#$'))
    
    @staticmethod
    def parse_int(string):
        return int(Parser.clean_string(string))

    @staticmethod
    def parse_float(string):
        return float(Parser.clean_string(string))
    
    @staticmethod
    def parse_date(string):
        try:
            return datetime.date.fromisoformat(string)
        except ValueError as e:
            raise NotImplementedError(f"TODO: Handle failed string to date conversion in Parser.parse_date: {e}")


    