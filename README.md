# OccuMap

An LLM-based occupation classifier that maps dirty CRM job titles to Singapore's 
Standard Occupational Classification (SSOC 2024), categorising union members as 
PME (Professional, Manager, Executive), Technician, or Rank-and-File.

## Problem
Union member occupation fields in CRM systems are free-text and highly inconsistent. 
Without a reliable PME/RNF classification, targeted outreach and policy advocacy 
for Singapore's increasingly PME-heavy workforce is difficult.

## Solution
OccuMap uses LLM reasoning against SSOC 2024 definitions to classify any occupation 
title — however messy — into one of three categories with a confidence score and 
human-readable reasoning. Low-confidence cases are flagged for human review.

## Classification Logic
- **PME** — SSOC Major Groups 1 (Managers) and 2 (Professionals)
- **T** — SSOC Major Group 3 (Technicians & Associate Professionals)  
- **RNF** — SSOC Major Groups 4–9
- **NA** — Unclassifiable (retired, self-employed, blank, etc.)

## Stack
- Python + Ollama (local development)
- Snowflake Cortex (production)
- Streamlit (review UI)

## Status
🚧 In development