class BaseCurrencyError(Exception):
    pass


class NotCurrencyOnDateError(BaseCurrencyError):
    pass


class WrongDateFormatError(BaseCurrencyError):
    pass
