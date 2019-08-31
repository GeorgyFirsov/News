# News
[![Version][]][Releases] [![Implemented][]][Repo] [![Refactored][]][Repo] [![Coverage][]][Repo] [![License][]][GPL License]

[Repo]:        https://github.com/GeorgyFirsov/News
[Releases]:    https://github.com/GeorgyFirsov/News/releases
[GPL License]: https://github.com/GeorgyFirsov/News/blob/master/LICENSE
[Version]:     https://img.shields.io/badge/Version-1.2-brightgreen
[Implemented]: https://img.shields.io/badge/Implemented-100%25-brightgreen
[Refactored]:  https://img.shields.io/badge/Refactored-100%25-brightgreen
[Coverage]:    https://img.shields.io/badge/Coverage-0%25-red
[License]:     https://img.shields.io/badge/License-GNU%20GPL%20v3-blue

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
That's it! Fell free to use according to [GPL License][].

### Generating a new predictor
Sometimes you may get Segmentation Fault error. Or maybe you have some other reasons to generate your own predictor.
You can do it by following instructions:

##### Windows
* Make sure you have jupyter notebook installed (you have, if you use Anaconda).
* Launch jupyter notebook via Anaconda Navigator (or somehow else).
* Run all cells in Learn.ipynb. You can rerun 'Training our predictor' section until you get accuracy you want (consider that you **cannot** get score above 90%!).
* Replace Predictor.pickle in data folder with newly generated one (it is located near Learn.ipynb).
##### Linux / Mac OS X
* Usually you have installed jupyter notebook, if you have Python installed. If not - install it.
* Run
```bash
jupyter notebook
```
* Look for Learn.ipynb.
* Run all cells. You can rerun 'Training our predictor' section until you get accuracy you want (consider that you **cannot** get score above 90%!).
* Replace Predictor.pickle in data folder with newly generated one (it is located near Learn.ipynb).

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
