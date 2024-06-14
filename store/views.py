from django.shortcuts import render, redirect
from .models import Test, Hangman, Hangman_category, Team, Stats, Link, Favorit_link, Post
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .forms import SignUpForm, PostForm, EditForm, EditProfileForm
from django import forms
from django.http import HttpRequest
import uuid
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
import subprocess


def home(request: HttpRequest):
    user_get = request.user

    context = {
        "user_get":user_get,
    }
    return render(request, "home.html", context)

def about(request):
    return render(request, "about.html", {})

def tildelt_nummer(request: HttpRequest):
    test1_ses = ""
    test_date_fra_get_ses = ""
    test_date_til_get_ses = ""
    message = None
    message2 = None
    message3 = None
    test1 = request.POST.get('test1')
    test_date_fra_get = request.POST.get('test_date_fra')
    test_date_til_get = request.POST.get('test_date_til')
    user_get = request.user
    condition = test1 and test_date_fra_get and test_date_til_get
    konstant = 30.44

    #   Gemmer i session. Ændr navn til variable:
    request.session['test1'] = request.POST.get('test1')
    request.session['test_date_fra'] = request.POST.get('test_date_fra')
    request.session['test_date_til'] = request.POST.get('test_date_til')

    if request.method == 'POST':
        # -- Calculation logic -- 
        if test_date_til_get != "" and test_date_fra_get != "":
            #   Convert string representations to datetime objects
            test_date_til_get = datetime.strptime(test_date_til_get, '%Y-%m-%d')  # Adjust the format as needed
            test_date_fra_get = datetime.strptime(test_date_fra_get, '%Y-%m-%d')  # Adjust the format as needed
            delta_dage = test_date_til_get - test_date_fra_get
            

            #   Cr8 if not none since site crashes if price has no input
            if test1 != "":
                #   Change test1 to int or float to avoid site crash
                test1 = int(test1)
                test1 = float(test1)
                udregning = (test1 / konstant) * delta_dage.days
                message2 = f"Kopier dette i log: Krediterer for tildelt nummer, hvor udregning er: ({test1} / {konstant}) * {delta_dage.days} = {udregning:.2f}."
                print(message2)
                test1_ses = request.session.get('test1', '')
                test_date_fra_get_ses = request.session.get('test_date_fra', '')
                test_date_til_get_ses = request.session.get('test_date_til', '')
                print(test_date_til_get_ses)
            else:
                message2 = f"{delta_dage.days}"    
        else:
            message2 = "Ingen udregning gives, da intet er udfyldt"
            
        if 'test_knap' in request.POST:
            #   Laver try da side crasher hvis man laver udregning uden at være logget ind.
            try:
                print("Nu gemmer jeg")
                udregning_str = "{:.2f}".format(udregning)
                test2 = Test(test1=test1, test_date_fra=test_date_fra_get, test_date_til=test_date_til_get, udregning_db=udregning_str, user=user_get)
                test2.save()


                #   Request get info fra inputfelter
                #   Bruger filter, da den sorterer i stedet for at gette. Get tager kun en query, hvis der derfor er to krediteringer som er fuldstændig ens og lavet af samme brugere, kan de begge nu printes.
                get_inputs = Test.objects.filter(test1=test1, test_date_fra=test_date_fra_get, test_date_til=test_date_til_get, udregning_db=udregning_str, user=user_get)
                #   Print id til variablen der henter
                #   Laver condition hvis der er flere rows i DB med samme indhold
                if get_inputs.count() > 1:
                    #   Henter ID og username fra den row der er lig med inputs
                    id_user_list = get_inputs.values_list('id', 'user__username')  # Retrieve IDs and usernames
                    #   Laver om til strings. Benytter for loop for at hente alle instanser
                    id_user_str_list = [f"{id} ({username})" for id, username in id_user_list]  # Format IDs and usernames into strings
                    #   Syntaks formattering
                    id_user_str = ', '.join(id_user_str_list)  # Join formatted strings with commas
                    #   Output som f-string
                    message3 = f"Der er flere id'er med dette indhold, vælg en vilkårlig {id_user_str}"
                elif get_inputs.count() == 1:
                    #   Hvis ikke der er flere rows med indhold fra inputs
                    message3 = f"{get_inputs[0].id} ({get_inputs[0].user.username})"
            except:
                messages.success(request, 'Log venligst ind for at gemme ID.')

        # -- Create new entry in DB -- 
        #   Creating if where the condition is met if field is filled out.
        #if condition:
            # Convert udregning to a string and round it to two decimal places
            #udregning_str = "{:.2f}".format(udregning)
            #test2 = Test(test1=test1, test_date_fra=test_date_fra_get, test_date_til=test_date_til_get, udregning_db=udregning_str, user=user_get)
            #test2.save()
    
    context = {
        'message':message, 
        'message2':message2,
        'test1_ses':test1_ses,
        'test_date_fra_get_ses':test_date_fra_get_ses,
        'test_date_til_get_ses':test_date_til_get_ses,
        'message3':message3,
    }


    return render(request, "tildelt_nummer.html", context)

