from typing import Any, Iterable, List, Mapping, MutableMapping, Optional, Tuple
from airbyte_cdk.sources import AbstractSource
from airbyte_cdk.sources.streams import Stream
from airbyte_cdk.sources.streams.http import HttpStream
from airbyte_cdk.sources.streams.http.auth import NoAuth
from datetime import * 
import requests

class TvMaze(HttpStream):

    url_base = "https://api.tvmaze.com/"
    primary_key = None
    cursor_field = "airdate" # informs the stream that it now supports incremental sync

    def __init__(self, config: Mapping[str, Any], start_date: datetime, **kwargs):
        
        super().__init__()
        self.country = config['country']
        self.start_date = start_date
        self._cursor_value = None

    def get_updated_state(self, current_stream_state: MutableMapping[str, Any], latest_record: Mapping[str, Any]) -> Mapping[str, any]:
        
        # This method is called once for each record returned from the API to compare the cursor field value in that record with the current state
        # we then return an updated state object. If this is the first time we run a sync or no state was passed, current_stream_state will be None.
        if current_stream_state is not None and "airdate" in current_stream_state:
            current_parsed_date = datetime.strptime(current_stream_state["airdate"], "%Y-%m-%d")
            latest_record_date = datetime.strptime(latest_record["airdate"], "%Y-%m-%d")
            return {"airdate": max(current_parsed_date, latest_record_date).strftime("%Y-%m-%d")}
        else:
            return {"airdate": self.start_date.strftime("%Y-%m-%d")}

    def _chunk_date_range(self, start_date: datetime) -> List[Mapping[str, Any]]: 
        
        dates = []
        while start_date < datetime.now():
            dates.append({self.cursor_field: start_date.strftime("%Y-%m-%d")})
            start_date += timedelta(days=1)
        return dates

    def stream_slices(self, sync_mode, cursor_field: List[str] = None, stream_state: Mapping[str, Any]=None)-> Iterable[Optional[Mapping[str, Any]]]:
        
        start_date = datetime.strptime(stream_state[self.cursor_field], "%Y-%m-%d") if stream_state and self.cursor_field in stream_state else self.start_date 
        return self._chunk_date_range(start_date)

    def next_page_token(self, response: requests.Response) -> Optional[Mapping[str, Any]]:
        
        # this api does not offer pagination, so we return None to indicate that there are no more pages         
        return None

    def path(
        self, stream_state: Mapping[str, Any] = None, stream_slice: Mapping[str, Any] = None, next_page_token: Mapping[str, Any] = None
    ) -> str:
         
        # The "/schedule" path gives us the schedule endpoint        
        return "schedule"

    def request_params(
            self,
            stream_state: Mapping[str, Any],
            stream_slice: Mapping[str, Any] = None,
            next_page_token: Mapping[str, Any] = None,
    ) -> MutableMapping[str, Any]:
        
        # The api does not require that we include apikey as a header
        return {"country":self.country, "date":stream_slice["airdate"] }

    def parse_response(
            self,
            response: requests.Response,
            stream_state: Mapping[str, Any],
            stream_slice: Mapping[str, Any] = None,
            next_page_token: Mapping[str, Any] = None,
    ) -> Iterable[Mapping]:
        
        # The response is a simple JSON whose schema matches our stream's schema exactly, 
        # so we just return a list containing the response
        return response.json()

class SourceTvmaze(AbstractSource):

    """
        Entrypoint class
    """

    def check_connection(self, logger, config) -> Tuple[bool, any]:

        accepted_countries = {"US","GB"}
        input_country = config['country']
        if input_country not in accepted_countries:
            return False, f"Input country {input_country} is invalid. Please input one of the following country codes: {accepted_countries}"
        else:
            return True, None

    def streams(self, config: Mapping[str, Any]) -> List[Stream]:

        # TODO remove the authenticator if not required.
        auth = NoAuth()
        start_date = datetime.strptime(config['start_date'], '%Y-%m-%d')
        return [TvMaze(authenticator=auth, config=config, start_date=start_date)]