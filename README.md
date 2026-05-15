# Edenred IMDb Playwright Python

Repositorio IMDb del challenge QA Edenred, organizado para escalar por modalidad de pruebas.

## Estructura

```text
Edenred-IMDb-Playwright-Python/
+-- API/          # reservado para futuras pruebas API relacionadas a IMDb
+-- UI/           # automatizacion UI de IMDb con Python + Playwright
+-- Performance/  # reservado para futuras pruebas de performance
+-- Mobile/       # reservado para futuras pruebas mobile
```

## UI

Automatizacion UI de IMDb usando Python, Playwright, pytest y behave.

### Stack

- Python 3.11+
- Playwright
- pytest
- behave

### Alcance

La suite cubre los escenarios UI del challenge IMDb:

- Buscar Nicolas Cage, abrir su perfil y seleccionar la primera pelicula completada en proximos estrenos.
- Abrir las peliculas mas taquilleras, entrar al segundo titulo, seleccionar 5 estrellas y llegar hasta Sign in.
- Abrir las 250 mejores series, entrar a Breaking Bad, filtrar fotos por Danny Trejo y abrir la segunda foto.
- Buscar celebridades nacidas ayer, abrir el tercer resultado y tomar captura.
- Buscar celebridades nacidas exactamente hace 40 anos, abrir el primer enlace disponible y tomar captura.

### Instalacion

```powershell
cd UI
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m playwright install chromium firefox
```

### Ejecucion pytest

```powershell
cd UI
pytest -m ui --headless
```

Con navegador visible:

```powershell
cd UI
pytest -m ui --headed --slowmo 300
```

### Ejecucion behave

```powershell
cd UI
behave features -D browser=chromium
```

```powershell
cd UI
behave features -D browser=firefox
```

### Estructura UI

```text
UI/features/challenge/   Escenarios propios del challenge Edenred
UI/features/search/      Reservado para busquedas futuras
UI/features/titles/      Reservado para paginas y flujos de titulos
UI/features/people/      Reservado para perfiles de celebridades
UI/features/media/       Reservado para galerias, fotos y videos
UI/features/navigation/  Reservado para menu y navegacion general
UI/pages/                Page Objects agrupados por modulo IMDb
UI/steps/                Step definitions y hooks de behave
UI/tests/                Tests pytest parametrizados por navegador
UI/utils/                Utilidades compartidas
UI/screenshots/          Capturas generadas por los escenarios
```

## Notas

- `API/`, `Performance/` y `Mobile/` quedan preparados para crecimiento futuro.
- Las capturas generadas no se versionan.
- Las fechas se calculan dinamicamente al ejecutar la suite.
- Los selectores priorizan roles, texto visible y locators estables de Playwright.

