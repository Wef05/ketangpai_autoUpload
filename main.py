from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from datetime import datetime
import time
import sys
import argparse
op=None;
import os
# 上传文件功能
# def upload_files(driver, url, upload_button_xpath, directory_path):
#     # 打开目标页面
#     time.sleep(1)  # 等待页面加载
#     # 获取指定目录中的文件
#     files = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
#     print(f"发现 {len(files)} 个文件需要上传")

#     for file_path in files:
#         try:
#             # 定位上传控件（<input type="file">）
#             upload_input = driver.find_element(By.XPATH, upload_button_xpath)
#             # 将文件路径传递给上传控件
#             upload_input.send_keys(file_path)
#             print(f"上传文件: {file_path}")
#             time.sleep(1)  # 等待上传完成（根据页面需求调整时间）
#         except Exception as e:
#             print(f"上传失败: {file_path}, 错误信息: {e}")


def delete_all_files_in_directory(directory):
    """
    删除指定目录下的所有文件，但保留目录本身。
    如果目录不存在，则输出提示信息。
    """
    if not os.path.exists(directory):
        putLog(f"目录不存在: {directory}")
        return

    # 遍历目录中的所有文件
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        # 检查是否是文件，防止误删子目录
        if os.path.isfile(file_path):
            os.remove(file_path)
            putLog(f"已删除文件: {file_path}")
        elif os.path.isdir(file_path):
            putLog(f"跳过子目录: {file_path}")

    putLog(f"目录下的所有文件已删除: {directory}")
def clear_file(file_path):
    with open(file_path, "w") as file:
        file.write('')
def write_to_file(file_path, content):
    """
    写入内容到指定文件。
    """
    with open(file_path, "a") as file:
        file.write(content)
    putLog(f"文件已写入: {file_path}")
def write_to_log(file_path, content):
    """
    写入内容到指定文件。
    """
    with open(file_path, "a") as file:
        file.write(content)
def read_file(file_path):
    """
    读取指定文件内容。
    """
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            data = file.read()
        putLog("文件内容如下：")
        putLog(data)
        print(data)
        return data
    else:
        putLog(f"文件不存在: {file_path}")
        return None
def delete_file(file_path):
    """
    删除指定文件。
    """
    if os.path.exists(file_path):
        os.remove(file_path)
        putLog(f"文件已删除: {file_path}")
    else:
        putLog(f"文件不存在: {file_path}")
def putLog(str):

    now = datetime.now()
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
    write_to_log('log.txt',formatted_time+'  log:'+str+'\n')
    if op.log:
        print(formatted_time)
        print('  log:'+str);
def putError(str):
    now = datetime.now()
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
    write_to_log('log.txt',formatted_time+'  error:'+str+'\n')
    print(formatted_time)
    print('  error:'+str);# 初始化 Selenium WebDriver
def init_browser():
    # 使用 Chrome 浏览器（需要安装 ChromeDriver）
    path_to_chromedriver = '/usr/local/bin/chromedriver'
    service = Service(executable_path=path_to_chromedriver)
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')  # 如果需要
    options.add_argument('--headless')    # 如果不需要浏览器窗口
    #driver = webdriver.Chrome(service=service)
    #driver = webdriver.Chrome(options=options)
    driver = webdriver.Chrome(service=service,options=options)
    #driver = webdriver.Chrome()
    return driver

# 自动识别和点击
def auto_click_subject(driver, url , subject):
    time.sleep(1)  # 等待页面加载
    # 查找所有 <h5> 标签
    clickable_elements = driver.find_elements(By.XPATH, "//h5[@class='info_title']")
    putLog(f"发现 {len(clickable_elements)} 个 <h5> 元素")

    for element in clickable_elements:
        try:
            # 判断元素是否可见且文本内容符合要求
            if element.is_displayed():
                content = element.text.strip()
                if subject in content:
                    putLog(f"点击元素: {content}")
                    element.click()
                    time.sleep(1)  # 等待页面响应
                    break  # 停止循环，因为已经找到并点击了目标
        except Exception as e:
            putError(f"元素处理失败: {e}")

# 自动识别和点击
def auto_click_homework(driver, url):
    time.sleep(1)  # 等待页面加载

    # 定位所有包含目标 <span> 的 <div> 元素
    clickable_elements = driver.find_elements(By.XPATH, "//div[@class='flex-align' and .//span[text()='作业']]")
    putLog(f"发现 {len(clickable_elements)} 个目标 <div> 元素")

    for element in clickable_elements:
        try:
            # 判断元素是否可见
            if element.is_displayed():
                content = element.text.strip()  # 获取元素文本内容
                if content=="作业":
                    putLog(f"点击元素: {content}")
                    element.click()
                    time.sleep(1)  # 等待页面响应
                    break  # 停止循环，因为已经找到并点击了目标
        except Exception as e:
            putError(f"元素处理失败: {e}")
