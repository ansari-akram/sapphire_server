from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import spacy
from .models import *
from word2number import w2n


ner_custom = spacy.load("chatbot_appv1\\model-last")
ner_inbuilt = spacy.load("en_core_web_sm")
greetings_list = ["hello", "how are you",
                  "how area you?", "hey there", "hi", "hey"]
farewell_list = ["bye", "take care", "good bye", "see you"]


# def chatbot(request=""):
#     # global type1, type2, type3, type4

#     print('REQUEST', request)

#     type1 = ""
#     type2 = ""
#     type3 = ""
#     type4 = ""

#     if type1 == "":
#         if request == "":
#             print('in type 1 return')
#             return [{'response': 'What type of Cloth do you want?'}]

#         out = ner_inbuilt(request)
#         if out.ents.__len__() >= 1 and type1 == "":
#             for word in out.ents:
#                 if word.label_ == 'CARDINAL':
#                     type1 = word.text + " piece"
#                     return {'type1': type1}
#         else:
#             print('in type 1 recursion')
#             chatbot()

#     if type2 == "":
#         if request == "":
#             return {'response': 'Which color do you want?'}

#         out = ner_custom(request)
#         if out.ents.__len__() >= 1 and type2 == "":
#             for word in out.ents:
#                 if word.label_ == 'COLOR':
#                     type2 = word.text
#                     return {'type1': type1, 'type2': type2}

#         else:
#             chatbot()

#     if type3 == "":
#         if request == "":
#             return {'response': 'Which Fabric do you want?'}

#         # request has lawn then type 3
#         out = ner_custom(request)
#         if out.ents.__len__() >= 1 and type3 == "":
#             for word in out.ents:
#                 if word.label_ == 'FABRIC':
#                     type3 = word.text
#                     return {'type1': type1, 'type2': type2, 'type3': type3}
#         else:
#             chatbot()

#     if type4 == "":
#         if request == "":
#             return {'response': 'Which Design do you want?'}

#         out = ner_custom(request)
#         if out.ents.__len__() >= 1 and type4 == "":
#             for word in out.ents:
#                 if word.label_ == 'DESIGN':
#                     type4 = word.text
#                     return {'type1': type1, 'type2': type2, 'type3': type3, 'type4': type4, 'status': 'okay'}
#         else:
#             chatbot()

#     if type1 == "" or type2 == "" or type3 == "" or type4 == "":
#         print('in all empty')
#         chatbot()

#     else:
#         print(f"\nYou have selected:\nCloth Type:\t {type1} clothes\nColor:\t\t {type2}\nFabric:\t\t {type3}\nDesign:\t\t {type4}")
#         user_response = input("\nDo you need anything else? [Yes/No]\t")

#         if user_response.lower() == "yes":
#             type1, type2, type3, type4 = "", "", "", ""
#             chatbot()

#         elif user_response.lower() == "no":
#             print("\nThank You!")


def chatbot(request="", _type1="", _type2="", _type3="", _type4=""):
    type1 = _type1
    type2 = _type2
    type3 = _type3
    type4 = _type4

    if type1 == "":
        if request == "":
            return "How many dress piece do you want?"
            # request = input("\nWhat type of Cloth do you want?:\t")

        out = ner_inbuilt(request)
        if out.ents.__len__() >= 1 and type1 == "":
            for word in out.ents:
                if word.label_ == 'CARDINAL':
                    # print("TYPE1", w2n.word_to_num(word.text), type(w2n.word_to_num(word.text)))
                    type1 = str(w2n.word_to_num(word.text)) + " piece"
        else:
            chatbot(request, type1, type2, type3, type4)

    if type2 == "":
        if request == "":
            return "Which color do you want?"
            # request = input("\nWhich color do you want?:\t")

        out = ner_custom(request)
        if out.ents.__len__() >= 1 and type2 == "":
            for word in out.ents:
                if word.label_ == 'COLOR':
                    type2 = word.text
        else:
            chatbot(_type1=type1, _type2=type2, _type3=type3, _type4=type4)

    if type3 == "":
        if request == "":
            return "Which Fabric do you want?"
            # request = input("\nWhich Fabric do you want?:\t")

        # request has lawn then type 3
        out = ner_custom(request)
        if out.ents.__len__() >= 1 and type3 == "":
            for word in out.ents:
                if word.label_ == 'FABRIC':
                    type3 = word.text
        else:
            chatbot(_type1=type1, _type2=type2, _type3=type3, _type4=type4)

    if type4 == "":
        if request == "":
            return "Which Design do you want?"
            # request = input("\nWhich Design do you want?:\t")

        out = ner_custom(request)
        if out.ents.__len__() >= 1 and type4 == "":
            for word in out.ents:
                if word.label_ == 'DESIGN':
                    type4 = word.text
        else:
            chatbot(_type1=type1, _type2=type2, _type3=type3, _type4=type4)

    print('ALL', type1, type2, type3, type4)
    return type1, type2, type3, type4

    # if type1 == "" or type2 == "" or type3 == "" or type4 == "":
    # chatbot(_type1=type1, _type2=type2, _type3=type3, _type4=type4)