def tjek_id(request,pk):
    #   Fetching info from db to call it on page in HTML
    indhold_fra_id = Test.objects.get(id=pk)
    #   Copying calculation logic from other view
    message = None
    message3 = None
    test1 = request.POST.get('test1')
    test_date_fra_get = request.POST.get('test_date_fra')
    test_date_til_get = request.POST.get('test_date_til')
    konstant = 30.44

    if request.method == 'POST':
        # -- Calculation logic -- 
        if test_date_til_get != "" and test_date_fra_get != "":
            #   Convert string representations to datetime objects
            test_date_til_get = datetime.strptime(test_date_til_get, '%Y-%m-%d')  # Adjust the format as needed
            test_date_fra_get = datetime.strptime(test_date_fra_get, '%Y-%m-%d')  # Adjust the format as needed
            delta_dage = test_date_til_get - test_date_fra_get

            #   Cr8 if not none since site crashes if price has no input
            if test1 != "":
                #   Change test1 to int or float to avoid site crash
                test1 = int(test1)
                test1 = float(test1)
                udregning = (test1 / konstant) * delta_dage.days
                message3 = f"Udregning er: ({test1} / {konstant}) * {delta_dage.days} = {udregning:.2f}"
            else:
                message3 = f"{delta_dage.days}"
                
            
        else:
            message3 = "Ingen udregning gives, da intet er udfyldt"

    return render(request, "tjek_id.html", {'indhold_fra_id':indhold_fra_id, 'message':message, 'message3':message3,})

def hangman(request):
    msg = ""
    counter = 10
    svar_felt = ""
    order = ""
    rigtige_ord = ""
    not_unique_msg = None
    word1 = request.POST.get('word')
    #   Lav word om til random row fra DB og print word så jeg ved hvilket
    word = Hangman_category.objects.get(id=2).word
    word_set = set(word)
    word_length = range(len(word))
    guess = request.POST.get('guess')
    guesses = Hangman.objects.all().values_list('guess', flat=True)
    word_count = Hangman_category.objects.all().count()
    


    #   Gem alle gæt i DB og lav for loop der viser samtlige. 
    #   Hav en funktion klar der genkender at spillet er færdigt og slet 
    #   alle elementer i DB. Workaround for en session !
    print(guesses)
    print(set(word))
    if request.method == 'POST':
        #   Lav tæller hvoraf man har 10 forsøg
        counter = (counter-1)
        #   Laver try, da hvert bogstav skal være unikt
        try:
            guess_db = Hangman(guess=guess)
            guess_db.save()
        except:
            not_unique_msg = f"{guess} har du allerede prøvet, tast et nyt bogstav"

        #   Laver if for at tjekke om input er i ord
        if guess in word:
            #   Display in HTML instead where guess= for loop with all info from db
            msg = f"{guess} is correct"
        else:
            msg = f"{guess} is incorrect"

        
    #   Sæt korrekte svar op
    #   For loop laver variabel for alle gæt, if kigger i alle gæt og finder dem der matcher ordet
    for rigtige_ord in guesses:
            if rigtige_ord in word_set:
                    svar_felt += rigtige_ord 
                    #   Dette er ikke universelt, og kan ikke bruges til andre ord.
                    order = ''.join(sorted(svar_felt, key=lambda x:("h","e","j").index(x)))
            else:
                pass


    #   Således vinder man. 
    if all(char in guesses for char in word_set):
            msg = "Du har vundet! Spillet starter nu forfra"
            Hangman.objects.all().delete()


    context = {
        'word':word, 
        'guesses':guesses, 
        'not_unique_msg':not_unique_msg, 
        'word_length':word_length,
        'word_count':word_count,
        'svar_felt':svar_felt,
        'order':order,
        'word_set':word_set,
        'rigtige_ord':rigtige_ord,
        'msg':msg,
    }


    return render(request, "hangman.html", context)



    #   guess.db = Hangman.objects.get()
    #   if guess.db in word
            # delete all from db

