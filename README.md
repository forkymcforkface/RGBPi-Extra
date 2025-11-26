# OS4 Tools

OS4 Tools is a dynamic, modular system utility for OS4 that allows users to manage scripts, tweaks, and system settings through a unified interface. It supports simple executable scripts as well as interactive toggles with state management.

## Features

*   **Dynamic Menus**: Automatically generates menus based on the folder structure.
*   **Smart Sorting**: Folders can be ordered numerically (e.g., `01_Tweaks`) but display with clean names ("Tweaks").
*   **Toggle Support**: Create on/off switches with persistent state tracking.
*   **Metadata System**: Add titles, descriptions, and short info text to both folders and scripts.
*   **Safe Execution**: Visual feedback during script execution ("Executing..." / "Complete").

## Usage

1.  Launch **OS4 Tools** from the Ports menu.
2.  Navigate categories using the **D-Pad**.
3.  Press **A** (or Start) to enter a category.
4.  Select a script or toggle:
    *   **Scripts**: Press **A** to execute.
    *   **Toggles**: Press **A** or **Left/Right** to change state (On/Off).
5.  Press **X** (or Select) to view detailed descriptions for any item.

---

## Developer Guide

You can easily add your own scripts and categories to OS4 Tools. The system automatically scans the `os4-tools` directory.

### 1. Adding Categories (Folders)

Create a new folder in the `os4-tools` directory.
*   **Ordering**: Prefix with a number to control sort order (e.g., `99_MyScripts`). The prefix is hidden in the UI.
*   **Naming**: Underscores are replaced with spaces (e.g., `User_Scripts` -> "User Scripts").

#### Folder Metadata (`folder.ini`)
To add a description to your category, create a `folder.ini` file inside the folder:

```ini
[Metadata]
title=My Custom Scripts
info=User added scripts
description=A collection of my personal system maintenance scripts.
```
# description: Clears the system page cache, dentries, and inodes to free up memory.
```

*   **title**: Overrides the filename in the menu.
*   **info**: Short text shown at the bottom of the screen.
*   **description**: Long text shown in the popup info view (Press X).

### 2. Adding Scripts

Supported format: `.bash`
Place your scripts inside any category folder.

#### Script Metadata
Add special comments at the top of your script to define how it appears in the menu:

```bash
#!/bin/bash
# title: Clear Cache
# info: Free RAM
# description: Clears the system page cache, dentries, and inodes to free up memory.
```

*   **title**: Overrides the filename in the menu.
*   **info**: Short text shown at the bottom of the screen.
*   **description**: Long text shown in the popup info view (Press X).

### 3. Creating Toggles
Toggles are special scripts that have `On` and `Off` states. You define these states using python-style `def` blocks inside your `.bash` file.

**Structure:**
```bash
#!/bin/bash
# title: SSH Server
# info: Remote Access
# description: Enable or disable the SSH server for remote access.

def on
    systemctl start ssh
    echo "SSH Started"

def off
    systemctl stop ssh
    echo "SSH Stopped"

def status
    # Return exit code 0 for ON, 1 for OFF
    systemctl is-active ssh --quiet
```

*   **def on**: Commands to run when switching to ON.
*   **def off**: Commands to run when switching to OFF.
*   **def status** (Optional): Commands to check current state.
    *   If omitted, OS4 Tools will track state locally in `config.ini`.
    *   If provided, it should return exit code 0 for ON and non-zero for OFF.

### 4. Creating Selection Scripts
Selection scripts allow you to choose from a list of options.

**Metadata Required:**
*   `# type: selection`
*   `# options: Option 1, Option 2, Option 3` (Comma separated list)
*   `# default: Option 1` (Optional default value)

**Structure:**
```bash
#!/bin/bash
# title: System Performance
# type: selection
# options: Powersave, Balanced, Performance
# default: Balanced

def powersave
    echo "powersave" | tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor

def balanced
    echo "ondemand" | tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor

def performance
    echo "performance" | tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor

def status
    # Optional: Return the current value to override config.ini
    cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
```

*   **Function Names**: Create a `def` block for each option. The function name should be the option name in lowercase, with spaces replaced by underscores (e.g., "High Performance" -> `def high_performance`).
*   **Persistence**: The selected option is automatically saved to `config.ini`.
*   **Status Override**: If you provide a `def status` block that outputs a valid option name, it will take precedence over the saved value. If it returns nothing, the saved value is used.

### Environment Variables

Your scripts have access to these variables:
*   `$CONFIG_FILE`: Path to the local `config.ini` for OS4 Tools.
*   `$RTK_CFG_FILE`: Path to the main OS4 system configuration.
