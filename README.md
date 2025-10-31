<div align="center">
  <img src="https://img.shields.io/badge/Project-Portfolio-blue?style=for-the-badge&logo=github" alt="Project Badge">
  <img src="https://img.shields.io/badge/Language-Python-informational?style=for-the-badge&logo=python&logoColor=white" alt="Python Badge">
  <img src="https://img.shields.io/badge/Framework-Django-success?style=for-the-badge&logo=django" alt="Django Badge">
</div>

# 🚀 Portfolio Project

---

## 🏗️ Project Architecture

---

This Django project is organized into two distinct applications to maintain a clean separation of concerns:

<a href="./main">**Main**</a> App: Contains the full portfolio landing page, including all static content, contact forms, and the core presentation logic.

<a href="./blog">**Blog**</a> App: Houses the complete blog functionality, including its own dedicated models, views, and templates for post creation, display, and management.

---

### 🛠️ Local Setup and Installation

---

Follow these steps to set up and run the project locally.

#### 1. Create a Virtual Environment

It is highly recommended to use a virtual environment to manage project dependencies.

```bash
python3 -m venv env
```

#### 2. Activate the Environment

-On Linux/macOS:

```bash

source env/bin/activate
```
-On Windows:

```bash

.\env\Scripts\activate
```

#### 3. Install Dependencies
-Install all necessary project requirements using pip.

```bash

pip install -r requirements.txt
```

---

### ⚙️ Database and Static Files

---
-Generate Migrations (if model changes were made):

```bash

python manage.py makemigrations
```

Apply Migrations:

```bash

python manage.py migrate
```

Collect Static Files:

```bash

python manage.py collectstatic
```
---

### ▶️ Running the Server

---

-Start the local development server:

```bash

python manage.py runserver
````
Note: For testing deployment behavior, remember to set DEBUG = False in settings.py.

### 🌐 Deployment Information

---

<table border="1" cellpadding="10" cellspacing="0" style="width: 100%;"> <thead> <tr> <th style="background-color: #f2f2f2;">Component</th> <th style="background-color: #f2f2f2;">Details</th> </tr> </thead> <tbody> <tr> <td><strong>Deployed Application URL</strong></td> <td><a href="https://ajitchauhan31.pythonanywhere.com/">https://ajitchauhan31.pythonanywhere.com/</a></td> </tr> <tr> <td><strong>Hosting Platform</strong></td> <td>PythonAnywhere</td> </tr> </tbody> </table>

### ✅ Post-Deployment Changes & Learnings

---

<table border="1" cellpadding="10" cellspacing="0" style="width: 100%;">
<thead>
<tr>
<th style="background-color: #e6f7ff; width: 30%;">Change Category</th>
<th style="background-color: #e6f7ff;">Implementation Details</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Search Engine Optimization (SEO)</strong></td>
<td>Integrated <a href="https://ajitchauhan31.pythonanywhere.com/sitemap.xml"><code>sitemap.xml</code></a> (Deployed URL) and configured <code>robots.txt</code> for better indexing.</td>
</tr>
<tr>
<td><strong>Email Service Integration</strong></td>
<td>Added SMTP Gmail service for reliable email functionality (e.g., contact forms).</td>
</tr>
<tr>
<td><strong>Performance Optimization</strong></td>
<td>Significant refactoring of templates and static files to improve site speed. Detailed information on techniques and results can be found in the <a href="./PERFORMANCE_OPTIMIZATION.md">PERFORMANCE_OPTIMIZATION.md</a> file.</td>
</tr>
</tbody>
</table>