def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("Du er nu logget ind"))
            return redirect('home')
        else:
            messages.success(request, ("Der var en fejl i brugernavn eller adgangskode."))
            return redirect('login')
    else:
        return render(request, "login.html", {})

def logout_user(request):
    logout(request)
    messages.success(request, ("Du er nu logget ud"))
    return redirect('home')

    #return render(request, "logout.html", {})

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            #   log in user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("You have registered successfully"))

            # Create a new instance in the Stats model
            new_stats_instance = Stats.objects.create(user=user)
            new_stats_instance.save()

            return redirect('home')
        else:
            messages.success(request, ("Der var en fejl i registreringen, forsøg igen."))
            return redirect('register')
        
    else:
        return render(request, "register.html", {'form':form})

def stat_konkurrence(request: HttpRequest):
    #   Session logik
    kpt_felt_ses = None
    ga_felt_ses = None
    kt_felt_ses = None
    csat_felt_ses = None
    copc_felt_ses = None
    message = None
    counter = None
    request.session['kpt_felt'] = request.POST.get('kpt_felt')
    request.session['ga_felt'] = request.POST.get('ga_felt')
    request.session['kt_felt'] = request.POST.get('kt_felt')
    request.session['csat_felt'] = request.POST.get('csat_felt')
    request.session['copc_felt'] = request.POST.get('copc_felt')





    #   Fetching info from db to call it on page in HTML
    try:
        user_get = request.user
        user_stats = Stats.objects.get(user=user_get)
        # Convert fetched values to floats - make them None first so site can load

        user_stats.kpt_2 = float(user_stats.kpt_2)
        user_stats.kpt_3 = float(user_stats.kpt_3)
        user_stats.kpt = float(user_stats.kpt)
        #   GA
        user_stats.ga = float(user_stats.ga)
        user_stats.ga_2 = float(user_stats.ga_2)
        user_stats.ga_3 = float(user_stats.ga_3)

        #   KT
        user_stats.kontakttilladelser = float(user_stats.kontakttilladelser)
        user_stats.kontakttilladelser_2 = float(user_stats.kontakttilladelser_2)
        user_stats.kontakttilladelser_3 = float(user_stats.kontakttilladelser_3)

        #   CSAT
        user_stats.csat = float(user_stats.csat)
        user_stats.csat_2 = float(user_stats.csat_2)
        user_stats.csat_3 = float(user_stats.csat_3)

        #   COPC
        user_stats.copc = float(user_stats.copc)
        user_stats.copc_2 = float(user_stats.copc_2)
        user_stats.copc_3 = float(user_stats.copc_3)

        #   Trin
        user_stats.trin_1 = float(user_stats.trin_1)
        user_stats.trin_2 = float(user_stats.trin_2)
        user_stats.trin_3 = float(user_stats.trin_3)

        print("Prøver 1")
    except:
        messages.success(request, ("Der er ikke lavet nogen stats til dig. Venligst tilgå din leder så han kan lave stats til dig!"))
        return redirect('home')
    
    if request.method == "POST":
        counter = 0
        # Defining sessions
        kpt_felt_ses = request.session.get('kpt_felt', '')
        ga_felt_ses = request.session.get('ga_felt', '')
        kt_felt_ses = request.session.get('kt_felt', '')
        csat_felt_ses = request.session.get('csat_felt', '')
        copc_felt_ses = request.session.get('copc_felt', '')

        print(kpt_felt_ses)
        print(user_stats.kpt_3)

        # Convert string input to float
        try:
            kpt_felt_ses = float(kpt_felt_ses)
            ga_felt_ses = float(ga_felt_ses)
            kt_felt_ses = float(kt_felt_ses)
            csat_felt_ses = float(csat_felt_ses)
            copc_felt_ses = float(copc_felt_ses)

        except ValueError:
            kpt_felt_ses = None
            ga_felt_ses = None
            kt_felt_ses = None
            csat_felt_ses = None
            copc_felt_ses = None


            print("virker ikke")

        if user_stats.kpt_2 > kpt_felt_ses and kpt_felt_ses >= user_stats.kpt:
        # Increment counter by 2 if the first condition is met
            counter += 2
        elif user_stats.kpt_3 > kpt_felt_ses and kpt_felt_ses >= user_stats.kpt_2:
            counter += 3
        elif kpt_felt_ses >= user_stats.kpt_3:
            counter += 5
        elif user_stats.kpt > kpt_felt_ses:
            message = "Du opnår desværre ingen point."
        
        # For GA
        if user_stats.ga_2 > ga_felt_ses and ga_felt_ses >= user_stats.ga:
            # Increment counter by 2 if the first condition is met
            counter += 2
        elif user_stats.ga_3 > ga_felt_ses and ga_felt_ses >= user_stats.ga_2:
            # Increment counter by 3 if the second condition is met
            counter += 3
        elif ga_felt_ses >= user_stats.ga_3:
            # Increment counter by 5 if the third condition is met
            counter += 5
        elif user_stats.ga > ga_felt_ses:
            ga_message = "Du opnår desværre ingen point."

        # For KT
        if user_stats.kontakttilladelser_2 > kt_felt_ses and kt_felt_ses >= user_stats.kontakttilladelser:
            # Increment counter by 2 if the first condition is met
            counter += 2
        elif user_stats.kontakttilladelser_3 > kt_felt_ses and kt_felt_ses >= user_stats.kontakttilladelser_2:
            # Increment counter by 3 if the second condition is met
            counter += 3
        elif kt_felt_ses >= user_stats.kontakttilladelser_3:
            # Increment counter by 5 if the third condition is met
            counter += 5
        elif user_stats.kontakttilladelser > kt_felt_ses:
            kt_message = "Du opnår desværre ingen point."

        # For CSAT
        if user_stats.csat_2 > csat_felt_ses and csat_felt_ses >= user_stats.csat:
            # Increment counter by 2 if the first condition is met
            counter += 2
        elif user_stats.csat_3 > csat_felt_ses and csat_felt_ses >= user_stats.csat_2:
            # Increment counter by 3 if the second condition is met
            counter += 3
        elif csat_felt_ses >= user_stats.csat_3:
            # Increment counter by 5 if the third condition is met
            counter += 5
        elif user_stats.csat > csat_felt_ses:
            kt_message = "Du opnår desværre ingen point."
        
        #   For COPC
        if user_stats.copc_2 > copc_felt_ses and copc_felt_ses >= user_stats.copc:
            # Increment counter by 2 if the first condition is met
            counter += 2
        elif user_stats.copc_3 > copc_felt_ses and copc_felt_ses >= user_stats.copc_2:
            # Increment counter by 3 if the second condition is met
            counter += 3
        elif copc_felt_ses >= user_stats.copc_3:
            # Increment counter by 5 if the third condition is met
            counter += 5
        elif user_stats.copc > copc_felt_ses:
            kt_message = "Du opnår desværre ingen point."

        try:
            counter = float(counter)
        except ValueError:
            counter = None

        #   Counter logik
        if counter >= user_stats.trin_3:
            messages.success(request, ("Du har opnået point-trin 3"))
        elif user_stats.trin_3 > counter and counter >= user_stats.trin_2:
            messages.success(request, ("Du har opnået point-trin 2"))
        elif user_stats.trin_2 > counter and counter >= user_stats.trin_1:
            messages.success(request, ("Du har opnået point-trin 1"))
            pass




        print(counter)


    context = {
        "user_get":user_get,
        "user_stats":user_stats,
        "kpt_felt_ses":kpt_felt_ses,
        "ga_felt_ses":ga_felt_ses,
        "kt_felt_ses":kt_felt_ses,
        "csat_felt_ses":csat_felt_ses,
        "copc_felt_ses":copc_felt_ses,
        "message":message,
        "counter":counter,
    }

    return render(request, "stat_konkurrence.html", context)

