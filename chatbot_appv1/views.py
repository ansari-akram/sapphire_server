from re import I
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import spacy
from .models import *
from word2number import w2n
import os


ner_custom = spacy.load(f"chatbot_appv1{os.sep}model_v4")
ner_inbuilt = spacy.load("en_core_web_sm")
greetings_list = ["hello", "how are you",
                  "how area you?", "hey there", "hi", "hey"]
farewell_list = ["bye", "take care", "good bye", "see you"]

# QUERIES FOR CHATS
COSMETIC_QUERIES = ['COSMETIC', 'HIGHLIGHTER']
BAG_QUERIES = ['ACCESSORY', 'BAG', 'COLOR']
SHOE_QUERIES = ['ACCESSORY', 'SHOES', 'COLOR']
FRAGRANCE_QUERIES = ['BEAUTY', 'GENDER', 'SCENT']
DRESS_QUERIES = ['CARDINAL', 'COLOR', 'FABRIC', 'DESIGN']
PRODUCT_NOT_AVAIL = "We don't have this product.<br>You can try another if you like."


def detect(request, detection_list):
    detected_list = []
    detected_labels = []
    # print(request)

    for i in detection_list:
        out = ner_custom(request)
        for w in out.ents:
            if w.label_ == i:
                # print(f'{w.label_} {w.text}')
                detected_list.append(w.text)
                detected_labels.append(w.label_)
        
        out = ner_inbuilt(request)
        for w in out.ents:
            if w.label_ == i:
                detected_list.append(str(w2n.word_to_num(w.text)) + " piece")
                detected_labels.append(w.label_)
    
    return detected_list, detected_labels


def indexOfQuery(label, detection_list):
    idx = -1
    for i in range(len(detection_list)):
        if detection_list[i] == label:
            idx = i
    
    if i == -1: return None
    else: return idx


def rearrange(detected_response, detected_labels, detection_list):
    ordered_list_res = []
    ordered_list_lab = []

    for i in range(len(detection_list)):
        if detection_list[i] in detected_labels:
            idx = indexOfQuery(detection_list[i], detected_labels)
            ordered_list_res.append(detected_response[idx])
            ordered_list_lab.append(detected_labels[idx])
    
    return ordered_list_res, ordered_list_lab


def cosmeticOrderedQuery(detected_response, detected_labels, detection_list, prev_response, prev_labels):
    ordered_list = []
    print()
    print('PRINT ORDERED QUERY', detected_response, detected_labels)

    if prev_labels[0] != '':
        print('PRINT ORDERED QUERY', indexOfQuery(prev_labels[0], detection_list))

    # for i in range(len(detected_labels)):
    #     if i == indexOfQuery(detected_labels[i], detection_list):
    #         ordered_list.append(detected_response[i])
    #     print('PRINT ORDERED QUERY', indexOfQuery(detected_labels[i], detection_list))

    print('LAST ORDERED LIST', ordered_list)
    print()
    return ordered_list


