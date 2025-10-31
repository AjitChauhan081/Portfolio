# 💻 `main` Django Application

The `main` application serves as the **core portfolio landing page** for the entire Django project. It is a data-heavy application responsible for fetching and presenting all personal, professional, and technical information to a visitor in a single, comprehensive view.

---

## 🎯 Purpose and Scope

The primary goal of the `main` app is to display a **full, single-page portfolio** (rendered by the `portfolio_view` using the `try4.html` template).

### Key Responsibilities:

* **Data Aggregation:** Collects data from a wide range of models (About, Education, Project, Skill, etc.) and integrates the latest blog posts from the `blog` application.
* **Contact Management:** Handles the submission of the **contact form** and saves messages to the database.
* **Skill Visualization:** Prepares and serializes skill data into a JSON format optimized for **Highcharts** visualization (e.g., a bubble chart).

---

## 📁 Application Structure

### `main/models.py`

This file defines the comprehensive data structure for the portfolio content, with most models having a **`ForeignKey`** relationship to `django.contrib.auth.models.User` (specifically targeting the 'cajit' user in the views).

| Model | Purpose | Key Fields |
| :--- | :--- | :--- |
| **`About`** | Stores core personal info, profile photo, and resume link. | `name`, `description`, `profile_photo`, `resume_pdf` |
| **`Education`** | Details of academic background. | `institute`, `degree`, `start_year`, `end_year` |
| **`Experience`** | Work and professional history. | `job_title`, `company_name`, `description` |
| **`Project`** | Showcases key personal or work projects. | `project_name`, `github_link`, `live_link`, `related_posts` (M2M to `blog.BlogPost`) |
| **`Certificate`** | Professional certifications and training. | `certificate_name`, `institute`, `link` |
| **`Award`** | Honors and recognition received. | `award_name`, `awarded_by` |
| **`Category`** | Defines groups for skills (e.g., 'Backend', 'Data Analysis'). | `name` |
| **`Skill`** | Specific technical skills and proficiency level. | `skill_name`, `category` (FK), `proficiency` (1-100) |
| **`SocialLink`** | Links to external profiles (GitHub, LinkedIn, etc.). | `platform_name`, `url`, `icon_name` (`@property` for Feather Icons) |
| **`Contact`** | Stores messages submitted via the contact form. | `name`, `email`, `message`, `submitted_on` |
| **`ChatSession`** | Tracks individual user chat conversations. | `session_id`, `user` (FK) |
| **`ChatMessage`** | Stores messages within a specific `ChatSession`. | `session` (FK), `role`, `content` |

---

### `main/views.py`

The core logic resides in a single, powerful function:

#### `portfolio_view(request)`

* **HTTP Methods:** Handles both `GET` (display) and `POST` (contact form submission).
* **User Targeting:** All database queries are filtered to fetch content only for the hardcoded **`username='cajit'`** (a single-user portfolio pattern).
* **Skill Data Preparation:**
    * It uses **`Prefetch`** to efficiently load `Skill` objects related to `Category` and filters them by the target user.
    * It then iterates through the categories and skills to build the **`highcharts_series`** structure, using a custom `color_palette` dictionary for visualization.
    * The final data is converted to a safe JSON string (`json_series_data`) for frontend consumption.
* **Context:** Compiles all fetched data and form objects into the context dictionary for rendering the `try4.html` template.
* **Contact Handling:** On successful `POST`, it saves the `Contact` message and performs a redirect to prevent duplicate submissions.

#### `custom_404(request)`

* A simple view used to render a dedicated `404.html` template for pages not found.

---

### `main/urls.py`

This app defines the root path for the entire project, ensuring the portfolio is the first thing a user sees.

```python
urlpatterns = [
    # Maps the project's root URL (e.g., '/') directly to the main portfolio view
    path('', views.portfolio_view, name='portfolio_view'),
]
```


### `main/forms.py`

* Contains the simple ContactForm based on the Contact model.

```bash

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'message']
```

### `main/admin.py`

* All models within the main application are registered here for administrative management.
