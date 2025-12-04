#!/usr/bin/env node
/**
 * Advance a pack to a target stage
 * 
 * Usage:
 *   pnpm tsx pack-crm/scripts/advance-stage.ts <slug> <stage> [--score <score>] [--gate <pass|fail>] [--note <note>]
 * 
 * Example:
 *   pnpm tsx pack-crm/scripts/advance-stage.ts tax-assist deep_dive
 *   pnpm tsx pack-crm/scripts/advance-stage.ts tax-assist scoring --score 85 --gate pass
 */

import { PackStage } from '../src/models';
import { getPack } from '../src/store';
import { advancePackStage } from '../src/lifecycle';

// Parse command line arguments
const args = process.argv.slice(2);

if (args.length < 2) {
  console.error('Usage: pnpm tsx pack-crm/scripts/advance-stage.ts <slug> <stage> [--score <score>] [--gate <pass|fail>] [--note <note>]');
  console.error('');
  console.error('Arguments:');
  console.error('  slug    Pack slug (e.g., "tax-assist")');
  console.error('  stage   Target stage: idea, validation, scoring, deep_dive, build, published');
  console.error('  --score Score (0-100) for validation/scoring stages');
  console.error('  --gate  Gate result (pass|fail) for scoring stage');
  console.error('  --note  Optional note');
  process.exit(1);
}

const slug = args[0];
const stageStr = args[1] as PackStage;

// Validate stage
const validStages: PackStage[] = ['idea', 'validation', 'scoring', 'deep_dive', 'build', 'published'];
if (!validStages.includes(stageStr)) {
  console.error(`Invalid stage: ${stageStr}`);
  console.error(`Valid stages: ${validStages.join(', ')}`);
  process.exit(1);
}

// Parse optional arguments
let score: number | undefined;
let gate: 'pass' | 'fail' | undefined;
let note: string | undefined;

const scoreIndex = args.indexOf('--score');
if (scoreIndex !== -1 && scoreIndex + 1 < args.length) {
  const scoreStr = args[scoreIndex + 1];
  const scoreNum = parseFloat(scoreStr);
  if (isNaN(scoreNum) || scoreNum < 0 || scoreNum > 100) {
    console.error(`Invalid score: ${scoreStr}. Must be between 0 and 100.`);
    process.exit(1);
  }
  score = scoreNum;
}

const gateIndex = args.indexOf('--gate');
if (gateIndex !== -1 && gateIndex + 1 < args.length) {
  const gateStr = args[gateIndex + 1];
  if (gateStr !== 'pass' && gateStr !== 'fail') {
    console.error(`Invalid gate: ${gateStr}. Must be "pass" or "fail".`);
    process.exit(1);
  }
  gate = gateStr as 'pass' | 'fail';
}

const noteIndex = args.indexOf('--note');
if (noteIndex !== -1 && noteIndex + 1 < args.length) {
  note = args[noteIndex + 1];
}

// Check if pack exists
const pack = getPack(slug);
if (!pack) {
  console.error(`❌ Pack not found: ${slug}`);
  process.exit(1);
}

// Advance stage
const options = {
  score,
  gate,
  note,
};

const updated = advancePackStage(slug, stageStr, options);

if (!updated) {
  console.error(`❌ Failed to advance pack stage`);
  process.exit(1);
}

console.log(`✅ Pack stage advanced successfully!`);
console.log('');
console.log(`Pack: ${updated.name} (${updated.slug})`);
console.log(`Previous Stage: ${pack.currentStage}`);
console.log(`Current Stage: ${updated.currentStage}`);
console.log(`Stage Status: ${updated.stages[stageStr].status}`);
if (updated.stages[stageStr].startedAt) {
  console.log(`Started At: ${updated.stages[stageStr].startedAt}`);
}
if (updated.stages[stageStr].completedAt) {
  console.log(`Completed At: ${updated.stages[stageStr].completedAt}`);
}
if (score !== undefined) {
  console.log(`Score: ${score}`);
}
if (gate !== undefined) {
  console.log(`Gate: ${gate}`);
}
console.log(`Updated At: ${updated.metadata.updatedAt}`);

