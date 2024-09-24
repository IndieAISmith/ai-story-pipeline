# AI Story Pipeline

This project implements an AI-powered story generation and visualization pipeline. It uses various AI models to generate a story, extract characters and scenes, and create corresponding images.

## Features

- Story generation using GPT-based models
- Character extraction and description
- Scene extraction from the generated story
- Image generation for characters and scenes
- Conversation history management

## Prerequisites

- Python 3.x
- Required Python packages (install using `pip install -r requirements.txt`):
  - dotenv
  - groq
  - requests
  - logging

## Setup

1. Clone the repository:
   ```shell git clone https://github.com/IndieAISmith/ai-story-pipeline.git
   cd ai-story-pipeline
   ```
2. Install the required packages:
   ```shell
    pip install -r requirements.txt
   ```
3. Set up your environment variables:
Create a `.env` file in the project root and add your API keys:
``` shell GROQ_API_KEY=your_groq_api_key_here ```

## Usage

Run the main script to start the story generation pipeline:
python app.py

The script will:
1. Generate a story
2. Extract characters
3. Generate character descriptions
4. Extract scenes
5. Generate image prompts for each scene
6. Create images based on the prompts

## Project Structure
- `app.py`: Main application file
## Output

- Generated images will be saved as `images_of_scene{number}.png`
- Conversation history will be saved in `history.json`

## Logging

Logs are written to `app.log` for debugging and tracking the application's execution.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- GPT-4 for story generation
- Groq for API services
- AiForce for image generation