@csrf_exempt
def get_response(request):
    question = request.POST.get('question')
    pre = request.POST.get('pre')
    prev = pre.split(',')
    detections = request.POST.get('detected').split(',')

    _greetings = AddGreeting.objects.all()
    # print(_greetings.values()[0]['query'].split(','), type(_greetings.values()[0]['query']))
    # print(_greetings.values()[0]['response'], type(_greetings.values()[0]['response']))

    if question.lower() in greetings_list:
        return JsonResponse({'response': 'Hello! how can I help you?', 'pre': [], 'detection': []})

    if question.lower() in farewell_list:
        return JsonResponse({'response': 'Please do visit again!', 'pre': [], 'detection': []})
    
    print('PREV', prev, detections)
    print('QUESTION', question)

    #####################################  COSMETIC RESPONSE  #######################################
    _cos_response, _cos_labels = detect(question.lower(), COSMETIC_QUERIES)

    if detections[0] != "" and _cos_response:
        cos_response = prev + _cos_response
        cos_labels = detections + _cos_labels
    else:
        cos_response = _cos_response
        cos_labels = _cos_labels

    cos_response, cos_labels =  rearrange(cos_response, cos_labels, COSMETIC_QUERIES)
    print('COSMETIC RESPONSE', cos_response, cos_labels)

    if cos_response:
        if cos_response[0].lower() != '' and cos_labels[0] in COSMETIC_QUERIES:
            try:
                _h_type = cos_response[cos_labels.index(COSMETIC_QUERIES[1])]
                _highlighter_type = AddHighlighterType.objects.get(highlighter_name=_h_type)

                highlighter = Highlighter.objects.all().filter(highlighter_type=_highlighter_type)

                if len(highlighter) == 1:
                    return JsonResponse({'link': highlighter[0].link, 'image': 'chatbot_appv1/media/' + highlighter[0].photo.name, 'pre': [], 'detection': []})
                else:
                    return JsonResponse({'response': PRODUCT_NOT_AVAIL, 'pre': [], 'detection': []})

            except:
                return JsonResponse({'response': 'Powder or Liquid?', 'pre': cos_response, 'detection': cos_labels})
    
    #####################################  BAG RESPONSE  #######################################
    _bag_response, _bag_labels = detect(question.lower(), BAG_QUERIES)

    if detections[0] != "" and _bag_response:
        bag_response = prev + _bag_response
        bag_labels = detections + _bag_labels
    else:
        bag_response = _bag_response
        bag_labels = _bag_labels

    bag_response, bag_labels =  rearrange(bag_response, bag_labels, BAG_QUERIES)
    print('BAG RESPONSE', bag_response, bag_labels)

    if bag_response:
        if bag_response[0].lower() == 'bag' or bag_response[0].lower() == 'bags' and bag_labels[0] == BAG_QUERIES[0]:
            try:
                if bag_response[1].lower() != "" and bag_labels[1] == BAG_QUERIES[1]:
                    try:
                        _bag_type = AddBagType.objects.get(bag_type_name=bag_response[1])
                        _color = AddColor.objects.get(color_name=bag_response[2])
                        
                        bag = Bag.objects.all().filter(bag_type=_bag_type, color=_color)

                        if len(bag) == 1:
                            return JsonResponse({'link': bag[0].link, 'image': 'chatbot_appv1/media/' + bag[0].photo.name, 'pre': [], 'detection': []})
                        else:
                            return JsonResponse({'response': PRODUCT_NOT_AVAIL, 'pre': [], 'detection': []})

                    except:
                        return JsonResponse({'response': 'Color?', 'pre': bag_response, 'detection': bag_labels})

            except:
                return JsonResponse({'response': 'Bag type?', 'pre': bag_response, 'detection': bag_labels})

    #####################################  SHOE RESPONSE  #######################################
    _shoe_response, _shoe_labels = detect(question.lower(), SHOE_QUERIES)

    if detections[0] != "" and _shoe_response:
        shoe_response = prev + _shoe_response
        shoe_labels = detections + _shoe_labels
    else:
        shoe_response = _shoe_response
        shoe_labels = _shoe_labels
    
    shoe_response, shoe_labels =  rearrange(shoe_response, shoe_labels, SHOE_QUERIES)
    print('SHOE RESPONSE', shoe_response, shoe_labels)

    if shoe_response:
        if shoe_response[0].lower() == 'shoe' or shoe_response[0].lower() == 'shoes' and shoe_labels[0] == SHOE_QUERIES[0]:
            try:
                if shoe_response[1].lower() != "" and shoe_labels[1] == SHOE_QUERIES[1]:
                    try:
                        print('in last try', shoe_response, shoe_labels)
                        _shoe_type = AddShoeType.objects.get(shoe_type_name=shoe_response[1])
                        _color = AddColor.objects.get(color_name=shoe_response[2])
                        print(_shoe_type, _color)

                        shoe = Shoe.objects.all().filter(shoe_type=_shoe_type, color=_color)

                        if len(shoe) == 1:
                            return JsonResponse({'link': shoe[0].link, 'image': 'chatbot_appv1/media/' + shoe[0].photo.name, 'pre': [], 'detection': []})
                        else:
                            return JsonResponse({'response': PRODUCT_NOT_AVAIL, 'pre': [], 'detection': []})

                    except:
                        return JsonResponse({'response': 'Color?', 'pre': shoe_response, 'detection': shoe_labels})

            except:
                return JsonResponse({'response': 'Shoes type?', 'pre': shoe_response, 'detection': shoe_labels})

    #####################################  FRAGRANCE RESPONSE  #######################################
    _frag_response, _frag_labels = detect(question.lower(), FRAGRANCE_QUERIES)

    if detections[0] != "" and _frag_response:
        frag_response = prev + _frag_response
        frag_labels = detections + _frag_labels
    else:
        frag_response = _frag_response
        frag_labels = _frag_labels
    
    frag_response, frag_labels =  rearrange(frag_response, frag_labels, FRAGRANCE_QUERIES)
    print('FRAGRANCE RESPONSE', frag_response, frag_labels)

    if frag_response:
        if frag_response[0].lower() != '' and frag_labels[0] == FRAGRANCE_QUERIES[0]:
            try:
                if frag_response[1].lower() != "" and frag_labels[1] == FRAGRANCE_QUERIES[1]:
                    try:
                        _type = AddFragranceType.objects.get(fragrance_type_name__icontains=frag_response[1])
                        _scent = AddScentType.objects.get(scent_type_name=frag_response[2])
                        print('INFO', _type, _scent)

                        frag = Perfume.objects.all().filter(perfume_type=_type, scent=_scent)

                        if len(frag) == 1:
                            return JsonResponse({'link': frag[0].link, 'image': 'chatbot_appv1/media/' + frag[0].photo.name, 'pre': [], 'detection': []})
                        else:
                            return JsonResponse({'response': PRODUCT_NOT_AVAIL, 'pre': [], 'detection': []})

                    except:
                        return JsonResponse({'response': 'Scent?', 'pre': frag_response, 'detection': frag_labels})
                
                else:
                    return JsonResponse({'response': 'For?', 'pre': frag_response, 'detection': frag_labels})

            except:
                return JsonResponse({'response': 'For?', 'pre': frag_response, 'detection': frag_labels})
    
    #####################################  DRESS RESPONSE  #######################################
    _dress_response, _dress_labels = detect(question.lower(), DRESS_QUERIES)

    if detections[0] != "" and _dress_response:
        dress_response = prev + _dress_response
        dress_labels = detections + _dress_labels
    else:
        dress_response = _dress_response
        dress_labels = _dress_labels

    dress_response, dress_labels =  rearrange(dress_response, dress_labels, DRESS_QUERIES)
    print('DRESS RESPONSE', dress_response, dress_labels)

    if dress_response:
        if dress_response[0].lower() != '' and dress_labels[0] == DRESS_QUERIES[0]:
            try:
                if dress_response[1].lower() != "" and dress_labels[1] == DRESS_QUERIES[1]:
                    try:
                        if dress_response[2].lower() != "" and dress_labels[2] == DRESS_QUERIES[2]:
                            try:
                                _dress = AddDressPiece.objects.get(dress_piece=dress_response[0])
                                _color = AddColor.objects.get(color_name=dress_response[1])
                                _fabric = AddDressFabric.objects.get(fabric_name=dress_response[2])
                                _design = AddDressDesign.objects.get(design_name=dress_response[3])

                                dress = Suit.objects.all().filter(dress=_dress, color=_color, fabric=_fabric, design=_design)

                                if len(dress) == 1:
                                    return JsonResponse({'link': dress[0].link, 'image': 'chatbot_appv1/media/' + dress[0].photo.name, 'pre': [], 'detection': []})
                                else:
                                    return JsonResponse({'response': PRODUCT_NOT_AVAIL, 'pre': [], 'detection': []})
                            except:
                                return JsonResponse({'response': 'Design?', 'pre': dress_response, 'detection': dress_labels})
                        
                        else:
                            return JsonResponse({'response': 'Fabric?', 'pre': dress_response, 'detection': dress_labels})

                    except:
                        return JsonResponse({'response': 'Fabric?', 'pre': dress_response, 'detection': dress_labels})

                else:
                    return JsonResponse({'response': 'Color?', 'pre': dress_response, 'detection': dress_labels})

            except:
                return JsonResponse({'response': 'Color?', 'pre': dress_response, 'detection': dress_labels})
            
        else:
            return JsonResponse({'response': 'Dress pieces?', 'pre': dress_response, 'detection': dress_labels})
    
    return JsonResponse({'response': 'error', 'pre': [], 'detection': []})