# News
[![Version][]][Repo] [![Implemented][]][Repo] [![Refactored][]][Repo] [![Coverage][]][Repo]

[Repo]:        https://github.com/GeorgyFirsov/News
[Version]:     https://img.shields.io/badge/Version-1.1-brightgreen
[Implemented]: https://img.shields.io/badge/Implemented-100%25-brightgreen
[Refactored]:  https://img.shields.io/badge/Refactored-100%25-brightgreen
[Coverage]:    https://img.shields.io/badge/Coverage-0%25-red

This program uses some machine learning technologies to predict increasing or decreasing of stocks in the nearest 2-3 days.

### Supported platforms:
- Windows
- Linux
- Mac OS X

### Authors
* [Georgy Firsov](https://github.com/GeorgyFirsov)
* [Egor Korekov](https://github.com/Kron610)
* [Irina Prokopenko](https://github.com/shybotan)

### Usage
* Make sure you have Python 3 (or higher) installed
* Clone repo onto your local machine (no matter running Windows or Linux)
* Run following command:
```bash
python ./Main.py
```
Or this one (to start flask server):
```bash
python ./FlaskServer.py
```

There should arise some errors. If not - that's it.
Otherwise run following commands:
```bash
pip install selenium
pip install user_agent
pip install pymorphy2
pip install xgboost
```
Maybe you can get some other import errors. To fix it install absent modules like above
