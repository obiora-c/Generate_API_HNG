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
            status=status.HTTP_400_BAD_REQUEST
        )

    if not isinstance(name, str):
        return Response(
            {"status": "error", "message": "Name must be a string"},
            status=status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    try:
        # -------- CALL EXTERNAL API --------
        response = requests.get(
            "https://api.genderize.io",
            params={"name": name},
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        response.raise_for_status()
        data = response.json()

        gender = data.get("gender")
        probability = data.get("probability")
        count = data.get("count")

        # -------- NORMALIZE DATA TYPES --------
        try:
            probability = float(probability)
        except (TypeError, ValueError):
            probability = None

        try:
            count = int(count)
        except (TypeError, ValueError):
            count = 0

        # -------- EDGE CASE --------
        if gender is None or count == 0:
            return Response(
                {"status": "error", "message": "No prediction available for the provided name"},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        # -------- PROCESS DATA --------
        sample_size = count
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
        }, status=status.HTTP_200_OK)

    except requests.exceptions.RequestException:
        return Response(
            {"status": "error", "message": "Upstream API error"},
            status=status.HTTP_502_BAD_GATEWAY
        )

    except Exception:
        return Response(
            {"status": "error", "message": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )