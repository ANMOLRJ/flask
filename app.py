from flask import Flask
import re
import long_responses as long

app = Flask(__name__)

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

#@app.route("/avg/<int:a>")
#def avg(a):
        #return "(a)/2"
@app.route("/get_response/<string:user_input>")   

def get_response(user_input):
    split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
    response = check_all_messages(split_message)
    return response

def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True

    # Counts how many words are present in each predefined message
    for word in user_message:
        if word in recognised_words:
            message_certainty += 1

    # Calculates the percent of recognised words in a user message
    percentage = float(message_certainty) / float(len(recognised_words))

    # Checks that the required words are in the string
    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break

    # Must either have the required words, or be a single response
    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0


def check_all_messages(message):
    highest_prob_list = {}

    # Simplifies response creation / adds it to the dict
    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    # Responses -------------------------------------------------------------------------------------------------------
    response('Hi,<br>  @#%EndRes%#@$  Looking for a job?*#&EndSug*&$#  Information regarding Letmegrab *#&EndSug*&$#  How to apply? *#&EndSug*&$#  Track your application ', ['hello', 'hi','hola', 'hey', 'sup', 'heyo','namaste','gm','ge','gf','good morning','good afternoon','good evening'], single_response=True)
    response('See you! @#%EndRes%#@$ ', ['bye', 'goodbye','gn','goodnight','night'], single_response=True)
    response(' Im doing fine, and you? @#%EndRes%#@$  ', ['how', 'are', 'you', 'doing'], required_words=['how','are'])

    response('  Please visit <a style="color:blue" href="carrer@letmegrab.com"> https://alphacareer.letmegrab.in/ </a> and click on the jobs tab on the main page. Here you will find the list of available jobs and you can click on the apply button to apply for the chosen available job. @#%EndRes%#@$  ', ['how', 'to', 'apply'], required_words=['how','apply'])
    
    response('Please choose from the following options @#%EndRes%#@$  About Letmegrab *#&EndSug*&$#  How do we work? *#&EndSug*&$#  Work-life philosophy *#&EndSug*&$#  Employee conduct *#&EndSug*&$#  Employee privileges *#&EndSug*&$#  Salient services at Letmegrab ', ['information', 'regarding','letmegrab'], required_words=['information','letmegrab'])
    
    response('We have the following available positions open to work at Letmegrab  @#%EndRes%#@$  Junior PHP Developer *#&EndSug*&$#  React Developer *#&EndSug*&$#  Jr. Android Developer *#&EndSug*&$#  Testing *#&EndSug*&$#  HR Executive *#&EndSug*&$#  Sr. Sales Manager *#&EndSug*&$#  Jr. Sales Manager *#&EndSug*&$# Digital Marketing *#&EndSug*&$#  Field Marketing ', ['I', 'am', 'looking',' for' ,'a', 'job'], required_words=['job'])
    response('If you are eligible and pursuing to work for any of the job positions,<br> please e-mail us your resume on <a style="color:blue" href="carrer@letmegrab.com">carrer@letmegrab.com </a>. <br> please click on this link:-<a style="color:blue" href="https://alphacareer.letmegrab.in/">https://alphacareer.letmegrab.in/ </a> to know more about Letmegrab and how we work. @#%EndRes%#@$', ['interested', 'php', 'ui', 'sales', 'hr','react developer','react','android','developer','testing','marketing'], single_response=True)
    response('We hope to see you soon. Is there anything else I can help you with?', ['ok'], single_response=True)
    #response('Hi,<br> Glad to have you here. What are you looking for? @#%EndRes%#@$ 1. Looking for a job?  *#&EndSug*&$#2. Information regarding Letmegrab*#&EndSug*&$#3. How to apply?*#&EndSug*&$#4. Track your application', ['ok'], single_response=True)
    response('Thank you, Have a great day ahead!', ['thank', 'thanks','thankyou','no'], single_response=True)
   # response('Thank you!', ['i', 'love', 'code', 'palace'], required_words=['code','palace'])
    response('You are required to fill the form and go through the registration process.<br> link:- <a style="color:blue" href="carrer@letmegrab.com"> https://alphacareer.letmegrab.in/ </a>', ['salary', 'offered'], single_response=True)

    # Longer responses
    response(long.R_ADVICE, ['give', 'advice'], required_words=['advice'])
    response(long.R_EATING, ['what', 'you', 'eat'], required_words=['you', 'eat'])

    best_match = max(highest_prob_list, key=highest_prob_list.get)
    # print(highest_prob_list)
    # print(f'Best match = {best_match} | Score: {highest_prob_list[best_match]}')

    return long.unknown() if highest_prob_list[best_match] < 1 else best_match


# Used to get the response


# Testing the response system
#while True:
    #print('Bot: ' + get_response(input('You: ')))
    

#def hello_world():
   # return "<p>Hello, Anmol</p>" 



if __name__ =="__main__":
    app.run(debug=True)
