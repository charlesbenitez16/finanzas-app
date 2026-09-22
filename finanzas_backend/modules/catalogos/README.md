# Módulo catalogos — módulo de referencia (completo)

Este módulo está **100% implementado** a propósito: es tu plantilla para
replicar el mismo patrón en `ingresos`, `gastos`, `planes_financieros`,
`alertas` y `usuarios`. Cada archivo tiene comentarios explicando el
*por qué* de cada decisión, no solo el *qué*.

## Qué se implementó en cada capa (y por qué, en ese orden)

**1. `shared/domain/base_entity.py` → `Entity.es_nueva()`**
Un método trivial (`return self.id is None`), pero establece el patrón:
la clase base de toda entidad no sabe nada de Django.

**2. `domain/entities.py` → `CategoriaGasto.es_global()`**
Lógica de negocio que la entidad SÍ puede resolver por sí sola (no
necesita ver nada más que sus propios atributos).

Ojo con `NivelPrioridad`: originalmente tenía un método
`es_prescindible()` marcado como TODO con una pregunta de diseño. La
resolución fue **eliminarlo**: esa entidad, aislada, no puede saber si es
"la más baja" sin conocer a las demás. Quedó documentado en el archivo
como ejemplo de que no todo comportamiento pertenece a la entidad.

**3. `infrastructure/repositories.py` → el mapeo ORM ↔ dominio**
El método `_a_entidad()` en cada repositorio es el corazón del patrón:
convierte un `*Model` de Django en una entidad de dominio. Todo lo demás
(`obtener_por_id`, `listar_para_usuario`, `crear`) sigue el mismo molde:
consultar con el ORM, mapear con `_a_entidad()`, devolver la entidad.

**4. `application/use_cases/*.py` → la orquestación**
Con el repositorio ya funcionando, los casos de uso son cortos: reciben
el repositorio (inyección de dependencias), lo llaman, aplican alguna
regla si corresponde (ver `crear_categoria_personalizada.py`, que valida
duplicados antes de crear).

**5. `interfaces/api/serializers.py` → corrección importante**
La versión con TODOs los tenía como `ModelSerializer`, apuntando al
modelo Django. Al completarlos encontré que eso **rompe**: un
`ModelSerializer` para una `ForeignKey` espera un atributo `usuario` (la
relación completa) en la instancia, pero nuestras entidades de dominio
solo tienen `usuario_id` (un int). Los cambié a `serializers.Serializer`
simples, con campos que coinciden con la entidad de dominio, no con el
modelo ORM. **Replicá esto en los próximos módulos**: los serializers
son parte de `interfaces/`, no deberían conocer `infrastructure/`.

**6. `interfaces/api/views.py` → conectar todo**
Patrón repetido en las tres vistas: armar el caso de uso con su
repositorio → ejecutarlo con los datos del request → serializar la
respuesta.

**7. Tests, en las tres capas**
- `tests/domain/` y `tests/application/`: **Python puro**, sin Django.
  El de `application/` usa `RepositorioCategoriaGastoFalso`, una
  implementación en memoria del mismo puerto que usa el repositorio
  Django real — así se prueban los casos de uso sin base de datos.
  Podés correrlos directo, sin Docker ni Postgres corriendo:
  ```bash
  uv run python -m unittest modules.catalogos.tests.domain.test_entities modules.catalogos.tests.application.test_use_cases -v
  ```
- `tests/infrastructure/`: sí necesitan Postgres real (`uv run manage.py
  test`). Tienen un gotcha propio: como los modelos son `managed =
  False`, Django no crea las tablas en la base de datos de test
  automáticamente. Cada clase de test las crea con SQL crudo en
  `setUpClass` (ver el comentario al inicio del archivo).

## Cómo replicar este patrón en el próximo módulo (ej. `ingresos`)

1. Copiá la estructura de carpetas de `catalogos/` (`domain/`,
   `application/`, `infrastructure/`, `interfaces/`, `tests/`)
2. `domain/entities.py`: definí la entidad (ej. `Ingreso`) como dataclass
   heredando de `Entity`. Pensá qué comportamiento SÍ pertenece a la
   entidad (como `es_global()`) vs. qué necesita contexto externo (como
   el caso `es_prescindible()` que eliminamos)
3. `domain/ports/repositories.py`: definí la interfaz abstracta con los
   métodos que la aplicación va a necesitar
4. `infrastructure/models.py`: el modelo Django. Decidí si aplica
   `managed = False` (si la tabla ya existe en `01_schema.sql`, como acá)
5. `infrastructure/repositories.py`: implementá el mapeo `_a_entidad()`
   y los métodos del puerto
6. `application/use_cases/`: un archivo por caso de uso
7. `interfaces/api/`: serializers como `Serializer` simple (no
   `ModelSerializer`), vistas que conectan con los casos de uso
8. No olvides: `models.py` y `admin.py` "puente" en la raíz del módulo,
   `MIGRATION_MODULES` en `config/settings/base.py`, y agregar el módulo
   a `INSTALLED_APPS`

## Cómo probar manualmente (sin Postman/curl)

Mientras no tengas el módulo de usuarios armado, `NivelesPrioridadView`
no requiere login, pero `CategoriasGastoView` sí. Para probarla:

```bash
uv run manage.py createsuperuser
uv run manage.py runserver
```

Iniciá sesión en `http://localhost:8000/admin/` y, en el mismo
navegador, andá a `http://localhost:8000/api/catalogos/categorias/` — la
API navegable de DRF reutiliza esa sesión.

O desde la shell, sin servidor ni HTTP de por medio:

```bash
uv run manage.py shell
```

```python
from modules.catalogos.infrastructure.repositories import DjangoNivelPrioridadRepository
from modules.catalogos.application.use_cases.listar_niveles_prioridad import ListarNivelesPrioridadUseCase

repo = DjangoNivelPrioridadRepository()
caso_de_uso = ListarNivelesPrioridadUseCase(repositorio=repo)
caso_de_uso.ejecutar()
```

Si devuelve los 3 niveles del seed SQL (Esencial, Importante,
Prescindible) en ese orden, el módulo funciona de punta a punta.
