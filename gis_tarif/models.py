from django.contrib.gis.db import models  # important pour PostGIS

class ForestParcel(models.Model):
    code_parcelle = models.CharField(max_length=50, unique=True)
    canton = models.CharField(max_length=10, blank=True, null=True)
    surface_ha = models.FloatField(null=True, blank=True)
    geom = models.PolygonField(srid=4326)  # géométrie de la parcelle

    def __str__(self):
        return self.code_parcelle


class TarifCubage(models.Model):
    ESPECE_CHOICES = [
        ("EUCALYPTUS", "Eucalyptus"),
        ("PIN", "Pin"),
        ("CHENE_LIEGE", "Chêne-liège"),
    ]
    espece = models.CharField(max_length=30, choices=ESPECE_CHOICES)
    zone = models.CharField(max_length=50)
    diametre_cm = models.IntegerField()
    hauteur_m = models.FloatField()
    volume_m3 = models.FloatField()

    class Meta:
        unique_together = ("espece", "zone", "diametre_cm", "hauteur_m")

    def __str__(self):
        return f"{self.espece} - {self.zone} D={self.diametre_cm} H={self.hauteur_m}"


class TarifLiege(models.Model):
    zone = models.CharField(max_length=50)
    circonference_cm = models.IntegerField()
    epaisseur_mm = models.FloatField()
    rendement_kg = models.FloatField()

    class Meta:
        unique_together = ("zone", "circonference_cm", "epaisseur_mm")

    def __str__(self):
        return f"Liège {self.zone} C={self.circonference_cm} E={self.epaisseur_mm}"


class OperationBois(models.Model):
    date_calcule = models.DateTimeField(auto_now_add=True)
    espece = models.CharField(max_length=30)
    zone = models.CharField(max_length=50)
    diametre_cm = models.IntegerField()
    hauteur_m = models.FloatField()
    nb_arbres = models.IntegerField(default=1)
    volume_total_m3 = models.FloatField()

    def __str__(self):
        return f"Bois {self.zone} - {self.volume_total_m3} m3"


class OperationLiege(models.Model):
    date_calcule = models.DateTimeField(auto_now_add=True)
    zone = models.CharField(max_length=50)
    circonference_cm = models.IntegerField()
    epaisseur_mm = models.FloatField()
    nb_arbres = models.IntegerField(default=1)
    rendement_total_kg = models.FloatField()

    def __str__(self):
        return f"Liège {self.zone} - {self.rendement_total_kg} kg"
