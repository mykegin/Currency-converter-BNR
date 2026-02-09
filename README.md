# Currency Converter (BNR)

A desktop currency converter built with Python and Tkinter that uses official exchange rates from the National Bank of Romania (BNR).  
The application fetches daily FX rates, caches them locally, and performs conversions between currencies using RON as a pivot.  
It works both online and offline, falling back to cached data when needed.

---

## Features

- Fetches official daily exchange rates from BNR (XML).
- Normalizes rates to an internal map `{currency: RON_per_unit}` including RON.
- Local JSON cache with 24-hour validity.
- Automatic reuse of cached rates to minimize network requests.
- Offline mode with a clear banner when using cached data.
- Accurate currency conversion using RON as a pivot.
- Supports all BNR-published currencies plus RON.
- Conversion results rounded to 4 decimals.
- Responsive GUI built with Tkinter using background threads for fetching rates.

---
