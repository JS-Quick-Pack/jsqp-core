<div align="center">

  # 🟣 jsqp-core
  
  <sub>An open-source Minecraft package management library.</sub>
  
</div>

> #### ⚠️ Warning: ``JSQPCore`` is very work in progress so some utils and code will be incomplete. IT'S NOT READY, give it time to develop and mature.

<div align="center">

  ### [🚀 Supported Launchers](https://github.com/JS-Quick-Pack/jsqp-core/blob/main/LAUNCHERS.md)
  
</div>

```python
from jsqp_core.packages import TexturePack

pack = TexturePack("./Whimscape_1.20_r3.zip")

print(pack)
```
#### Output
```python
[INFO] (JSQP_CORE) - [TexturePackParser] [Whimscape_1.20_r3] Parsed the texture pack 'Whimscape_1.20_r3'!
[INFO] (JSQP_CORE) - [TexturePackParser] [Whimscape_1.20_r3] Detected Version -> JAVA_1_20
🖌️  TexturePack = {
    'display_name': 'Whimscape_1.20_r3',
    'mc_meta': {
        'pack': {'pack_format': 15, 'description': '§6A crisp pixel art look'}
    },
    'minecraft_version': '1.20'
}
```
<div align="center">

  #### [Want to see what is going on under the hood of this example?](#under-the-hood-of-the-example)
  
</div>

## 🤔 What the hell is this?
🟣 ``JS:QP Core`` is an open-source Minecraft package manager written in Python.

> WHY THE FUCK DO I NEED A PACKAGE MANAGER FOR MINECRAFT, you may ask...

First of all, jsqp-core isn't just a package manager; it will also serve as our API capable of handling various tasks from managing Minecraft content to programmatically editing content all via Python.

It can already:
- Detect the exact Minecraft version of texture packs.
  ```python
  pack = TexturePack("./goldish_pack")
  print(pack.minecraft_version)
  ```
- Parse texture packs for details like pack format, real pack name and pack description.
  ```python
  pack = TexturePack("./goldish_pack")
  
  print(pack.name)
  print(pack.description)
  print(pack.mc_meta)
  
  # There are also some low-level attributes like paths under the parser.
  print(pack.parser.root_path)
  print(pack.parser.assets_path)
  ```
- Install packs into the game.
  ```python
  minecraft = Minecraft()
  pack = TexturePack("./goldish_pack")
  
  minecraft.install(pack)
  ```
- *and much more*

Imagine you had a bunch of texture packs on different Minecraft installs, now you have to manually move/copy those packs around whenever you want one on a different installation. JS:QP core can manage all of that for you with just a SINGLE copy of that texture pack increasing the unused disk space on your system.

## 🧠 I'm still not buying it.
The current state of JS:QP core may appear underwhelming as it currently functions solely as a library without any practical implementations **yet**. Soon we'll have things like GUI apps, command-line interfaces and more. You are also open to using this library however you want. I'm designing this library in a way that allows you to leverage it in any way you see fit.

## ❓ *Questions, I guess...*
  - Is jsqp core just for texture packs?
    - Nope, jsqp core will soon manage more than just texture packs, it's only that our focus right now is texture packs but once that is all gucci we can begin handling other content like mods, data packs and skins.

  - What is the `jsqp` in jsqp core?
    - This library was meant to be written within the [JS:QP app](https://github.com/JS-Quick-Pack/jsqp-app) which was a gui app I used to work on. I decided to separate the two codebases for the good of it being a standalone open-source library other developers can leverage and allowing us to maintain the codebase easier than ever.

## 🏆 The Goal
The goal of JSQPCore is to create an open-source library that can manage resources like texture packs, mods, data packs, skins and a lot more from Minecraft. Alongside that, because of its 100% open-source nature, we plan to support as many Minecraft launchers and versions as possible, encouraging the community to do so too.

<br>

## 🤓 The Nerdy Stuff
<div align="center">

  ### Under the hood of the example.
  Let's re-run the example code from earlier with debugging enabled to showcase to you what is going on under the hood. ✨
  
</div>

```python
import logging

from jsqp_core.logger import core_logger
from jsqp_core.packages import TexturePack

core_logger.setLevel(logging.DEBUG) # Debugging mode, also know as 🤓 nerd mode...

pack = TexturePack("./Whimscape_1.20_r3.zip")

print(pack)
```
#### Output
```python
[DEBUG] (JSQP_CORE) - [FilePackage] Extracting zip to temp directory...
[DEBUG] (JSQP_CORE) - [TexturePackParser] [Whimscape_1.20_r3] Assets folder found!
[INFO] (JSQP_CORE) - [TexturePackParser] [Whimscape_1.20_r3] Parsed the texture pack 'Whimscape_1.20_r3'!
[DEBUG] (JSQP_CORE) - [Package] Updated file package path object to '/home/goldy/.devgoldy/JSQPCore/.temp/Whimscape_1.20_r3'!
[DEBUG] (JSQP_CORE) - [Package] Updated package name to 'Whimscape_1.20_r3'!
[DEBUG] (JSQP_CORE) - [Package] Texture Pack Initialized!
[DEBUG] (JSQP_CORE) - [TexturePackParser] [Whimscape_1.20_r3] Parsing pack.mcmeta...
[DEBUG] (JSQP_CORE) - [TexturePackParser] [Whimscape_1.20_r3] Parsing pack.mcmeta...
[DEBUG] (JSQP_CORE) - [TexturePackParser] [Whimscape_1.20_r3] Parsing pack.mcmeta...
[DEBUG] (JSQP_CORE) - [TexturePackParser] [Whimscape_1.20_r3] Detecting minecraft version of 'Whimscape_1.20_r3'...
[DEBUG] (JSQP_CORE) - [TexturePackParser] [Whimscape_1.20_r3] Testing against 'JAVA_1_20' map...
[INFO] (JSQP_CORE) - [TexturePackParser] [Whimscape_1.20_r3] Detected Version -> JAVA_1_20
[DEBUG] (JSQP_CORE) - [TexturePackParser] [Whimscape_1.20_r3] Version difference = ['JAVA_1_20 (64)']
🖌️  TexturePack = {
    'display_name': 'Whimscape_1.20_r3',
    'mc_meta': {
        'pack': {'pack_format': 15, 'description': '§6A crisp pixel art look'}
    },
    'minecraft_version': '1.20'
}
```

<div align="center">

  ### Oh yeah btw all of that info can be accessed as attributes.
  
</div>

```python
pack = TexturePack("./Whimscape_1.20_r3.zip")

print(pack.name)
print(pack.display_name)
print(pack.description)
print(pack.minecraft_version)
print(pack.mc_meta)
print(pack.parser.root_path)
print(pack.parser.assets_path)
```

<br>

> ### Much more nerdy stuff will come soon...