def stat_konkurrence_admin(request: HttpRequest):
    user_get = request.user
    users = User.objects.all()
    user_stats = None
    user_felt_ses = None

    print(users)

    if request.method == "POST":
        try:
            request.session['user_felt'] = request.POST.get('user_felt')
            user_felt_ses = request.session.get('user_felt', '')
            print(user_felt_ses)

            username = User.objects.get(username=user_felt_ses)
            #user_id = username.id
            print(username)

            user_stats = Stats.objects.get(user=username)
        except:
            messages.success(request, ("Vælg bruger igen"))


    if 'upload_stats_button' in request.POST:
        request.session['user_felt'] = request.POST.get('user_felt')
        user_felt_ses = request.session.get('user_felt', '')
        stats_to_update = Stats.objects.get(user=username)

        
        #   All data from input fields are requested
        # Update the fields with the new values
        stats_to_update.kpt = request.POST.get('kpt')
        stats_to_update.kpt_2 = request.POST.get('kpt_2')
        stats_to_update.kpt_3 = request.POST.get('kpt_3')

        stats_to_update.ga = request.POST.get('ga')
        stats_to_update.ga_2 = request.POST.get('ga_2')
        stats_to_update.ga_3 = request.POST.get('ga_3')

        stats_to_update.kontakttilladelser = request.POST.get('kontakttilladelser')
        stats_to_update.kontakttilladelser_2 = request.POST.get('kontakttilladelser_2')
        stats_to_update.kontakttilladelser_3 = request.POST.get('kontakttilladelser_3')

        stats_to_update.csat = request.POST.get('csat')
        stats_to_update.csat_2 = request.POST.get('csat_2')
        stats_to_update.csat_3 = request.POST.get('csat_3')

        stats_to_update.copc = request.POST.get('copc')
        stats_to_update.copc_2 = request.POST.get('copc_2')
        stats_to_update.copc_3 = request.POST.get('copc_3')

        stats_to_update.trin_1 = request.POST.get('trin_1')
        stats_to_update.trin_2 = request.POST.get('trin_2')
        stats_to_update.trin_3 = request.POST.get('trin_3')

        stats_to_update.save()


    context = {
        "user_get":user_get,
        "user_stats":user_stats,
        "users":users,
        "user_felt_ses":user_felt_ses,
    }


    return render(request, "stat_konkurrence_admin.html", context)

