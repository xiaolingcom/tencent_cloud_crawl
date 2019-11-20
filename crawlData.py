from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd


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
#参考链接https://www.cnblogs.com/eastmount/p/4810690.html
    
    
class tencent_cloud:
    def __init__(self,url,username,password):
        #参数设置
        self.url = url
        self.username=username
        self.password=password

    
    def crawl(self):
        #/////////////////////首先登入网站//////////////////////////////////
        self.driver=webdriver.Chrome()
        self.driver.set_window_size(1920,1080) #设置为屏幕分辨率
        self.driver.get(self.url)
        self.driver.save_screenshot('0-打开页面.png')#/////////////截图保存0.png
        print('---------------------页面请求成功!---------------------')

        self.driver.find_element_by_xpath('//a[@data-type="qq"]').click()
        iframe=self.driver.find_element_by_xpath('//iframe[@id="ptlogin_iframe"]')#发现开始找不到'switcher_plogin'，是因为这部分代码放到了#document下
        self.driver.switch_to_frame(iframe)#跳转到iframe
        self.driver.find_element_by_xpath('//a[@id="switcher_plogin"]').click()
        self.driver.save_screenshot('1-QQ登录页面.png')#////////////截图保存1.png
        
        self.driver.find_element_by_xpath('//input[@id="u"]').send_keys(self.username) #这里不用跳转了，!!!iframe没有改变!!!,我被搞疯了
        self.driver.find_element_by_xpath('//input[@id="p"]').send_keys(self.password)
        self.driver.find_element_by_xpath('//input[@id="login_button"]').click()
        time.sleep(8)
        print('---------------------登入并跳转到目标页面!---------------------')
        self.driver.save_screenshot('2-登录成功页面.png')#////////////截图保存2.png


        #/////////////////////开始爬取网站信息//////////////////////////////////
        api_list=[[]]
        ul=self.driver.find_elements_by_xpath('//ul[@class="qc-menu-list"]') #两个边栏
        a_1=ul[0].find_elements_by_xpath('li/a')
        for item1 in a_1: #len=88
            item1.click()
            # time.sleep(3)
            # print(item1.text,len(a_1))
            a_2=ul[1].find_elements_by_xpath('li/a')
            tmp=ul[1].find_elements_by_xpath('li/ul[@class="qc-menu-subitem"]')
            for item2,tmp_item in zip(a_2,tmp): 
                if not tmp_item.is_displayed():
                    item2.click()
                # time.sleep(3)
                # print(item2.text,len(a_2))
                a_3=tmp_item.find_elements_by_xpath('li/a')
                for item3 in a_3:
                    api=[]
                    item3.click()
                    # print(item3.text,len(a_3))
                    try:
                        code=self.driver.find_element_by_tag_name('code')
                        api.append(item1.text)
                        api.append(item2.text)
                        api.append(item3.text)
                        api.append(code.text.replace('\n',' '))
                        api_list.append(api)
                    except NoSuchElementException:
                        code='None'
                        api.append(item1.text)
                        api.append(item2.text)
                        api.append(item3.text)
                        api.append(code)
                        api_list.append(api)
                        continue
        return api_list


               


       
        
if __name__ == "__main__":
    url = 'https://cloud.tencent.com/login?s_url=https%3A%2F%2Fconsole.cloud.tencent.com%2Fapi%2Fexplorer%3FProduct%3Dcvm%26Version%3D2017-03-12%26Action%3DAllocateHosts%26SignVersion%3D'
    print('输入qq号:')
    username=input()
    print('输入qq密码')
    password=input()
    admin = tencent_cloud(url,username,password) 
    api_list=admin.crawl()
    print("---------------------数据爬取完成!---------------------")
    #将list数据转换为csv
    name=['1','2','3','4']
    tmp=pd.DataFrame(columns=name,data=api_list)
    tmp.to_csv('./crawl_data.csv',encoding='gbk')
    print("---------------------数据保存完成!---------------------")
    
    





