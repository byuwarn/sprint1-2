# IT Asset & Vulnerability Manager

*[Ler em português](./README.pt-br.md)*

A command-line (CLI) application in Python for registering and managing IT assets and their associated security vulnerabilities. Built as a study project for a Cybersecurity course, applying clean code practices (expressive naming, single-responsibility functions, error handling that doesn't leak internal details).

## ✨ Features

- **Asset registration**: ID, name, owner, and status (Active / Inactive / Under maintenance), with input validation
- **Asset listing**: view all registered assets or look up a specific one by ID
- **Asset deletion**: remove an asset by ID
- **Vulnerability management**: add, list, and remove vulnerabilities tied to a given asset, with a severity level (Low / Medium / High)
- **Data persistence**: data is automatically saved to an `ativos.json` file and reloaded on every run

## 🫧 Tech Stack

- Python 3
- Standard library modules: `json`, `enum`

## ✨ Project Structure

```
.
├── main code s1.py     # Entry point: interactive menu and program flow
├── funcoes_s1.py         # Business logic, validation, and data persistence
├── .gitignore
└── README.md
```

> The `ativos.json` file (saved data) is generated automatically on first run and is not version-controlled.

## 🫧 Getting Started

Requirement: Python 3.8 or higher.

```bash
git clone https://github.com/byuwarn/it-asset-vulnerability-manager.git
cd it-asset-vulnerability-manager
python "main code s1.py"
```

The program opens an interactive menu in the terminal. Follow the numbered options to register assets, manage vulnerabilities, and save data.

## ✨ Main Menu

```
1 - Register asset
2 - List assets
3 - Delete asset
4 - Manage vulnerabilities
5 - Exit
```

Inside option **4 (Manage vulnerabilities)**, a submenu lets you list, add, and remove vulnerabilities for a specific asset.

## 🫧 Project Status

This project is developed incrementally across sprints in the early weeks of my Cybersecurity degree at the Federal University of Uberlândia, with a focus on:
- Clear, expressive naming
- Single-responsibility functions
- Error handling that doesn't expose internal details
- User input validation

## ✨ License

Study project, free to use for educational purposes.
