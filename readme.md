[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/carrot2803/Comp3613A1)

# Comp 3613 Job Board

A CLI-based Flask application designed using the **Model-View-Controller (MVC)** architecture. This app allows for seamless job creation, listings and job applications.


https://github.com/user-attachments/assets/1f9d497b-7d40-49c5-9584-09392a477eee


## Installation Guide
<details>
<summary><code>There are several ways you can install the application</code></summary>

1. **Clone the repository**:
    ```sh
    git clone https://github.com/carrot2803/Comp3613A1.git
    cd Comp3613A1
    ```

2. **(Optional) Create a virtual environment**:

    - Using `venv`:
        ```sh
        python -m venv venv
        source venv/bin/activate    # On Windows use `venv\Scripts\activate`
        ```
    - Using `conda`:
        ```sh
        conda create --name your-env-name python=3.x
        conda activate your-env-name
        ```

3. **Install the required packages**:
    ```sh
    pip install -r requirements.txt
    ```
    
4. **Run the Code**
    ```sh
    flask init
    ```

#### **Alernative**
- [Downloading repository as ZIP](https://github.com/carrot2803/Comp3613/archive/refs/heads/master.zip)
- Running the following command in a terminal, assuming you have [GitHub CLI](https://cli.github.com/) installed:

</details>

## CLI Commands

`wsgi.py` is a utility script for performing various tasks related to the project. Below are the available CLI commands:

| Command                        | Description                                                                                          | Usage                                                      |
|---------------------------------|------------------------------------------------------------------------------------------------------|------------------------------------------------------------|
| `flask init`                    | Initializes the database by creating necessary tables.                                               | `flask init`                                               |
| **Company Commands**            |                                                                                                      |                                                            |
| `flask company create`          | Creates a new company entry in the database.                                                         | `flask company create <name> <industry>`                   |
| **Applicant Commands**          |                                                                                                      |                                                            |
| `flask applicant create`        | Creates a new applicant in the database.                                                             | `flask applicant create <first_name> <last_name> <education> <skills>` |
| `flask applicant view-all`      | Displays a list of all applicants. Requires admin password (`password`).                             | `flask applicant view-all`                                 |
| **Job Commands**                |                                                                                                      |                                                            |
| `flask job create`              | Adds a new job listing to the database. Prompts for company ID.                                      | `flask job create <title> <description>`                   |
| `flask job apply`               | Allows an applicant to apply for a job. Prompts for applicant ID and job ID.                         | `flask job apply`                                          |
| `flask job view-all`            | Displays a table of all available job listings.                                                      | `flask job view-all`                                       |
| `flask job view-applicants`     | Shows all applicants for a company's jobs. Prompts for company ID and job ID.                        | `flask job view-applicants`                                |
| `flask job view-all-applicants` | Shows all applicants for a specific job. Requires admin password (`password`).                       | `flask job view-all-applicants`                            |
| **General Commands**            |                                                                                                      |                                                            |
| `flask help`                    | Displays all available commands and their descriptions in a table format.                           | `flask help`                                               |
