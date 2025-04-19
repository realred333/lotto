from playwright.sync_api import Playwright, sync_playwright
import time
import os
import telegram

USER_ID = os.environ['USER_ID']
USER_PW = os.environ['USER_PW']
COUNT = 5

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    # Go to login page
    page.goto("https://dhlottery.co.kr/user.do?method=login")

    # 로그인
    page.fill("[placeholder='아이디']", USER_ID)
    page.fill("[placeholder='비밀번호']", USER_PW)
    with page.expect_navigation():
        page.press("form[name='jform'] >> text=로그인", "Enter")
    
    page.wait_for_selector("#lottoGame")  # 게임 페이지 확인

    # 로또 게임 페이지로 이동
    page.goto("https://ol.dhlottery.co.kr/olotto/game/game645.do")

    # 우회 팝업 처리
    try:
        page.locator("#popupLayerAlert").get_by_role("button", name="확인").click()
    except Exception as e:
        print("팝업이 없거나 이미 닫혔습니다.")
    
    # 자동번호 발급 및 구매 개수 설정
    page.click("text=자동번호발급")
    page.select_option("select", str(COUNT))
    page.click("text=확인")
    page.click("input:has-text('구매하기')")

    time.sleep(2)
    page.click("text=확인 취소 >> input[type='button']")
    page.click("input[name='closeLayer']")

    context.close()
    browser.close()

    # 텔레그램 알림
    token = os.environ['TELE_TOKEN']
    bot = telegram.Bot(token)
    bot.sendMessage(chat_id=5467498555, text="응 이번주 로또 샀다. 제발 당첨되길..")

with sync_playwright() as playwright:
    run(playwright)
