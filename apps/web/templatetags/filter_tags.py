from django import template

from .form_tags import _render_field

register = template.Library()


# These tags are suitable within the filter-form. By using a suitable hx-trigger, and hx-get, filter-changes
# can be sent to the server dynamically.
# You can specify most other htmx attributes at a higher level (e.g. at the filter-form),
# but hx-get or hx-trigger have to be specified at this level.


@register.simple_tag
def render_text_hx_filter(filter, form_field, xget=""):
    """Render a text input field, which sends hx-get when the contents change, with
    a 500ms idle-delay."""
    TEXT_INPUT_TEMPLATE = f"""{{% load widget_tweaks %}}
    <div class="field">
        <label class="label is-small">{{{{ form_field.label }}}}</label>
        <div class="control is-expanded">
            <input type="text" class="input is-small"
                hx-trigger="keyup delay:500ms changed" hx-get="{xget}"
                name="{{{{ form_field.name }}}}"
                {{% if form_field.value != None %}} value="{{{{ form_field.value|stringformat:'s' }}}}"{{% endif %}}
                id="id_{{{{ form_field.name }}}}">
        </div>
        <div class="help">{{{{ form_field.help_text|safe }}}}</div>
        {{{{ form_field.errors }}}}
    </div>
    """
    return _render_field(TEXT_INPUT_TEMPLATE, form_field)


@register.simple_tag
def render_select_hx_filter(form_field, xget=""):
    """For filters, render a select field, styled for filters (small, rounded),
    and which sends hx-get when the value changes."""

    SELECT_INPUT_TEMPLATE = f"""{{% load widget_tweaks %}}
    <div class="field">
        <label class="label is-small">{{{{ form_field.label }}}}</label>
        <div class="control is-expanded">
            <div class="select is-small is-fullwidth is-rounded">
                {{% render_field form_field hx-trigger="change" hx-get="{xget}" %}}
            </div>
        </div>
        <div class="help">{{{{ form_field.help_text|safe }}}}</div>
        {{{{ form_field.errors }}}}
    </div>
    """
    return _render_field(SELECT_INPUT_TEMPLATE, form_field)
