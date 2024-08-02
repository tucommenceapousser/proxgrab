from flask import Flask, render_template, request, redirect, url_for, flash
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from secrets import choice as randchoice
from json import load
from datetime import datetime
from pytz import timezone
from PyRoxy import Proxy, ProxyChecker, ProxyType, ProxyUtiles
from requests import get, exceptions
from contextlib import suppress
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

__dir__ = Path(__file__).parent
SITE_URL = ""

with open(__dir__ / "config.json") as f:
    con = load(f)

class ProxyManager:

    @staticmethod
    def DownloadFromConfig(cf, Proxy_type: int):
        providrs = [
            provider for provider in cf["proxy-providers"]
            if provider["type"] == Proxy_type or Proxy_type == 0
        ]
        proxes = set()

        with ThreadPoolExecutor(len(providrs)) as executor:
            future_to_download = {
                executor.submit(
                    ProxyManager.download, provider,
                    ProxyType.stringToProxyType(str(provider["type"])))
                for provider in providrs
            }
            for future in as_completed(future_to_download):
                for pro in future.result():
                    proxes.add(pro)
        return proxes

    @staticmethod
    def download(provider, proxy_type: ProxyType):
        proxes = set()
        with suppress(TimeoutError, exceptions.ConnectionError,
                      exceptions.ReadTimeout):
            data = get(provider["url"], timeout=provider["timeout"]).text
            try:
                for proxy in ProxyUtiles.parseAllIPPort(
                        data.splitlines(), proxy_type):
                    proxes.add(proxy)
            except Exception as e:
                pass
        return proxes

def logTime():
    now_utc = datetime.now(timezone('UTC'))
    now_pacific = now_utc.astimezone(timezone("Asia/Jakarta"))
    return now_pacific.strftime("%H:%M:%S")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    global SITE_URL
    site_url = request.form.get('site_url')
    if not site_url:
        flash('Please enter a site URL.', 'error')
        return redirect(url_for('index'))

    SITE_URL = "https://" + site_url
    proxy_li = Path(__dir__ / "proxy.txt")

    if proxy_li.exists():
        os.unlink(proxy_li)

    flash(f"{logTime()} Downloading Proxies..", 'info')
    proxies = handleProxyList(con, proxy_li, 1)
    return render_template('results.html', proxies=proxies)

def handleProxyList(con, proxy_li, proxy_ty):
    if proxy_ty not in {4, 5, 1, 0, 6}:
        exit("Socks Type Not Found [4, 5, 1, 0, 6]")
    if proxy_ty == 6:
        proxy_ty = randchoice([4, 5, 1])
    if not proxy_li.exists():
        proxy_li.parent.mkdir(parents=True, exist_ok=True)
        with proxy_li.open("w") as wr:
            Proxies = ProxyManager.DownloadFromConfig(con, proxy_ty)
            Proxies = ProxyChecker.checkAll(Proxies, timeout=1, threads=200, url=SITE_URL)

            if not Proxies:
                exit("Proxy Check failed, Your network may be the problem")
            stringBuilder = ""
            for proxy in Proxies:
                stringBuilder += (proxy.__str__() + "\n")
            wr.write(stringBuilder)

    proxies = ProxyUtiles.readFromFile(proxy_li)
    return proxies

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)