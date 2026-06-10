# Spec Driven Development Learning Guide

## Fase 1: Entender OpenSpec y SDD

### ¿Qué es OpenSpec?
OpenSpec es una herramienta para escribir especificaciones en formato legible (YAML). Estas especificaciones sirven como documentación ejecutable del sistema.

**Ventajas:**
- ✅ Especificaciones legibles por humanos y máquinas
- ✅ Documentación que siempre está actualizada
- ✅ Tests generados automáticamente desde las specs
- ✅ Trazabilidad completa de requisitos → tests → código

### ¿Qué es Spec Driven Development (SDD)?
SDD es una variación de Test-Driven Development donde comenzamos escribiendo especificaciones claras ANTES de cualquier código.

**Ciclo SDD:**
```
1. ESPECIFICAR: Escribir specs en OpenSpec
   └─ Define QUÉ debe hacer el sistema
   
2. GENERAR: OpenSpec genera tests desde las specs
   └─ Tests describen el comportamiento esperado
   
3. RED: Los tests fallan (no hay implementación)
   └─ Esto es NORMAL y ESPERADO
   
4. GREEN: Implementar el código mínimo para pasar tests
   └─ Código simple que cumple la especificación
   
5. REFACTOR: Mejorar el código sin cambiar comportamiento
   └─ Mantener todos los tests pasando
```

## Fase 2: Estructura del Proyecto

### Carpeta `specs/`
Contiene las especificaciones en OpenSpec:
- `price_fetcher.spec.yaml` - Especificación principal
- `bitcoin.spec.yaml` - Detalles de Bitcoin
- `gold.spec.yaml` - Detalles de Oro
- `currency.spec.yaml` - Detalles de Monedas

**Anatomía de una spec:**
```yaml
spec:
  name: NombreDelServicio
  description: Descripción clara
  version: 1.0.0

scenarios:
  - name: "Descripción legible del caso"
    given:      # Precondiciones (Estado inicial)
    when:       # Acción/Evento
    then:       # Resultado esperado

data_types:
  NombreDelTipo:
    campo1: tipo
    campo2: tipo

properties:
  - name: "Invariante o restricción"
    constraint: "Expresión de la regla"

examples:
  nombre_del_ejemplo:
    field: value
```

### Carpeta `src/`
Implementación del código:
- `models.py` - Modelos de datos (basados en data_types de specs)
- `price_fetcher.py` - Lógica principal

**Nota:** Los modelos incluyen validaciones basadas en las especificaciones.

### Carpeta `tests/`
Tests generados/basados en las specs:
- `test_models.py` - Tests de validación de modelos
- `test_price_fetcher.py` - Tests de funcionalidad

**Patrón en los tests:**
```python
def test_nombre_descriptivo(self):
    """Spec: Texto literal de la spec"""
    # Arrange
    # Act
    # Assert
```

## Fase 3: Ejecutar el Ciclo SDD

### Paso 1: Ver los tests FALLAR (Red)
```bash
pytest tests/ -v
```

Esto es correcto. Los tests fallan porque no hemos implementado `fetch_bitcoin()`, etc.

### Paso 2: Implementar el código mínimo (Green)
Implementar las funciones en `src/price_fetcher.py` para pasar los tests.

**Ejemplo mínimo:**
```python
def fetch_bitcoin(self) -> BitcoinPrice:
    """Mínima implementación para pasar tests"""
    return BitcoinPrice(
        price=45000.0,
        timestamp=datetime.utcnow(),
        change_24h=2.5,
        source="mock",
    )
```

### Paso 3: Ejecutar tests (Green)
```bash
pytest tests/ -v
```

Todos los tests deben pasar.

### Paso 4: Refactorizar (Refactor)
Una vez verdes, mejora el código:
- Extrae lógica común
- Mejora nombres
- Añade documentación
- Mantén los tests en verde

### Paso 5: Iterar
Vuelve al Paso 1 con la siguiente especificación.

## Fase 4: Patrones SDD a Observar

### Patrón GWT (Given-When-Then)
Las specs usan el patrón GWT:

**Given** - Establece el contexto/precondiciones
```
- "El servicio está disponible"
- "Bitcoin es un activo válido"
```

**When** - Describe la acción/evento
```
- "Se solicita el precio de Bitcoin"
```

**Then** - Define el resultado esperado
```
- "Se retorna un precio numérico válido"
- "El precio es mayor a 0"
```

### Patrón Data-Driven
Las specs incluyen ejemplos concretos:

```yaml
examples:
  valid_price:
    price: 45000.50
    currency: "USD"
```

Estos ejemplos pueden generar tests parametrizados.

### Propiedades Invariantes
Las specs definen propiedades que SIEMPRE deben cumplirse:

```yaml
properties:
  - name: "Precios siempre positivos"
    constraint: "price > 0"
```

## Fase 5: Próximos Pasos

1. **Instala OpenSpec:**
   ```bash
   pip install openspec
   ```

2. **Genera tests automáticamente:**
   ```bash
   openspec generate specs/
   ```

3. **Ejecuta el ciclo SDD:**
   - Ver fallar (Red)
   - Implementar (Green)
   - Refactorizar (Refactor)

4. **Observa cómo:**
   - Las specs son documentación ejecutable
   - Los tests describen el comportamiento
   - El código implementa las especificaciones
   - Todo está trazable y en sincronía

## Ventajas de este Enfoque

✅ **Claridad:** Las specs son legibles y ejecutables
✅ **Documentación:** La spec es la documentación
✅ **Calidad:** Todos los caminos tienen tests
✅ **Confianza:** Refactoriza sin miedo
✅ **Trazabilidad:** De spec → test → código
✅ **Colaboración:** Specs facilitan discussiones con no-técnicos

## Errores Comunes a Evitar

❌ Escribir tests primero, specs después
❌ Implementar sin leer las specs
❌ Modificar specs para que pasen los tests
❌ Ignorar los ejemplos en las specs
❌ Saltar el refactor por prisa

## Recursos

- [OpenSpec GitHub](https://github.com/Fission-AI/OpenSpec/)
- [BDD Cucumber Docs](https://cucumber.io/docs/gherkin/)
- [Test Driven Development - Kent Beck]

---

<div align="center">

[← Back to README](../README.md) | [→ Usage Reference](03-usage-reference.md)

</div>
