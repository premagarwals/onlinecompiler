
# Online Compiler Project
### Current status: Backend Under Developement

Welcome to the **Online Compiler** project! This is an ongoing development effort to build a robust backend for an online code compilation platform using Django. The backend will serve as the foundation for a future full-stack application, enabling users to write, compile, and execute code securely within a sandboxed environment.

---

## 🚧 Project Status: Under Development 🚧

The project is **not yet ready for production use**. Features and functionalities are being actively developed, tested, and improved.

---

## Vision

The goal of this project is to provide a scalable and secure backend for an online compiler that supports multiple programming languages. This platform will be designed for:
- Students and educators for learning and teaching programming.
- Developers testing code snippets without needing a local environment.
- Organizations conducting coding assessments or competitions.

Planned features include:
- Support for various programming languages (e.g., Python, Java, C++).
- Real-time compilation and execution with instant feedback.
- REST APIs to integrate with a future front-end application.
- A secure and isolated execution environment to handle user code.

---

## Installation Guide

To run the backend locally, follow the steps below:

#### Note: *We are using docker to sandbox the user submitted code, hence make sure to have docker installed, following images available.*
----------

### **1. Install Docker**

-   **For Linux:** Follow the [official Docker installation guide for Linux](https://docs.docker.com/engine/install/).
-   **For macOS:** Use [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/).
-   **For Windows:** Use [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/).

### **2. Set Up Docker Group (Optional for Linux)**
```bash
sudo usermod -aG docker $USER
newgrp docker  # Apply group changes without logout

```

### **3. Pull Required Docker Images**

Ensure the following Docker images are installed on the user's system:

-   **Python image** (for running the Python code)
-   **GCC image** (for compiling and running C++ code)
-   **OpenJDK image** (for compiling and running Java code)

```bash
docker pull python:3.10      # Python image for running Python code
docker pull gcc:latest       # GCC image for compiling C++ code
docker pull openjdk:latest   # OpenJDK image for compiling and running Java code

```
We will run our codes in these images instead of directly running on our system.

### **4. Verify Docker Images Are Installed**

After pulling the images, users can verify that they are installed by running:

```bash
docker images
```
This will list all the Docker images available, and you should see `python:3.10`, `gcc:latest`, and `openjdk:latest` in the output.

**Also make sure docker is running by running `sudo systemctl start docker` command in terminal.** Now, you can proceed to set up the project.
------------
### Steps

1. **Clone the Repository**
   ``` bash
   git clone https://github.com/premagarwals/onlinecompiler.git
   cd onlinecompiler
	```


2.  **Create a Virtual Environment**
    
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```
    
3.  **Install Dependencies** Install the required Python libraries by running:
    
    ```bash
    pip install -r requirements.txt
    ```
    
4.  **Run the Development Server** Start the Django development server:
    
    ```bash
    python manage.py runserver
    ```
    
    The server will be accessible at `http://127.0.0.1:8000/`.


## Future Roadmap

-   **Multi-language Support**: Add compiler support for Python, Java, C++, and more.
-   **RESTful APIs**: Provide APIs for front-end integration and external usage.
-   **Secure Execution**: Implement sandboxed environments for running untrusted user code.
-   **Error Handling**: Develop robust error reporting and debugging tools.
-   **Testing**: Add unit tests and integration tests for all APIs.

Stay tuned for updates!

----------

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

```
COPYRIGHT (C) [YEAR] [AUTHOR/ORGANIZATION]

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

```
