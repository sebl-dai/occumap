"""Global configuration for OccuMap."""

import os

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

MODEL = "claude-sonnet-4-6"
PROMPT_VERSION = "v1.3"
CONFIDENCE_THRESHOLD = 0.75
MAJORITY_VOTE_RUNS = 3
BATCH_SIZE = 5
TOP_N_CANDIDATES = 15

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
