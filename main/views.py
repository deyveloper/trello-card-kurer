from django.shortcuts import render
from django.http import JsonResponse

from trello import TrelloApi
import json

from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def index(request):
    KEY = "safbin198afad8489asf894saf19"
    
    try:
       key_ = request.GET["key"]
       if key_ != KEY:
           raise Exception
    except:
       resp = JsonResponse({"data": {"status": "failed"}})
       return resp
    
    webhook_data = json.loads(request.body)
    print(webhook_data)
    startChecking(webhook_data)
    return JsonResponse({"data": {"status": "success"}}) 
  


def startChecking(webhook_data):
    # Constants
    TRELLO_API_KEY = "1c7cec096175a93ed305cff00caf0592"
    TRELLO_API_TOKEN = "4ad7c1fa64ecb1c3e47928e60145f67fe035dd25238d9a9e817c6d13e436cd3d"
    BOARD_ID = "tbU0BvI3"
    # Trigger word for preparing
    TRIGGER = "lega"
    # Whitelist to dedicate users
    WHITELIST = [
        "trello",
    ]

    # Setting up trello
    trello = TrelloApi(TRELLO_API_KEY)
    trello.set_token(TRELLO_API_TOKEN)

    # Action type triggering
    action_type = "action_changed_description_of_card"

    # Check for action type 
    if webhook_data["action"]["display"]["translationKey"] == action_type:
        # Member creator seperating
        member_creator = webhook_data["action"]["memberCreator"]
        # Check for trigger word and whitelist
        if TRIGGER in webhook_data["action"]["data"]["card"]["desc"] and not member_creator["username"] in WHITELIST:
            # Get shortlink from webhook
            shortlink = webhook_data["action"]["data"]["card"]["shortLink"]
            # Get all custom fields from server
            custom_fields = trello.cards.get_custom_fields_board(BOARD_ID)

            # Parsing necessary custom field
            custom_field = None
            for curr_cf in custom_fields:
                if not curr_cf["name"] == "Курьер" or not curr_cf["type"] == "text":
                   continue

                custom_field = curr_cf

                # Finded breaking...
                break

            # Check for custom field
            if custom_field:
                print(111)
                custom_field_id = custom_field["id"]
                member_creator_check = member_creator["fullName"]

                # Updating data in trello servers 
                resp = trello.cards.update_custom_field(shortlink, custom_field_id, {"value": {"text": member_creator_check}})  
