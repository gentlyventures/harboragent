#!/usr/bin/env node
/**
 * Run deep-dive research for a pack
 * 
 * Usage:
 *   pnpm tsx pack-crm/scripts/run-deep-dive.ts <slug>
 * 
 * Example:
 *   pnpm tsx pack-crm/scripts/run-deep-dive.ts tax-assist
 * 
 * This script:
 * 1. Loads the pack by slug
 * 2. Reads the research template
 * 3. Builds the prompt
 * 4. Calls OpenAI API
 * 5. Saves the report to pack-crm/research/{slug}-deep-dive.md
 * 6. Updates the pack in packs.json with research completion status
 */

import * as fs from 'fs';
import * as path from 'path';
import { fileURLToPath } from 'url';
import { getPack } from '../src/store';
import { advancePackStage } from '../src/lifecycle';
import { buildDeepDivePrompt } from '../src/prompts/deepDive';
import { callOpenAI } from '../src/openai-client';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const RESEARCH_DIR = path.join(__dirname, '..', 'research');

// Ensure research directory exists
if (!fs.existsSync(RESEARCH_DIR)) {
  fs.mkdirSync(RESEARCH_DIR, { recursive: true });
}

// Parse command line arguments
const args = process.argv.slice(2);

if (args.length < 1) {
  console.error('Usage: pnpm tsx pack-crm/scripts/run-deep-dive.ts <slug>');
  console.error('');
  console.error('Arguments:');
  console.error('  slug    Pack slug (e.g., "tax-assist")');
  console.error('');
  console.error('Environment:');
  console.error('  OPENAI_API_KEY    Required: OpenAI API key');
  process.exit(1);
}

const slug = args[0];

// Load pack
const pack = getPack(slug);
if (!pack) {
  console.error(`❌ Pack not found: ${slug}`);
  process.exit(1);
}

console.log(`🔍 Starting deep-dive research for: ${pack.name}`);
console.log(`   Regulation: ${pack.metadata.regulationName}`);
console.log('');

// Check for API key
if (!process.env.OPENAI_API_KEY) {
  console.error('❌ OPENAI_API_KEY environment variable is not set');
  console.error('   Please set it before running this script:');
  console.error('   export OPENAI_API_KEY=your-api-key-here');
  process.exit(1);
}

try {
  // Build prompt
  console.log('📝 Building research prompt...');
  const prompt = buildDeepDivePrompt(pack);
  console.log(`   Prompt length: ${prompt.length} characters`);
  console.log('');

  // Call OpenAI
  console.log('🤖 Calling OpenAI API (this may take a few minutes)...');
  const report = await callOpenAI(prompt);
  console.log(`   Response length: ${report.length} characters`);
  console.log('');

  // Save report
  const reportPath = path.join(RESEARCH_DIR, `${slug}-deep-dive.md`);
  fs.writeFileSync(reportPath, report, 'utf-8');
  console.log(`✅ Research report saved to: ${reportPath}`);
  console.log('');

  // Update pack
  console.log('📦 Updating pack in CRM...');
  const updated = advancePackStage(slug, 'deep_dive', {
    researchArtifacts: [reportPath],
  });

  if (!updated) {
    console.error('❌ Failed to update pack');
    process.exit(1);
  }

  console.log('✅ Pack updated successfully!');
  console.log('');
  console.log('Summary:');
  console.log(`  Pack: ${updated.name} (${updated.slug})`);
  console.log(`  Current Stage: ${updated.currentStage}`);
  console.log(`  Research Completed: ${updated.research.researchCompleted}`);
  console.log(`  Research Artifacts: ${updated.research.researchArtifacts.length} file(s)`);
  console.log(`  Report Path: ${reportPath}`);
  console.log('');
  console.log('Next steps:');
  console.log(`  1. Review the report: ${reportPath}`);
  console.log(`  2. Use the report to create pack content in packs/${slug}/`);
  console.log(`  3. Advance to build stage: pnpm tsx pack-crm/scripts/advance-stage.ts ${slug} build`);
} catch (error) {
  console.error('❌ Error running deep-dive research:');
  console.error(error instanceof Error ? error.message : String(error));
  process.exit(1);
}

