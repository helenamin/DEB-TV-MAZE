
{% macro clean_string_list(text) %}

    {% set re = modules.re %}
    {% set regex_pattern = '[\[\]]' %}
    {% set text1 = re.sub(regex_pattern ,'',  text) %}
    {% set text2 = re.sub('\s*?"', '', text1) %}
    {% set text3 = re.sub('"', '', text2) %}
    {% set text4 = text3.replace(',','|') %}
    {{ print('text4:' + text4) }}
    {{ return(text4) }}

{% endmacro %}