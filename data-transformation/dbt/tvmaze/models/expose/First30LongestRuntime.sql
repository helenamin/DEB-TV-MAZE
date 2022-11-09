{{
    config(
        materialized='view',
        database='TVSHOW',
        schema='EXPOSE'
    )
}}

select show_type,
       Avg(Case When rating is null then 0
                Else rating
       End) as Avg_Rating,
       Rank() Over(
                    Order by (Avg(Case When rating is null then 0
                                       Else rating
                                  End)) desc) Rating_Rank
from {{ ref('tvshow_staging') }}
group by show_type