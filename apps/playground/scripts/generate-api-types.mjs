import { readFile, writeFile } from "node:fs/promises"
import path from "node:path"
import { fileURLToPath } from "node:url"

import openapiTS, { astToString } from "openapi-typescript"

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)
const rootDir = path.resolve(__dirname, "../../..")
const snapshotPath = path.resolve(rootDir, "openapi/openapi.snapshot.json")

async function loadSchema() {
  if (process.env.OPENAPI_SOURCE === "url") {
    const baseUrl = process.env.VITE_API_BASE_URL || "http://localhost:8000"
    const schemaUrl = `${baseUrl.replace(/\/$/, "")}/openapi.json`
    return { source: schemaUrl, schema: new URL(schemaUrl) }
  }

  const raw = await readFile(snapshotPath, "utf8")
  return { source: snapshotPath, schema: JSON.parse(raw) }
}

try {
  const { source, schema } = await loadSchema()
  const ast = await openapiTS(schema)
  const contents = astToString(ast)
  await writeFile(new URL("../src/lib/api-types.ts", import.meta.url), contents, "utf8")
  console.log(`Generated API types from ${source}`)
} catch (error) {
  console.error("Failed to generate API types")
  throw error
}
