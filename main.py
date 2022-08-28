import subprocess, glob, os, shutil, argparse, requests
from bs4 import BeautifulSoup

def download_from(url):
    print(f'Downloading {url}')
    cp = subprocess.run(['gallery-dl', url], encoding='utf-8')
    
    if cp.returncode != 0:
        print('[gallery-dl] Something went wrong.')
        return cp.returncode
    
    images = glob.glob('.\gallery-dl\**\*.*', recursive=True)
    
    try:
        os.mkdir('./images/')
    except FileExistsError:
        pass
    
    for image in images:
        try:
            shutil.move(image, './images/')
            print(f'Image moved: {image}')
        except shutil.Error:
            print(f'Image already exists: {image}')
    
    shutil.rmtree('./gallery-dl/')
    
    return 0

def main():
    parser = argparse.ArgumentParser(description='Download an image from a gallery')
    parser.add_argument('url', help='URL of the image')
    args = parser.parse_args()
    source_url = args.url
    
    if source_url.startswith('https://danbooru.donmai.us/'):
        html_text = requests.get(source_url).text
        soup = BeautifulSoup(html_text, 'html.parser')
        
        source = soup.find(id='post-info-source')
        source_link = source.find('a')
        
        if source_link is not None:
            temp_url = source_link['href']
            
            # pixiv
            if temp_url.startswith('https://www.pixiv.net/'):
                res = requests.get(temp_url)
                if res.status_code == 200:
                    source_url = temp_url
            # twitter
            elif temp_url.startswith('https://twitter.com/'):
                source_url = temp_url
    
    r = download_from(source_url)
    if r != 0:
        print('Retrying...')
        download_from(args.url)

if __name__ == '__main__':
    main()