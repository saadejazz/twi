# twisearch

## Install

1. For dependencies:  
```bash
python -m pip install selenium bs4
```
2. Download the chromedriver from [here](https://chromedriver.chromium.org/downloads)
3. Open the file *twisearch.py* and set the variable EXECUTABLE_PATH to the path where the driver is downloaded.

## Code

```python
from twisearch import twitterSearch

results = twitterSearch("Pakistan News")
print(results)
```

## Ouput

```
[{'id': '18140095',
  'username': 'paknews',
  'name': 'Pakistan News',
  'media_directory': 'https://pbs.twimg.com/profile_images/1737791275/Flag-of-Pakistan-256_bigger.png'},
 {'id': '54246210',
  'username': 'NewsInsider',
  'name': 'Latest Pakistan News',
  'media_directory': 'https://pbs.twimg.com/profile_images/303756524/images_bigger.jpeg'},
 {'id': '480682661',
  'username': 'PakistanWeekly',
  'name': 'Pakistan Weekly News',
  'media_directory': 'https://pbs.twimg.com/profile_images/2341730932/8l4e9321u5tzme9a333s_bigger.jpeg'}]
```
