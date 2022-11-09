{{
    config(
        materialized='view',
        database='TVSHOW',
        schema='EXPOSE'
    )
}}

select show_name,
       Case When rating is null then 0
                Else rating
       End Rating,
       Dense_Rank() Over(
                    Order by (Case When rating is null then 0
                                    Else rating
                              End) desc) Rating_Rank
from {{ ref('tvshow_staging') }}
limit 10