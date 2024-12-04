# Gemini Research Reviewer

This project provides a powerful and efficient way for AI researchers to get instant feedback on their research papers directly from the latest Gemini model! It uses a Gradio GUI that allows you to upload your paper as a pdf and get out not only a review but also help with addressing and understanding that feedback as well! Providing feedback on the paper's strengths and weaknesses, suggest improvements, and even help refine the writing.

## Features

* **Automated Analysis:** Upload a PDF of your research paper and get instant feedback from an AI reviewer (Outputs typically take around 1-2 minutes).
* **Constructive Suggestions:** Receive concrete suggestions for improvement from an AI writing assistant.
* **Downloadable Outputs:** Directly download both the Reviewer and Writer model responses as a Jupyter notebooks (`.ipynb`) for later.

## Getting Started

In order to run the code you will need a [Gemini API key](https://ai.google.dev), once you have done this create a file called 'GOOGLE_API_KEY.txt' and paste the key. Then run the following commands:

   ```
   conda create -n reviewer python=3.9
   conda activate reviewer
   pip install -q -U google-generativeai
   pip install gradio
   ```

## Time to Run the Code!
To get your reviews all you have to do now is run this command:
   ```
   python Gemini_Research_Reviewer.py.py
   ```

## Future Work

- [ ]  Add chat implementation for interactive feedback (Chat with your reviewer)
- [ ]  Add more ability for customization (temperature, add to system prompt, etc.)

## Contributions
Contributions are welcome! Feel free to open issues for bug reports or feature requests. Pull requests are also encouraged for code improvements or new functionalities.

