# StocksParser

This module provides stocks parsing.

Entry point is `parse` function. Use module like this:
```python
import StocksParser.StocksParser as StocksParser
...
StocksParser.parse(companies_file, stocks_directory)
```

This module contains StocksParser class that provides main task - parses stocks from www.finam.ru. But this class is for internal usage only. Just call `parse` function to perform parsing.

Name of file with parsed data is: Stocks\<TICKER>.csv
