from django.shortcuts import render,redirect
import openai
import re
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login



openai.api_key = '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'
key = openai.api_key


def root_page(request):
    return render(request, 'root_page.html')



# Sample data structure (list of dictionaries)
all_data = [
    {'code': 'P0101', 'description':	'Mass air flow (MAF) sensor circuit, range or performance problem','fix': ''},
    {'code': 'P0102', 'description':	'Mass air flow (MAF) sensor circuit, low input','fix': '102'},
    {'code': 'P0103', 'description':	'Mass air flow (MAF) sensor circuit, high input','fix': ''},
    {'code': 'P0106', 'description':	'Manifold absolute pressure (MAP) sensor circuit, range or performance problem','fix': ''},
    {'code': 'P0107', 'description':	'Manifold absolute pressure (MAP) sensor circuit, low input','fix': ''},
    {'code': 'P0108', 'description':	'Manifold absolute pressure (MAP) sensor circuit, high input','fix': ''},
    {'code': 'P0112', 'description':	'Intake air temperature (IAT) circuit, low input','fix': ''},
    {'code': 'P0113', 'description':	'Intake air temperature (IAT) circuit, high input','fix': ''},
    {'code': 'P0117', 'description':	'Engine coolant temperature (ECT) circuit, low input','fix': ''},
    {'code': 'P0118', 'description':	'Engine coolant temperature (ECT) circuit, high input','fix': ''},
    {'code': 'P0121', 'description':	'Throttle position sensor (TPS) circuit, range or performance problem','fix': ''},
    {'code': 'P0122', 'description':	'Throttle position sensor (TPS) circuit, low input','fix': ''},
    {'code': 'P0123', 'description':	'Throttle position sensor (TPS) circuit, high input','fix': ''},
    {'code': 'P0125', 'description':	'Insufficient coolant temperature for closed loop fuel control','fix': ''},
    {'code': 'P0131', 'description':	'Oxygen sensor circuit, low voltage (pre-converter sensor, left bank)','fix': ''},
    {'code': 'P0132', 'description':	'Oxygen sensor circuit, high voltage (pre-converter sensor, left bank)','fix': ''},
    {'code': 'P0133', 'description':	'Oxygen sensor circuit, slow response (pre-converter sensor, left bank)','fix': ''},
    {'code': 'P0134', 'description':	'Oxygen sensor circuit - no activity detected (pre-converter sensor, left bank)','fix': ''},
    {'code': 'P0135', 'description':	'Oxygen sensor heater circuit malfunction (pre-converter sensor, left bank)','fix': ''},
    {'code': 'P0137', 'description':	'Oxygen sensor circuit, low voltage (post-converter sensor, left bank)','fix': ''},
    {'code': 'P0138', 'description':	'Oxygen sensor circuit, high voltage (post-converter sensor, left bank)','fix': ''},
    {'code': 'P0140', 'description':	'Oxygen sensor circuit - no activity detected (post-converter sensor, left bank)','fix': ''},
    {'code': 'P0141', 'description':	'Oxygen sensor heater circuit malfunction (post-converter sensor, left bank)','fix': ''},
    {'code': 'P0143', 'description':	'Oxygen sensor circuit, low voltage (#2 post-converter sensor, left bank)','fix': ''},
    {'code': 'P0144', 'description':	'Oxygen sensor circuit, high voltage (#2 post-converter sensor, left bank)','fix': ''},
    {'code': 'P0146', 'description':	'Oxygen sensor circuit - no activity detected (#2 post-converter sensor, left bank)','fix': ''},
    {'code': 'P0147', 'description':	'Oxygen sensor heater circuit malfunction (#2 post-converter sensor, left bank)','fix': ''},
    {'code': 'P0151', 'description':	'Oxygen sensor circuit, low voltage (pre-converter sensor, right bank)','fix': ''},
    {'code': 'P0152', 'description':	'Oxygen sensor circuit, high voltage (pre-converter sensor, right bank)','fix': ''},
    {'code': 'P0153', 'description':	'Oxygen sensor circuit, slow response (pre-converter sensor, right bank)','fix': ''},
    {'code': 'P0154', 'description':	'Oxygen sensor circuit - no activity detected (pre-converter sensor, right bank)','fix': ''},
    {'code': 'P0155', 'description':	'Oxygen sensor heater circuit malfunction (pre-converter sensor, right bank)','fix': ''},
    {'code': 'P0157', 'description':	'Oxygen sensor circuit, low voltage (post-converter sensor, right bank)','fix': ''},
    {'code': 'P0158', 'description':	'Oxygen sensor circuit, high voltage (post-converter sensor, right bank)','fix': ''},
    {'code': 'P0160', 'description':	'Oxygen sensor circuit - no activity detected (post-converter sensor, right bank)','fix': ''},
    {'code': 'P0161', 'description':	'Oxygen sensor heater circuit malfunction (post-converter sensor, right bank)','fix': ''},
    {'code': 'P0171', 'description':	'System too lean, left bank','fix': ''},
    {'code': 'P0172', 'description':	'System too rich, left bank','fix': ''},
    {'code': 'P0174', 'description':	'System too lean, right bank','fix': ''},
    {'code': 'P0175', 'description':	'System too rich, right bank','fix': ''},
    {'code': 'P0300', 'description':	'Engine misfire detected','fix': ''},
    {'code': 'P0301', 'description':	'Cylinder number 1 misfire detected','fix': ''},
    {'code': 'P0302', 'description':	'Cylinder number 2 misfire detected','fix': ''},
    {'code': 'P0303', 'description':	'Cylinder number 3 misfire detected','fix': ''},
    {'code': 'P0304', 'description':	'Cylinder number 4 misfire detected','fix': ''},
    {'code': 'P0305', 'description':	'Cylinder number 5 misfire detected','fix': ''},
    {'code': 'P0306', 'description':	'Cylinder number 6 misfire detected','fix': ''},
    {'code': 'P0307', 'description':	'Cylinder number 7 misfire detected','fix': ''},
    {'code': 'P0308', 'description':	'Cylinder number 8 misfire detected','fix': ''},
    {'code': 'P0325', 'description':	'Knock sensor circuit malfunction','fix': ''},
    {'code': 'P0327', 'description':	'Knock sensor circuit, low output','fix': ''},
    {'code': 'P0336', 'description':	'Crankshaft position sensor circuit, range or performance problem','fix': ''},
    {'code': 'P0337', 'description':	'Crankshaft position sensor, low output','fix': ''},
    {'code': 'P0338', 'description':	'Crankshaft position sensor, high output','fix': ''},
    {'code': 'P0339', 'description':	'Crankshaft position sensor, circuit intermittent','fix': ''},
    {'code': 'P0340', 'description':	'Camshaft position sensor circuit','fix': ''},
    {'code': 'P0341', 'description':	'Camshaft position sensor circuit, range or performance problem','fix': ''},
    {'code': 'P0401', 'description':	'Exhaust gas recirculation, insufficient flow detected','fix': ''},
    {'code': 'P0404', 'description':	'Exhaust gas recirculation circuit, range or performance problem','fix': ''},
    {'code': 'P0405', 'description':	'Exhaust gas recirculation sensor circuit low','fix': ''},
    {'code': 'P0410', 'description':	'Secondary air injection system','fix': ''},
    {'code': 'P0418', 'description':	'Secondary air injection pump relay control circuit','fix': ''},
    {'code': 'P0420', 'description':	'Catalyst system efficiency below threshold, left bank','fix': ''},
    {'code': 'P0430', 'description':	'Catalyst system efficiency below threshold, right bank','fix': ''},
    {'code': 'P0440', 'description':	'Evaporative emission control system malfunction','fix': ''},
    {'code': 'P0441', 'description':	'Evaporative emission control system, purge control circuit malfunction','fix': ''},
    {'code': 'P0442', 'description':	'Evaporative emission control system, small leak detected','fix': ''},
    {'code': 'P0446', 'description':	'Evaporative emission control system, vent system performance','fix': ''},
    {'code': 'P0452', 'description':	'Evaporative emission control system, pressure sensor low input','fix': ''},
    {'code': 'P0453', 'description':	'Evaporative emission control system, pressure sensor high input','fix': ''},
    {'code': 'P0461', 'description':	'Fuel level sensor circuit, range or performance problem','fix': ''},
    {'code': 'P0462', 'description':	'Fuel level sensor circuit, low input','fix': ''},
    {'code': 'P0463', 'description':	'Fuel level sensor circuit, high input','fix': ''},
    {'code': 'P0500', 'description':	'Vehicle speed sensor circuit','fix': ''},
    {'code': 'P0506', 'description':	'Idle control system, rpm lower than expected','fix': ''},
    {'code': 'P0507', 'description':	'Idle control system, rpm higher than expected','fix': ''},
    {'code': 'P0601', 'description':	'Powertrain Control Module, memory error','fix': ''},
    {'code': 'P0602', 'description':	'Powertrain Control module, programming error','fix': ''},
    {'code': 'P0603', 'description':	'Powertrain Control Module, memory reset error','fix': ''},
    {'code': 'P0604', 'description':	'Powertrain Control Module, memory error (RAM)','fix': ''},
    {'code': 'P0605', 'description':	'Powertrain Control Module, memory error (ROM)','fix': ''},
    # Add more data points as needed
]

def get_vector(input_text):
    """
    Get an embedding vector for a given input using OpenAI's model.

    Args:
    - input_text (str): Input text for generating the embedding vector.

    Returns:
    - list: Embedding vector.
    """
    response = openai.Embed.create(
        model="text-embedding-ada-002",
        inputs=[input_text],
    )
    return response['data'][0]['embedding']

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





