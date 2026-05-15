# Edenred IMDb Playwright Python

Automatizacion UI de IMDb para el challenge QA Edenred usando Python, Playwright, pytest y behave.

## Stack

- Python 3.11+
- Playwright
- pytest
- behave

## Alcance

La suite cubre los escenarios UI del challenge IMDb:

- Buscar Nicolas Cage, abrir su perfil y seleccionar la primera pelicula completada en proximos estrenos.
- Abrir las peliculas mas taquilleras, entrar al segundo titulo, seleccionar 5 estrellas y llegar hasta Sign in.
- Abrir las 250 mejores series, entrar a Breaking Bad, filtrar fotos por Danny Trejo y abrir la segunda foto.
- Buscar celebridades nacidas ayer, abrir el tercer resultado y tomar captura.
- Buscar celebridades nacidas exactamente hace 40 anos, abrir el primer enlace disponible y tomar captura.

## Instalacion

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m playwright install chromium firefox
```

## Ejecucion pytest

```powershell
pytest -m ui --headless
```

Para ejecutar con navegador visible:

```powershell
pytest -m ui --headed --slowmo 300
```

## Ejecucion behave

```powershell
behave features -D browser=chromium
```

```powershell
behave features -D browser=firefox
```

## Estructura

```text
features/     Escenarios Gherkin del challenge
pages/        Page Objects agrupados por modulo IMDb
steps/        Step definitions y hooks de behave
tests/        Tests pytest parametrizados por navegador
utils/        Utilidades compartidas
screenshots/  Capturas generadas por los escenarios
```

## Notas

- Las capturas generadas no se versionan.
- Las fechas se calculan dinamicamente al ejecutar la suite.
- Los selectores priorizan roles, texto visible y locators estables de Playwright.
