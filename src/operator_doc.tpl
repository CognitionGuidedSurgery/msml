.. role:: red
.. raw:: html

    <style> .red {color: #ff6b59;} </style>

{{ operator.name }}
{{ operator.name|title("=")}}

{% if "doc" in operator.meta %}
{{ operator.meta["doc"] | indent }}
{% else %}
:red:`DOCUMENTATION MISSING`
{% endif %}

{% if operator.runtime['exec'] == 'python' %}
:type: PythonOperator
:modul: :py:mod:`{{ operator.modul_name }}`
:function: :py:func:`{{ operator.modul_name }}.{{ operator.function_name }}`
{% elif operator.runtime['exec'] == 'sh' %}
:type: **ShellOperator**
:template: ``{{ operator.command_tpl }}%s``
{% elif operator.runtime['exec'] == 'so' %}
:type: **SharedObject**
:file: ``{{ operator.filename }}``
:symbol: ``{{operator.symbol_name}}``
{%- endif %}

{% macro slot_list(name, slots) %}
:{{ name }}:
    {% for s in slots.values() %}
        * **{{ s.name }}** : {{ s.sort | format_sort }}

            {% if 'meta' in s.meta -%} {{ s.doc }} {% else %} :red:`DOCUMENTATION MISSING` {%- endif %}
    {% endfor %}
{% endmacro %}

{{ slot_list("Inputs", operator.input) }}
{{ slot_list("Output", operator.output) }}
{{ slot_list("Parameter", operator.parameters) }}


{% for k,v in operator.meta.items() %}
:{{ k }}:
{{ v|indent }}
{% endfor %}

