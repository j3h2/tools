import sys, os, time, json, random, string
from selenium.webdriver.support.ui import Select

from faker import Faker
faker = Faker()

sys.path.insert(0, sys.path[0]+"/..")

from base.adspower import Adspower
from base import logger
from base import getAdsPowerByIndex
from utils.pwd import generate_pwd18


def getUserName():
    n = random.randint(4, 6)
    random_string = ''.join(random.choices(string.digits, k=n))
    username = faker.user_name()[:24] + random_string
    return username

def getPassword():
    return generate_pwd18()

def regsiter(index):
    url = 'https://outlook.live.com/owa/?nlp=1&signup=1'
    ads = getAdsPowerByIndex(index)
    driver = ads.lunch()
    driver.open_new_window(url)

    first_name = faker.first_name()
    last_name = faker.last_name()
    user_name = getUserName()

    driver.try_click('//*[@id="LiveDomainBoxList"]', 3)
    ele = driver.try_find('//*[@id="LiveDomainBoxList"]')
    Select(ele).select_by_value('hotmail.com')
    ele = driver.try_find('//*[@id="MemberName"]')
    if ele is None:
        logger.error('未找到输入框')
        return
    ele.send_keys(user_name)

    driver.try_click('//*[@id="iSignupAction"]', 3)


    pwd = getPassword()
    ele = driver.try_find('//*[@id="PasswordInput"]')
    if ele is None:
        logger.error('未找到密码输入框')
        return
    ele.send_keys(pwd)
    
    driver.try_click('//*[@id="ShowHidePasswordCheckbox"]', 2)
    driver.try_click('//*[@id="iOptinEmail"]', 2)
    driver.try_click('//*[@id="iSignupAction"]', 3)
    
    # 输入first name  last name
    ele = driver.try_find('//*[@id="FirstName"]')
    if ele is None:
        logger.error('未找到输入框')
        return
    ele.send_keys(first_name)

    time.sleep(3)
    ele = driver.try_find('//*[@id="LastName"]')
    if ele is None:
        logger.error('未找到输入框')
        return
    ele.send_keys(last_name)
    time.sleep(3)

    driver.try_click('//*[@id="iSignupAction"]', 3)

    # 选择日期
    eles = driver.try_finds('//select')
    if eles is None:
        logger.error('未找到选择框')
        return

    # day
    time.sleep(2)
    day = random.randint(1, 28)
    Select(eles[1]).select_by_value(str(day))
    # month 
    time.sleep(2)
    month =  random.randint(1, 12)
    Select(eles[2]).select_by_value(str(month))

    # year
    time.sleep(2)
    year = random.randint(1978, 2003)
    year_ele = driver.try_find('//*[@id="BirthYear"]')
    if year_ele is None:
        logger.error('未找到年份输入框')
        return
    year_ele.send_keys(str(year))
    
    # 确定
    driver.try_click('//*[@id="iSignupAction"]', 3)

    logger.info(f"{index} 号指纹浏览器，hotmail 账号创建成功! 您的邮箱账号为 {user_name}@hotmail.com, 密码为: {pwd} ,生日: {year}-{month}-{day}, first_name is {first_name}, last_name is {last_name}")
    logger.info('注意：验证码需要自行点击才能最终创建成功')

if __name__ == '__main__':
    regsiter(47)




