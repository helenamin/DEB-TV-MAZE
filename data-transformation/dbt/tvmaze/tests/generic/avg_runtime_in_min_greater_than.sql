{% test avg_runtime_in_min_greater_than(model, column_name, var_value) %}

    select *
    from {{ model }}
    where {{ column_name }} = {{var_value}}

{% endtest %}