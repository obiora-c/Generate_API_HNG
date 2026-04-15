from django.shortcuts import render


# Create your views here.
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timezone


#-----Validation for name -------

def classify_name (requests): 
    name = requests.get('name')
    
    if name is None or name.strip() == '' :
        return Response(
            {"status": "error", "Message": "Missing Name or You didnt Enter a Name"},
            status=status.HTTP_400_BAD_REQUEST
            
            )
        
        
    if not isinstance(name, str):
        return Response(
            {"status":status.HTTP_422_UNPROCESSABLE_ENTITY
        })
        
# ----- Calling an EExternal API ---------     
    try:
        response = requests.get(
            "https://api.genderize.io", 
            params={"name": name},
            timeout = 3
            )
        if response.status_code  != 200:
            return Response(
                {"status": "error", "message": "Upstream API error"},
                status=status.HTTP_502_BAD_GATEWAY)
            
        data = response.json()
        
        gender = data.get("gender")
        probability = data.get("probability")
        count = data.get("count")
        
        if gender is None or count == 0:
            return Response(
                {"status" : "error", "message" : "Gender missing or count disabled"}, 
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
                ) 
            
        if probability is None or count is None:
            return Response(
               {"status": "error", "message": "No prediction available for the provided name"},
               status=422
               )
            
# -----  data to be processed -----      
        sample_size = count
        is_confident = probability >= 0.7 and sample_size >= 100
        
        
        processed_at = datetime.now(timezone).isoformat
        
        
        return Response({
            "status": "SUCCESS NIGGA",
            "data": {
                "name": name,
                "gender": gender,
                "probability": probability,
                "is_confident": is_confident,
                "processed_at": processed_at   
            }
        }, status=status.HTTP_200_OK)
        
    except requests.exceptions.RequestException:
        return Response(
            {"status": "error", "Message" : "API error (API not found)"},
            status=status.HTTP_502_BAD_GATEWAY
            )
        
    except Exception:
        return Response(
            {"status" : "error", "Message" : "Internal Server Error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        
        
        
        

            
            
    
    