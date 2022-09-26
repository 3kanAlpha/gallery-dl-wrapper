import subprocess, glob, os, shutil, argparse, requests
from bs4 import BeautifulSoup

OUTPUT_DIR = '.\\'

def download_from(url, output_dir=OUTPUT_DIR):
    print(f'Downloading {url}')
    cp = subprocess.run(['gallery-dl', url], encoding='utf-8')
    
    if cp.returncode != 0:
        print('[gallery-dl] Something went wrong.')
        return cp.returncode
    
    images = glob.glob('.\gallery-dl\**\*.*', recursive=True)
    
    if output_dir != OUTPUT_DIR:
        os.makedirs(output_dir, exist_ok=True)
    
    for image in images:
        try:
            shutil.move(image, output_dir)
            print(f'Image moved: {image}')
        except shutil.Error:
            print(f'Image already exists: {image}')
    
    shutil.rmtree('./gallery-dl/')
    
    return 0

def main():
    parser = argparse.ArgumentParser(description='Download an image from a gallery')
    parser.add_argument('url', help='URL of the image')
    parser.add_argument('-f', '--force', help='force wrapper to download image from given URL', action='store_true')
    parser.add_argument('-o', '--output-dir', help='output directory', default=OUTPUT_DIR)
    args = parser.parse_args()
    source_url = args.url
    
    if not args.force and source_url.startswith('https://danbooru.donmai.us/'):
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
    
    if source_url.startswith('https://twitter.com/'):
        # remove the query params
        if source_url.find('?') != -1:
            source_url = source_url[:source_url.find('?')]
    
    r = download_from(source_url, args.output_dir)
    if r != 0:
        print('Retrying...')
        download_from(args.url, args.output_dir)

if __name__ == '__main__':
    main()