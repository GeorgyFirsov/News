# NewsParser

This module provides news parsing.

Entry point is `parse` function. Use module like this:
```python
import NewsParser.NewsParser as NewsParser
...
NewsParser.parse(driver_path, companies_file, news_directory)
```

This module contains NewsParser class that provides main task - parses news from www.investing.com. But this class is for internal usage only. Just call `parse` function to perform parsing.
