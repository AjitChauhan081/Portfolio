# ✍️ `blog` Django Application

The `blog` application is a self-contained content management system responsible for the full functionality of the project's blog section. It manages posts, categories, comments, searching, and archives.

---

## 🎯 Purpose and Scope

The `blog` app handles all blog-related CRUD operations and presentation logic. It integrates with the `main` app for sharing common user data (About, Social Links) to maintain a consistent portfolio and blog experience.

### Key Features:

* **Post Management:** Creation, viewing, and listing of `BlogPost` content.
* **Categorization & Filtering:** Allows filtering posts by `Category` using slugs.
* **Search Functionality:** Enables searching across post titles, summaries, and categories.
* **Comments:** Supports user comments with a built-in moderation mechanism (`active=False` by default).
* **Archive View:** Groups posts chronologically by year.
* **Dedicated Pages:** Hosts the **Archive** and the **About** page content.

---

## 📁 Application Structure

### `blog/models.py`

This file defines the core content and interaction models for the blog:

| Model | Purpose | Key Relationships & Fields |
| :--- | :--- | :--- |
| **`Category`** | Tags for organizing blog content. | `name`, **`slug`** (auto-generated) |
| **`BlogPost`** | The main blog content model. | **`user`** (FK), **`categories`** (M2M to `Category`), `title`, **`slug`** (unique, auto-generated), **`description`** (`CKEditor5Field`), `image`, `read_time` |
| **`Comment`** | User feedback and discussion. | **`post`** (FK to `BlogPost`), `author_name`, `body`, **`active`** (Boolean for moderation) |
| `Blog` | *(Note: This model appears redundant given `BlogPost`'s existence and should be considered for removal.)* | N/A |

### `blog/views.py`

The views handle all display, filtering, and interaction logic.

#### Helper Functions

* `get_common_context(request, username='cajit')`: **Crucial helper** that fetches the required `About` data and `SocialLink` data from the **`main`** application's models, ensuring the blog pages have the necessary portfolio context (sidebar, footer, etc.).
* `apply_search_filter(posts_queryset, query)`: Implements search logic using the Django **`Q` object** to filter posts by matching the query in the `title`, `summary`, OR `categories__name`.
* `handle_pagination(request, posts_list)`: Standard function to apply pagination (10 posts per page) to any list of posts.

#### Core Views

| View Function | URL Pattern | Description |
| :--- | :--- | :--- |
| `blog_list_view` | `/blog/` | Displays all blog posts, applies **search filtering**, and uses **pagination**. |
| `category_filter_view` | `/blog/category/<slug:slug>/` | Filters posts by a specific `Category` slug, then applies optional search filtering. |
| `blog_detail_view` | `/blog/<slug:slug>/` | Displays a single `BlogPost`, handles the **`CommentForm`** submission, and lists active comments. |
| `archive` | `/blog/archive/` | Fetches all posts and uses Python's `defaultdict` to **group posts by year** for chronological archive display. |
| `about` | `/blog/about/` | Serves as the dedicated **About page**. Fetches and displays chronological data (`Experience`, `Education`, `Project`) from the `main` app models. |

### `blog/urls.py`

Defines clean, semantic URLs for navigation and content retrieval:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_list_view, name='blog'), # Blog Home
    path('archive/', views.archive, name='archive'),
    path('about/', views.about, name='about'),
    path('category/<slug:slug>/', views.category_filter_view, name='category_filter'),
    path('<slug:slug>/', views.blog_detail_view, name='blog_detail'), # Post Detail
]
```


### `blog/forms.py`

Defines the CommentForm which is tied to the Comment model, including custom widget attributes for styling and user guidance in the frontend template.

```python

# Snippet from forms.py
class CommentForm(forms.ModelForm):
    # ... widget definitions for styling ...
    class Meta:
        model = Comment
        fields = ('author_name', 'author_email', 'body')
```
