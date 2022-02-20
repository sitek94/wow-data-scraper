import { Page } from 'puppeteer'

export async function scrapeAchievementsPage(page: Page) {
  const rowHandles = await page.$x('//*[@id="achievements"]/tbody/tr')
  const achievements = []

  /*
    Table structure, has the following structure, so it's "very convenient" to
    search for the data we want 🙈

    <tr>
      <td class="col-name">   - Name
      <td>                    - Description
      <td class="col-c">      - Fraction
      <td>                    - Points
      <td class="col-c>       - Category
    </tr>
  */
  for (const rowHandle of rowHandles) {
    const iconUrl = await rowHandle.$eval(
      '.listing-icon img',
      (el: HTMLImageElement) => el.src,
    )
    const name = await rowHandle.$eval('a.t', el => el.textContent)
    const description = await rowHandle.$eval('.subtext', el => el.textContent)

    const fractionHtml = await rowHandle.$eval(
      'td.col-name + td',
      el => el.innerHTML,
    )
    let fraction = null
    if (fractionHtml) {
      fraction = /horde/.test(fractionHtml) ? 'horde' : 'alliance'
    }

    let points = null
    const pointsHtml = await rowHandle.$eval('td.col-c', el => el.innerHTML)
    if (pointsHtml) {
      points = Number(pointsHtml.replace(/[^0-9]/g, ''))
    }

    const category = await rowHandle.$eval(
      'td.col-c:last-child',
      el => el.textContent,
    )

    const achievement = {
      name,
      description,
      iconUrl,
      fraction,
      points,
      category,
    }
    achievements.push(achievement)
  }

  return achievements
}
