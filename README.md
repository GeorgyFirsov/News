# News
[![Version][]][Repo] [![Implemented][]][Repo] [![Refactored][]][Repo] [![Coverage][]][Repo]

[Repo]:        https://github.com/GeorgyFirsov/News
[MIT License]: https://github.com/GeorgyFirsov/News/blob/master/LICENSE
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

### Installation guide
* Make sure you have Python 3 (or higher) installed
* Run following commands in your terminal:
```bash
cd installation_directory
git clone https://github.com/GeorgyFirsov/News.git
cd News
pip install selenium
pip install user_agent
pip install pymorphy2
pip install xgboost
pip install numpy
pip install scipy
pip install pandas
pip install flask
pip install string
pip install datetime
pip install unicodecsv
pip install scikit-learn
```
Or you can create \*.sh or \*.bat script, paste this code there and run it (it is a bit easier).
* Try to run program by following code
```bash
python ./Main.py
```
If something else is not installed, just install it :)

### Running
* Run following command:
```bash
python ./Main.py
```
Or this one (to start flask server):
```bash
python ./FlaskServer.py
```
That's it! Fell free to use according to [MIT License][].

### Contributing

Feel free to contribute! We are happy to work with you :)

> 👉 **Note**: All the pull-requests will be strictly checked and reviewed before being accepted or declined. All external pull-requests have the same scrutiny for quality, coding standards, performance, globalization, accessibility, and compatibility as those of our internal contributors.

> ⚠ **Attention\!** If you don't follow code guidelines, your pull-request will be declined anyway. Carefully read PEP conventions. It is highly required to make our code cleaner and more understandable.

How to make contributions:
* Fork this repo
* Clone YOUR own repository onto your computer
* Make changes you want
* Push your changes to your repository
* Make PR
* We will examine your PR and merge or decline it
