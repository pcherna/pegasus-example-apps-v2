# Example Models for SaaS Pegasus, v2

[SaaS Pegasus](https://saaspegasus.com) is a great framework for getting up and running quickly and robustly with Django web applications.

Here are example apps for SaaS Pegasus. You can use these to help your create and improve your own apps, models, and views, using either Class-Based Views (CBV) or Function-Based Views (FBV).

Some of the things showcased in these examples include:

* FBV and CBV implemations of objects that are not team-related (for when you've configured Pegasus without teams, or if you need cross-team objects)
* FBV and CBV implemations of team-specific objects (for objects that belong to a specific team)
* API access to non-team and team-specific objects
* Use of pagination
* HTMX to make better-looking updates in pagination

## Apps and Models Introduction

* **crud_example1** is an app containing the **Thing** model, which is an example non-team-related object.
* **crud_example2** is an app containing the **TeamThing** model, which is an example team-specific object.

Each app:

* Implements a model with several sample fields (`Name`, `Number`, and `Notes`)
* Implements clean Function-Based Views and Class-Based Views for:
  * Create
  * List (summarize all objects, showing their `Name` and `Number`), with pagination
  * Details (details on one object, showing all their fields)
  * Update
  * Delete
* Implements a basic CRUD API using django-rest-framework

## Choosing FBV or CBV

The `views.py` files in each app contain Class-Based View and Function-Based View implementations that are basically equivalent to each other. You don't need both, so you can delete or comment out the one you don't need.

The apps' `urls.py` contain `path()` bindings for both CBV and FBV styles. To keep things cleaner, only one of these can be active at once, so the CBV style is commented out. You can switch any or all of the views by commenting out the FBV `path()` bindings and uncommenting the corresponding FBV `path()` bindings.

## HTMX

The normal Django request lifecycle (simplified) is that the user submits a request from the browser (e.g. "show the next page of a list"), Django creates a full HTML response using a template, and returns that. The browser then renders a full new page based on that HTML.

HTMX lets the web page send requests in a way that doesn't require a full page refresh. For example, when doing pagination that lets Django return just the HTML rendition of the new list items, and then the browser just replaces that part of the web page, which is faster and cleaner looking.

See the [Tech Notes – HTMX](#tech-notes----htmx) for more information.

## Installation

In the following instructions, replace `<project_slug>` with your Pegasus project slug.

### Clone this repository into its own folder

```bash
git clone git@github.com:pcherna/pegasus-example-apps.git
```

### Integrate the new apps into your project

* Add the code by copying `apps/crud_example1/*` and `apps/crud_example_2/*` into the matching place in your project, i.e. into your project as `apps/crud_example1/*` etc.
* Add the templates by copying `templates/crud_example1/*` and `templates/crud_example_2/*` into the matching place in your project, i.e. into your project as `templates/crud_example1/*` etc.
* Copy the following files from `web/components` into the same place in your project, i.e. into your project's `web/components` folder:
  * `paginator.html`
  * `paginator_htmx.html`
  * `crud_example_nav.html`

* Activate the apps in your project, in `<project_slug>/settings.py`, to `PROJECT_APPS`, by adding:

```python
    "apps.crud_example1.apps.CrudExample1Config",
    "apps.crud_example2.apps.CrudExample2Config",
```

* Add **crud_example1**'s URLs to your project in `<project_slug>/urls.py`, by adding to `urlpatterns`:

```python
    path("crud_example1/", include("apps.crud_example1.urls")),
```

* Add **crud_example2**'s URLs to your project in `<project_slug>/urls.py`, by adding to `team_urlpatterns`:

```python
    path("crud_example2/", include("apps.crud_example2.urls")),
```

### Update your Database

You need to create and apply database migrations for these models. If you are using Docker, do this:

```bash
make migrations
make migrate
```

If you're running natively, do

```bash
./manage.py makemigrations
./manage.py migrate
```

## Tech Notes -- Pegasus

* The code has been tested using Pegasus 2023.2 (and Pegasus 2023.1)
* The HTML for the views is designed to match the Pegasus example app.
* Pegasus offers a choice of CSS frameworks, but so far this module only implements the Bulma option.

Most of the files for the example apps live in distinct folders, namely:

* `apps/crud_example1`
* `apps/crud_example2`
* `templates/crud_example1`
* `templates/crud_example2`

A handful of changes are best placed in Pegasus folders or as edits to Pegasus files. In addition to the above changes to your project's `settings.py` and `urls.py` files, there is the following:

* `paginator.html` (new file)
* `paginator_htmx.html` (new file)
* `crud_example_nav.html` (new file)
* `app_nav.html` (edit existing file to include `crud_example_nav.html`)

## Tech Notes -- Views

As mentioned above, `views.py` contains code for both FBVs and CBVs. These can co-exist without conflict, so both versions are enabled. You do not need both, so comment out or delete the flavor you don't ultimately need.

Most of the views contain something like this:

```python
    context["active_tab"] = "crud_example1"
```

This is set in the view, and picked up by the HTML template for the nav-bar, in order to highlight the section the user is in. (See `web/components/crud_example_nav.html`)

## Tech Notes -- URLs

As mentioned above, `urls.py` contain `path()` definitions for both FBVs and CBVs. Allowing these to co-exist would create other cruft that complicates things, so you need to have only one set enabled at a time. You can delete or comment out the ones you don't need.

The HTMX flavor of the list view is only provided in CBV style. To enable that, you need to comment out or delete the other flavors of this view.

## Tech Notes -- Pagination

Each of the list views implements pagination, showing N entries at a time with controls in the UI to move to previous and next pages, and pages by number. With FBVs that requires creating a Paginator object and using it correctly. For CBVs, you can just directly call for pagination.

Note that in the example files, we set the number of items per page to 4, which is unusually small. That way one doesn't need to create dozens of objects in order to see the pagination feature in use. In a real application, the items per page might be 10, 20, or more.

The Django Paginator class has a helper method called `get_elided_page_range()` that returns a suitable set of page numbers to shown in the paginator. It will always include the first few pages and last few pages, as well as a few pages on either side of current. We use that to generate the page list for our controls.

The `web/components/paginator.html` file implements the logic and visuals for displaying the pagination controls. See also [Tech Notes – HTMX](#tech-notes----htmx), for the HTMX version of pagination.

## Tech Notes -- HTMX

## Notes and Todos

Any and all comments and suggestions welcome. [peter@cherna.com](mailto:peter@cherna.com)

* I have a decent mixin for team-specific apps using Class Based Views (see `apps/teams/mixins`, but not everything is transparently solved. Looking to see if I can carry this further. I don't yet have a strategy for common team code for team-specific apps using Function Based Views.
