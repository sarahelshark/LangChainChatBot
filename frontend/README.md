# Basic Digital Assistant Frontend
***LangChain and OpenAI / Gemini***

This is the frontend branch for the RAG based Digital Assistant. Please push all frontend changes to this branch only.

## Project Structure

- `public/`: Contains public assets
  - `favicon.ico`: Favicon for the website
  - `index.html`: Main HTML file
  - `manifest.json`: Web app manifest file
  - `robots.txt`: Robots exclusion protocol file
- `src/`: Source code directory
  - `components/`: React components 
  - `hooks/`: Custom React hooks 
  - `utils/`: Utility functions
  - `App.js`: Main React component
  - `index.css`: Main CSS file
  - `index.js`: Entry point for React app
- `package.json`: NPM package configuration
- `package-lock.json`: Locked versions of NPM packages
- `postcss.config.js`: PostCSS configuration
- `tailwind.config.js`: Tailwind CSS configuration
- `.gitignore`: Git ignore file, of which you have a sample @.sample_gitignore.txt
- `README.md`: This file

## Setup

1. Install dependencies:
   ```
   npm install
   ```

2. Start the development server:
   ```
   npm start
   ```

3. Open `http://your_local_host` to view it in the browser.

## Available Scripts

In the project directory, you can run:

- `npm start`: Runs the app in development mode
- `npm test`: Launches the test runner
- `npm run build`: Builds the app for production (not suggested yet)

## Features

- React-based frontend for the RAG based Digital Assistant
- Integration with LangChain and OpenAI/Gemini backends (WIP ollama embeddings)
- Responsive design using Tailwind CSS

## Dependencies

- React
- Tailwind CSS



