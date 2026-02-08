from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Client, Project, Assignment
import json


@csrf_exempt
def create_client(request):
    """
    CREATE - Cliente (padre de relación uno a muchos)
    """

    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    data = json.loads(request.body)

    client = Client.objects.create(
        name=data["name"],
        contact_email=data["contact_email"]
    )

    return JsonResponse({"id": client.id, "status": "created"}, status=201)


@csrf_exempt
def create_project(request):
    """
    CREATE - Proyecto asociado a un cliente
    """

    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    data = json.loads(request.body)

    client = Client.objects.get(id=data["client_id"])

    project = Project.objects.create(
        name=data["name"],
        client=client,
        start_date=data["start_date"],
        end_date=data.get("end_date")
    )

    return JsonResponse({"id": project.id, "status": "created"}, status=201)


@csrf_exempt
def assign_collaborator(request):
    """
    CREATE - Asignación de colaborador a proyecto (M2M con entidad intermedia)
    """

    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    data = json.loads(request.body)

    project = Project.objects.get(id=data["project_id"])
    collaborator = User.objects.get(id=data["user_id"])

    assignment = Assignment.objects.create(
        project=project,
        collaborator=collaborator,
        role=data["role"],
        assigned_hours=data["assigned_hours"]
    )

    return JsonResponse(
        {"id": assignment.id, "status": "assigned"},
        status=201
    )


def list_projects(request):
    """
    READ - Proyectos con cliente y colaboradores
    """

    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])

    projects = Project.objects.select_related("client").prefetch_related("collaborators")

    return JsonResponse(
        [
            {
                "id": project.id,
                "name": project.name,
                "client": project.client.name,
                "collaborators": [
                    {
                        "username": u.username,
                        "role": Assignment.objects.get(
                            project=project,
                            collaborator=u
                        ).role
                    }
                    for u in project.collaborators.all()
                ]
            }
            for project in projects
        ],
        safe=False
    )