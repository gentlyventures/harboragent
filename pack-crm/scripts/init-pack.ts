#!/usr/bin/env node
/**
 * Initialize a new pack in the CRM system
 * 
 * Usage:
 *   pnpm tsx pack-crm/scripts/init-pack.ts <slug> <name> [--price <price>]
 * 
 * Example:
 *   pnpm tsx pack-crm/scripts/init-pack.ts new-pack "New Pack Name" --price 499
 */

import * as path from 'path';
import { createDefaultPackLifecycle } from '../src/models';
import { addPack, getAllPacks } from '../src/store';

// Parse command line arguments
const args = process.argv.slice(2);

if (args.length < 2) {
  console.error('Usage: pnpm tsx pack-crm/scripts/init-pack.ts <slug> <name> [--price <price>]');
  console.error('');
  console.error('Arguments:');
  console.error('  slug    URL-friendly identifier (e.g., "new-pack")');
  console.error('  name    Display name (e.g., "New Pack Name")');
  console.error('  --price Price in dollars (default: 199)');
  process.exit(1);
}

const slug = args[0];
const name = args[1];

// Parse price (default: 199)
let price = 19900; // $199 in cents
const priceIndex = args.indexOf('--price');
if (priceIndex !== -1 && priceIndex + 1 < args.length) {
  const priceStr = args[priceIndex + 1];
  const priceDollars = parseFloat(priceStr);
  if (isNaN(priceDollars) || priceDollars < 0) {
    console.error(`Invalid price: ${priceStr}. Must be a positive number.`);
    process.exit(1);
  }
  price = Math.round(priceDollars * 100); // Convert to cents
}

// Get next pack number
const existingPacks = getAllPacks();
const nextPackNumber = existingPacks.length > 0
  ? Math.max(...existingPacks.map(p => p.packNumber)) + 1
  : 1;

// Create default pack
const pack = createDefaultPackLifecycle(
  slug,
  name,
  nextPackNumber,
  '', // regulationName - will need to be filled in later
  [], // targetAudience - will need to be filled in later
  price
);

try {
  addPack(pack);
  console.log(`✅ Pack created successfully!`);
  console.log('');
  console.log(`Slug: ${pack.slug}`);
  console.log(`Name: ${pack.name}`);
  console.log(`Pack Number: ${pack.packNumber}`);
  console.log(`Current Stage: ${pack.currentStage}`);
  console.log(`Price: $${(pack.metadata.price / 100).toFixed(2)}`);
  console.log('');
  console.log(`Next steps:`);
  console.log(`  1. Update metadata (regulationName, targetAudience) in pack-crm/data/packs.json`);
  console.log(`  2. Run research: pnpm tsx pack-crm/scripts/run-deep-dive.ts ${slug}`);
  console.log(`  3. Advance stages: pnpm tsx pack-crm/scripts/advance-stage.ts ${slug} <stage>`);
} catch (error) {
  console.error(`❌ Error creating pack: ${error}`);
  process.exit(1);
}

