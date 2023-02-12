# Example Apps for SaaS Pegasus, v2

[SaaS Pegasus](https://saaspegasus.com) is a great framework for getting up and running quickly and robustly with Django web applications.

Here are example apps for SaaS Pegasus. You can use these to help your create and improve your own apps, models, and views, using either Class-Based Views (CBV) or Function-Based Views (FBV). For what's new, see the [CHANGELOG](CHANGELOG.md).

Some of the things showcased in these examples include:

* FBV and CBV implemations of objects that are not team-related (for when you've configured Pegasus without teams, or if you need cross-team objects)
* FBV and CBV implemations of team-specific objects (for objects that belong to a specific team)
* API access to non-team and team-specific objects
* Use of pagination
* HTMX to make better-looking updates in pagination
* Use of role-based permissions
* Enhanced form field abilities including AlpineJS for simple client-side logic

This replaces the older [first version of this project](https://github.com/pcherna/pegasus-example-apps)). It is cleaner, better organized, and is refreshed to match the current Saas Pegasus.

## Apps and Models Introduction

* **crud_example1** is an app containing the **Thing** model, which is an example non-team-related object.
* **crud_example2** is an app containing the **TeamThing** model, which is an example team-specific object.
* **crud_example3** is an app containing the **PermThing** model, which is an example showing how permissions can be used to shape the UI and capabilities.
* **crud_example4** is an app containing the **InputThing** model, which is an example showing enhanced form fields including client-side behaviors.

Each app:

* Implements a model with several sample fields (`Name`, `Number`, and `Notes`)
* Implements clean Class-Based Views for:
  * Create
  * List (summarize all objects, showing their `Name` and `Number`), with pagination
  * Details (details on one object, showing all their fields)
  * Update
  * Delete
* **Thing** and **TeamThing** also implement clean Function-Based Views for the above
* **Thing** and **TeamThing** implement a basic CRUD API using django-rest-framework
* **PermThing** implements permission-based access to deny all, view, add, change, and delete objects, as well as one custom permission ("view summary")
* **InputThing** implements enhanced form-field options such as controlling the number of rows in a text input, and disabling fields. As well, it shows the use of AlpineJS for simple client-side actions like showing/hiding related fields, or validating an email address.
 
## Choosing FBV or CBV

(**Thing** and **TeamThing** only, the others have CBVs)

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

* Choose which apps you want to try in your project (see [Tech Notes – Dependencies](#tech-notes----dependencies)).
* Add the code by copying `apps/crud_example1/*`, `apps/crud_example_2/*`, `apps/crud_example_4/*`, and `apps/crud_example_4/*` into the matching place in your project, i.e. into your project as `apps/crud_example1/*` etc.
* Add the templates by copying `templates/crud_example1/*`, `templates/crud_example_2/*`, `templates/crud_example_3/*`, and `templates/crud_example_4/*` into the matching place in your project, i.e. into your project as `templates/crud_example1/*` etc.
* Copy the following files from `web/components` into the same place in your project, i.e. into your project's `web/components` folder:
  * `paginator.html`
  * `paginator_htmx.html`
  * `crud_example_nav.html`
* If you did not choose all four apps, delete any you did not choose from `crud_example_nav.html`
* Add entries for the example classes to the left nav, by editing `web/components/app_nav.html`, as follows:
  * After the line `{% include "web/components/team_nav.html" %}`, add:

```python
    {% include "web/components/crud_example_nav.html" %}
```

* Activate the apps in your project, in `<project_slug>/settings.py`, to `PROJECT_APPS`, by adding:

```python
    "apps.crud_example1.apps.CrudExample1Config",
    "apps.crud_example2.apps.CrudExample2Config",
    "apps.crud_example3.apps.CrudExample3Config",
    "apps.crud_example4.apps.CrudExample4Config",
```

* Add **crud_example1**'s URLs to your project in `<project_slug>/urls.py`. Since this example is not team-specific, add the URLs to `urlpatterns`:

```python
    path("crud_example1/", include("apps.crud_example1.urls")),
```

* Add **crud_example2**'s URLs to your project in `<project_slug>/urls.py`. Since these example are team-speicif, add the URLs to `team_urlpatterns`:

```python
    path("crud_example2/", include("apps.crud_example2.urls")),
    path("crud_example3/", include("apps.crud_example3.urls")),
    path("crud_example4/", include("apps.crud_example4.urls")),
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
* Pegasus offers a choice of CSS frameworks, but so far these examples only implement the Bulma option.

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

## Tech Notes -- Dependencies

**InputThing** from **crud_example4** depends on AlpineJS and upon the `django-widget-tweaks` package. The template code pulls in AlpineJS, but you need to add `django-widget-tweaks` to your project.

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

Our list templates include the paginator at the top of the list, and show how you can include a second copy at the bottom, if desired (can be useful if each page can be quite long).

## Tech Notes -- Perimissions

**crud_example3** gives us **PermThing**, which shows off the use of permissions to shape the UI and capabilities. Every model automatically is given four permissions, for view, change, add, and delete. Those permissions get named after the app and model, thus:

* `crud_example3.view_permthing`
* `crud_example3.change_permthing`
* `crud_example3.add_permthing`
* `crud_example3.delete_permthing`

In addition, we show how to define additional custom permissions, in our case `crud_example3.view_summary_permthing` that we imlement to mean the user can only see the summary info in the list of objects.

The **PermThing** templates show how we can adapt by permission to hide details, remove buttons, not use links, depending on the level of permissions the user has. The **PermThing** views show how to use these permissions to block access to views (e.g. prevent adding an object if you don't have `add_permthing` permission. We block at the view level so the user can't just enter an otherwise valid URL.)

**Note**: If the currently-logged in user is a superuser they automatically have all access, so you won't be able to see what is being shown here. If you log in as a normal user, you will see some buttons that can change the current user's permissions. This is not the way you'd normally do things in a production application, but it makes it easy to see and explore the template and view behaviors.

## Tech Notes -- HTMX

HTMX lets you send requests from your front-end to Django, and integrate the results back into the page without a full refresh. It's a good companion to Django for a number of different use cases. We use it here to implement pagination of the list view in a way that only redraws the items in the list.

Every request to Django is served by a view. There are a number of different strategies for defining the view for the "partial" pages that an HTMX request typically wants. For pagination, we actually use the same URL, hence the same view. We can look in the HTTP headers to tell an HTMX request from a full page refresh, and return a different result. In our case, we simply want a different template, and we achieve that like so:

```python
    def get_template_names(self):
        """If we are receiving an htmx request, return just the partial, else the whole page."""
        if "HX-Request" in self.request.headers:
            return ["crud_example1/thing_list_htmx_partial.html"]
        else:
            # Use the full template
            return ["crud_example1/thing_list_htmx.html"]
```

**Note**: There is a nice package called [django-htmx](https://github.com/adamchainz/django-htmx) (see [django-htmx documentation](https://django-htmx.readthedocs.io/)) – one of its conveniences is that you can use a slightly simpler test, namely:

```python
        if request.htmx:
```

Our strategy is to extra the for-loop that renders the actual items into its own template file, here called `teamthing_list_htmx_partial.html`. In the main list template `teamthing_list_htmx.html`, we use

```html
{% include "crud_example2/teamthing_list_htmx_partial.html" %}
```

so that the main template still includes the list.

The magic happens in `web/components/paginator_htmx.html`. Whereas the regular paginator `web/components/paginator.html` goes to page _num_ by

```html
<a ... href="?page={{ num }}">
```

The HTMX version uses

```html
<a ...hx-get="?page={{ num }}">
```

As you see, this is the same URL, but as an HTMX get-request. That causes Django to return HTML built from the "partial" flavor of the template, which essentially is a `div` containing the paginator and the list of objects. What does the browser do? It replaces the target `div` with this response, and from the partial template we can see where we defined the target `div`:

```html
<div hx-target="this">
```

So the correct part of the HTML is replaced, and cleanly re-rendered.

The other HTMX technique we're using is that in the request next to `hx-get`, we also specify `hx-push-url="true"` which causes the new URL to end up in the browser history, part of what we need to allow **Back** and **Next** functionality to work. (This is another reason why using the same URL for full and partial requests is valuable – that URL is ready for inclusion in browser history.) Setting `hx-history="false"` tells HTMX not to cache the history, but to go ask the server when the user hits **Back** or **Next**.

## Tech Notes -- Enhanced Form Fields

This module includes `apps\web\templatetags\form_tags_x.py`, which extends Pegasus standard `{% render_..._input %}` template tags with some useful features. See some sample uses in `inputthing_form.html`.

### render_text_input

The `{% render_text_input %}` template tag supports the following additional parameters:

* **rows**=_n_: For multi-line text input, sets the row-height of this form-field
* **type**=_type_: Lets you specify any HTML input type, such as `password`, `date`, etc.
* **disabled**=_True/False_: Lets you specify this field should be disabled. The field's value still gets posted with the form.
* **locked**=_True/False_: Like **disabled**, but adds a lock icon next to the label.
* **xmodel**=_model-name_: For use with AlpineJS, bind the field to an AlpineJS `x-model`.
* **xref**=_ref-name_: For use with AlpineJS, create an `x-ref` to the field.

### render_select_input

The `{% render_select_input %}` template tag supports the following additional parameters:

* **disabled**=_True/False_: Lets you specify this field should be disabled. The field's value still gets posted with the form.
* **locked**=_True/False_: Like **disabled**, but adds a lock icon next to the label.
* **xmodel**=_model-name_: For use with AlpineJS, bind the field to an AlpineJS `x-model`.
* **xref**=_ref-name_: For use with AlpineJS, create an `x-ref` to the field.

In addition, if the underlying widget supports multi-selection, this can be used.

### render_checkbox_input

The `{% render_checkbox_input %}` template tag supports the following additional parameters:

* **disabled**=_True/False_: Lets you specify this field should be disabled. The field's value still gets posted with the form.
* **locked**=_True/False_: Like **disabled**, but adds a lock icon next to the label.
* **xmodel**=_model-name_: For use with AlpineJS, bind the field to an AlpineJS `x-model`.
* **xref**=_ref-name_: For use with AlpineJS, create an `x-ref` to the field.

### render_checkboxlist_input

The `{% render_checkboxlist_input %}` template tag lets you render a CheckboxSelectMultiple field as a list of checkboxes, which can be bound to an AlpineJS model.

* **xmodel**=_model-name_: For use with AlpineJS, bind the field to an AlpineJS `x-model`.

## Tech Notes -- AlpineJS

AlpineJS lets you easily achieve lightweight client side behaviors. The form template `inputthing_form.html` shows two different uses:

* How to use one field (our checkbox called **extra**) to show or hide other fields
* How to do as-you-type validation (of an email address)

Here's a look at a slightly-reduced extract of the show/hide logic:

```html
<div x-data="{ extra: {{ form.extra.value|lower }} }">
    ...
    {% render_checkbox_input form.extra xmodel="extra" %}
    <div x-cloak x-show="extra" x-transition.duration.250ms>
        {% render_text_input form.number %}
    </div>
</div>

```

Breaking that down:

* `x-data` is an AlpineJS directive that declares a JavaScript variable called `extra`, that's initialized from the `form.extra` field's value. The use of `|lower` converts Python-style `True` / `False` to JavaScript compatible `true` / `false`.
* `xmodel="extra"` binds the live value of the checkbox to the JavaScript `extra` variable.
* `x-show` is an AlpineJS directive that conditionally shows its div when the expression `extra` is true (i.e. when checked).
* `x-cloak` hides the div until AlpineJS gets a chance to initialize, which prevents it from flashing then vanishing if `extra` is false initially.
* `x-transition.duration.250ms` is an Alpine directive requesting that a transition be used to make the div come and go.

The other example showcases as-you-type validation. A `validateEmail()` JavaScript function will return True if the email looks fully formed. We then show or hide a valid or invalid message based on that. See the actual code for details.



## Notes and Todos

Any and all comments and suggestions welcome. [peter@cherna.com](mailto:peter@cherna.com)
