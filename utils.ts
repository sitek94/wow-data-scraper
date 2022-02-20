import { Page } from 'puppeteer'

export function acceptCookies(page: Page) {
  return page.evaluate(() => {
    const acceptBtn = document.querySelector<HTMLButtonElement>(
      '#onetrust-accept-btn-handler',
    )
    acceptBtn?.click()
  })
}

export function declineNotifications(page: Page) {
  return page.evaluate(() => {
    const declineBtn = document.querySelector<HTMLButtonElement>(
      '.notifications-dialog-buttons-decline',
    )
    declineBtn?.click()
  })
}
