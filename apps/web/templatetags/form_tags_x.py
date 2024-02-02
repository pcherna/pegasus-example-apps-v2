from django import template

from .form_tags import _render_field

# Django template tags based on the bulma-styled Pegasus form_tags.py, with extra capabilities

# ZZZ: Todo
# - Dive into search filter tags
# - Add is-fullwidth to select_class makes most buttons look better (fix any overwide ones with layout)

register = template.Library()


# General notes:
# - django-widget-tweaks:
#   - Gives us an easy way to add attrs to HTML (plus other stuff we're not using)
#   - Both Pegasus and django-widget-tweaks have a tag called {% render_field %}
#     the last thing you {% load %} wins. I'm loading widget_tweaks a bit magically within
#     my own tags so it "wins", but that's also goofy
#   - I could make {% load widget_tweaks %} an explicit requirement, would need to be after form_tags
# - disabled handling:
#   - Per the HTML spec, disabled fields do not post. So, we handle that by including a
#     hidden non-disabled copy that will post. Otherwise our form validation needs to be
#     overridden to allow disabled field values to be "missing" at post.
# - I use F-strings, which means any literal { } within have to be doubled


@register.simple_tag
def render_text_input(form_field, disabled=False, locked=False, rows=None, type=None, xmodel=None, xref=None):
    """Enhanced tag for rendering a text-input widget. Like Pegasus-standard render_text_input,
    with support for additional parameters:
    - rows: Optional, number of rows to allocate in the textarea widget
    - type: html input type, e.g. "date", "datetime", "password", ...
    - disabled: Optional, whether the field should be disabled
    - locked: Optional, whether the field should be locked (disabled, plus lock icon)
    - xmodel: Optional, AlpineJS variable to use as x-model
    - xref: Optional, name to use as AlpineJS x-ref"""
    disabled = disabled or locked
    rows_attr = f"rows={rows}" if rows else ""
    type_attr = f'type="{type}" class="input"' if type else ""
    x_model_attr = f'x-model="{xmodel}"' if xmodel else ""
    x_ref_attr = f'x-ref="{xref}"' if xref else ""
    disabled_attr = 'disabled="disabled"' if disabled else ""
    # Use django-widget-tweaks' render_field tag to add any of our enhanced attributes, and handle disabled case:
    form_field_x = _expand_disabled(
        disabled, f"{{% render_field form_field {type_attr} {rows_attr} {x_model_attr} {x_ref_attr} {disabled_attr} %}}"
    )
    label = _expand_label(locked)

    # Now that form_field_x is our enhanced field, include it in the overall template for the widget:
    TEXT_INPUT_TEMPLATE = f"""{{% load widget_tweaks %}}
    <div class="field">
        <label class="label">{label}</label>
        <div class="control">
            {form_field_x}
        </div>
        <div class="help">{{{{ form_field.help_text|safe }}}}</div>
        {{{{ form_field.errors }}}}
    </div>
    """
    return _render_field(TEXT_INPUT_TEMPLATE, form_field)


# ZZZ: Add is-fullwidth to select_class makes most buttons look better (fix any overwide ones with layout)
@register.simple_tag
def render_select_input(form_field, disabled=False, locked=False, xmodel=None, xref=None):
    """Enhanced tag for rendering a select widget. Like Pegasus-standard render_select_input,
    with support for additional parameters:
    - disabled: Optional, whether the field should be disabled
    - locked: Optional, whether the field should be locked (disabled, plus lock icon)
    - xmodel: Optional, AlpineJS variable to use as x-model
    - xref: Optional, name to use as AlpineJS x-ref
    In addition, it handles widgets that specify multi-selection."""
    disabled = disabled or locked
    select_class = "select"
    # Handle multi-select widgets (Note: in the case the field is hidden, the form_field is a string,
    # not a field object, so I have to test so I don't fail when I look at .widget_type)
    if hasattr(form_field, "widget_type") and form_field.widget_type == "selectmultiple":
        select_class = "select is-multiple"

    x_model_attr = f'x-model="{xmodel}"' if xmodel else ""
    x_ref_attr = f'x-ref="{xref}"' if xref else ""
    disabled_attr = 'disabled="disabled"' if disabled else ""
    # Use django-widget-tweaks' render_field tag to add any of our enhanced attributes, and handle disabled case:
    form_field_x = _expand_disabled(
        disabled, f"{{% render_field form_field {x_model_attr} {x_ref_attr} {disabled_attr} %}}"
    )
    label = _expand_label(locked)

    # Now that form_field_x is our enhanced field, include it in the overall template for the widget:
    SELECT_INPUT_TEMPLATE = f"""{{% load widget_tweaks %}}
        <div class="field">
            <label class="label">{label}</label>
            <div class="control">
                <div class="{select_class}">
                    {form_field_x}
                </div>
            </div>
            <div class="help">{{{{ form_field.help_text|safe }}}}</div>
            {{{{ form_field.errors }}}}
        </div>
    """
    return _render_field(SELECT_INPUT_TEMPLATE, form_field)


