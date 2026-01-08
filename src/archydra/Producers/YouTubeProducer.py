from typing import Iterable
from archydra.Producers import BaseProducer
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from pathlib import Path
from loguru import logger

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def handle_pagination(request_func,**request_args):
    request = request_func(**request_args)
    next_page_token = ""
    while True:
        response = request.execute()
        next_page_token = response.get('nextPageToken','')
        if 'items' in response:
            yield from response['items']
        else:
            yield response
        request_args['pageToken'] = next_page_token
        if next_page_token == '':
            break
        request = request_func(**request_args)

class YouTubeProducer(BaseProducer):
    def __init__(self, client_secrets_file:Path|str, playlist_name="Watch later") -> None:
        self.playlist_name = playlist_name
        client_secrets_file = Path(client_secrets_file)
        api_service_name = "youtube"
        api_version = "v3"
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
        credentials = flow.run_local_server(port=0)
        self.youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)
        super().__init__()
    
    def get_urls(self) -> Iterable[str]:
        request = self.youtube.playlists().list(part="snippet,contentDetails",mine=True)
        title = ""
        pl_id = ""
        found_playlist = False
        while request is not None:
            response = request.execute()
            for p in response['items']:
                logger.debug(p)
                title = p['snippet']['title']
                pl_id = p['id']
                logger.debug(f"Playlist: {title}, id: {pl_id}")
                if title == self.playlist_name:
                    found_playlist = True
                    break
            else:
                # You hit this block when the for loop was not broken
                request = self.youtube.playlists().list_next(request, response)
                continue
            break    

        if not found_playlist:
            raise ValueError(f"No Playlist called \"{self.playlist_name}\" Found")
        request = self.youtube.playlistItems().list(part="snippet,contentDetails",playlistId=pl_id)
        while request is not None:
            response = request.execute()
            for video in response['items']:
                video_id = video['snippet']['resourceId']['videoId']
                logger.trace(f"video_id: {video_id}")
                yield f"https://www.youtube.com/watch?v={video_id}"
            request = self.youtube.playlistItems().list_next(request, response)
        

if __name__ == "__main__":
    p = YouTubeProducer("client_secret.json",playlist_name="Archydra")
    for item in p.get_urls():
        print(item)