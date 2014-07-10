.. role:: red
.. raw:: html

    <style> .red {color: #ff6b59;} </style>

Version: {{ time }}

**Operatoren:** {% for name in alphabet.operators %} {{ name }}_ {% endfor %}

**Elemente:** {% for name in alphabet.object_attributes %} {{ name }}_ {% endfor %}


Operatoren
---------------------------------------

{% for name, operator in alphabet.operators.items() %}

{{ name }}
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

{% if "doc" in operator.meta %}
{{ operator.meta["doc"] | indent }}
{% else %}
:red:`DOCUMENTATION MISSING`
{% endif %}

{{ operator|runtime }}

*Inputs:*

{{ operator.input.values()|rsttable }}

*Output:*

{{ operator.output.values()|rsttable }}

*Parameters:*

{{ operator.parameters.values()|rsttable }}


*Annotations:*

{% for k,v in operator.meta.items() %}
{{ k }}
{{ v|indent }}
{% endfor %}


{% endfor %}


Attributes
---------------------------------------

{% for name, attrib in alphabet.object_attributes.items() %}

.. _{{name}}:

{{ name }} ``{{ attrib|type }}``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    {{ attrib.description }}


{{ attrib.parameters.values()|rsttable}}

{% endfor %}
