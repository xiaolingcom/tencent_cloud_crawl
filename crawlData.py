from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


# 环境设置:
#     一、使用pip安装selenium==3.11.0版本
#     二、在python中测试以下代码,若无报错则表示selenium+webdriver的环境搞定了，
#     browser = webdriver.Chrome()
#     browser.get('http://www.baidu.com')
#     time.sleep(5) -5表示等待的秒数
#     否则要在指定的网址去下载对应的webdriver，解压后有一个webdriver.exe
#     将webdriver.exe拷贝到python3.7和Chrome根目录下（我的是D:\axiaoling\python37和C:\Program Files (x86)\Google\Chrome\Application）
    # 然后测试上面的代码的代码，没有报错则成功
    #XXXXXXXXXXXXXXXXXXXX不用做这步操作！！！！三、下载PhantomJS，俗称无界面的浏览器XXXXXXXXXXXXXXXXXXXXXX(这个已经弃用了！！！用Chrome()或则和Firefox()代替，而且速度快很多)
    #XXXXXXXXXXXXXXXXXXXX下载地址https://phantomjs.org/download.html 打个叉
    
    
class tencent_cloud:
    def __init__(self,url,username,password):
        #参数设置
        self.url = url
        self.username=username
        self.password=password

    
    def crawl(self):
        #/////////////////////首先登入网站//////////////////////////////////
        #使用webkit无界面浏览器
        ##如果路径为 exe 启动程序的路径，那么该路径需要加一个 r
        # self.driver=webdriver.PhantomJS(executable_path=r'./phantomjs.exe')
        self.driver=webdriver.Chrome()
        self.driver.set_window_size(1920,1080) #设置为屏幕分辨率
        self.driver.get(self.url)
        self.driver.save_screenshot('0-打开页面.png')#/////////////截图保存1.png
        print('load succeed!')
        try:
            self.driver.find_element_by_xpath('//a[@data-type="qq"]').click()
            # # with open('./page_source.txt', 'w',encoding='utf-8') as f:  #发现开始找不到'switcher_plogin'，是因为这部分代码放到了#document下
            # #     f.write(self.driver.page_source)
            iframe=self.driver.find_element_by_xpath('//iframe[@id="ptlogin_iframe"]')
            self.driver.switch_to_frame(iframe)#跳转到iframe
            self.driver.find_element_by_xpath('//a[@id="switcher_plogin"]').click()
            self.driver.save_screenshot('1-QQ登录页面.png')#////////////截图保存2.png
           
            self.driver.find_element_by_xpath('//input[@id="u"]').send_keys(self.username) #这里不用跳转了，!!!iframe没有改变!!!,我被搞疯了
            self.driver.find_element_by_xpath('//input[@id="p"]').send_keys(self.password)
            self.driver.find_element_by_xpath('//input[@id="login_button"]').click()
            time.sleep(15)
            print('login & jump to the target page!')
            self.driver.save_screenshot('2-登录成功页面.png')#////////////截图保存3.png
        except Exception as e:
            print(e)

        #/////////////////////开始爬取网站信息//////////////////////////////////
        left_bar=self.driver.find_elements_by_xpath('//ul[@class="qc-menu-list"]') 
        # mid_bar=left_bar[0].finde_elements_by_xpath('/li')
        self.driver.close()
        
if __name__ == "__main__":
    url = 'https://cloud.tencent.com/login?s_url=https%3A%2F%2Fconsole.cloud.tencent.com%2Fapi%2Fexplorer%3FProduct%3Dcvm%26Version%3D2017-03-12%26Action%3DAllocateHosts%26SignVersion%3D'
    print('输入qq号:')
    username=input()
    print('输入qq密码')
    password=input()
    admin = tencent_cloud(url,username,password) 
    admin.crawl()
    
    





