{{
    config(
        materialized='view',
        database='TVSHOW',
        schema='EXPOSE'
    )
}}

with show_type_with_best_rating_cte as (
select show_type,
       Avg(Case When rating is null then 0
                Else rating
       End) as Avg_Rating,
       Rank() Over(
                    Order by (Avg(Case When rating is null then 0
                                       Else rating
                                  End)) desc) Rating_Rank
from {{ ref('tvshow_staging') }}
group by show_type)
select show_type, show_name,
       Case When runtime_in_min is null then 0
                Else runtime_in_min
       End runtime_in_min, Rank() Over(Order By (Case When runtime_in_min is null then 0
                                                     Else runtime_in_min
                                                End) Desc) as Ranking
from {{ ref('tvshow_staging') }} ts
where show_type in (select show_type from show_type_with_best_rating_cte
                    order by Rating_Rank
                    limit 1)
limit 1