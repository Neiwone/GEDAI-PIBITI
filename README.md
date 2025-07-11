# Decision Helper Weight Elicitation API

API for calculating evaluation criteria weights using multi-criteria decision-making methods, specifically the **Analytic Hierarchy Process (AHP)** and **Best-Worst Method (BWM)**.  
Developed as part of the GEDAI-UFAL project:  
*"Ferramentas Baseadas em Agentes Inteligentes de Apoio à Decisão para Seleção de Projetos de Negócios Inovadores em Pré-Incubadoras e Incubadoras."*

---

## Project

This backend service provides an interface for decision support processes, allowing agencies and evaluators to:

- Calculate criteria weights using AHP and BWM methods.
- Integrate these weights into multi-agent systems for innovation project evaluation.

---

## ⚙️ Technologies Used

- Python 3.11
- FastAPI
- pyDecision
- Docker

---

## 📄 API Endpoints

### 1. Calculate AHP Weights

**POST** `/api/ahp_weights`

**Request Body Example:**

```json
{
    "request": {
        "criteria": ["Cost", "Impact", "Risk"],
        "matrix": [
            [1, 2, 3],
            [0.5, 1, 4],
            [0.33, 0.25, 1]
        ]
    }
} 
```

### 2. Calculate BWM Weights

**POST** `/api/bwm_weights`

**Request Body Example:**

```json
{
    "request": {
        "criteria": ["Cost", "Inovation", "Tecnology", "Management", "Market"],
        "most_important": [2, 1, 4, 3, 8],
        "least_important": [4, 8, 2, 3, 1]
    }
}
```

## 📚 References

- Saaty, T. L. (1990). The Analytic Hierarchy Process. McGraw-Hill.
- Rezaei, J. (2015). Best-Worst Method: A new approach to multi-criteria decision-making.  
  Omega, Volume 53, Pages 49–57. [https://doi.org/10.1016/j.omega.2014.11.009](https://doi.org/10.1016/j.omega.2014.11.009)
- pyDecision Documentation: [https://pypi.org/project/pyDecision/](https://pypi.org/project/pyDecision/)
- FastAPI Documentation: [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)



