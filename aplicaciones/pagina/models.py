from django.db import models
from django.conf import settings


class Progress(models.Model):
	"""Guarda el progreso de un usuario en un curso.

	topics: diccionario opcional con progreso por tópico, ejemplo:
		{"Límites": 100, "Derivadas": 60, "Integrales": 0}
	"""
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='progresses')
	course = models.CharField(max_length=100)
	percent = models.PositiveSmallIntegerField(default=0)
	topics = models.JSONField(default=dict, blank=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		unique_together = ('user', 'course')
		ordering = ['course']

	def __str__(self):
		return f"{self.user.username} - {self.course}: {self.percent}%"
