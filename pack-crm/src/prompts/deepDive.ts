/**
 * Deep Dive Research Prompt Builder
 * 
 * Constructs prompts for deep-dive research reports using the ChatGPT research template.
 */

import * as fs from 'fs';
import * as path from 'path';
import { fileURLToPath } from 'url';
import { PackLifecycle } from '../models';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const TEMPLATE_PATH = path.join(
  __dirname,
  '..',
  '..',
  '..',
  'pack-process',
  'CHATGPT_RESEARCH_TEMPLATE.md'
);

/**
 * Reads the ChatGPT research template from disk
 */
function readTemplate(): string {
  if (!fs.existsSync(TEMPLATE_PATH)) {
    throw new Error(
      `Research template not found at: ${TEMPLATE_PATH}\n` +
      'Please ensure pack-process/CHATGPT_RESEARCH_TEMPLATE.md exists.'
    );
  }
  
  return fs.readFileSync(TEMPLATE_PATH, 'utf-8');
}

/**
 * Builds a deep-dive research prompt for a pack
 * 
 * @param pack The pack lifecycle data
 * @param templateText The research template text (optional, will read from disk if not provided)
 * @returns The complete prompt string
 */
export function buildDeepDivePrompt(
  pack: PackLifecycle,
  templateText?: string
): string {
  const template = templateText || readTemplate();
  
  // Build pack metadata header
  const metadataHeader = {
    packSlug: pack.slug,
    packName: pack.name,
    packNumber: pack.packNumber,
    regulationName: pack.metadata.regulationName,
    targetAudience: pack.metadata.targetAudience,
    currentStage: pack.currentStage,
    price: `$${(pack.metadata.price / 100).toFixed(2)}`,
  };
  
  // Construct the prompt
  const prompt = `# Deep-Dive Research Request for Harbor Agent Pack

## Pack Metadata
\`\`\`json
${JSON.stringify(metadataHeader, null, 2)}
\`\`\`

## Research Context
You are conducting deep-dive research for the **${pack.name}** (Pack #${pack.packNumber}).

**Regulation/Standard:** ${pack.metadata.regulationName}

**Target Audience:**
${pack.metadata.targetAudience.map(audience => `- ${audience}`).join('\n')}

**Current Stage:** ${pack.currentStage}

## Instructions
Please use the following research template to conduct comprehensive research and produce all necessary content for this pack. Replace all placeholders in the template with specific information about **${pack.metadata.regulationName}**.

---

${template}

---

## Additional Notes
- This research will be used to create a Harbor Agent compliance pack
- Focus on engineering and developer-ready content
- Make content AI-copilot friendly (for Cursor, GitHub Copilot, etc.)
- Provide actionable, practical guidance
- Include code examples and templates where relevant

Please provide complete output for all 16 sections of the template, tailored specifically to **${pack.metadata.regulationName}**.
`;

  return prompt;
}

