# MathLite — Intérprete DSL

Intérprete completo para el DSL MathLite con análisis léxico, sintáctico, semántico e interpretación del AST.  
**Backend:** Python + FastAPI | **Frontend:** React + Vite

---

## Estructura del Proyecto

```
mathlite/
├── backend/
│   ├── main.py                         ← Arranque del servidor (solo CORS + rutas)
│   ├── requirements.txt
│   ├── core/                           ← Motor del intérprete (sin modificar lógica)
│   │   ├── __init__.py
│   │   ├── lexer.py                    ← Analizador léxico (tokenizador)
│   │   ├── parser_ml.py               ← Parser recursivo descendente + AST
│   │   ├── semantic.py                ← Análisis semántico + tabla de símbolos
│   │   ├── interpreter.py             ← Evaluador del AST
│   │   └── ast_printer.py             ← Visualización textual, markdown y visual del AST
│   ├── controllers/
│   │   └── expression_controller.py   ← Controlador de peticiones
│   ├── services/
│   │   └── expression_service.py      ← Orquestación del pipeline completo
│   ├── dtos/
│   │   ├── requests.py                ← Esquemas de entrada (Pydantic)
│   │   └── responses.py               ← Esquemas de salida (Pydantic)
│   └── routes/
│       └── expression_routes.py       ← Definición de endpoints FastAPI
└── frontend/
    ├── index.html
    ├── vite.config.js
    ├── package.json
    └── src/
        ├── main.jsx
        ├── index.css
        ├── App.jsx                     ← Orquestador principal (~140 líneas)
        ├── constants/
        │   └── testCases.js            ← Casos de prueba y código por defecto
        ├── styles/
        │   └── appStyles.js            ← Estilos inline centralizados
        ├── services/
        │   └── api.js                  ← Comunicación con el backend
        ├── helpers/
        │   └── utils.js                ← Utilidades (escHtml, TK_CATS)
        └── components/
            ├── Titlebar.jsx            ← Barra de título + tabs
            ├── EditorPanel.jsx         ← Editor de código + errores
            ├── ConsolePanel.jsx        ← Consola de salida
            ├── TokensPanel.jsx         ← Flujo de tokens
            ├── AnalysisPanel.jsx       ← Análisis léxico/sintáctico/semántico
            ├── ASTPanel.jsx            ← Árbol de sintaxis abstracta con render Mermaid
            ├── TestsPanel.jsx          ← Casos de prueba
            └── common/
                ├── ConsoleLine.jsx
                ├── SectionHd.jsx
                ├── SemTbl.jsx
                └── ChkItem.jsx
```

---

## Arquitectura Backend

```
request → routes → controller → service → core (lexer/parser/semantic/interpreter) → response
```

| Capa | Responsabilidad |
|------|-----------------|
| **routes/** | Define endpoints FastAPI |
| **controllers/** | Recibe peticiones, delega al servicio |
| **services/** | Orquesta el pipeline completo del intérprete |
| **core/** | Lógica del compilador (lexer → parser → semantic → interpreter) |
| **dtos/** | Esquemas de validación Pydantic |

---

## Instalación y Ejecución

### 1. Backend (Python)

```bash
cd backend
pip install -r requirements.txt
python main.py
# Servidor en http://localhost:8000
```

### 2. Frontend (React)

```bash
cd frontend
npm install
npm run dev
# App en http://localhost:3000
```

Abre el navegador en **http://localhost:3000**

---

## Fases Implementadas

| Fase | Descripción | Archivo |
|------|-------------|---------|
| 1 | Especificación del lenguaje | `core/lexer.py` (tokens, AFD) |
| 2 | Analizador léxico | `core/lexer.py` |
| 3 | Parser + AST | `core/parser_ml.py` + `core/ast_printer.py` |
| 4 | Análisis semántico | `core/semantic.py` |
| 5 | Intérprete | `core/interpreter.py` |
| 6 | Aplicación web | `frontend/` |
| 7 | Visualización dinámica del AST | `frontend/src/components/ASTPanel.jsx` + Mermaid |

## Visualización del AST

La pestaña **árbol AST** del frontend renderiza el AST con Mermaid de forma dinámica y mantiene una vista textual de respaldo cuando el render no está disponible.

Dependencias relevantes:

- `frontend/package.json` incluye `mermaid` como dependencia.
- `frontend/src/components/ASTPanel.jsx` construye el grafo Mermaid y lo renderiza en tiempo de ejecución.

---

## API

### `POST /api/run`
```json
{ "code": "let x = 5\nprint(x)" }
```
Respuesta:
```json
{
  "tokens":       [...],
  "ast":          {...},
  "ast_text":     "Program\n└─ ...",
  "ast_markdown": "- **Program**\n  - ...",
  "ast_visual":   "  Program\n  / \\\n...",
  "node_count":   5,
  "symbols":      [...],
  "output":       ["5"],
  "errors":       [],
  "lex_errors":   [],
  "syn_errors":   [],
  "sem_errors":   [],
  "run_errors":   []
}
```

---

## Lenguaje MathLite

```
-- Variables
let x = 5
let y = 3.14

-- Funciones
def area(b, h) {
  return (b * h) / 2
}

-- Condicionales
if x > 0 {
  print("positivo")
} else {
  print("negativo")
}

-- Ciclos
let i = 1
while i <= 10 {
  print(i)
  let i = i + 1
}

-- Funciones integradas
print(sin(3.14159))
print(sqrt(16))
print(abs(-5))
```

### Tipos de datos
- `Int` — enteros: `42`, `-7`
- `Real` — decimales: `3.14`, `-0.5`
- `Bool` — lógicos: `true`, `false`
- `String` — cadenas: `"hola mundo"`

### Operadores (por precedencia)
| Operador | Descripción |
|----------|-------------|
| `or` | disyunción lógica |
| `and` | conjunción lógica |
| `not` | negación |
| `== != < > <= >=` | comparación |
| `+ -` | suma/resta |
| `* / %` | multiplicación/división/módulo |
| `^` | potencia (asociatividad derecha) |
| `-` unario | negación aritmética |
