<p align="center" style="background: #06b6d4">
  <img src="https://raw.githubusercontent.com/tataraba/musicbinder/a6958c098fb223677e5ce0cdd5e9a2424e4a7d85/app/static/img/mb-logo.svg" alt="Music Binder" style="max-width: 100%;">
</p>

<h2 align="center">Music Binder</h2>
<h3 align="center">Created With a Python-backed Frontend!</h3>

<p align="center"> Music Binder is a demo project showcasing what you can do with a Python-backed frontend, featuring htmx and TailwindCSS.
    <br>
</p>

## Table of Contents

- [Table of Contents](#table-of-contents)
- [🧐 About ](#-about-)
- [🏁 Getting Started ](#-getting-started-)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
    - [Codespaces:](#codespaces)
    - [Locally](#locally)
- [🔧 Run pytest ](#-run-pytest-)
- [🎈 Guide ](#-guide-)
- [⛏️ Built Using ](#️-built-using-)
- [✍️ Author ](#️-author-)
- [🎉 Acknowledgements ](#-acknowledgements-)

## 🧐 About <a name = "about"></a>

You can build a beautiful web application using nothing more than Python, htmx, and TailwindCSS. Create dynamic pages using the power of Jinja templates and server-side rendering to create a HyperText driven application.

## 🏁 Getting Started <a name = "getting_started"></a>

This repository was prepared for a PyCon tutorial on how to create a python-backed frontend, featuring Jinja templates for HTML rendering, TailwindCSS for style, and htmx for pizzazz! 😎

The tutorial is scheduled for Wednesday - April 19th, 2023 9 - 12:30 pm (Mountain Time).

### Prerequisites

The example app was created with **Python 3.11**, but it is likely compatible with earlier versions. However, I would highly recommend using the latest version of Python. The rest of the dependencies are listed in the `requirements.txt` file.

```
fastapi[all]
jinja2
jinja2-fragments
pytailwindcss
pytest
python-multipart
tinydb
```

> **Note**
> The `fastapi[all]` dependency installs some other optional dependencies and features. It also includes `uvicorn`, which is used as the server to run your code. (You could choose to just use `fastapi` and `uvicorn[standard]` separately, if you prefer.)

### Installation

There are two methods to get started. The first and recommended method is using Codespaces. The second, more traditional route is to clone/copy the repo and install locally.

#### Codespaces:

Press the `<> Code` button above and select `Create a Codespace on main`. This will open a new window in your browser, where you can run the code in a virtual environment.

#### Locally

Create a copy of the repo using the `Use this template` button above. Select `Create a new repository`.

> **Warning**
> Be sure to select **`Include all branches`** when cloning the repo.

After cloning or using this template, you will need to create a virtual environment. Navigate to the location where you have cloned the project (your project root) and run the following command in your terminal:

```
python -m venv .venv
```

This will create a `.venv` directory within your project.

Next, activate your environment:

```
# On Windows
.\.venv\Scripts\activate

# On MacOS/Linux
$ source .venv/bin/activate
```

Then, install the requirements:

```
python -m pip install -r requirements.txt
```

> **Warning**
> Make sure you are only using **one** of the above options to get started. If you use Codespaces, you will NOT need to install any dependencies, nor need to "activate" your environment when using the in-browser terminal.

As a recap... To get started, use ONE of the methods listed below:

| 🥇 Method 1: Codespaces (recommended) | 🥈 Method 2: Locally |
| --- | --- |
| Click on "Use this template" | Check for latest Python version
| Select "Open in a codespace" | Clone repo or use template
| Wait for the build | Navigate to project root in terminal
| Start Coding | Create virtual environment
| ... | Activate virtual environment
| ... | Install from requirements.txt
| ... | Run `tailwindcss init`

## 🔧 Run pytest <a name = "run_pytest">

After activating your virtual environment, you can run tests by typing `pytest` on the command line. This makes sure that your application is able to generate the index page.

```
pytest
```

> **Note**
> The application does not include comprehensive testing (yet). As of now, if the tests pass, it means that the application runs and generates a response.


## 🎈 Guide <a name="guide"></a>

If you would like to learn how to build a site like this from the ground up, considering following the instructions over on the [Simple Site repository](https://github.com/tataraba/simplesite).

The repo includes [documentation](https://github.com/tataraba/simplesite/blob/main/docs/00_Preface.md) on how to get started from scratch, with more information on some of the libraries used in this application, including FastAPI, Jinja2, pytailwindcss, and htmx.


## ⛏️ Built Using <a name = "built_using"></a>

- FastAPI
- Jinja2
- TailwindCSS
- TinyDB
- htmx

## ✍️ Author <a name = "author"></a>

- [@tataraba](https://github.com/tataraba) - Mario Munoz, _Python By Night_

## 🎉 Acknowledgements <a name = "acknowledgement"></a>

- [@kjaymiller](https://github.com/kjaymiller) - Jay Miller, _Senior Cloud Advocate-Python_, Microsoft