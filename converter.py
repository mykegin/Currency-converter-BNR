from typing import Dict

class ConversionError(Exception):
    pass

def convert(amount: float, from_currency: str, to_currency: str, rates: Dict[str, float]) -> float:
    if not isinstance(amount, (int, float)):
        raise ConversionError("Amount must be numeric")

    if amount <= 0:
        raise ConversionError("Amount must be greater than zero")

    from_currency = from_currency.upper()
    to_currency = to_currency.upper()

    if from_currency not in rates:
        raise ConversionError(f"Unknown currency: {from_currency}")

    if to_currency not in rates:
        raise ConversionError(f"Unknown currency: {to_currency}")

    amount_in_ron = amount * rates[from_currency]
    result = amount_in_ron / rates[to_currency]

    return round(result, 4)
