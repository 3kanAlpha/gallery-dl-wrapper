# gallery-dl-wrapper
自分用のgallery-dlのラッパー

## Requirements
- [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [gallery-dl](https://github.com/mikf/gallery-dl)

## How to build a package
```sh
$ git clone https://github.com/3kanAlpha/gallery-dl-wrapper.git
$ cd gallery-dl-wrapper
$ pip install -e .
```

## Usage
URLを渡すだけ
```sh
$ gdw [URL]
```
カレントディレクトリ内に```images```というディレクトリが生成され画像が保存される。