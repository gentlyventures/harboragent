/**
 * Pack CRM File-Based Storage
 * 
 * Provides file-based read/write operations for pack lifecycle data.
 * Uses JSON files for persistence, matching the project's file-based approach.
 */

import * as fs from 'fs';
import * as path from 'path';
import { fileURLToPath } from 'url';
import { PackLifecycle } from './models';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const DATA_DIR = path.join(__dirname, '..', 'data');
const PACKS_FILE = path.join(DATA_DIR, 'packs.json');

/**
 * Ensures the data directory exists
 */
function ensureDataDir(): void {
  if (!fs.existsSync(DATA_DIR)) {
    fs.mkdirSync(DATA_DIR, { recursive: true });
  }
}

/**
 * Loads all packs from packs.json
 * Returns empty array if file doesn't exist or is invalid
 */
export function loadPacks(): PackLifecycle[] {
  ensureDataDir();
  
  if (!fs.existsSync(PACKS_FILE)) {
    return [];
  }
  
  try {
    const content = fs.readFileSync(PACKS_FILE, 'utf-8');
    const packs: PackLifecycle[] = JSON.parse(content);
    
    // Validate that it's an array
    if (!Array.isArray(packs)) {
      console.warn(`Invalid packs.json format: expected array, got ${typeof packs}`);
      return [];
    }
    
    return packs;
  } catch (error) {
    console.error(`Error reading packs.json: ${error}`);
    return [];
  }
}

/**
 * Saves packs to packs.json
 * Sorts by slug for consistent output and pretty-prints JSON
 */
export function savePacks(packs: PackLifecycle[]): void {
  ensureDataDir();
  
  // Sort by slug for consistent output
  const sorted = [...packs].sort((a, b) => a.slug.localeCompare(b.slug));
  
  // Pretty-print with 2-space indentation
  const content = JSON.stringify(sorted, null, 2);
  
  try {
    // Write atomically: write to temp file, then rename
    const tempFile = `${PACKS_FILE}.tmp`;
    fs.writeFileSync(tempFile, content, 'utf-8');
    fs.renameSync(tempFile, PACKS_FILE);
  } catch (error) {
    console.error(`Error writing packs.json: ${error}`);
    throw error;
  }
}

/**
 * Gets a pack by slug
 */
export function getPack(slug: string): PackLifecycle | undefined {
  const packs = loadPacks();
  return packs.find(p => p.slug === slug);
}

/**
 * Updates a pack by slug with partial data
 * Returns the updated pack, or undefined if pack not found
 */
export function updatePack(slug: string, partial: Partial<PackLifecycle>): PackLifecycle | undefined {
  const packs = loadPacks();
  const index = packs.findIndex(p => p.slug === slug);
  
  if (index === -1) {
    return undefined;
  }
  
  // Update the pack
  const updated: PackLifecycle = {
    ...packs[index],
    ...partial,
    // Ensure metadata.updatedAt is always updated
    metadata: {
      ...packs[index].metadata,
      ...partial.metadata,
      updatedAt: new Date().toISOString(),
    },
  };
  
  packs[index] = updated;
  savePacks(packs);
  
  return updated;
}

/**
 * Adds a new pack
 * Throws if pack with same slug already exists
 */
export function addPack(pack: PackLifecycle): void {
  const packs = loadPacks();
  
  if (packs.some(p => p.slug === pack.slug)) {
    throw new Error(`Pack with slug "${pack.slug}" already exists`);
  }
  
  packs.push(pack);
  savePacks(packs);
}

/**
 * Gets all packs, sorted by packNumber
 */
export function getAllPacks(): PackLifecycle[] {
  const packs = loadPacks();
  return packs.sort((a, b) => a.packNumber - b.packNumber);
}

