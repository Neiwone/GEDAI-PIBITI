# Decision Helper Weight Elicitation API

API for calculating evaluation criteria weights using multi-criteria decision-making methods, specifically the **Analytic Hierarchy Process (AHP)** and **Best-Worst Method (BWM)**.
Developed as part of the GEDAI-UFAL project:
*"Ferramentas Baseadas em Agentes Inteligentes de Apoio à Decisão para Seleção de Projetos de Negócios Inovadores em Pré-Incubadoras e Incubadoras."*

---

## Project

This backend service provides an interface for decision support processes, allowing agencies and evaluators to:

-   Manage and evaluate innovation projects.
-   Calculate criteria weights using AHP and BWM methods.
-   Integrate these weights into multi-agent systems for innovation project evaluation.

---

## ⚙️ Technologies Used

-   Python 3.11
-   FastAPI
-   pyDecision
-   Docker

---

## 📄 API Endpoints

The API is organized into two main sections: **Projects** for managing decision problems and **Weights** for calculating criteria weights using specific methods.

### 1. Projects Endpoints

These endpoints manage the core project entities, which consist of alternatives and criteria.

-   **GET** `/projects/`
    -   **Description:** Retrieve all evaluation projects.

-   **POST** `/projects/`
    -   **Description:** Create a new evaluation project.

-   **GET** `/projects/{evaluation_id}`
    -   **Description:** Retrieve a specific evaluation project by its unique ID.

-   **DELETE** `/projects/{evaluation_id}`
    -   **Description:** Delete an evaluation project.

-   **PUT** `/projects/{evaluation_id}`
    -   **Description:** Update an entire evaluation project.

-   **POST** `/projects/{evaluation_id}/alternatives/`
    -   **Description:** Add a new alternative to an existing project.

-   **POST** `/projects/{evaluation_id}/criteria/`
    -   **Description:** Add a new criterion to an existing project.

### 2. Weights Endpoints

These endpoints are specifically for calculating and retrieving criteria weights using the AHP and BWM methods.

-   **POST** `/weights/ahp`
    -   **Description:** Retrieve criterion weights from the AHP method.
    -   **Request Body Example:**
        ```json
        {
          "criteria": ["Cost", "Impact", "Risk"],
          "matrix": [
            [1, 2, 3],
            [0.5, 1, 4],
            [0.33, 0.25, 1]
          ]
        }
        ```

-   **POST** `/weights/bwm`
    -   **Description:** Retrieve criterion weights from the BWM method.
    -   **Request Body Example:**
        ```json
        {
          "criteria": ["Cost", "Inovation", "Tecnology", "Management", "Market"],
          "most_important": [2, 1, 4, 3, 8],
          "least_important": [4, 8, 2, 3, 1]
        }
        ```

---

## 📚 References

-   Saaty, T. L. (1990). The Analytic Hierarchy Process. McGraw-Hill.
-   Rezaei, J. (2015). Best-Worst Method: A new approach to multi-criteria decision-making.
    Omega, Volume 53, Pages 49–57. [https://doi.org/10.1016/j.omega.2014.11.009](https://doi.org/10.1016/j.omega.2014.11.009)
-   pyDecision Documentation: [https://pypi.org/project/pyDecision/](https://pypi.org/project/pyDecision/)
-   FastAPI Documentation: [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)