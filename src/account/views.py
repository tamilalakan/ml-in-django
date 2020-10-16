from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from account.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
# NLP Pkgs
import spacy 
nlp = spacy.load('en_core_web_sm')
# Pkgs for Normalizing Text
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
# Import Heapq for Finding the Top N Sentences
from heapq import nlargest

from bs4 import BeautifulSoup
from urllib.request import urlopen



def registration_view(request):
	context = {}
	if request.POST:
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			email = form.cleaned_data.get('email')
			raw_password = form.cleaned_data.get('password1')
			account = authenticate(email=email, password=raw_password)
			if account is not None:
				login(request, account)
				return redirect('home')
		else:
			context['registration_form'] = form
	else:
		form = RegistrationForm()
		context['registration_form'] = form
	return render(request, 'account/register.html',context)





def logout_view(request):
	logout(request)
	return redirect('home')





def login_view(request):
	context = {}

	user = request.user
	if user.is_authenticated:
		return redirect("home")

	if request.POST:
		form = AccountAuthenticationForm(request.POST)
		if form.is_valid():
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)

			if user:
				login(request, user)
				return redirect("home")

	else:
		form = AccountAuthenticationForm()

	context['login_form'] = form
	return render(request, 'account/login.html',context)




def account_view(request):
	if not request.user.is_authenticated:
		return redirect("login")

	context = {}

	if request.POST:
		form = AccountUpdateForm(request.POST, instance=request.user)
		if form.is_valid():
			form.initial = {
					"email": request.POST['email'],
					"username": request.POST['username'],
					}
			form.save()
			context['success_message'] = "update"
			
			


	else:
		form = AccountUpdateForm(
				initial={
					"email": request.user.email,
					"username": request.user.username,
				}
			)

	context['account_form'] = form
	return render(request, 'account/account.html',context)



# Design
def project_view(request):
	return render(request,'account/project.html')

def project_sum(request):
	return render(request,'account/project_summerize.html')

def upload(request):
	return render(request, 'account/upload.html')

def url_view(request):
	return render(request,'account/url_summerize.html')



# Default Summerizer
def text_summarizer(raw_docx):
    raw_text = raw_docx
    docx = nlp(raw_text)
    stopwords = list(STOP_WORDS)
    # Build Word Frequency # word.text is tokenization in spacy
    word_frequencies = {}  
    for word in docx:  
        if word.text not in stopwords:
            if word.text not in word_frequencies.keys():
                word_frequencies[word.text] = 1
            else:
                word_frequencies[word.text] += 1

    maximum_frequncy = max(word_frequencies.values())

    for word in word_frequencies.keys():  
        word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)
    # Sentence Tokens
    sentence_list = [ sentence for sentence in docx.sents ]

    # Sentence Scores
    sentence_scores = {}  
    for sent in sentence_list:  
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if len(sent.text.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word.text.lower()]
                    else:
                        sentence_scores[sent] += word_frequencies[word.text.lower()]

    summarized_sentences = nlargest(7, sentence_scores, key=sentence_scores.get)
    final_sentences = [ w.text for w in summarized_sentences ]
    text_summarizer.summary = ' '.join(final_sentences)

    return text_summarizer.summary





# Paragraph_Summerize
def result_view(request):
	if request.method == 'POST':
		result=""
		val1 = str(request.POST['num']) 
		for i in val1:
			result+=i
		
		text_summarizer(result)
		return render(request, "account/result.html", {"result1":text_summarizer.summary})


# Url_Summerize
def result_url(request):

	if request.method == 'POST':
		val1 = str(request.POST['num']) 
		page = urlopen(val1)
		soup = BeautifulSoup(page,'lxml')
		result_url.fetched_text = ''.join(map(lambda p:p.text,soup.find_all('p')))
		text_summarizer(result_url.fetched_text)
		return render(request, "account/result.html", {"result2":text_summarizer.summary})

# File_summerize
def result_file(request):

	if request.method == 'POST':
		upload_file = request.FILES['document']
		soup = BeautifulSoup(upload_file,'lxml')
		result_file.fetched_text = ''.join(map(lambda p:p.text,soup.find_all('p')))
		print(result_file.fetched_text)
		text_summarizer(result_file.fetched_text)
		return render(request, "account/result.html", {"result3":text_summarizer.summary})


		