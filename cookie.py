import os
import pickle
import requests

import requests
import time
import math
import random
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import json


load_dotenv()
timestamp = int(time.time() * 1000)
timestamp = round(timestamp / 1E3)

username = os.getenv("ACCOUNT")
if len(username) == 0:
    raise Exception("没有设置账号名")
password = os.getenv("PASSWORD")
if len(password) == 0:
    raise Exception("没有设置账户密码")


def get_TGC(cookies):
    headers = {
        'sec-ch-ua-platform': '"Windows"',
        'Referer': 'https://id.sspu.edu.cn/cas/login?service=https%3A%2F%2Foa.sspu.edu.cn%2Fsso%2Flogin.jsp%3FtargetUrl%3D%7Bbase64%7DL3d1aS9pbmRleC5odG1s',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
        'Accept': '*/*',
        'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
        'sec-ch-ua-mobile': '?0',
    }
    # ---------------------------------------------------------
    # 获取密码加密
    response = requests.get('https://id.sspu.edu.cn/cas/jwt/publicKey', headers=headers)
    publicKey = response.text
    import execjs

    # 读取 JS 文件
    with open("descripty.js", "r", encoding="utf-8") as f:
        js_code = f.read()

    ctx = execjs.compile(js_code)
    # 调用函数
    password_d = ctx.call("get_encoder", publicKey, password)
    # -----------------------------------------------------
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'If-Modified-Since': 'Tue, 12 Sep 2023 08:08:30 GMT',
        'If-None-Match': '"/Tmg39agQOM"',
        'Referer': 'https://oa.sspu.edu.cn/',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        # 'Cookie': 'loginfileweaver=%2Fmain.jsp',
    }

    response = requests.get('https://oa.sspu.edu.cn/sso/login.jsp?targetUrl=%2Fwui%2Findex.html', cookies=cookies,
                            headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    # 找到 name="execution" 的 input 标签
    execution_input = soup.find("input", {"name": "execution"})
    execution_value = None
    if execution_input:
        execution_value = execution_input.get("value")
    else:
        print("没有找到 execution")

    # ------------------------------------------------------
    # 获取cookies
    # 这个是密码验证后的cookies
    # -----------------------------------------------------
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://id.sspu.edu.cn',
        'Referer': 'https://id.sspu.edu.cn/cas/login?service=https%3A%2F%2Foa.sspu.edu.cn%2Fsso%2Flogin.jsp%3FtargetUrl%3D%7Bbase64%7DL3d1aS9pbmRleC5odG1s',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        # 'Cookie': 'SESSION=81f30445-688c-4647-b9fd-e17a0a20d0d4; Hm_lvt_d605d8df6bf5ca8a54fe078683196518=1760591301; HMACCOUNT=FD46A5E5BA43C522; Hm_lpvt_d605d8df6bf5ca8a54fe078683196518=1760592092',
    }

    params = {
        'service': 'https://oa.sspu.edu.cn/sso/login.jsp?targetUrl={base64}L3d1aS9pbmRleC5odG1s',
    }
    data = {
        'username': username,
        'password': password_d,
        'captcha': '',
        'currentMenu': '1',
        'failN': '0',
        'mfaState': '',
        "execution": execution_value,
        '_eventId': 'submit',
        'geolocation': '',
        'fpVisitorId': '2e522e86de47f2f8cb1e280bcbf27ac8',
        'submit1': 'Login1',
    }
    response = requests.post('https://id.sspu.edu.cn/cas/login', params=params, headers=headers, data=data,
                             cookies=cookies,
                             allow_redirects=False)

    return response.cookies.get_dict()


# 获取id网站的session
def get_session(cookies):
    cookies = {
        'Hm_lvt_d605d8df6bf5ca8a54fe078683196518': '1760518737',
        'Hm_lpvt_d605d8df6bf5ca8a54fe078683196518': '1760519495',
        'HMACCOUNT': '342411FA7A67FA48',
    }

    headers = {
        'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Referer': 'https://id.sspu.edu.cn/cas/login?service=https%3A%2F%2Foa.sspu.edu.cn%2Fsso%2Flogin.jsp%3FtargetUrl%3D%7Bbase64%7DL3d1aS9pbmRleC5odG1s',
        'Sec-Fetch-Dest': 'image',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        # 'Cookie': 'Hm_lvt_d605d8df6bf5ca8a54fe078683196518=1760518737; Hm_lpvt_d605d8df6bf5ca8a54fe078683196518=1760519495; HMACCOUNT=342411FA7A67FA48',
    }
    timestamp = int(time.time() * 1000)
    timestamp = str(timestamp) + str(math.floor(random.random() * 24))
    params = {
        'r': timestamp,
    }

    response = requests.get('https://id.sspu.edu.cn/cas/qr/qrcode', params=params, cookies=cookies, headers=headers)
    return response.cookies.get_dict()


