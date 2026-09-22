# Módulo `usuarios` — esqueleto (kata)

Entidad `USUARIOS` del `.mermaid` / tabla `usuarios` de `01_schema.sql`.
Estructura calcada de `modules/catalogos/`. Todo el cuerpo está vacío
(`raise NotImplementedError` / `self.skipTest`), con la consigna en cada
docstring y un `# TODO:` por pieza.

## Qué implementar y en qué orden

1. **`domain/entities.py` → `Usuario`**: `esta_activo()` (lectura directa,
   como `CategoriaGasto.es_global()`), `desactivar()` (baja lógica).
2. **`domain/ports/repositories.py` → `UsuarioRepository`**: contrato de
   persistencia. `obtener_por_email` / `existe_email` son la traducción
   del `UNIQUE (email)` del schema.
3. **`infrastructure/models.py`**: `UsuarioModel` (`managed = False`).
   ⚠️ **Decisión pendiente**: cruce entre esta tabla `usuarios` y
   `settings.AUTH_USER_MODEL` (`auth_user`), que es lo que usan las FK de
   los demás módulos. Documentado en el docstring del archivo.
4. **`infrastructure/repositories.py`**: `_a_entidad()` + métodos del puerto.
5. **`application/use_cases/`**: `registrar_usuario` (email único + hash),
   `autenticar_usuario` (email + hash + activo), `desactivar_usuario`.
6. **`interfaces/api/`**: `serializers.Serializer` simples (nunca sale
   `password_hash`), vistas `RegistroView` / `LoginView`.

## Consultas SQL mapeadas (regla 4)

| SQL | Puerto | Caso de uso |
|---|---|---|
| `usuarios.email UNIQUE` | `UsuarioRepository.existe_email` / `obtener_por_email` | `RegistrarUsuarioUseCase` |

## Probar

```bash
uv run python -m unittest modules.usuarios.tests.domain.test_entities \
    modules.usuarios.tests.application.test_use_cases -v
```
