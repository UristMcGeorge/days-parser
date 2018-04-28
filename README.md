# Days parser
Test data parser project for Sainsbury's.

## How to use this
Import the module, that's it. There is no installation, just copy-paste the directory tree somewhere. The are no prerequisites either, everything is standard library. Tested on CPython 3.6.4. Please, bear in mind that CPython 3.6+ and Python 3.7+ dicts are ordered.

Example:
```python
from days_parser.days_parser import DaysParser
parser = DaysParser('tests/1.csv')
parser.print_parsed()
```

## How to run the tests
python -m unittest

## Author
George Georgiev - eorg@mail.bg

## License
This project is licensed under GPLv3 - see the [LICENSE.txt](LICENSE.txt) file for details

## Acknowledgments
[https://www.youtube.com/watch?v=7_JUBgPHYmY](https://www.youtube.com/watch?v=7_JUBgPHYmY)
