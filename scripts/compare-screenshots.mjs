#!/usr/bin/env node
import fs from 'node:fs';
import { spawnSync } from 'node:child_process';

const [, , baseline, current] = process.argv;
if (!baseline || !current) {
  console.error('Usage: node compare-screenshots.mjs <baseline.png> <current.png>');
  process.exit(2);
}

if (!fs.existsSync(baseline)) {
  console.error(`Baseline not found: ${baseline}`);
  process.exit(1);
}
if (!fs.existsSync(current)) {
  console.error(`Current screenshot not found: ${current}`);
  process.exit(1);
}

const adapterCommand = process.env.FRONTEND_VLM_COMMAND;
if (adapterCommand) {
  const payload = {
    instruction: 'Compare two UI screenshots. Identify visual drift, composition differences, hierarchy changes, density changes, and whether the current image preserves the baseline intent. Return markdown with scores and targeted fixes.',
    baseline,
    current
  };
  const result = spawnSync(adapterCommand, {
    input: JSON.stringify(payload, null, 2),
    encoding: 'utf8',
    shell: true,
    maxBuffer: 20 * 1024 * 1024
  });
  if (result.status !== 0) {
    console.error(result.stderr || result.stdout || 'VLM adapter failed.');
    process.exit(result.status || 1);
  }
  console.log(result.stdout.trim());
  process.exit(0);
}

console.log('No FRONTEND_VLM_COMMAND configured.');
console.log('For deterministic regression, use Playwright toHaveScreenshot, Chromatic, Storybook, pixelmatch/pngjs, or a project-specific adapter.');
console.log('For open-ended visual quality, configure a VLM adapter and run score-reference-match.mjs.');
console.log(`Baseline: ${baseline}`);
console.log(`Current: ${current}`);
