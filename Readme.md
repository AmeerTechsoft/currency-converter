# Currency Converter Lite

A lightweight, offline-ready Python library for currency conversion with support for caching exchange rates.

## Features

- Convert between any two currencies using Yahoo or Google Finance.
- Caches exchange rates for offline use.
- Simple and easy-to-use API.

## Installation

Install the library using pip:

```py
pip install currency-converter-lite
```
## Usage

``` py
from currency_converter.converter import CurrencyConverter

```

### Initialize converter

``` py
# using Yahoo finance

converter = CurrencyConverter(use_yahoo=True)

```

``` py
# using Google finance

converter = CurrencyConverter(use_yahoo=False)

```

### Convert 100 USD to EUR

``` py
amount_in_eur = converter.convert(100, "USD", "EUR")
print(f"100 USD is {amount_in_eur} EUR")

```
## License
This project is licensed under the MIT License.


Copyright (c) 2024 Ameer Adeigbe

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions: ...