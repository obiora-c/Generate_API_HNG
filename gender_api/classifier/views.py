from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timezone
import requests


@api_view(['GET'])
def classify_name(request):
    name = request.GET.get('name')

    # -------- VALIDATION --------
    if name is None or name.strip() == '':
        return Response(
            {"status": "error", "message": "Missing or empty name parameter"},
            status=400
        )

    try:
        # -------- CALL EXTERNAL API --------
        res = requests.get(
            "https://api.genderize.io",
            params={"name": name},
            timeout=10
        )

        if res.status_code != 200:
            return Response(
                {"status": "error", "message": "Upstream API error"},
                status=502
            )

        data = res.json()

        gender = data.get("gender")
        probability = data.get("probability")
        count = data.get("count")

        # -------- EDGE CASE (STRICT RULE) --------
        if gender is None or count == 0:
            return Response(
                {"status": "error", "message": "No prediction available for the provided name"},
                status=422
            )

        # -------- PROCESS DATA --------
        probability = float(probability)
        sample_size = int(count)

        is_confident = probability >= 0.7 and sample_size >= 100
        processed_at = datetime.now(timezone.utc).isoformat()

        # -------- SUCCESS --------
        return Response({
            "status": "success",
            "data": {
                "name": name,
                "gender": gender,
                "probability": probability,
                "sample_size": sample_size,
                "is_confident": is_confident,
                "processed_at": processed_at
            }
        }, status=200)

    except requests.exceptions.RequestException:
        return Response(
            {"status": "error", "message": "Upstream API error"},
            status=502
        )

    except Exception:
        return Response(
            {"status": "error", "message": "Internal server error"},
            status=500
        )