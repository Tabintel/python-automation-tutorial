## Python Automation Tutorial

This repository contains Python automation examples for the tutorial, using Playwright on LambdaTest. It demonstrates how to automate scenarios like form submission, e-commerce search, parallel execution, visual regression, mobile testing, PDF comparison, and smart UI validations.

By integrating with LambdaTest, we can run our automation scripts on different browsers, operating systems, and devices without setting up local infrastructure.


1. [Prerequisites](#prerequisites)
2. [Setup](#setup)
3. [Running the Examples](#running-the-examples)
   - [Playground Form Test](#playground-form-test)
   - [E-Commerce Search Test](#e-commerce-search-test)
   - [Parallel Execution Test](#parallel-execution-test)
   - [Docker Integration Test](#docker-integration-test)
   - [Visual Regression Test](#visual-regression-test)
   - [Mobile Automation Test](#mobile-automation-test)
   - [PDF Comparison Test](#pdf-comparison-test)
   - [Smart UI Test](#smart-ui-test)
4. [Project Structure](#project-structure)
5. [Best Practices](#best-practices)
6. [Troubleshooting](#troubleshooting)
7. [FAQ](#faq)

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- A valid [LambdaTest](https://www.lambdatest.com/) account with credentials
- (Optional) Docker, to run the Docker Integration Test

## Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Tabintel/python-automation-tutorial.git
   cd python-automation-tutorial
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set LambdaTest Credentials:**
   
   Create a `.env` file based on the provided `.env-example`:
   ```bash
   cp .env-example .env
   ```
   
   Edit the `.env` file and add your LambdaTest credentials:
   ```
   LT_USERNAME="your_lambdatest_username"
   LT_ACCESS_KEY="your_lambdatest_access_key"
   ```

## Running the Examples

> You can create a specific environment for Playwright with the following commands:

```
python -m venv playwright-env
playwright-env\Scripts\activate
pip install playwright
python -m playwright install
```

### Playground Form Test

**Description:** Automates a form submission on the LambdaTest Selenium Playground.

**Run:**
```bash
python scripts/playground_form_test.py
```

- Connects to LambdaTest using Chrome
- Navigates to the Selenium Playground
- Fills out a form and submits it
- Verifies the form submission

### E-Commerce Search Test

**Description:** Searches for a product and simulates an add-to-cart action on the LambdaTest E-Commerce Playground.

**Run:**
```bash
python scripts/ecommerce_search_test.py
```

- Connects to LambdaTest using Firefox on Windows 10
- Navigates to the LambdaTest E-Commerce Demo site
- Searches for a product ("iPhone")
- Adds the product to the cart
- Verifies the product was added successfully

### Parallel Execution Test

**Description:** Demonstrates running tests in parallel across multiple browsers (Chrome, Firefox, Safari).

**Run:**
```bash
python scripts/parallel_execution_test.py
```

- Creates three separate browser configurations
- Launches three parallel test sessions on LambdaTest
- Each session navigates to a different URL
- Demonstrates how to scale testing across browsers

### Docker Integration Test

**Description:** Shows how to run Playwright tests inside a Docker container while connecting to LambdaTest.

**Build and Run the Docker Container:**
```bash
docker build -t playwright-lambda .
docker run --env-file .env playwright-lambda
```

- Uses the provided Dockerfile to create a container with Python and Playwright
- Runs the test inside the container
- Connects to LambdaTest from within the container
- Demonstrates containerized test execution

### Visual Regression Test

**Description:** Performs visual comparison by taking screenshots and comparing them against baselines.

**Run:**
```bash
python scripts/visual_regression_test.py
```

- Connects to LambdaTest using Chrome
- Navigates to the LambdaTest homepage
- Takes a screenshot of the page
- Saves the screenshot for visual comparison
- Demonstrates visual testing capabilities

### Mobile Automation Test

**Description:** Automates testing on a mobile device using LambdaTest's real device cloud.

**Run:**
```bash
python scripts/mobile_automation_test.py
```

- Connects to a real mobile device on LambdaTest
- Navigates to a mobile-friendly website
- Interacts with mobile-specific elements
- Demonstrates mobile testing capabilities

### PDF Comparison Test

**Description:** Simulates PDF comparison by navigating to a sample PDF URL and capturing its screenshot.

**Run:**
```bash
python scripts/pdf_comparison_test.py
```


- Connects to LambdaTest using Chrome
- Navigates to a sample PDF URL
- Takes a screenshot of the PDF
- Saves the screenshot for later comparison
- Demonstrates PDF testing capabilities

### Smart UI Test

**Description:** Validates UI element details by capturing its location and size for smart UI validation.

**Run:**
```bash
python scripts/smart_ui_test.py
```

**What it does:**
- Connects to LambdaTest using Firefox
- Navigates to the Selenium Playground
- Locates a header element and retrieves its dimensions
- Demonstrates SmartUI validation concepts
