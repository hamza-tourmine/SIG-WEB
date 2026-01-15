import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from .models import (
    OperationBois,
    OperationLiege,
    TarifCubage,
    TarifLiege,
)


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


@csrf_exempt
@require_POST
def calcul_rendement_liege(request):
    """API de calcul de rendement de liège à partir d'un tarif de cubage."""
    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON invalide"}, status=400)

    zone = data.get("zone")
    circonference_cm = data.get("circonference_cm")
    epaisseur_mm = data.get("epaisseur_mm")
    nb_arbres = data.get("nb_arbres", 1)

    if not all([zone, circonference_cm, epaisseur_mm]):
        return JsonResponse({"error": "Paramètres manquants"}, status=400)

    try:
        tarif = TarifLiege.objects.get(
            zone=zone,
            circonference_cm=circonference_cm,
            epaisseur_mm=epaisseur_mm,
        )
    except TarifLiege.DoesNotExist:
        return JsonResponse(
            {"error": "Tarif de rendement liège introuvable pour ces paramètres."},
            status=404,
        )

    rendement_total = tarif.rendement_kg * nb_arbres

    op = OperationLiege.objects.create(
        zone=zone,
        circonference_cm=circonference_cm,
        epaisseur_mm=epaisseur_mm,
        nb_arbres=nb_arbres,
        rendement_total_kg=rendement_total,
    )

    return JsonResponse(
        {
            "operation_id": op.id,
            "rendement_par_arbre_kg": tarif.rendement_kg,
            "rendement_total_kg": rendement_total,
        }
    )
