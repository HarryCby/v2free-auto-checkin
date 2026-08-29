import asyncio
import os
import sys
from playwright.async_api import async_playwright

from dotenv import load_dotenv
load_dotenv()

async def login():
    # 从环境变量读取
    email = os.environ.get('V2F_EMAIL')
    password = os.environ.get('V2F_PASSWORD')
    url=os.environ.get('V2F_URL')
    # 调试：打印是否读取到（但不要打印密码值！）
    print(f"email: {'be set' if email else 'not be set'}")
    print(f"pswd: {'be set' if password else 'not be set'}")

    if not email or not password:
        print("pls set V2AI_EMAIL 和 V2AI_PASSWORD")
        return False  # 返回失败

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto(url)
        await page.wait_for_load_state("networkidle")

        email_input = page.locator('#email')
        password_input = page.locator('#passwd')
        login_btn=page.locator('#login')
        # 检查元素是否存在
        if await email_input.count() == 0:
            print("not find email")
            await browser.close()
            return False
        if await password_input.count() == 0:
            print("not find password")
            await browser.close()
            return False
        if await login_btn.count() == 0:
            print("not find login_btn")
            await browser.close()
            return False
        # 输入
        await email_input.fill(email)
        await password_input.fill(password)
        await login_btn.click()
        print("inf put and login")

        await asyncio.sleep(5)
        await page.mouse.click(245, 3)
        checkin=page.locator('#checkin')
        if await checkin.count() == 0:
            checkin_already = page.locator('a.btn-brand.disabled:has-text("今日已签到")')
            if await checkin_already.count()>0:
                print("already checkin")
                await browser.close()
                return True  # 已签到算成功
            else:
                print("not find checkin\npls checkin manually")
                await browser.close()
                return False  # 没找到签到按钮，失败
        await checkin.click()
        await asyncio.sleep(3)
        
        # 点击签到后检查是否成功
        # 检查是否出现"今日已签到"（签到成功后的状态）
        checkin_already = page.locator('a.btn-brand.disabled:has-text("今日已签到")')
        if await checkin_already.count()>0:
            print("checkin success")
            await browser.close()
            return True
        else:
            print("checkin may failed, pls check manually")
            await browser.close()
            return False


if __name__ == "__main__":
    success = asyncio.run(login())
    if success:
        print("task done")
        sys.exit(0)
    else:
        print("task failed")
        sys.exit(1)