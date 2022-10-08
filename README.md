chromedriver-binary-sync
===

![Software Version](http://img.shields.io/badge/Version-v0.1.0-green.svg?style=flat)
[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)

[Japanese Page](./README.ja.md)

## Overview
Sync chromedriver version with the installed chrome version at runtime.  

- Download the version of chromedriver to match chrome at runtime.  
- Internally, the function of [chromedriver-binary-auto](https://pypi.org/project/chromedriver-binary-auto/) is used.
    - It matches the version at install time.

## Requirements
- chromedriver-binary-auto

## License
[MIT License](./LICENSE)

## OSS used
- [python-chromedriver-binary](https://github.com/danielkaiser/python-chromedriver-binary)

## Installation
### pip
```
pip install chromedriver-binary-sync
```

### github
```
pip install git+https://github.com/bugph0bia/chromedriver-binary-sync.git
```

## Usage
```py
from selenium import webdriver
import chromedriver_binary_sync


# Download chromedriver to current directory.
# (chromedriver version matches installed chrome)
chromedriver_binary_sync.download()

driver = webdriver.Chrome()
driver.get("http://www.python.org")
assert "Python" in driver.title
```

### Note
The path to chromedriver is not automatically added to the "PATH" environment variable, so it is necessary to pass the path to the chromedriver download destination in addition to the current directory.  

### Case: Download to other than the current directory
```py
chromedriver_binary_sync.download(download_dir='...')
```

### Case: To match a portable version of Chrome (For Windows)
```py
chromedriver_binary_sync.download(chrome_portable=r'...\GoogleChromePortable\App\Chrome-bin\chrome.exe')
```

