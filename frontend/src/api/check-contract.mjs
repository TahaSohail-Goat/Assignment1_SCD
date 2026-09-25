import { readFile, writeFile } from 'node:fs/promises'
import { fileURLToPath } from 'node:url'
import { resolve, dirname } from 'node:path'
import openapiTS, { astToString } from 'openapi-typescript'

const here = dirname(fileURLToPath(import.meta.url))
const source = resolve(process.env.OPENAPI_SCHEMA ?? resolve(here, 'design.openapi.json'))
const output = resolve(here, 'schema.d.ts')
const schema = JSON.parse(await readFile(source, 'utf8'))
const generated = astToString(await openapiTS(schema))

if (process.argv.includes('--write')) {
  await writeFile(output, generated)
  console.log(`Generated ${output} from ${source}`)
} else if (await readFile(output, 'utf8') !== generated) {
  console.error(`API types differ from ${source}. Run this script with --write after reviewing the schema.`)
  process.exitCode = 1
} else {
  console.log(`API types match ${source}`)
}