# 自动识别和点击
def auto_click_upload(driver, url):
    time.sleep(1)  # 等待页面加载
    # 定位所有包含目标 <span> 的 <div> 元素
    clickable_elements = driver.find_elements(By.XPATH, "//button[@class='van-button van-button--info van-button--normal']")
    putLog(f"发现 {len(clickable_elements)} 个目标 <div> 元素")

    for element in clickable_elements:
        try:
            # 判断元素是否可见
            if element.is_displayed():
                content = element.text.strip()  # 获取元素文本内容
                if content=="提交作业":
                    putLog(f"点击元素: {content}")
                    element.click()
                    time.sleep(1)  # 等待页面响应
                    break  # 停止循环，因为已经找到并点击了目标
        except Exception as e:
            putError(f"元素处理失败: {e}")

def click_upload(driver, url):
    time.sleep(1)  # 等待页面加载
    # 定位所有包含目标 <span> 的 <div> 元素
    clickable_elements = driver.find_elements(By.XPATH, "//button[@class='van-button van-button--info van-button--mini']")
    putLog(f"发现 {len(clickable_elements)} 个目标 <div> 元素")

    for element in clickable_elements:
        try:
            # 判断元素是否可见
            if element.is_displayed():
                content = element.text.strip()  # 获取元素文本内容
                if content=="提交":
                    putLog(f"点击元素: {content}")
                    element.click()
                    time.sleep(1)  # 等待页面响应
                    break  # 停止循环，因为已经找到并点击了目标
        except Exception as e:
            putError(f"元素处理失败: {e}")
def get_homeWork(driver, url,sub):
    time.sleep(1)  # 等待页面加载
    # 定位所有 card-item 元素
    card_items = driver.find_elements(By.XPATH, "//div[@class='card-item']")
    cnt=0;
    for card in card_items:
        try:
            # 获取 van-ellipsis 的内容（标题）
            title_element = card.find_element(By.XPATH, ".//span[@class='van-ellipsis']")
            title = title_element.text.strip() if title_element else ""

            # 获取 tag-list 的内容（状态）
            tag_elements = card.find_elements(By.XPATH, ".//p[@class='tag-list']/span")
            tags = [tag.text.strip() for tag in tag_elements]

            # 获取提示按钮内容（提交状态）
            submission_element = card.find_element(By.XPATH, ".//span[contains(@class,'tip-btn')]")
            submission = submission_element.text.strip() if submission_element else ""

            
            # 整合内容
            content_list = [title, " ".join(tags), submission]
            putLog(f"发现内容: {content_list}")
            if '未提交' in submission:
                #click_homeWork(driver,url,title)
                #get_deadline_elements(driver);
                write_to_file('all_homework.txt',sub+' -- '+title+'\n')
                putLog(f"追加作业: {content_list}  ")
                cnt=cnt+1;
                

        except Exception as e:
            putError(f"处理 card-item 出错: {e}")
    return cnt;
def updata_homework():
    cnt=0;
    clear_file('all_homework.txt')

    driver.get(url)
    auto_click_subject(driver, url,'数学分析')
    auto_click_homework(driver, url)
    cnt+=get_homeWork(driver, url,'数学分析')
    driver.get(url)
    auto_click_subject(driver, url,'高等代数')
    auto_click_homework(driver, url)
    cnt+=get_homeWork(driver, url,'高等代数')
    driver.get(url)
    auto_click_subject(driver, url,'测试')
    auto_click_homework(driver, url)
    cnt+=get_homeWork(driver, url,'测试')
    write_to_file('all_homework.txt','(手动刷新)')
    print(f"找到{cnt}个作业")
def upload_files(driver, url, upload_button_xpath, directory_path):
    """
    自动上传指定目录中的所有文件。

    :param driver: Selenium WebDriver 实例
    :param url: 目标页面 URL
    :param upload_button_xpath: 上传控件的 XPath
    :param directory_path: 包含需要上传文件的目录路径
    """
    try:
        # 打开目标页面
        time.sleep(1)  # 可根据实际需求调整页面加载等待时间
        # 获取指定目录中的文件
        if not os.path.exists(directory_path):
            print(f"目录不存在: {directory_path}")
            return
        files = [os.path.abspath(os.path.join(directory_path, f)) for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
        if not files:
            print("指定目录中没有文件需要上传")
            return
        
        print(f"发现 {len(files)} 个文件需要上传")

        # 遍历文件并上传
        for file_path in files:
            if not os.path.exists(file_path):
                print(f"文件不存在: {file_path}")
                continue
            try:
                # 等待上传控件可用
                upload_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, upload_button_xpath))
                )
                # 上传文件
                upload_input.send_keys(file_path)
                print(f"成功上传文件: {file_path}")
                time.sleep(2)  # 根据页面反应调整时间

                # 可在这里添加文件上传后的确认操作
                # 如：点击“上传”按钮或等待上传结果
                # submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
                # submit_button.click()
            except Exception as e:
                print(f"上传失败: {file_path}，错误信息: {e}")

    except Exception as main_e:
        print(f"程序执行出错: {main_e}")
