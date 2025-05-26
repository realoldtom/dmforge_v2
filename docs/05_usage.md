## Version: 1.1 (2025-05-26)

# DMForge CLI Usage Guide

## Main CLI
```bash
Usage: main.py [OPTIONS] COMMAND [ARGS]...                                    
                                                                               
+- Options -------------------------------------------------------------------+
| --install-completion          Install completion for the current shell.     |
| --show-completion             Show completion for the current shell, to     |
|                               copy it or customize the installation.        |
| --help                        Show this message and exit.                   |
+-----------------------------------------------------------------------------+
+- Commands ------------------------------------------------------------------+
| deck                                                                        |
| render                                                                      |
+-----------------------------------------------------------------------------+
```

## Deck: Build
```bash
Usage: main.py deck build [OPTIONS]                                           
                                                                               
 Build a filtered deck of spells from input data.                              
                                                                               
+- Options -------------------------------------------------------------------+
| --spell-data          PATH     Path to spell JSON                           |
|                                [default: data\spells\spells.json]           |
| --output              PATH     Path to save deck JSON [default: None]       |
| --name                TEXT     Deck name [default: Untitled Deck]           |
| --class       -c      TEXT     Class filters [default: None]                |
| --level       -l      INTEGER  Level filters [default: None]                |
| --school      -s      TEXT     School filters [default: None]               |
| --help                         Show this message and exit.                  |
+-----------------------------------------------------------------------------+
```

## Render: Render
```bash
Usage: main.py render render [OPTIONS]                                        
                                                                               
 Render a deck as a PDF or HTML using the given JSON input.                    
                                                                               
+- Options -------------------------------------------------------------------+
| --input                 PATH  Path to deck JSON file                        |
|                               [default: exports\dev\deck_latest.json]       |
| --output                PATH  Path to rendered output (PDF or HTML)         |
|                               [default: None]                               |
| --format        -f      TEXT  Output format: pdf or html [default: pdf]     |
| --template-dir          PATH  Path to templates directory                   |
|                               [default: src\dmforge\resources\templates]    |
| --asset-dir             PATH  Path to assets directory                      |
|                               [default: src\dmforge\resources\assets]       |
| --verbose       -v            Enable verbose output                         |
| --help                        Show this message and exit.                   |
+-----------------------------------------------------------------------------+
```

## Render: Validate
```bash
Usage: main.py render validate [OPTIONS]                                      
                                                                               
 Validate a deck JSON file without rendering.                                  
                                                                               
+- Options -------------------------------------------------------------------+
| --input        PATH  Path to deck JSON file                                 |
|                      [default: exports\dev\deck_latest.json]                |
| --help               Show this message and exit.                            |
+-----------------------------------------------------------------------------+
```
