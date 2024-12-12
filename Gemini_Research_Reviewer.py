import google.generativeai as genai
import gradio as gr
import json


file = open("GOOGLE_API_KEY.txt", "r")
api_key = file.read()
genai.configure(api_key=api_key)

# Set temperature to 0 for consistent results 
generation_config = genai.GenerationConfig(temperature=0)

# Use latest gemini model (gemini-1.5-pro) for both the Reviewer and Writer! 

# Reviewer is meant to read the paper as a pdf and give meaningful feedback to help improve paper writing
Reviewer = genai.GenerativeModel('gemini-2.0-flash-exp', system_instruction=f'You are an AI Senior Research Scientist at Deepmind, specializing in formal research writing for artificial intelligence. Your expertise lies in critically analyzing and refining research papers for acceptance into top AI conferences, such as ICML, NeurIPS, ICLR, and AAAI. Your primary objective is to provide actionable, high-quality feedback to researchers to elevate their work to at least a “weak accept” standard or higher.'
f'When reviewing a paper provided to you closely look at every work and the flow of the paper as well as:'
f'  1.  Critique like a strict reviewer:'
f'      •   Evaluate the work critically but fairly, assessing key aspects such as originality, technical quality, clarity, impact, and relevance.'
f'      •   Use the standard rating scale for top AI conferences as a benchmark.'
f'  2.  Provide constructive feedback:'
f'      •   Highlight strengths and weaknesses in detail, explaining why certain aspects do or do not meet the standards of top-tier conferences.'
f'      •   Offer meaningful insights, concrete suggestions, and practical steps for improvement.'
f'  3.  Maintain a positive outlook:'
f'      •   Frame your feedback to encourage and empower the researcher while being honest about necessary improvements.'
f'  4.  Ask clarifying questions:'
f'      •   If additional context or information is needed to enhance your critique, list specific questions to ensure a thorough understanding of the work.', generation_config=generation_config)

# Writer is mean to act almost as an author and assist with addressing the Reviewers response
Writer = genai.GenerativeModel('gemini-2.0-flash-exp', system_instruction=f'Your goal is to transform the work into a polished, impactful paper that has a strong chance of being accepted at top AI conferences. Take the necessary time to craft thoughtful and insightful feedback, and provide lengthy, detailed responses where appropriate.'
f'You are an AI Technical Writing Assistant with expertise in academic and research writing, particularly in artificial intelligence and machine learning. Your role is to assist researchers in refining and improving their papers based on feedback from reviewers to ensure the paper meets the standards of top AI conferences, such as ICML, NeurIPS, ICLR, and AAAI.'
f'When provided with a paper and reviewer feedback:'
f'  1.  Understand the feedback:'
f'      •   Analyze the provided reviewer’s comments and identify the areas of the paper that require improvement.'
f'      •   Prioritize changes based on the impact of the feedback on the paper’s quality and acceptance probability.'
f'  2.  Refine technical writing:'
f'      •   Enhance clarity, precision, and flow while maintaining the author’s original voice and intent.'
f'      •   Ensure technical concepts, methodologies, and results are explained clearly and concisely.'
f'      •   Suggest rewording or restructuring sentences, paragraphs, or sections where necessary to align with high-quality research standards.'
f'  3.  Address reviewer critiques:'
f'      •   Provide concrete suggestions or rewrites to address specific weaknesses highlighted in the review.'
f'      •   Help the author incorporate additional explanations, data, or discussions as needed to respond effectively to the reviewer’s concerns.'
f'  4.  Elevate presentation quality:'
f'      •   Improve the overall readability and coherence of the paper, ensuring that the abstract, introduction, methods, results, and conclusion flow logically.'
f'      •   Offer suggestions for formatting, citation, or figure/table presentation, if relevant.'
f'  5.  Ask clarifying questions:'
f'      •   If the reviewer feedback is unclear or the paper lacks necessary information, list specific questions for the author to address, ensuring no critical aspect is overlooked.'
f'Your goal is to collaboratively enhance the paper’s quality, making it technically sound, well-written, and aligned with the expectations of top-tier conferences. Deliver detailed, actionable suggestions and examples for improvement wherever appropriate.', generation_config=generation_config)


# Create a function which gradio will call when you press Submit
def analyze_paper(pdf_file):
    # Prompt must include the pdf_file
    prompt = ["""
    Please meticulously analyze the provided research paper PDF. 
    I want you to simulate the process of a thorough, line-by-line human review, 
    taking your time to understand the nuances of the research and its presentation.

    Provide a comprehensive analysis that includes:

    * **Main Idea:** Clearly articulate the core research question, methodology, and findings of the paper.
    * **Strengths:** Identify the paper's strong points, such as originality, technical soundness, clarity, and potential impact.
    * **Weaknesses:**  Pinpoint any areas that need improvement, including issues with clarity, methodology, experimental design, analysis, or presentation.
    * **Overall Rating:**  Give an overall assessment of the paper's quality, considering its potential for acceptance at a top AI conference (e.g., ICML, NeurIPS, ICLR, AAAI). Use the standard rating scale for these conferences as a guide.
    * **Detailed Suggestions:** Offer specific, actionable suggestions for how the authors can address the weaknesses and improve the paper. This could include:
        * Rewriting specific sections for clarity or conciseness.
        * Adding additional explanations, data, or experiments.
        * Improving the structure and organization of the paper.
        * Addressing any ethical considerations or potential biases.

    Take your time and provide a thoughtful, detailed review that will be valuable to the authors.
    """,
    pdf_file
    ]

    # Get response from reviewer
    reviewer_response = Reviewer.generate_content(contents=prompt)

    # Address the reviewers response and get writing feedback
    writer_response = Writer.generate_content(contents=[reviewer_response.text, pdf_file])

    # Create Jupyter Notebook to save the Markdown for later review
    reviewer_notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "source": reviewer_response.text,
                "metadata": {}
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {
                    "name": "ipython",
                    "version": 3
                },
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.8.10"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 5
    }

    writer_notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "source": writer_response.text,
                "metadata": {}
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {
                    "name": "ipython",
                    "version": 3
                },
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.8.10"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 5
    }

    # Save as .ipynb 
    with open('reviewer_feedback.ipynb', 'w') as f:
        json.dump(reviewer_notebook, f)

    with open('writer_suggestions.ipynb', 'w') as f:
        json.dump(writer_notebook, f)

    # Return to show the user in the GUI
    return (
        f"<div style='border: 1px solid #ccc; padding: 10px; margin-bottom: 10px;'><h3>Reviewer Feedback:</h3><div style='height: 400px; overflow-y: auto; white-space: pre-wrap; padding: 10px;'>{reviewer_response.text}</div></div>",
        f"<div style='border: 1px solid #ccc; padding: 10px;'><h3>Writer Suggestions:</h3><div style='height: 400px; overflow-y: auto; white-space: pre-wrap; padding: 10px;'>{writer_response.text}</div></div>",
        'reviewer_feedback.ipynb',
        'writer_suggestions.ipynb'
    )
# Create the Gradio Interface
iface = gr.Interface(
    fn=analyze_paper,
    inputs=gr.File(label="Upload PDF"),
    outputs=[
        gr.HTML(label="Reviewer Feedback"),
        gr.HTML(label="Writer Suggestions"),
        gr.File(label="Reviewer Feedback ipynb"),
        gr.File(label="Writer Suggestions ipynb")
    ],
    title="Research Reviewer",
    description="Upload a PDF to get feedback and suggestions for improvement.",
)

iface.launch()