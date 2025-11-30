#!/usr/bin/env node

/**
 * Utility script to load .env file for Node.js scripts
 * Usage: node scripts/load-env.js your-script.js
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

// Check if .env exists
const envPath = path.join(process.cwd(), '.env');
if (!fs.existsSync(envPath)) {
  console.error('Error: .env file not found');
  console.error('Please copy .env.example to .env and fill in your values');
  process.exit(1);
}

// Load dotenv if available
try {
  require('dotenv').config();
} catch (error) {
  console.warn('Warning: dotenv not installed. Install with: npm install dotenv');
}

// Get the script to run
const script = process.argv[2];
if (!script) {
  console.error('Usage: node scripts/load-env.js <script.js>');
  process.exit(1);
}

// Run the script with env loaded
try {
  execSync(`node ${script}`, { stdio: 'inherit', env: process.env });
} catch (error) {
  process.exit(error.status || 1);
}

