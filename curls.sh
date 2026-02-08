# ============================================================
# curls.sh
# Sistema de Gestión de Proyectos y Equipos
# ============================================================

# Crear cliente
curl -X POST http://127.0.0.1:8000/api/clients/create/ \
-H "Content-Type: application/json; charset=utf-8" \
-d '{
  "name": "Empresa ABC",
  "contact_email": "contacto@empresaabc.cl"
}'

# Crear proyecto
curl -X POST http://127.0.0.1:8000/api/projects/create/ \
-H "Content-Type: application/json; charset=utf-8" \
-d '{
  "name": "Sistema ERP",
  "client_id": 1,
  "start_date": "2026-01-01"
}'

# Asignar colaborador a proyecto
curl -X POST http://127.0.0.1:8000/api/assignments/create/ \
-H "Content-Type: application/json; charset=utf-8" \
-d '{
  "project_id": 1,
  "user_id": 1,
  "role": "Backend Developer",
  "assigned_hours": 160
}'

# Listar proyectos con relaciones
curl http://127.0.0.1:8000/api/projects/