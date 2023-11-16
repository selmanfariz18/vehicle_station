from django.shortcuts import render
import openai
import re
import PyPDF2
from django.http import HttpResponse

# Chatbot view integrating PDF serving logic
def chatbot_view(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input')

        openai.api_key = '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'

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt="You are troubleshooting a car problem.\nUser: " + user_input,
            max_tokens=50  # Adjust max_tokens as needed
        )

        bot_response = response['choices'][0]['text']

        # Extract keywords related to problem number from user input
        user_keywords = re.findall(r'problem (\d+)', user_input, re.IGNORECASE)

        # Use keywords to find matching problem number in bot's response
        matching_number = None
        for keyword in user_keywords:
            if keyword in bot_response.lower():
                matching_number = keyword
                break
        pdf_file = 'car_manual.pdf'
        page_number = find_keyword_page(pdf_file, matching_number)
        # If no problem number is found in the bot's response, continue with default behavior or prompt for clarification
        serve_pdf_page(request, page_number)

    return render(request, 'chatbot/chatbot.html', {'response': None})



def serve_pdf_page(request, problem_number):
    pdf_file = 'car_manual.pdf'  # Replace with your PDF file

    if problem_number is None:
        return HttpResponse("Page not found")  # Return a message if problem_number is None

    # Open the PDF file
    with open(pdf_file, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        total_pages = len(pdf_reader.pages)

        if problem_number <= total_pages:
            page = pdf_reader.pages[problem_number - 1]
            output = PyPDF2.PdfWriter()
            output.add_page(page)

            # Serve the extracted page as a response
            response = HttpResponse(content_type='application/pdf')
            output.write(response)
            return response

    return HttpResponse("Page not found")





def find_keyword_page(pdf_path, keyword):
    if keyword is None:
        return None  # Return None if the keyword is None

    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Iterate through each page in the PDF
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text = page.extract_text().lower()

            # Search for the keyword in the text content of the page
            if keyword.lower() in text:
                return page_num + 1

    return None