def er_det_fredag(request: HttpRequest):
    user_get = request.user
    # Get the current date
    current_date = datetime.today()

    # Get the day of the week (0 for Monday, 1 for Tuesday, ..., 6 for Sunday)
    day_of_week = current_date.weekday()

    monday_to_sunday = [0,1,2,3,5,6]
    friday = 6


    context = {
        "user_get":user_get,
        "current_date":current_date,
        "day_of_week":day_of_week,
        "monday_to_sunday":monday_to_sunday,
        "friday":friday,
    }
    return render(request, "er_det_fredag.html", context)

def åamp(request: HttpRequest):
    user_get = request.user
    chosen_links = None
    chosen_links_length = None
    chosen_links_length_range = None
    selected_links = []
    links = {}

    links_fra_db = Link.objects.all()
    for obj in links_fra_db:
        # Store the name and link in the dictionary
        links[obj.name] = obj.link


    if request.method == "POST":
        chosen_links = request.POST.getlist('link_dropdown')
        print(chosen_links)
        chosen_links_length = len(chosen_links)
        chosen_links_length_range = range(chosen_links_length)

        #   Iterates the amount of elements selected, fx 3, index then = 3 and gets input in the chosen_links variable.
        for index in range(chosen_links_length):
            print(index)
            selected_link = links[chosen_links[index]]
            #   Puts the selected links into the list defined at the start
            selected_links.append(selected_link)

        

        




    context = {
        "user_get":user_get,
        "links":links,
        "selected_links":selected_links,
        "chosen_links":chosen_links,
        "chosen_links_length":chosen_links_length,
        "chosen_links_length_range":chosen_links_length_range,

    }
    return render(request, "åamp.html", context)

