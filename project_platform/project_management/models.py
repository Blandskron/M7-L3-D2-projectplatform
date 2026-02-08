from django.db import models
from django.contrib.auth.models import User


class ProfessionalProfile(models.Model):
    """
    RELACIÓN UNO A UNO (OneToOne)

    Extiende al usuario del sistema con información profesional.
    Cada usuario tiene exactamente un perfil profesional.
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="professional_profile",
        help_text="Usuario base del sistema"
    )

    position = models.CharField(
        max_length=100,
        help_text="Cargo profesional (ej: Backend Developer, PM, QA)"
    )

    seniority = models.CharField(
        max_length=50,
        choices=[
            ("JR", "Junior"),
            ("MID", "Mid"),
            ("SR", "Senior"),
            ("LEAD", "Lead"),
        ],
        help_text="Nivel de seniority"
    )

    class Meta:
        db_table = "professional_profile"

    def __str__(self):
        return f"{self.user.username} - {self.position}"


class Client(models.Model):
    """
    ENTIDAD PADRE PARA RELACIÓN UNO A MUCHOS

    Un cliente puede tener múltiples proyectos.
    """

    name = models.CharField(
        max_length=150,
        help_text="Nombre del cliente o empresa"
    )

    contact_email = models.EmailField(
        help_text="Correo de contacto del cliente"
    )

    class Meta:
        db_table = "client"

    def __str__(self):
        return self.name


class Project(models.Model):
    """
    ENTIDAD CENTRAL DEL DOMINIO

    Relaciones:
    - Muchos a uno con Client
    - Muchos a muchos con User mediante Assignment
    """

    name = models.CharField(
        max_length=200,
        help_text="Nombre del proyecto"
    )

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="projects",
        help_text="Cliente dueño del proyecto (uno a muchos)"
    )

    start_date = models.DateField(
        help_text="Fecha de inicio del proyecto"
    )

    end_date = models.DateField(
        null=True,
        blank=True,
        help_text="Fecha de término del proyecto"
    )

    collaborators = models.ManyToManyField(
        User,
        through="Assignment",
        related_name="projects",
        help_text="Colaboradores asignados al proyecto"
    )

    class Meta:
        db_table = "project"

    def __str__(self):
        return self.name


class Assignment(models.Model):
    """
    ENTIDAD INTERMEDIA (ManyToMany con campos adicionales)

    Representa la asignación de un colaborador a un proyecto,
    incluyendo su rol y carga horaria.
    """

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        help_text="Proyecto asignado"
    )

    collaborator = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        help_text="Usuario asignado al proyecto"
    )

    role = models.CharField(
        max_length=100,
        help_text="Rol dentro del proyecto (ej: Dev, PM, QA)"
    )

    assigned_hours = models.PositiveIntegerField(
        help_text="Horas asignadas al proyecto"
    )

    assigned_at = models.DateField(
        auto_now_add=True,
        help_text="Fecha de incorporación al proyecto"
    )

    class Meta:
        db_table = "assignment"
        unique_together = ("project", "collaborator")

    def __str__(self):
        return f"{self.project.name} - {self.collaborator.username}"