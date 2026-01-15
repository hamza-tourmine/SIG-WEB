import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from .models import TarifCubage, OperationBois


def carte_view(request):
    """Affiche la carte + formulaire de calcul."""
    return render(request, "gis_tarif/carte.html")


@csrf_exempt
@require_POST
def calcul_volume_bois(request):
    """API de calcul de volume de bois à partir d'un tarif de cubage."""
    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON invalide"}, status=400)

    espece = data.get("espece")
    zone = data.get("zone")
    diametre_cm = data.get("diametre_cm")
    hauteur_m = data.get("hauteur_m")
    nb_arbres = data.get("nb_arbres", 1)

    if not all([espece, zone, diametre_cm, hauteur_m]):
        return JsonResponse({"error": "Paramètres manquants"}, status=400)

    try:
        tarif = TarifCubage.objects.get(
            espece=espece,
            zone=zone,
            diametre_cm=diametre_cm,
            hauteur_m=hauteur_m,
        )
    except TarifCubage.DoesNotExist:
        return JsonResponse(
            {"error": "Tarif de cubage introuvable pour ces paramètres."},
            status=404,
        )

    volume_total = tarif.volume_m3 * nb_arbres

    op = OperationBois.objects.create(
        espece=espece,
        zone=zone,
        diametre_cm=diametre_cm,
        hauteur_m=hauteur_m,
        nb_arbres=nb_arbres,
        volume_total_m3=volume_total,
    )

    return JsonResponse(
        {
            "operation_id": op.id,
            "volume_par_arbre_m3": tarif.volume_m3,
            "volume_total_m3": volume_total,
        }
    )