@csrf_exempt
def get_response1(request):

    query = request.POST.get('question')
    type1 = request.POST.get('type1')
    type2 = request.POST.get('type2')
    type3 = request.POST.get('type3')
    type4 = request.POST.get('type4')

    if query.lower() in greetings_list:
        return JsonResponse({'response': 'Hello! how can I help you?', 'type1': type1, 'type2': type2, 'type3': type3, 'type4': type4})

    if query.lower() in farewell_list:
        return JsonResponse({'response': 'Please do visit again!', 'type1': type1, 'type2': type2, 'type3': type3, 'type4': type4})

    print('BEFORE', type1, type2, type3, type4, query)
    type1, type2, type3, type4 = chatbot(query, type1, type2, type3, type4)
    print('AFTER', type1, type2, type3, type4, query)

    if type1 != "" and type2 != "" and type3 != "" and type4 != "":
        if type2.lower() == "white":
            type2 = "off-white"
        cloth = Cloth.objects.all().filter(type1=type1.lower(), type2=type2.lower(),
                                           type3=type3.lower(), type4=type4.lower())

        # /chatbot_appv1/media/images/sapphire_logo.png
        # print(cloth[0].photo)
        # print('PHOTO', '/chatbot_appv1/media/' + cloth[0].photo.name)

        if len(cloth) == 1:
            return JsonResponse({'type1': type1, 'type2': type2, 'type3': type3, 'type4': type4, 'link': cloth[0].link, 'image': 'chatbot_appv1/media/' + cloth[0].photo.name, 'status': 'okay'})

        else:
            return JsonResponse({'type1': type1, 'type2': type2, 'type3': type3, 'type4': type4, 'link': "We don't have this Product.", 'status': 'okay'})

    if type1 == "":
        if query == "":
            return JsonResponse({'response': 'How many dress piece do you want?'})
            # request = input("\nWhat type of Cloth do you want?:\t")

        out = ner_inbuilt(query)
        if out.ents.__len__() >= 1 and type1 == "":
            for word in out.ents:
                if word.label_ == 'CARDINAL':
                    type1 = word.text + " piece"
                    return JsonResponse({'response': 'Which color do you want?', 'type1': type1, 'type2': type2, 'type3': type3, 'type4': type4})
                return JsonResponse({'response': 'How many dress piece do you want?', 'type1': type1, 'type2': type2, 'type3': type3, 'type4': type4})

        else:
            return JsonResponse({'response': 'How many dress piece do you want?'})

    if type2 == "":
        out = ner_custom(query)
        if out.ents.__len__() >= 1 and type2 == "":
            for word in out.ents:
                if word.label_ == 'COLOR':
                    type2 = word.text
                    return JsonResponse({'response': 'Which Fabric do you want?', 'type1': type1, 'type2': type2, 'type3': type3, 'type4': type4})
                return JsonResponse({'response': 'Which color do you want?', 'type1': type1, 'type2': type2, 'type3': type3, 'type4': type4})

        else:
            return JsonResponse({'response': 'Which color do you want?', 'type1': type1, 'type2': type2, 'type3': type3, 'type4': type4})

    if type3 == "":
        if "lawn" in query.lower():
            type3 = "Lawn"
            return JsonResponse({'response': 'Which Design do you want?', 'type1': type1, 'type2': type2, 'type3': type3, 'type4': type4})

        out = ner_custom(query)
        if out.ents.__len__() >= 1 and type3 == "":
            for word in out.ents:
                if word.label_ == 'FABRIC':
                    type3 = word.text
                    return JsonResponse({'response': 'Which Design do you want?', 'type1': type1, 'type2': type2, 'type3': type3, 'type4': type4})
                return JsonResponse({'response': 'Which Fabric do you want?', 'type1': type1, 'type2': type2, 'type3': type3, 'type4': type4})

        else:
            return JsonResponse({'response': 'Which Fabric do you want?', 'type1': type1, 'type2': type2, 'type3': type3, 'type4': type4})

    if type4 == "":
        out = ner_custom(query)
        if out.ents.__len__() >= 1 and type4 == "":
            for word in out.ents:
                if word.label_ == 'DESIGN':
                    type4 = word.text
                    return JsonResponse({'type1': type1, 'type2': type2, 'type3': type3, 'type4': type4, 'status': 'okay'})
                return JsonResponse({'response': 'Which Design do you want?', 'type1': type1, 'type2': type2, 'type3': type3, 'type4': type4})

        else:
            return JsonResponse({'response': 'Which Design do you want?', 'type1': type1, 'type2': type2, 'type3': type3, 'type4': type4})


