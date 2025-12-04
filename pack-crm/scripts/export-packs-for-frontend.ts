#!/usr/bin/env node
/**
 * Export packs data for frontend consumption
 * 
 * Reads pack-crm/data/packs.json and writes a snapshot to src/data/packs.local.json
 * This is a manual export step (not wired into build yet).
 * 
 * Usage:
 *   pnpm tsx pack-crm/scripts/export-packs-for-frontend.ts
 */

import * as fs from 'fs';
import * as path from 'path';
import { fileURLToPath } from 'url';
import { loadPacks } from '../src/store';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const PACKS_FILE = path.join(__dirname, '..', 'data', 'packs.json');
const OUTPUT_FILE = path.join(__dirname, '..', '..', 'src', 'data', 'packs.local.json');

// Ensure output directory exists
const outputDir = path.dirname(OUTPUT_FILE);
if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true });
}

// Load packs
const packs = loadPacks();

if (packs.length === 0) {
  console.warn('⚠️  No packs found in pack-crm/data/packs.json');
  process.exit(0);
}

// Write to frontend data directory
const content = JSON.stringify(packs, null, 2);
fs.writeFileSync(OUTPUT_FILE, content, 'utf-8');

console.log(`✅ Exported ${packs.length} pack(s) to ${OUTPUT_FILE}`);
console.log('');
console.log('Packs exported:');
packs.forEach(pack => {
  console.log(`  - ${pack.name} (${pack.slug}) - Stage: ${pack.currentStage}`);
});

