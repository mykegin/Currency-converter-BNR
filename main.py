from bnr_rates import get_rates
from converter import convert, ConversionError

data = get_rates()
rates = data["rates"]

try:
    print(convert(100, "EUR", "RON", rates))
except ConversionError as e:
    print("Conversion error:", e)
