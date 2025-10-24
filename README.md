# AIES: AI Economy Simulator

A web-based simulation platform where Large Language Models (LLMs) act as autonomous economic agents with hidden information. Researchers can study emergent behaviors like negotiation, trust formation, and their effects on reservation prices and economic outcomes.

## Overview

AIES enables researchers to model complex economic and social systems by defining agent motivations ("culture"), needs, and desires through system prompts. Unlike traditional agent-based models that use rigid rules, AIES leverages LLMs to capture nuanced human behavior driven by imperfect information, negotiation, cultural values, and interpersonal dynamics.

## Key Features

- **Real-time Economic Simulation**: Agents negotiate and trade resources based on their cultural profiles and needs
- **Interactive Dashboard**: Monitor agent interactions, track subjective economic value, and analyze negotiation patterns
- **Configurable Parameters**: Adjust global settings (temperature, day length) and individual agent characteristics
- **LLM-Powered Decision Making**: Agents evaluate trade offers using AI, enabling emergent behaviors and authentic economic dynamics
- **Research-Ready Output**: Comprehensive event logs for post-simulation analysis

## Technology Stack

- **Frontend**: Next.js 14+ with TypeScript, Tailwind CSS, and shadcn/ui
- **Backend**: FastAPI (Python) with WebSocket support for real-time updates
- **AI Integration**: Google AI Python SDK with Gemini models
- **Visualization**: Recharts for economic value graphs and agent interaction diagrams

## Target Users

- Researchers in economics, sociology, and computer science
- Economists studying market dynamics and behavior
- Students and educators in relevant academic fields
- Policymakers interested in simulating economic scenarios

## Development Timeline

Following BMAD-methodology (4-phase model):
- **Phase 1-2**: Requirements analysis and planning (Week 44)
- **Phase 3**: Solution architecture and UI/UX design (Weeks 45-46)
- **Phase 4**: Development and deployment (Weeks 47-48)

## Repository Structure

This repository contains the complete AIES platform implementation, including frontend components, backend simulation engine, and AI integration modules.

---

*Repository for SG-418 – IBE160 Programmering med KI.*
