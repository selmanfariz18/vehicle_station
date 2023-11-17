from django.shortcuts import render,redirect
import openai
import re
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from pyjarowinkler import distance as get_similarity


openai.api_key = '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'
key = openai.api_key


def root_page(request):
    return render(request, 'root_page.html')

import ast
with open('chatbot\DCT7.txt','r') as file:
    lines=file.read()
# Original string representation
string_representation = lines
# Use ast.literal_eval to safely convert the string to a list
all_data = ast.literal_eval(string_representation)

def generate_response(customer_question, all_data):
    """
    Generate a response based on the customer's question and provided data.

    Args:
    - customer_question (str): Customer's question including error code.
    - all_data (list): List of dictionaries containing error code information.

    Returns:
    - str: Generated response using OpenAI's model.
    """


    # Sample conversation prompt
    prompt = """
    i am a mechanic and i get a car's obd reading as"""+customer_question+"""what the problem and can you give fix solutions?"""

    # Request the model to continue the conversation as MEC (AI Car Mechanic)
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
    )
    generated_response = response['choices'][0]['text']
    print("Generated Response:", generated_response)
    return generated_response

# Chatbot view integrating PDF serving logic
def chatbot_view(request):
    if request.method == 'POST':

        if key:
            try:
                response = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt="ping",
                    max_tokens=50  # Define the max tokens as needed
                )
                # Use the response from OpenAI API as needed
                pass
            except openai.error.AuthenticationError:
                messages.error(request, "API invalid.")
                return HttpResponseRedirect(reverse("home"))


        obd_code = request.POST.get("obd_code")

        if obd_code == '':
            messages.error(request, "Please select an obd code.")
            return HttpResponseRedirect(reverse("home"))
        else:

            context = {
                'obd_codes': all_data,
            }
            response = generate_response(obd_code, all_data)

            context = {
                'response': response,
            }
            return render(request, 'solution.html', context)

    context = {
        'obd_codes': all_data,
    }

    return render(request, 'home.html', context)


def login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(
            request=request, username=username, password=password)
        if user is not None:
            if user.is_superuser:
                messages.error(request, "Error in login")
                return render(request, 'login.html')
            else:
                auth_login(request, user)
                return HttpResponseRedirect(reverse("home"))
        else:
            messages.error(request, "Error in login")
            return render(request, 'login.html')
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    messages.success(request, "Logout Successfull!")
    return render(request, 'root_page.html')

def register(request):

    if request.method == 'POST':
        # get form data
        username = request.POST['username']
        email=request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']



        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username is already taken')
                return redirect('register')
            else:
                # create user and profile objects
                user = User.objects.create_user(
                    username=username, password=password,email=email)
                user.save()
                messages.success(request, 'Account created successfully.')
                return render(request, 'login.html')

        else:
            messages.info(request, 'Both passwords are not matching')
            return redirect('register')

    return render(request, 'register.html')

def sub(request):
    if request.method=='POST':
            user_input=request.POST.get('user_input')
            # Function to calculate Jaro-Winkler similarity between two strings
            def calculate_similarity(string1, string2):
                return get_similarity.get_jaro_distance(string1, string2, winkler=True)

            # Function to find the most similar data based on the Jaro-Winkler similarity
            def find_most_similar_data(query_text, data_list):
                # Calculate the similarity scores for each data point
                similarity_scores = [(data, calculate_similarity(query_text, data['description'])) for data in data_list]
                
                # Sort the data points based on similarity scores
                sorted_data = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
                
                # Return the most similar data
                return sorted_data[0][0] if sorted_data else None

            # Find the most similar data based on the user input
            most_similar_data = find_most_similar_data(user_input, all_data)

            
            if most_similar_data:
                return redirect('solution', odb_code=most_similar_data.get('code'))
            else:
                return render (request,'home.html')
    return render(request,'home.html')
def solution(request, odb_code):
    prompt = "i am a mechanic and i get a car's obd reading as"+odb_code+"what the problem and can you give fix solutions?"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
    )
    generated_response = response['choices'][0]['text']
    return render(request, 'solution.html',{'response':generated_response})