def kreditmax(request: HttpRequest):
    user_get = request.user
    kreditmax_ses = 1
    beløb_ses = 1
    message = None

    #   Logik til udregning - henter info fra inputs
    #   Gemmer i session
    request.session['kreditmax'] = request.POST.get('kreditmax')
    request.session['beløb'] = request.POST.get('beløb')

    #   Gemmer session som var
    kreditmax_ses = request.session.get('kreditmax', '')
    beløb_ses = request.session.get('beløb', '')

    #   Formatterer tal
    try:
        kreditmax_ses_float = float(kreditmax_ses)
        beløb_ses_float = float(beløb_ses)
    except:
        kreditmax_ses_float = 0
        beløb_ses_float = 0


    #   Udregning
    konstant = 1
    procent = 0.8
    udregning = beløb_ses_float - (kreditmax_ses_float * procent) + konstant
    formel = f"{beløb_ses_float} - ({kreditmax_ses_float} * {procent}) + {konstant}"

    if request.method == "POST":
        if kreditmax_ses_float >= beløb_ses_float:
            message = "Hvis kreditmax er højere end eller lig udestående beløb er kunden ikke spærret grundet kreditmax!"
        else:
            message = f"<h4>Kunden skal indbetale følgende beløb: {udregning}</h4> Dette præcise beløb SKAL indbetales. Når kunden kreditspærres er det fordi vi forbinder en risiko med deres udestående. Derfor SKAL vi modtage mere end 80% af deres kreditmax før der kan genåbnes. Dette vil ske automatisk når beløbet er modtaget. Ring til kredit for yderligere spørgsmål, efter at have sparret med en FC."



    context = {
        "user_get":user_get,
        "kreditmax_ses":kreditmax_ses,
        "beløb_ses":beløb_ses,
        "message":message,
        "formel":formel,
            }
    return render(request, "kreditmax.html", context)

def poke(request):
    return render(request, "kreditmax.html")

def dtfr(request: HttpRequest):
    user_get = request.user

    #   Skriv årstal på følgende måde 201701
    #   For hvert år gået siden 2017 + originale tal med 100
    #   Gentag 12 gange

   # årstal = 201701


    år_siden_2017 = datetime.now().year - 2016 #ændr til år_valgt
    årstal_list = []

    #   Looper index_2 7 gange. Definerer årstal med udgangspunkt i 2017. Plusser med 100, 7 gange (index_2 = 1,2->7). Looper resten 12 gange
    for index_2 in range(år_siden_2017):
        år = 201701+(100*index_2)
        for index in range(12):
            årstal = år+index
            årstal_list.append(årstal)

    context = {
        "user_get":user_get,
        "årstal_list":årstal_list,
    }
    return render(request, "dtfr.html", context)

def pause(request):
    if request.method == 'POST':
        try:
            # Run the Python script
            subprocess.run(['python', './pause.py'], check=True)
            return JsonResponse({'status': 'success'})
        except subprocess.CalledProcessError as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return render(request, "pause.html")



#   Blog classes
class BlogView(ListView):
    model = Post
    template_name = "blog.html"
    ordering = ["-post_date"]

class ArticleDetailView(DetailView):
    model = Post
    template_name = "article_details.html"

class AddPostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = "add_post.html"
    #fields = ["author", "title", "body"]
    #fields = "__all__"

class UpdatePostView(UpdateView):
    model = Post
    template_name = "update_post.html"
    form_class = EditForm
    #fields = ["title","body"]

class DeletePostView(DeleteView):
    model = Post
    template_name = "delete_post.html"
    success_url = reverse_lazy('blog')

class UserEditView(generic.UpdateView):
    form_class = EditProfileForm
    template_name = 'edit_profile.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user