# 获取id网站的HMACCOUNT值
def get_HMACCOUNT():
    import requests

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'If-None-Match': 'e8b53632a5a330cf51d11f88b235cb2b',
        'Referer': 'https://id.sspu.edu.cn/',
        'Sec-Fetch-Dest': 'script',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Storage-Access': 'active',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    response = requests.get('https://hm.baidu.com/hm.js?d605d8df6bf5ca8a54fe078683196518', headers=headers)
    return response.cookies.get_dict()


# 获取jx的session
def get_jsessionid():
    # --- 发起请求获取新的 cookie ---
    url = "https://jx.sspu.edu.cn/eams/login.action"
    session = requests.Session()
    response = session.get(url)

    if response.status_code == 200:
        print("[INFO] 已从服务器获取 JSESSIONID。")
        return session.cookies.get_dict()
    else:
        raise Exception(f"请求失败，状态码: {response.status_code}")


# 通过密码登录后，获取登录凭证和js的cookies绑定
def get_ticket():
    # 不知道有没有用，反正都逆向了
    cookies = {
        'Hm_lvt_d605d8df6bf5ca8a54fe078683196518': str(timestamp),
        'Hm_lpvt_d605d8df6bf5ca8a54fe078683196518': str(timestamp),
        'HMACCOUNT': get_HMACCOUNT()['HMACCOUNT'],
    }
    id_session = get_session(cookies)['SESSION']
    cookies['SESSION'] = id_session

    # ------------------------
    # TGC通过登录后返回的标志
    TGC = get_TGC(cookies)
    if 'TGC' not in TGC:
        raise Exception(f"账户登录失败，密码错误")
    cookies['TGC'] = TGC['TGC']

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Referer': 'https://oa.sspu.edu.cn/',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-site',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        # 'Cookie': 'SESSION=c08bd062-f1fc-437f-9d2d-3648b963d246; TGC=TGT-126084-GTxhg2xUdgAPHq1K6s886fHr6tvPajmCl5Yd1fJVXWg9SMIczRu51cAfowa9OGkLgkgcas-server-webapp-7c5c7fc659-2bv9w; Hm_lvt_d605d8df6bf5ca8a54fe078683196518=1759986638,1760022675,1760025508,1760091097; Hm_lpvt_d605d8df6bf5ca8a54fe078683196518=1760091097; HMACCOUNT=F0919804401AE860',
    }

    response = requests.get(
        'https://id.sspu.edu.cn/cas/login?service=https://jx.sspu.edu.cn/eams/login.action',
        cookies=cookies,
        headers=headers,
        allow_redirects=False
    )
    return response.headers.get('Location')


# 将登录的凭证和你的session绑定
def use_ticket(url, cookies):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Referer': 'https://oa.sspu.edu.cn/',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-site',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        # 'Cookie': 'Array_xuanke=web66; JSESSIONID=E63B76E5D9DB91F7B4CAF84904F719E1.-worker2; Array_xuanke=web66',
    }

    response = requests.get(url, cookies=cookies, headers=headers)
    return requests.utils.dict_from_cookiejar(response.cookies)


# 访问主页测试连通性
def test_connect(jx_cookie):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Referer': 'https://oa.sspu.edu.cn/',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    response = requests.get('https://jx.sspu.edu.cn/eams/home!index.action', cookies=jx_cookie, headers=headers)
    # execution是登录界面给的一个凭证
    return "execution" not in response.text


def get_jx_cookies():
    jx_cookies = load_cookies()
    if jx_cookies is None:
        jx_cookies = get_jsessionid()
        print("jx_cookies =", jx_cookies)
        ticket = get_ticket()
        print("jx_ticket =", ticket)
        jx_cookies = jx_cookies | use_ticket(ticket, jx_cookies)
        # jx_cookies = {
        #     'Array_xuanke': 'web66',
        #     'JSESSIONID': 'E63B76E5D9DB91F7B4CAF84904F719E1.-worker2',
        #     'Array_xuanke': 'web66',
        # }
        def save_cookies(cookies: dict, path="jx_cookies.json"):
            with open(path, "w", encoding="utf-8") as f:
                json.dump(cookies, f, ensure_ascii=False, indent=2)
            print(f"Cookies 已保存到 {path}")
        save_cookies(jx_cookies)
    if test_connect(jx_cookies):
        print("-------------------------连接成功 session建立成功-----------------------")
    else:
        if os.path.exists("jx_cookies.json"):
            os.remove("jx_cookies.json")
            print("文件已删除")
        print("文件已删除")
        raise Exception("连接建立出现错误")
    return jx_cookies


def load_cookies(path="jx_cookies.json") -> dict:
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        cookies = json.load(f)
    print(f"从 {path} 读取 {cookies}")
    return cookies


# 时间久了可以把js_cookies删除
if __name__ == "__main__":
    jx_cookies = get_jx_cookies()