# 登录功能
def login(driver, username, password, username_xpath, password_xpath, login_button_xpath):
    try:
        # 定位用户名输入框并输入用户名
        username_input = driver.find_element(By.XPATH, username_xpath)
        username_input.clear()
        username_input.send_keys(username)

        # 定位密码输入框并输入密码
        password_input = driver.find_element(By.XPATH, password_xpath)
        password_input.clear()
        password_input.send_keys(password)

        # 定位登录按钮并点击
        login_button = driver.find_element(By.XPATH, login_button_xpath)
        login_button.click()

        putLog("登录成功，正在等待页面加载...")
        time.sleep(3)  # 等待登录后页面加载完成
    except Exception as e:
        print(f"登录失败: {e}")
from selenium.webdriver.common.by import By

def get_deadline_elements(driver):
    putLog("find deadline")
    time.sleep(1)
    try:
        # 定位所有包含“截止”字样的 <span> 元素
        elements = driver.find_elements(By.XPATH, "//span[contains(text(), '截止')]")
        
        # 提取文本内容
        deadlines = [element.text for element in elements]
        
        if deadlines:
            putLog(f"找到 {len(deadlines)} 个包含“截止”的元素:")
            for deadline in deadlines:
                putLog(f" - {deadline}")
        else:
            putLog("未找到包含“截止”字样的元素")
        
        return deadlines
    except Exception as e:
        print(f"获取“截止”元素时发生错误: {e}")
        return '*****'
def C(content_list,target):
    # 示例条件：标题包含"作业"
    title, status, submission = content_list
    #return "作业" in title;
    return target in title
def click_homeWork(driver, url,target):
    time.sleep(1)  # 等待页面加载
    # 定位所有 card-item 元素
    card_items = driver.find_elements(By.XPATH, "//div[@class='card-item']")
    cnt=0;
    for card in card_items:
        try:
            # 获取 van-ellipsis 的内容（标题）
            title_element = card.find_element(By.XPATH, ".//span[@class='van-ellipsis']")
            title = title_element.text.strip() if title_element else ""

            # 获取 tag-list 的内容（状态）
            tag_elements = card.find_elements(By.XPATH, ".//p[@class='tag-list']/span")
            tags = [tag.text.strip() for tag in tag_elements]

            # 获取提示按钮内容（提交状态）
            submission_element = card.find_element(By.XPATH, ".//span[contains(@class,'tip-btn')]")
            submission = submission_element.text.strip() if submission_element else ""

            # 整合内容
            content_list = [title, " ".join(tags), submission]
            putLog(f"发现内容: {content_list}")
            if C(content_list,target):
                putLog(f"点击符合条件的 card-item: {content_list}")
                card.click()
                break  # 点击后退出循环

        except Exception as e:
            putError(f"处理 card-item 出错: {e}")
def uploadHomework(sub,work):
    driver.get(url)
    auto_click_subject(driver, url,sub)
    auto_click_homework(driver, url)
    click_homeWork(driver,url,work)
    auto_click_upload(driver,url)
    # 替换为上传按钮的 XPath
    upload_button_xpath = "//input[@type='file']"
    # 替换为本地目录路径
    directory_path = "upload_img"
    try:
        upload_files(driver, url, upload_button_xpath, directory_path)
        time.sleep(1);
        click_upload(driver, url)
        delete_all_files_in_directory('upload_img')
        updata_homework();
    except:
        putError("上传失败")
if __name__ == "__main__":
    operator = argparse.ArgumentParser(description="")
    # 添加参数
    operator.add_argument("--log", type=bool, help="输出日志", default=False)
    operator.add_argument("--op", type=int, help="操作：\n0 显示所有作业（上次更新） \n 1更新作业 \n 3提交作业 ", default=0)
    operator.add_argument("--subject", type=str, help="不同", default='***')
    operator.add_argument("--homework", type=str, help="不同", default='***')
    # 解析参数
    op = operator.parse_args()
    # write_to_file('all_homework.txt','test')
    # read_file('all_homework.txt')
    # 测试函数调用
    write_to_log('log.txt',f"{op.log} {op.op} {op.subject}\n")
    if op.op == 0:
        read_file('all_homework.txt');
        sys.exit()
    if op.op == 9:
        delete_all_files_in_directory('upload_img')
        sys.exit()
    url = "https://w.ketangpai.com"  # 替换为目标页面的 URL
    driver = init_browser()
    # 用户名和密码
    username = ""  # 替换为你的用户名
    password = ""  # 替换为你的密码

    # 替换为用户名、密码和登录按钮的 XPath
    username_xpath = "//input[@placeholder='请输入账号/手机/邮箱']"  # 替换为实际的用户名输入框 XPath
    password_xpath = "//input[@placeholder='请输入密码']"  # 替换为实际的密码输入框 XPath
    login_button_xpath = "//button[@class='van-button van-button--info van-button--large']"  # 替换为实际的登录按钮 XPath
    try:
    	# 打开目标页面
        driver.get(url)
        time.sleep(2)  # 等待页面加载
    except:
    	putError("打开浏览器失败")
    #auto_click(driver, url)
    login(driver, username, password, username_xpath, password_xpath, login_button_xpath)
    if op.op == 1:
        updata_homework();
    if op.op == 2:
        uploadHomework(op.subject,op.homework);
    driver.quit()