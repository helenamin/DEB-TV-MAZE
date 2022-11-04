{{
    config(
        materialized='table',
        database='TVSHOW',
        schema='MODEL'
    )
}}

SELECT
CAST(tm.id AS INTEGER) AS Episode_Id,
tm.name AS Episode_Name,
tm.number AS Episode_Number,
tm.season,
CAST(CONCAT(tm.airdate,' ',tm.airtime,':00')AS DATETIME) AS Air_Date_Time,
CAST(tms.id AS INTEGER) AS Show_Id,
CAST(tmsn.id AS INTEGER) AS Network_Id
FROM {{ source('TVSHOW', 'TV_MAZE') }} tm
JOIN {{ source('TVSHOW', 'TV_MAZE_SHOW') }} tms
    ON tm._airbyte_tv_maze_hashid = tms._airbyte_tv_maze_hashid
JOIN {{ source('TVSHOW', 'TV_MAZE_SHOW_NETWORK') }} tmsn
    ON tms._airbyte_show_hashid = tmsn._airbyte_show_hashid