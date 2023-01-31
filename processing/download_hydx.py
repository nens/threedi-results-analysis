from pathlib import Path
import requests
import time
from typing import List, Union
import zipfile
import io


KEY = "Bearer requestN&S"


class MockQgsProcessingFeedback:
    def pushInfo(self, info: str):
        pass

    def isCanceled(self) -> bool:
        return False


def download_hydx(
        dataset_name: str,
        target_directory: Path,
        wait_times: List = None,
        feedback=None
) -> Union[Path, None]:
    """
    Download GWSW HydX dataset of given `dataset_name` to given `target_directory`. A request to prepare the dataset for
    download will be send to the GWSW server. Subsequently, status requests will be sent until the dataset is ready for
    download. The wait time between these requests is determined by `wait_times`, a list of time durations (in seconds).
    If all `wait_times` have been used up, the last item in the list will be reused until the process has been completed
    or until the user cancels it (i.e. when feedback.isCanceled() returns True).

    `feedback` should have the methods .pushInfo() and .isCanceled(), e.g. a QgsProcessingFeedback

    :return: path to the downloaded hydx dataset
    """
    wait_times = wait_times or [1]
    feedback = feedback or MockQgsProcessingFeedback()
    request_hydx_url = f"https://apps.gwsw.nl/hyd/makehydx?filter={dataset_name}&delim=pk"
    hydx_headers = {"Authorization": KEY}
    hydx_download = requests.get(url=request_hydx_url, headers=hydx_headers)
    hydx_download_json = hydx_download.json()
    if hydx_download.status_code in (200, 202):
        feedback.pushInfo(f"HydX dataset has been requested (status code {hydx_download.status_code})")
    else:
        feedback.pushInfo(f"HydX dataset request has failed (status code {hydx_download.status_code})")
    finished = False
    i = 0
    while not finished:
        if feedback.isCanceled():
            return None
        if hydx_download.status_code == 202:
            status_url = hydx_download_json['lnk']
            hydx_status = requests.get(url=status_url, headers=hydx_headers)
            if hydx_status.status_code == 200:
                hydx_status_json = hydx_status.json()
                feedback.pushInfo(
                    f"HydX dataset {dataset_name} is ready for download (status code {hydx_status.status_code})"
                )
                hydx_download_url = hydx_status_json['files'][0]['url']
                finished = True
            elif hydx_status.status_code == 202:
                feedback.pushInfo(
                    f"HydX dataset is being prepared on the server (status code {hydx_status.status_code})"
                )
            else:
                feedback.pushInfo(
                    f"Something went wrong while processing the request (status code {hydx_status.status_code})"
                )
                finished = True
        elif hydx_download.status_code == 200:
            feedback.pushInfo(
                f"HydX dataset {dataset_name} is ready for download (status code {hydx_download.status_code})"
            )
            hydx_download_url = hydx_download_json['files'][0]['url']
            finished = True
        try:
            time.sleep(wait_times[i])
        except IndexError:
            time.sleep(wait_times[-1])
        i += 1
    hydx_folder = target_directory / (dataset_name + '.hydx')
    r = requests.get(url=hydx_download_url, headers=hydx_headers)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(hydx_folder)
    feedback.pushInfo(
        f'HydX dataset {dataset_name} has been downloaded and unzipped to {hydx_folder}'
    )
    return hydx_folder