def adoreta(request):
    print('request', request)
    for i in request:
        out = ner_custom(i)
        for w in out.ents:
            if w.label_ == 'COSMETIC':
                product = w.label_

            if w.label_ == 'HIGHLIGHTER':
                highlighter = Highlighter.objects.all().filter(highlighter_type=w.text)
                if len(highlighter) == 1:
                    return JsonResponse({'link': highlighter[0].link, 'image': 'chatbot_appv1/media/' + highlighter[0].photo.name})


def cosmetic_chatbot(request='', type1='', type2=''):
    cosmetic_type = type1
    highlighter_type = type2
    
    if cosmetic_type == "":
        out = ner_custom(request)
        for w in out.ents:
            if w.label_ == 'COSMETIC':
                cosmetic_type = w.text
    
    if highlighter_type == '':
        out = ner_custom(request)
        for w in out.ents:
            if w.label_ == 'HIGHLIGHTER':
                highlighter_type = w.text

    return [cosmetic_type, highlighter_type]


def bag_chatbot(request='', type1='', type2='', type3=''):
    product = type1
    bag_type = type2
    color = type3

    if product == "":
        out = ner_custom(request)
        for w in out.ents:
            if w.label_ == 'ACCESSORY':
                product = w.text

    if bag_type == "":
        out = ner_custom(request)
        for w in out.ents:
            if w.label_ == 'BAGS':
                bag_type = w.text
    
    if color == '':
        out = ner_custom(request)
        for w in out.ents:
            if w.label_ == 'COLOR':
                color = w.text
    
    return [product, bag_type, color]


def shoe_chatbot(request='', type1='', type2=''):
    shoe_type = type1
    color = type2

    if shoe_type == "":
        out = ner_custom(request)
        for w in out.ents:
            if w.label_ == 'SHOES':
                shoe_type = w.text
    
    if color == '':
        out = ner_custom(request)
        for w in out.ents:
            if w.label_ == 'COLOR':
                color = w.text
    
    return [shoe_type, color]


def perfume_chatbot(request='', type1='', type2=''):
    perfume_type = type1
    scent = type2
    gender = ""

    if perfume_type == "":
        out = ner_custom(request)
        for w in out.ents:
            if w.label_ == 'GENDER':
                gender = w.text

        out = ner_custom(request)
        for w in out.ents:
            if w.label_ == 'BEAUTY':
                perfume_type = w.text
    
    if scent == '':
        out = ner_custom(request)
        for w in out.ents:
            if w.label_ == 'COLOR':
                scent = w.text
    
    return [perfume_type, gender, scent]