@register.simple_tag
def render_checkbox_input(form_field, disabled=False, locked=False, xmodel=None, xref=None):
    """Enhanced tag for rendering a checkbox widget. Like Pegasus-standard render_checkbox_input,
    with support for additional parameters:
    - disabled: Optional, whether the field should be disabled
    - locked: Optional, whether the field should be locked (disabled, plus lock icon)
    - xmodel: Optional, AlpineJS variable to use as x-model
    - xref: Optional, name to use as AlpineJS x-ref"""
    disabled = disabled or locked
    x_model_attr = f'x-model="{xmodel}"' if xmodel else ""
    x_ref_attr = f'x-ref="{xref}"' if xref else ""
    disabled_attr = 'disabled="disabled"' if disabled else ""

    # Use django-widget-tweaks' render_field tag to add any of our enhanced attributes, and handle disabled case:
    form_field_x = _expand_disabled(
        disabled, f"{{% render_field form_field {x_model_attr} {x_ref_attr} {disabled_attr} %}}"
    )
    label = _expand_label(locked)

    # Now that form_field_x is our enhanced field, include it in the overall template for the widget:
    CHECKBOX_INPUT_TEMPLATE = f"""{{% load widget_tweaks %}}
        <div class="field">
            <div class="control">
                <label class="checkbox">
                    {form_field_x}
                    {label}
                </label>
            </div>
            <div class="help">{{{{ form_field.help_text|safe }}}}</div>
            {{{{ form_field.errors }}}}
        </div>
    """

    return _render_field(CHECKBOX_INPUT_TEMPLATE, form_field)


# Version for CheckboxSelectMultiple that takes a model name to bind to x-model, for AlpineJS
# the model will be an array of checked boxes
@register.simple_tag
def render_checkboxlist_input(form_field, xmodel=None):
    """Enhanced tag for rendering a list of checkbox widgets. Related to Pegasus-standard render_select_input,
    but renders as a list of checkboxes, and supports additional parameters:
    - xmodel: AlpineJS model variable to use as the array of checked boxes"""
    x_model_attr = f'x-model="{xmodel}"' if xmodel else ""

    CHECKBOX_SELECT_MULTIPLE_INPUT_TEMPLATE = f"""<div class="field" id="id_{{{{ item.data.name }}}}">
        {{% for item in form_field %}}
        <div class="control">
            <label class="checkbox" for="{{{{ item.data.attrs.id }}}}">
                <input type="checkbox" {x_model_attr}
                    value="{{{{ item.data.value }}}}"
                    name="{{{{ item.data.name }}}}"
                    id="{{{{ item.data.attrs.id }}}}">
                {{{{ item.data.label }}}}
            </label>
        </div>
        {{% endfor %}}
        <div class="help">{{{{ form_field.help_text|safe }}}}</div>
        {{{{ form_field.errors }}}}
    </div>
    """
    return _render_field(CHECKBOX_SELECT_MULTIPLE_INPUT_TEMPLATE, form_field)


def _expand_disabled(disabled, form_field_x):
    # Per HTML spec, disabled fields do not post. So include a hidden non-disabled copy that will post
    if disabled:
        form_field_x = form_field_x + "{% render_field form_field.as_hidden %}"
    return form_field_x


def _expand_label(locked):
    """Add a lock icon to the label if the locked property is set."""
    icon = '<span class="pg-icon mr-1"><i class="fa fa-xs fa-lock"></i></span>' if locked else ""
    return icon + "{{ form_field.label }}"
