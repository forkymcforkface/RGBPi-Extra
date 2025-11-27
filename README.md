# OS4 Tools for Pi5 (RGBPI-Extra refactor) WIP

OS4 Tools is a dynamic, modular system utility for OS4 that allows users to manage scripts, tweaks, and system settings through a unified interface. It supports **simple bash scripts**, **interactive on/off toggles**, and **multi-selection menus** with state management.


https://github.com/user-attachments/assets/aaf51379-8319-4318-b506-fffa9a74e059




## Features

* **Dynamic Menus**: Automatically generates menus based on the folder structure.
* **Smart Sorting**: Folders can be ordered numerically (e.g., `01_Tweaks`) but display with clean names ("Tweaks").
* **Script Support**: Run standard `.bash` scripts with visual feedback.
* **Toggle Support**: Create on/off switches with persistent state tracking.
* **Multi-Selection**: Create lists of options for users to choose from.
* **Metadata System**: Add titles, descriptions, and short info text to both folders and scripts.

## Usage

1.  Launch **OS4 Tools** from the Ports menu.
2.  Navigate categories using the **D-Pad**.
3.  Press **A** (or Start) to enter a category.
4.  Select an item:
    * **Standard Scripts**: Press **A** to execute.
    * **Toggles**: Press **A** or **Left/Right** to change state (On/Off).
    * **Selections**: Press **A** to open the list of options, then **A** again to select one.
5.  Press **X** (or Select) to view detailed descriptions for any item.

---

## Developer Guide

You can easily add your own scripts and categories to OS4 Tools. The system automatically scans the `os4-tools` directory.

### 1. Adding Categories (Folders)

Create a new folder in the `os4-tools` directory.
* **Ordering**: Prefix with a number to control sort order (e.g., `99_MyScripts`). The prefix is hidden in the UI.
* **Naming**: Underscores are replaced with spaces (e.g., `User_Scripts` -> "User Scripts").

#### Folder Metadata (`folder.ini`)
To add a description to your category, create a `folder.ini` file inside the folder:

```ini
[Metadata]
title=My Custom Scripts
info=User added scripts
description=A collection of my personal system maintenance scripts.