@csrf_exempt
def get_response(request):
    question = request.POST.get('question')
    pre = request.POST.get('pre')
    prev = pre.split(',')

    if question.lower() in greetings_list:
        return JsonResponse({'response': 'Hello! how can I help you?'})

    if question.lower() in farewell_list:
        return JsonResponse({'response': 'Please do visit again!'})
    
    print('PREV', prev)
    
    if prev[0] != '':
        for i in prev:
            out = ner_custom(i)
            for w in out.ents:
                if w.label_ == 'COSMETIC':
                    cos_response = cosmetic_chatbot(request=question, type1=w.text)
                    print('RESPONSE2', cos_response)
                    highlighter = Highlighter.objects.all().filter(highlighter_type=cos_response[1])
                    if len(highlighter) == 1:
                        return JsonResponse({'link': highlighter[0].link, 'image': 'chatbot_appv1/media/' + highlighter[0].photo.name, 'pre': []})
                
                if w.label_ == 'ACCESSORY':
                    bag_response = bag_chatbot(request=question, type1=w.text)
                    print('BAG RESPONSE2', bag_response)
                    bag = Bag.objects.all().filter(bag_type=bag_response[0], color=bag_response[1])
                    if len(bag) == 1:
                        return JsonResponse({'link': bag[0].link, 'image': 'chatbot_appv1/media/' + bag[0].photo.name, 'pre': []})
                
                if w.label_ == 'SHOES':
                    shoe_response = shoe_chatbot(request=question, type1=w.text)
                    print('SHOE RESPONSE2', shoe_response)
                    shoe = Shoe.objects.all().filter(shoe_type=shoe_response[0], color=shoe_response[1])
                    if len(shoe) == 1:
                        return JsonResponse({'link': shoe[0].link, 'image': 'chatbot_appv1/media/' + shoe[0].photo.name, 'pre': []})
                
                if w.label_ == 'FRAGRANCES':
                    bag_response = perfume_chatbot(request=question, type1=w.text)
                    print('SHOE RESPONSE2', shoe_response)
                    shoe = Shoe.objects.all().filter(shoe_type=shoe_response[0], color=shoe_response[1])
                    if len(shoe) == 1:
                        return JsonResponse({'link': shoe[0].link, 'image': 'chatbot_appv1/media/' + shoe[0].photo.name, 'pre': []})
            


    else:
        cos_response = cosmetic_chatbot(request=question)
        print('COSMETIC RESPONSE', cos_response)
        if cos_response[0] != '':
            return JsonResponse({'response': 'Powder or Liquid?', 'pre': [cos_response[0]]})
        
        bag_response = bag_chatbot(request=question)
        print('BAG RESPONSE', bag_response)
        if bag_response[0] != '':
            return JsonResponse({'response': 'Color?', 'pre': [bag_response[0]]})
        
        shoe_response = shoe_chatbot(request=question)
        print('SHOE RESPONSE', shoe_response)
        if shoe_response[0] != '':
            return JsonResponse({'response': 'Color?', 'pre': [shoe_response[0]]})
        
        perfume_response = perfume_chatbot(request=question)
        print('PERFUME RESPONSE', perfume_response)
        if perfume_response[0] != '':
            return JsonResponse({'response': 'Color?', 'pre': [perfume_response[0]]})
        
        dress_response = chatbot(request=question)
        print('DRESS RESPONSE', dress_response)
        if dress_response[0] != '':
            return JsonResponse({'response': 'Color?', 'pre': [dress_response[0]]})

    # out = ner_custom(question)

    # for word in out.ents:
    #     print(f'{word.text} {word.label_}')
    #     if word.label_ == 'COSMETIC':
    #         response = cosmetic_chatbot(request=question, type1=word.text)
    #         if response == "":
    #             return JsonResponse({'response': 'Powder or Liquid?', 'pre': [word.text]})
            
    #         if response != "":
    #             highlighter = Highlighter.objects.all().filter(highlighter_type=response)
    #             if len(highlighter) == 1:
    #                 return JsonResponse({'link': highlighter[0].link, 'image': 'chatbot_appv1/media/' + highlighter[0].photo.name})
        
        # if word.label_ == 'HIGHLIGHTER':
        #     # show highlighter
        #     highlighter = Highlighter.objects.all().filter(highlighter_type=word.text)
        #     if len(highlighter) == 1:
        #         return JsonResponse({'link': highlighter[0].link, 'image': 'chatbot_appv1/media/' + highlighter[0].photo.name})

    return JsonResponse({'response': 'working', 'pre': []})
