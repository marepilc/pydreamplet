import { readdir, writeFile } from 'node:fs/promises'
import { join, relative, sep } from 'node:path'
import { fileURLToPath } from 'node:url'

const root = new URL('..', import.meta.url)
const contentDir = fileURLToPath(new URL('./content/', root))
const publicDir = new URL('./public/', root)
const siteUrl = (
  process.env.NUXT_PUBLIC_SITE_URL
  || process.env.SITE_URL
  || 'https://py.dreamplet.com'
).replace(/\/+$/, '')

async function collectMarkdownFiles(directory) {
  const entries = await readdir(directory, { withFileTypes: true })
  const files = []

  for (const entry of entries) {
    const path = join(directory, entry.name)
    if (entry.isDirectory()) {
      files.push(...await collectMarkdownFiles(path))
    } else if (entry.isFile() && entry.name.endsWith('.md')) {
      files.push(path)
    }
  }

  return files
}

function routeFromFile(file) {
  const path = relative(contentDir, file)
    .split(sep)
    .join('/')
    .replace(/\.md$/, '')
    .replace(/\/index$/, '')

  return path === 'index' ? '/' : `/${path}`
}

function escapeXml(value) {
  return value
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&apos;')
}

const files = await collectMarkdownFiles(contentDir)
const applicationRoutes = ['/gallery']
const routes = [...new Set([...files.map(routeFromFile), ...applicationRoutes])].sort()
const urls = routes.map((route) => {
  const location = route === '/' ? siteUrl : `${siteUrl}${route}`
  return `  <url><loc>${escapeXml(location)}</loc></url>`
})

const sitemap = [
  '<?xml version="1.0" encoding="UTF-8"?>',
  '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
  ...urls,
  '</urlset>',
  ''
].join('\n')

const robots = [
  'User-agent: *',
  'Allow: /',
  '',
  `Sitemap: ${siteUrl}/sitemap.xml`,
  ''
].join('\n')

await writeFile(new URL('sitemap.xml', publicDir), sitemap, 'utf8')
await writeFile(new URL('robots.txt', publicDir), robots, 'utf8')
