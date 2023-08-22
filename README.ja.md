chromedriver-binary-sync
===

![Software Version](http://img.shields.io/badge/Version-v0.2.0-green.svg?style=flat)
[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)

[English Page](./README.md)

## 概要
実行時に chromedriver のバージョンをインストール済みの chrome のバージョンに同期する。  

- 実行時に chromedriver のバージョンを chrome に合わせてダウンロードする。  
- 内部で [chromedriver-binary-auto](https://pypi.org/project/chromedriver-binary-auto/) の機能を利用している。
    - こちらは、インストール時にバージョンを合わせる機能を持っている。

## Requirements
- chromedriver-binary-auto

## ライセンス
[MIT License](./LICENSE)

## 使用している OSS
- [python-chromedriver-binary](https://github.com/danielkaiser/python-chromedriver-binary)

## インストール
### pip
```
pip install chromedriver-binary-sync
```

### github
```
pip install git+https://github.com/bugph0bia/chromedriver-binary-sync.git
```

## 使用方法
```py
from selenium import webdriver
import chromedriver_binary_sync


# Download chromedriver to current directory.
# (Sync chromedriver version with the installed chrome version.)
chromedriver_binary_sync.download()

driver = webdriver.Chrome()
driver.get("http://www.python.org")
assert "Python" in driver.title
```

### 注意
chromedriver のパスは環境変数に自動追加されないため、カレントディレクトリ以外に chromedriver のダウンロード先にパスを通す必要がある。  

### カレントディレクトリ以外にダウンロードする場合
```py
chromedriver_binary_sync.download(download_dir='...')
```

### ポータブル版 Chrome のバージョンに合わせる場合 (Windows)
```py
chromedriver_binary_sync.download(chrome_portable=r'...\GoogleChromePortable\App\Chrome-bin\chrome.exe')
```
