# Software FJ - Sistema Integral de Gestión de Clientes, Servicios y Reservas

Proyecto de POO en Python (UNAD - Programación 213023). Sin base de datos:
toda la información vive en objetos y listas; solo se usan archivos para logs.

## Estructura
```
software_fj/
├── main.py            # Simulación de operaciones
├── logs/              # Archivo de logs (software_fj.log)
├── docs/              # Documentación
└── src/
    ├── exceptions.py  # Excepciones personalizadas
    ├── logger.py      # Configuración de logs
    ├── entidad.py     # Clase abstracta base
    ├── cliente.py
    ├── servicios.py   # Servicio abstracto + 3 derivados
    ├── reserva.py
    └── gestor.py      # Listas internas y orquestación
```

## Ejecución
```
python main.py
```

## Responsables
| Integrante | Módulo | Rama |
|---|---|---|
| 1 | exceptions, logger, entidad, estructura | feature/estructura-base |
| 2 | cliente | feature/cliente |
| 3 | servicios | feature/servicios |
| 4 | reserva, gestor | feature/reserva-gestor |
| 5 | main (simulación) | feature/main-simulacion |

## Flujo de trabajo en equipo (Git)
1. `git checkout main && git pull`
2. `git checkout -b feature/nombre-de-su-rama`
3. Trabajar solo en sus archivos; commits pequeños y descriptivos.
4. `git push -u origin feature/nombre-de-su-rama`
5. Abrir un Pull Request hacia `main` y pedir revisión a un compañero.

## Convenciones
- Todas las entidades heredan de `Entidad` y llaman a `super().__init__()`.
- Las excepciones se importan de `src.exceptions`; el log, de `src.logger`.
- Nunca usar `except Exception: pass`: todo error se registra con `registrar_error`.
- Docstrings en todas las clases y métodos.
