/**
 * Pack Lifecycle Management
 * 
 * Handles stage transitions and lifecycle state updates.
 */

import { PackStage, PackLifecycle, StageState, GateResult } from './models';
import { getPack, updatePack } from './store';

export interface AdvanceStageOptions {
  score?: number;
  gate?: GateResult;
  note?: string;
  researchArtifacts?: string[];
}

/**
 * Advances a pack to a target stage
 * 
 * Updates:
 * - currentStage to targetStage
 * - stages[targetStage].status to 'completed' (or 'in_progress' if not yet started)
 * - stages[targetStage].startedAt (if not set)
 * - stages[targetStage].completedAt
 * - stages[targetStage].score (if provided)
 * - stages[targetStage].gate (if provided)
 * - stages[targetStage].researchArtifacts (if provided)
 * - metadata.updatedAt
 * 
 * @param slug Pack slug
 * @param targetStage Target stage to advance to
 * @param options Optional: score, gate, note, researchArtifacts
 * @returns Updated PackLifecycle, or undefined if pack not found
 */
export function advancePackStage(
  slug: string,
  targetStage: PackStage,
  options?: AdvanceStageOptions
): PackLifecycle | undefined {
  const pack = getPack(slug);
  
  if (!pack) {
    return undefined;
  }
  
  const stage = pack.stages[targetStage];
  const now = new Date().toISOString();
  
  // Update stage state
  const updatedStage: StageState = {
    ...stage,
    status: 'completed',
    startedAt: stage.startedAt || now,
    completedAt: now,
  };
  
  // Apply score if provided (for validation/scoring stages)
  if (options?.score !== undefined) {
    updatedStage.score = options.score;
  }
  
  // Apply gate if provided (for scoring stage)
  if (options?.gate !== undefined) {
    updatedStage.gate = options.gate;
  }
  
  // Apply research artifacts if provided (for deep_dive stage)
  if (options?.researchArtifacts !== undefined) {
    updatedStage.researchArtifacts = options.researchArtifacts;
  }
  
  // Set publishedAt for published stage
  if (targetStage === 'published') {
    updatedStage.publishedAt = now;
  }
  
  // Update the pack
  const updated = updatePack(slug, {
    currentStage: targetStage,
    stages: {
      ...pack.stages,
      [targetStage]: updatedStage,
    },
    // Update research if deep_dive is completed
    research: targetStage === 'deep_dive' && options?.researchArtifacts
      ? {
          ...pack.research,
          researchCompleted: true,
          researchArtifacts: [
            ...pack.research.researchArtifacts,
            ...options.researchArtifacts,
          ],
        }
      : pack.research,
  });
  
  return updated;
}

/**
 * Gets the next stage after the current one
 * Returns undefined if already at the last stage
 */
export function getNextStage(currentStage: PackStage): PackStage | undefined {
  const stages: PackStage[] = ['idea', 'validation', 'scoring', 'deep_dive', 'build', 'published'];
  const currentIndex = stages.indexOf(currentStage);
  
  if (currentIndex === -1 || currentIndex === stages.length - 1) {
    return undefined;
  }
  
  return stages[currentIndex + 1];
}

/**
 * Gets the previous stage before the current one
 * Returns undefined if already at the first stage
 */
export function getPreviousStage(currentStage: PackStage): PackStage | undefined {
  const stages: PackStage[] = ['idea', 'validation', 'scoring', 'deep_dive', 'build', 'published'];
  const currentIndex = stages.indexOf(currentStage);
  
  if (currentIndex <= 0) {
    return undefined;
  }
  
  return stages[currentIndex - 1];
}

/**
 * Checks if a pack can advance to a target stage
 * Returns true if the target stage is the next logical stage or a later stage
 */
export function canAdvanceToStage(currentStage: PackStage, targetStage: PackStage): boolean {
  const stages: PackStage[] = ['idea', 'validation', 'scoring', 'deep_dive', 'build', 'published'];
  const currentIndex = stages.indexOf(currentStage);
  const targetIndex = stages.indexOf(targetStage);
  
  if (currentIndex === -1 || targetIndex === -1) {
    return false;
  }
  
  // Can advance to any stage that's at or after the current stage
  return targetIndex >= currentIndex;
}

