/**
 * Pack CRM Data Models
 * 
 * Defines the data structures for tracking pack lifecycle, stages, and metadata.
 */

export type PackStage = 'idea' | 'validation' | 'scoring' | 'deep_dive' | 'build' | 'published';

export type StageStatus = 'not_started' | 'in_progress' | 'completed';

export type GateResult = 'pass' | 'fail';

export interface StageState {
  status: StageStatus;
  startedAt?: string; // ISO 8601 timestamp
  completedAt?: string; // ISO 8601 timestamp
  score?: number; // For validation and scoring stages
  gate?: GateResult; // For scoring stage
  researchArtifacts?: string[]; // For deep_dive stage
  publishedAt?: string; // For published stage
}

export interface PackStages {
  idea: StageState;
  validation: StageState;
  scoring: StageState;
  deep_dive: StageState;
  build: StageState;
  published: StageState;
}

export interface PackMetadata {
  regulationName: string;
  targetAudience: string[];
  price: number; // Price in cents (e.g., 19900 = $199.00)
  createdAt: string; // ISO 8601 timestamp
  updatedAt: string; // ISO 8601 timestamp
}

export interface PackResearch {
  researchCompleted: boolean;
  researchArtifacts: string[]; // Paths to research files (e.g., "pack-crm/research/genesis-mission-deep-dive.md")
  researchNotes: string; // Free-form notes
}

export interface PackDeployment {
  frontendDeployed: boolean;
  workerDeployed: boolean;
  stripeConfigured: boolean;
  r2Uploaded: boolean;
}

export interface PackGateDecisionNotes {
  validation?: string; // Why it passed/failed validation
  scoring?: string; // Justification for scores
  deep_dive?: string; // Summary of research conclusions
}

export interface PackCRM {
  ideaNotes: string | null; // Initial stream-of-consciousness idea dump
  icpSummary: string | null; // Who this is for
  primaryPainPoints: string[]; // Bullet list of pains
  valueHypothesis: string | null; // How the pack helps
  pricingNotes: string | null; // Thoughts on price points / packages
  competitionNotes: string | null; // Notes on the market landscape / competitors
  gateDecisionNotes: PackGateDecisionNotes; // Gate decision justifications
}

export interface PackLifecycle {
  slug: string; // URL-friendly identifier (e.g., "genesis-mission", "tax-assist")
  name: string; // Display name (e.g., "Genesis Mission Readiness Pack")
  packNumber: number; // Sequential pack number (1, 2, 3, ...)
  currentStage: PackStage;
  stages: PackStages;
  metadata: PackMetadata;
  research: PackResearch;
  deployment: PackDeployment;
  crm: PackCRM; // CRM fields for idea + research + pipeline tracking
}

/**
 * Creates a default StageState with 'not_started' status
 */
export function createDefaultStageState(): StageState {
  return {
    status: 'not_started',
  };
}

/**
 * Creates default PackStages with all stages set to 'not_started'
 */
export function createDefaultPackStages(): PackStages {
  return {
    idea: createDefaultStageState(),
    validation: createDefaultStageState(),
    scoring: createDefaultStageState(),
    deep_dive: createDefaultStageState(),
    build: createDefaultStageState(),
    published: createDefaultStageState(),
  };
}

/**
 * Creates default PackCRM with empty/null values
 */
export function createDefaultPackCRM(): PackCRM {
  return {
    ideaNotes: null,
    icpSummary: null,
    primaryPainPoints: [],
    valueHypothesis: null,
    pricingNotes: null,
    competitionNotes: null,
    gateDecisionNotes: {},
  };
}

/**
 * Creates a new PackLifecycle with default values
 */
export function createDefaultPackLifecycle(
  slug: string,
  name: string,
  packNumber: number,
  regulationName: string,
  targetAudience: string[],
  price: number
): PackLifecycle {
  const now = new Date().toISOString();
  
  return {
    slug,
    name,
    packNumber,
    currentStage: 'idea',
    stages: createDefaultPackStages(),
    metadata: {
      regulationName,
      targetAudience,
      price,
      createdAt: now,
      updatedAt: now,
    },
    research: {
      researchCompleted: false,
      researchArtifacts: [],
      researchNotes: '',
    },
    deployment: {
      frontendDeployed: false,
      workerDeployed: false,
      stripeConfigured: false,
      r2Uploaded: false,
    },
    crm: createDefaultPackCRM(),
  };
}

