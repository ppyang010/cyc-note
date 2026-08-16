---
id: "3361690166"
title: "使用selenium爬取前程无忧遭遇滑块验证，在selenium窗口手动滑都不通过，是什么原因?"
author: "李良熹"
type: zhihu-answer
source: "https://www.zhihu.com/question/597053858/answer/3361690166"
created: "2024-01-14 10:00"
updated: "2024-01-14 10:00"
collected: "2024-01-14 10:00"
downloaded: "2026-08-16"
---
因为使用selenium，会在Chrome上显示一个“已经被自动测试软件控制”，然后被网站检测到。

你可以参考下面这段代码，去除掉selenium的痕迹就可以了。

后面应该怎么拖动滑块，你就怎么拖动滑块。

```text
    chrome_driver = 'D:/selenium/chromedriver.exe'

    options = webdriver.ChromeOptions()

    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(chrome_options=options,executable_path=chrome_driver)

    # webdriver防屏蔽
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
           Object.defineProperty(navigator, 'webdriver', {
             get: () => false
           })
         """
    })

    driver.get(url)
```