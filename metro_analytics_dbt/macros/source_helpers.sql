{% macro metro_source(day) %}
    {{ source('external_source_' ~ day ~ '_ridership', day ~ '_ridership') }}
{% endmacro %}
