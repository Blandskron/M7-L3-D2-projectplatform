# Sistema de Gestión de Proyectos y Equipos con Roles y Asignaciones  
## Django ORM – Relaciones Uno a Uno, Uno a Muchos y Muchos a Muchos

Este proyecto implementa una **capa de acceso a datos completa en Django** para modelar un sistema realista de **gestión de proyectos**, clientes y equipos de trabajo.  
El foco está puesto en el **diseño correcto de modelos y relaciones**, el uso consciente del ORM y la aplicación de **reglas de negocio mediante relaciones y políticas de eliminación**.

No existe frontend.  
No existe lógica innecesaria.  
Todo el valor está en **cómo se modelan y explotan los datos**.

---

## 1. Objetivo del proyecto

El objetivo es demostrar, de forma clara y profesional, cómo Django ORM permite:

- Modelar **relaciones reales del mundo profesional**
- Elegir correctamente entre:
  - OneToOne
  - ForeignKey (Muchos a Uno)
  - ManyToMany con entidad intermedia
- Definir **reglas de eliminación** coherentes (`CASCADE`, `PROTECT`)
- Navegar relaciones desde consultas ORM
- Construir una base sólida para sistemas de gestión reales

---

## 2. Dominio del problema

El sistema representa un entorno típico de trabajo por proyectos:

- Personas usuarias del sistema (usuarios base de Django)
- Información profesional adicional (perfil)
- Clientes que contratan proyectos
- Proyectos asociados a clientes
- Colaboradores asignados a proyectos con roles y horas

Cada elemento cumple un rol específico en el modelo de datos.

---

## 3. Relación UNO A UNO (OneToOne)

### Modelos involucrados
- `User` (modelo nativo de Django)
- `ProfessionalProfile`

### Qué representa

Un **perfil profesional** extiende a un usuario del sistema con información laboral:

- Cargo
- Nivel de seniority

Cada usuario:
- Tiene **un solo perfil profesional**
- No puede existir un perfil sin usuario

### Implementación

```python
user = models.OneToOneField(
    User,
    on_delete=models.CASCADE,
    related_name="professional_profile"
)
````

### Regla de eliminación

* Si se elimina el usuario → se elimina el perfil automáticamente (`CASCADE`)

### Cuándo usar OneToOne

* Cuando se necesita **extender una entidad existente**
* Cuando los datos adicionales no justifican una tabla independiente sin vínculo estricto
* Cuando el ciclo de vida depende totalmente de la entidad principal

---

## 4. Relación UNO A MUCHOS (ManyToOne)

### Modelos involucrados

* `Client`
* `Project`

### Qué representa

* Un cliente puede tener **muchos proyectos**
* Cada proyecto pertenece a **un solo cliente**

Este es uno de los patrones más comunes en sistemas de negocio.

### Implementación

```python
client = models.ForeignKey(
    Client,
    on_delete=models.CASCADE,
    related_name="projects"
)
```

### Regla de eliminación

* Si se elimina un cliente → se eliminan todos sus proyectos (`CASCADE`)

### Cuándo usar ManyToOne

* Cuando existe una relación jerárquica clara
* Cuando la entidad hija no tiene sentido sin la entidad padre
* Cuando se quiere navegar fácilmente:

  * cliente → proyectos
  * proyecto → cliente

### Navegación ORM

```python
client.projects.all()
project.client
```

---

## 5. Relación MUCHOS A MUCHOS (ManyToMany)

### Modelos involucrados

* `Project`
* `User` (colaboradores)

### Qué representa

* Un proyecto puede tener **muchos colaboradores**
* Una persona puede participar en **muchos proyectos**

Esta relación por sí sola no es suficiente, porque **la asignación tiene información propia**.

---

## 6. Entidad intermedia: Assignment

### Por qué es necesaria

La relación proyecto–colaborador requiere datos adicionales:

* Rol dentro del proyecto
* Horas asignadas
* Fecha de incorporación

Esto obliga a usar una **entidad intermedia explícita**.

### Modelo intermedio

`Assignment` representa la asignación real de una persona a un proyecto.

### Implementación

```python
class Assignment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    collaborator = models.ForeignKey(User, on_delete=models.PROTECT)
    role = models.CharField(max_length=100)
    assigned_hours = models.PositiveIntegerField()
    assigned_at = models.DateField(auto_now_add=True)
```

### Regla de unicidad

```python
unique_together = ("project", "collaborator")
```

Esto evita que la misma persona sea asignada dos veces al mismo proyecto.

---

## 7. Reglas de eliminación (decisiones de diseño)

Este proyecto usa **distintas estrategias de borrado** para reflejar reglas reales:

### CASCADE

* Usuario → Perfil profesional
* Cliente → Proyectos
* Proyecto → Asignaciones

Cuando la entidad principal desaparece, sus dependencias también.

### PROTECT

* Usuario en Assignment

Un colaborador **no puede eliminarse** si está asignado a proyectos.
Esto protege la integridad histórica y operativa del sistema.

---

## 8. Flujo de creación de datos

### Crear un cliente

* Se inserta una fila en `client`

### Crear un proyecto

1. Se obtiene el cliente (FK)
2. Se crea el proyecto asociado

### Asignar colaborador

1. Se obtiene el proyecto
2. Se obtiene el usuario
3. Se crea la asignación con rol y horas

Este flujo muestra cómo:

* El ORM impone las reglas del modelo
* Las relaciones guían la lógica de negocio
* No se requiere SQL manual

---

## 9. Consultas ORM relevantes

### Proyectos con cliente y colaboradores

```python
Project.objects.select_related("client").prefetch_related("collaborators")
```

* `select_related` optimiza relaciones ManyToOne
* `prefetch_related` optimiza ManyToMany

### Navegación de relaciones

```python
project.client.name
project.collaborators.all()
user.projects.all()
```

El ORM permite recorrer el modelo de datos como un grafo.

---

## 10. API y endpoints

El proyecto expone endpoints mínimos en JSON para demostrar el uso del ORM:

| Método | Endpoint                   | Acción                          |
| ------ | -------------------------- | ------------------------------- |
| POST   | `/api/clients/create/`     | Crear cliente                   |
| POST   | `/api/projects/create/`    | Crear proyecto                  |
| POST   | `/api/assignments/create/` | Asignar colaborador             |
| GET    | `/api/projects/`           | Listar proyectos con relaciones |

El uso de `curl` permite interactuar con la API como cliente real HTTP.

---

## 11. Panel de administración

Todos los modelos están registrados en el admin:

* ProfessionalProfile
* Client
* Project
* Assignment

Esto permite:

* Visualizar relaciones
* Validar reglas de eliminación
* Inspeccionar datos sin construir interfaz adicional

---

## 12. Conceptos reforzados por el proyecto

* El ORM no es solo CRUD
* Las relaciones representan **decisiones de negocio**
* Una mala relación genera problemas aguas abajo
* Una entidad intermedia es una herramienta, no una complicación
* Django impone coherencia si el modelo está bien diseñado

---

## 13. Posibles extensiones

* Estados de proyecto
* Historial de asignaciones
* Control de horas reales vs asignadas
* Reportes agregados por cliente o colaborador
* Autorizaciones basadas en rol dentro del proyecto
