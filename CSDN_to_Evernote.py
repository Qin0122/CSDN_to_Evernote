from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import pyautogui


class CSDN(object):
    def __init__(self):
        # 实例化driver对象
        self.driver = webdriver.Chrome()

    def login(self):
        self.driver.get('https://mp.csdn.net/mp_blog/manage/article?')

        # 获取保存下的cookie值
        with open('csdn_cookies.txt', 'r', encoding='utf8') as f:
            listCookies = json.loads(f.read())

        # 往browser里添加cookies
        for cookie in listCookies:
            cookie_dict = {
                'domain': '.csdn.net',
                'name': cookie.get('name'),
                'value': cookie.get('value'),
                "expires": '',
                'path': '/',
                'httpOnly': False,
                'HostOnly': False,
                'Secure': False
            }
            self.driver.add_cookie(cookie_dict)

        self.driver.refresh()  # 刷新网页,cookies才成功

        # 等待内容管理加载完毕后点击
        WebDriverWait(self.driver, 1000).until(
            EC.presence_of_element_located((By.XPATH, '//ul[@role="menu"]/li/a[text()="内容管理"]'))
        )
        # 点击内容管理
        self.driver.find_element(By.XPATH, '//ul[@role="menu"]/li/a[text()="内容管理"]').click()

    # 分析网页
    def parse_page(self):
        """
        用户选择好分栏并点击后，输入1，程序继续运行
        :return:
        """
        print('\n请确认是否已选择专栏，点击搜索……')

        user1 = input('确认无误后请输入1，进行下一步操作……：')

        # 等待文章url加载
        WebDriverWait(self.driver, 1000).until(
            EC.presence_of_element_located((By.XPATH, '//p[@class="article-list-item-txt"]/a'))
        )
        time.sleep(2)

        # 用try来进行下一页的搜索
        page_urls = [] # 存储文章url
        while True:
            try:
                # 先添加文章url和文章标签
                page_urls += [ele.get_attribute('href') for ele in self.driver.find_elements(By.XPATH, '//p[@class="article-list-item-txt"]/a')]
                # 点击下一页
                self.driver.find_element(By.XPATH, '//*[@id="view-containe"]/div/div/div[4]/div/button[2]').click()
                time.sleep(3)
            except:
                break

        # 调用修改文章为粉丝可见的函数
        self.change_fans(page_urls)

    # 获取文章的url并点击，修改文章为粉丝可见
    def change_fans(self, page_urls):
        for page_url in page_urls:
            self.driver.get(page_url)

            time.sleep(3)
            try:
                # 点击发布博客
                button = self.driver.find_element(By.XPATH, '//div[@id="moreDiv"]/div[10]/div/div/div[2]/button')
                if button.is_enabled():
                    continue
            except:
                self.move()

    # 将CSDN中的文章转移到印象笔记
    def move(self):
        # 点击CSDN标题
        r = None
        while r is None:
            r = pyautogui.locateOnScreen('./photo/1.png')
        x, y = pyautogui.center(r)
        pyautogui.doubleClick(x, y)
        pyautogui.leftClick(x, y)

        # 复制标题
        pyautogui.hotkey('ctrl', 'c')

        # 点击印象笔记的更多新建
        r = None
        while r is None:
            r = pyautogui.locateOnScreen('./photo/2.png')
        x, y = pyautogui.center(r)
        pyautogui.leftClick(x, y)

        # 点击Markdown编辑
        r = None
        while r is None:
            r = pyautogui.locateOnScreen('./photo/3.png')
        x, y = pyautogui.center(r)
        pyautogui.leftClick(x, y)

        # 点击标题
        time.sleep(1)
        r = None
        while r is None:
            r = pyautogui.locateOnScreen('./photo/4.png')
        x, y = pyautogui.center(r)
        pyautogui.doubleClick(x, y)

        # 粘贴复制的文本
        pyautogui.hotkey('ctrl', 'v')

        # 点击CSDN文章的目录
        r = None
        while r is None:
            r = pyautogui.locateOnScreen('./photo/5.png')
        x, y = pyautogui.center(r)
        pyautogui.doubleClick(x, y)

        # 按下alt + a
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.hotkey('ctrl', 'c')

        # 点击印象笔记的空白处
        r = None
        while r is None:
            r = pyautogui.locateOnScreen('./photo/6.png')
        x, y = pyautogui.center(r)
        pyautogui.leftClick(x, y)

        # 粘贴
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(1)
        # 点击打叉印象笔记窗口
        r = None
        while r is None:
            r = pyautogui.locateOnScreen('./photo/7.png')
        x, y = pyautogui.center(r)
        pyautogui.leftClick(x, y)


    # 文章移动
    def run(self):
        user = int(input('请输入专栏的数目：'))
        self.login()
        for i in range(user):
            self.parse_page()

csdn = CSDN()
csdn.run()



