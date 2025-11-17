````markdown
# Inferno MLaaS (ML-as-a-Service)

A production-grade, auto-deploying API platform for serving machine learning models. This project uses FastAPI, Terraform for Infrastructure as Code, and GitHub Actions for a complete CI/CD pipeline, deploying the service to AWS ECS Fargate.

---

## 🎯 Real-World Scenarios & Business Value

This project is more than just a single API; it's a **platform (MLaaS)** designed to serve *any* machine learning model in a reliable, scalable, and automated way. The *architecture* is the true product.

While this demo uses a **Sentiment Analysis** model, the same infrastructure could be used to solve numerous critical business problems:

* **Customer Feedback Analysis (The current model)**
    * **Problem:** A company has thousands of customer reviews, support tickets, or social media mentions and needs to understand customer sentiment in real-time.
    * **Solution:** This API receives the text and instantly classifies it as "positive," "negative," or "neutral." This data can feed a live dashboard, automatically escalate angry customers to support, or identify product features people love.

* **Real-Time Fraud Detection**
    * **Problem:** An e-commerce platform needs to block fraudulent transactions *before* they are processed.
    * **Solution:** Swap the sentiment model with a fraud-detection model. The API receives transaction data (amount, location, user history) and returns a risk score. The **CI/CD pipeline** is critical here, allowing data scientists to deploy new models to fight emerging fraud tactics daily without downtime.

* **Scalable Recommendation Engine**
    * **Problem:** An online store wants to show "Recommended for You" products, but traffic spikes during holidays.
    * **Solution:** The API serves a recommendation model. The serverless **ECS Fargate** infrastructure automatically scales up the number of containers during peak traffic (like Black Friday) and scales back down afterward, ensuring low latency and high availability while only paying for the compute used.

---

## 🏛️ Architecture

This project is built on a fully automated CI/CD pipeline. A `git push` to the `master` (or `main`, adjust as needed) triggers GitHub Actions to automatically build, test, and deploy the new version to production without downtime.

**Deployment Flow:**

+----------+       +-----------------+       +-----------------+
|          |       |                 |       |                 |
| Developer|-----> |  git push main  |-----> |  GitHub Actions |
|          |       |   (GitHub)      |       |  (CI/CD)        |
|          |       |                 |       |                 |
+----------+       +-----------------+       +-----------------+
                                                     |
+----------------------------------------------------+
|
v
+-----------------+       +-----------------+       +-------------------+
|                 |       |                 |       |                   |
|  1. Build/Push  |-----> |  Amazon ECR     |       |  3. Update Service|
|     Docker Image|       | (Image Registry)|       |     (Force Deploy)|
|                 |       |                 |       |                   |
+-----------------+       +-----------------+       +---------+---------+
                                                                |
+---------------------------------------------------------------+
|
v
+-------------------+       +-----------------+       +-----------------+
|                   |       |                 |       |                 |
|  4. ECS Fargate   |-----> |  5. FastAPI App |-----> |  Amazon S3      |
|  (Pulls new image)|       |  (Loads on start)|       | (model.pkl)     |
|                   |       |                 |       |                 |
+-------------------+       +-----------------+       +-----------------+
````

-----

## ✨ Technology Stack

  * **Application:** **FastAPI** (ASGI framework), **Uvicorn** (Server)
  * **ML:** **Scikit-learn** (Model training)
  * **Infrastructure (IaC):** **Terraform**
  * **Cloud Platform (AWS):**
      * **ECS (Fargate):** For serverless container orchestration.
      * **ECR:** For storing Docker images.
      * **S3:** For storing the `model.pkl` artifact.
      * **Application Load Balancer (ALB):** To route public traffic.
      * **CloudWatch:** For container logging.
  * **CI/CD:** **GitHub Actions**
  * **Containerization:** **Docker**
  * **Dependency Management:** **Poetry**

-----

## 🚀 How to Run Locally

### 1\. Prerequisites

  * Python 3.11+
  * Poetry
  * An AWS Account (for S3 access)
  * AWS CLI configured (run `aws configure`)

### 2\. Installation

Clone the repository and install the dependencies using Poetry:

```bash
git clone <your-repo-url>
cd inferno-mlaas
poetry install
```

### 3\. Generate the Model

The local server expects a `model.pkl` file in the root. Run the training script to generate it:

```bash
poetry run python scripts/train.py
```

### 4\. Set Environment Variables

The API needs to know which S3 bucket to read from (even though the local server loads the local file, the `api/main.py` code expects this variable).

Create a file named `.env` in the project root:

```
# File: .env
MODEL_BUCKET_NAME=your-s3-bucket-name
```

### 5\. Run the Server

Use `uvicorn` to start the local server.

```bash
poetry run uvicorn api.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

-----

## 📒 API Reference

### Health Check

`GET /health`

Returns the operational status of the API.

**Success Response (200 OK):**

```json
{
  "status": "ok_v4" 
}
```

### Sentiment Prediction

`POST /predict`

Runs sentiment analysis on a provided string of text.

**Request Body:**

```json
{
  "text": "This movie was fantastic, I loved it!"
}
```

**Success Response (200 OK):**

```json
{
  "text": "This movie was fantastic, I loved it!",
  "sentiment": "positive" 
}
```

**Error Response (503 Service Unavailable):**
(This occurs if the server could not load the model from S3 on startup)

```json
{
  "detail": "Model is not loaded or failed to load. Check server logs."
}
```

-----

## 🤖 Deployment Process

This project is configured for **Continuous Deployment (CD)**.

Any `git push` to the `master` (ou `main`) branch will automatically trigger the `.github/workflows/cd.yml` workflow. This workflow will:

1.  Build a new Docker image.
2.  Push the image to the Amazon ECR repository.
3.  Force a new deployment on the ECS service, which pulls the `:latest` image and replaces the old tasks.

There is **no manual approval step**. Deployment to production is immediate upon pushing to the main branch.

```
```
