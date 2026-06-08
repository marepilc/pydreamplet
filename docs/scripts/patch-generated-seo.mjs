import { readFile, writeFile } from 'node:fs/promises'

const outputDir = new URL('../.output/public/', import.meta.url)

for (const filename of ['404.html', '200.html']) {
  const url = new URL(filename, outputDir)
  let html = await readFile(url, 'utf8')

  html = html.replace(
    /<title>.*?<\/title>/,
    '<title>Page not found · pyDreamplet</title>'
  )

  if (!html.includes('name="robots"')) {
    html = html.replace(
      '</head>',
      '<meta name="robots" content="noindex, nofollow"></head>'
    )
  }

  await writeFile(url, html, 'utf8')
}
