"""
Telemetry suite for Puppeteer orchestration.

Provides logging, reward shaping, and RL training capabilities.
"""

from orchestrator.telemetry.logger import OrchestratorLogger
from orchestrator.telemetry.reward import (
    RewardConfig,
    default_reward_config,
    compute_step_reward,
    compute_episode_reward,
)
from orchestrator.telemetry.rl_trainer import SimpleRLTrainer

__all__ = [
    "OrchestratorLogger",
    "RewardConfig",
    "default_reward_config",
    "compute_step_reward",
    "compute_episode_reward",
    "SimpleRLTrainer",
]

