# Fine-tuning Gemma Models for PDF Chat

This repository contains code for fine-tuning Google's Gemma 3 models on custom datasets, specifically designed for building a PDF chatbot that can answer questions about documents.

## Project Overview

This project demonstrates how to:
- Fine-tune Google's Gemma 3 models with LoRA (Low-Rank Adaptation)
- Process custom datasets for instruction tuning
- Optimize training for lower memory usage
- Deploy the fine-tuned model for chatting with PDF content

## Environment Setup

This project uses `uv`, a fast Python package installer and environment manager, for dependency management.

### Prerequisites

- Python 3.11 or newer
- CUDA-compatible GPU (recommended)
- Git

### Setting Up the Environment

1. **Install uv**

```bash
pip install uv
```

2. **Clone the repository**

```bash
git clone https://github.com/yourusername/pdf-chatter-fine-tuning.git
cd pdf-chatter-fine-tuning
```

3. **Create and activate virtual environment**

```bash
uv venv
uv venv activate
```

4. **Install dependencies**

```bash
uv pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
uv sync
```

## Dataset Preparation

The project expects data in a JSON Lines (.jsonl) format with the following structure:

```json
{"instruction": "Your instruction here", "context": "Optional context", "response": "Expected response"}
```

You can prepare your own dataset by:
1. Extracting text from PDFs
2. Creating instruction-response pairs
3. Saving them in the JSONL format

## Fine-tuning Process

### HuggingFace Access

1. Set up a HuggingFace account
2. Accept the Gemma model terms at https://huggingface.co/google/gemma-3-1b-it
3. Get your HuggingFace token and update it in the script

### Running Fine-tuning

```bash
uv run test.py
```

The script includes:
- Memory-efficient configuration (4-bit quantization)
- LoRA parameters for efficient adaptation
- Gradient checkpointing and accumulation for larger batch sizes

## Technical Details

### Models Used
- Base model: `google/gemma-3-1b-it`
- Training architecture: LoRA fine-tuning

### Key Dependencies
- `transformers`: For working with transformer models
- `peft`: Implements LoRA for parameter-efficient fine-tuning
- `bitsandbytes`: Used for 4-bit quantization
- `datasets`: For dataset handling
- `torch`: Deep learning framework

### Memory Optimization Techniques
- 4-bit quantization
- Gradient checkpointing
- Gradient accumulation
- Memory-efficient optimizers

## PDF Chat Integration

The fine-tuned model can be integrated with the PDF chatbot by:
1. Loading the fine-tuned model
2. Extracting content from PDFs
3. Building a retrieval system to locate relevant document sections
4. Using the fine-tuned model to generate responses based on PDF context

## Limitations

- Training time depends on GPU memory and available compute resources
- Larger models may require more aggressive memory optimization
- Response quality depends on the quality and diversity of the training data
