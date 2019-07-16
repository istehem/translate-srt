from enum import Enum, unique

@unique
class Language(Enum):
    EN = 'en'
    DE = 'de'
    FR = 'fr'
    PT = 'pt'
    SV = 'sv'
    ES = 'es'

    def __str__(self):
        return str(self.value)
