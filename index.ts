import puppeteer from 'puppeteer'

const baseUrl = 'https://www.wowhead.com'

const browser = await puppeteer.launch(
  process.env.DEBUG ? { headless: false, slowMo: 250 } : {},
)
const page = await browser.newPage()
await page.goto(baseUrl + '/achievements')

await acceptCookies()
await declineNotifications()

const [el] = await page.$x('//*[@id="fi"]/form/div[1]/h1')
const title = await el.getProperty('textContent')
console.log(await title.jsonValue())

await browser.close()

function acceptCookies() {
  return page.evaluate(() => {
    const acceptBtn = document.querySelector<HTMLButtonElement>(
      '#onetrust-accept-btn-handler',
    )
    acceptBtn?.click()
  })
}

function declineNotifications() {
  return page.evaluate(() => {
    const declineBtn = document.querySelector<HTMLButtonElement>(
      '.notifications-dialog-buttons-decline',
    )
    declineBtn?.click()
  })
}
