# 🎬 Buhe Holiday: Real-Time 2D Keyframed Vector Animation
A real-time **2D vector animation** inspired by the Ethiopian cultural celebration of **Buhe**, developed entirely with **Python**, **PyGame**, and **PyOpenGL**. Every scene, character, and animation is generated programmatically using geometric primitives—without relying on external images, sprites, videos, or textures.

This project demonstrates fundamental computer graphics concepts such as **hierarchical modeling**, **matrix transformations**, **keyframe animation**, **interpolation techniques**, and **state-based animation management**.

---

# 📖 Project Overview

The animation tells the story of the traditional Ethiopian **Buhe** celebration through a fully automated **90-second animation timeline**.

The story consists of three major scenes:

### 🥁 1. The Arrival

Traditional Buhe dancers enter the scene from outside the viewport using a smooth keyframed walking animation before gathering at the celebration area.

### 🎶 2. Stick Dance (Hoya Hoye)

The dancers perform the traditional **Hoya Hoye** stick dance with synchronized body movements, rhythmic footwork, and coordinated stick animations.

### ☕ 3. Ethiopian Coffee Ceremony

The final scene recreates the traditional Ethiopian coffee ceremony where the host:

* Prepares the ceremony environment.
* Brews coffee using a traditional **Jebena**.
* Produces animated steam effects.
* Pours coffee into individual cups.
* Serves the seated guests one by one.

---

# ✨ Features

* Fully automated 90-second animation.
* Entirely vector-based graphics.
* No external images, textures, sprites, or videos.
* Hierarchical character animation.
* Smooth keyframe interpolation.
* Interactive keyboard controls.
* Real-time rendering using OpenGL.
* Traditional Ethiopian cultural storytelling.

---

# 🛠️ Technical Implementation

## 1. Procedural Vector Graphics

Every graphical object is created at runtime using mathematical primitives.

The project uses:

* Circles
* Ellipses
* Rectangles
* Triangles
* Polygons
* Line segments

Procedural rendering techniques are also used for:

* Sky gradients
* Grass generation
* Trees
* Mountains
* Traditional huts
* Smoke animation
* Fire effects

No bitmap graphics are used anywhere in the project.

---

## 2. Hierarchical Character Modeling

Characters are constructed using a hierarchical joint system.

Each body part is attached to its parent using OpenGL's matrix stack:

```text
Shoulder
   └── Upper Arm
          └── Forearm
                 └── Hand
                        └── Stick / Coffee Pot
```
Every limb is transformed independently using:

* `glPushMatrix()`
* `glTranslatef()`
* `glRotatef()`
* `glPopMatrix()`

This ensures that child body parts automatically follow the movement of their parent joints.

---

## 3. Keyframe Animation System

The animation is controlled through a timeline-based keyframe engine.

Character poses are represented as dictionaries containing joint angles.

Smooth transitions between poses are achieved using:

### Linear Interpolation

```python
lerp(a, b, t)
```

for movement and position.

### Smoothstep Interpolation

```python
3t² − 2t³
```

for natural acceleration and deceleration of body movements.

This produces smooth walking, dancing, serving, and pouring animations.

---

## 4. Animation Timeline

The entire story is driven by a global timeline.

Different events are triggered automatically, including:

* Dancer entrance
* Walking sequence
* Stick dance
* Sitting transitions
* Coffee preparation
* Coffee pouring
* Serving guests
* Ending scene

The animation plays continuously without user intervention.

---

# 📂 Project Structure

```text
Buhe-Holiday-Animation/
│
├── config.py
│   ├── Global constants
│   ├── Colors
│   ├── Screen dimensions
│   └── Animation states
│
├── utils.py
│   ├── Mathematical helpers
│   ├── lerp()
│   ├── smoothstep()
│   └── Vector drawing primitives
│
├── animations.py
│   ├── Character poses
│   ├── Walk cycles
│   ├── Dance animations
│   ├── Coffee ceremony timeline
│   └── State management
│
├── main.py
│   ├── OpenGL initialization
│   ├── Rendering loop
│   ├── Event handling
│   └── Animation execution
│
└── README.md
```
---

# 🎮 Interactive Controls

Although the animation runs automatically, several keyboard shortcuts are available.

| Key               | Action                       |
| ----------------- | ---------------------------- |
| **Space**         | Pause / Resume animation     |
| **← Left Arrow**  | Rewind timeline by 2 seconds |
| **→ Right Arrow** | Skip forward by 2 seconds    |
| **R**             | Restart animation            |
| **Esc**           | Exit the application         |

---

# 🚀 Installation

## Prerequisites

* Python 3.x
* PyGame
* PyOpenGL
* PyOpenGL Accelerate

Install the required packages:

```bash
pip install pygame PyOpenGL PyOpenGL_accelerate
```

---

# ▶️ Running the Project

Run the animation using:

```bash
python main.py
```
---

# 📚 Computer Graphics Concepts Demonstrated

This project demonstrates the following computer graphics concepts:

* 2D Vector Graphics
* Hierarchical Modeling
* Matrix Transformations
* Forward Kinematics
* Keyframe Animation
* Linear Interpolation
* Smoothstep Interpolation
* Procedural Scene Generation
* Real-Time Rendering
* State Machine Animation
* Event-Driven Programming
* OpenGL Rendering Pipeline

---

# 🎯 Learning Objectives

This project was developed to demonstrate:

* Building complex scenes entirely from geometric primitives.
* Creating articulated character models using hierarchical transformations.
* Implementing smooth keyframe-based animation systems.
* Managing real-time animation with timeline state machines.
* Applying computer graphics principles to represent Ethiopian cultural heritage through interactive animation.

---

# 👨‍💻 Technologies Used

* Python
* PyGame
* PyOpenGL
* OpenGL (Immediate Mode)

---

# 📜 License

This project was developed for educational purposes as part of a Computer Graphics course and demonstrates real-time vector animation techniques using Python and OpenGL.
