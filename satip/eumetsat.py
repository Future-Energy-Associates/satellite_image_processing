"""
Imports
"""
import numpy as np
import pandas as pd
import dataset

import FEAutils as hlp
from typing import Union
import xmltodict
import dotenv
import zipfile
import copy
import os
import io

from requests.auth import HTTPBasicAuth
import requests

from ipypb import track
from IPython.display import JSON


"""
Objects
"""
metadata_maps = {
    'EO:EUM:DAT:MSG:MSG15-RSS': {
        'start_date': {
            'datatype': 'datetime',
            'location': ['eum:EarthObservation', 'om:phenomenonTime', 'gml:TimePeriod', 'gml:beginPosition']
        },
        'end_date': {
            'datatype': 'datetime',
            'location': ['eum:EarthObservation', 'om:phenomenonTime', 'gml:TimePeriod', 'gml:endPosition']
        },
        'result_time': {
            'datatype': 'datetime',
            'location': ['eum:EarthObservation', 'om:resultTime', 'gml:TimeInstant', 'gml:timePosition']
        },
        'platform_short_name': {
            'datatype': 'str',
            'location': ['eum:EarthObservation', 'om:procedure', 'eop:EarthObservationEquipment', 'eop:platform', 'eop:Platform', 'eop:shortName']
        },
        'platform_orbit_type': {
            'datatype': 'str',
            'location': ['eum:EarthObservation', 'om:procedure', 'eop:EarthObservationEquipment', 'eop:platform', 'eop:Platform', 'eop:orbitType']
        },
        'instrument_name': {
            'datatype': 'str',
            'location': ['eum:EarthObservation', 'om:procedure', 'eop:EarthObservationEquipment', 'eop:instrument', 'eop:Instrument', 'eop:shortName']
        },
        'sensor_op_mode': {
            'datatype': 'str',
            'location': ['eum:EarthObservation', 'om:procedure', 'eop:EarthObservationEquipment', 'eop:sensor', 'eop:Sensor', 'eop:operationalMode']
        },
        'center_srs_name': {
            'datatype': 'str',
            'location': ['eum:EarthObservation', 'om:featureOfInterest', 'eop:Footprint', 'eop:centerOf', 'gml:Point', '@srsName']
        },
        'center_position': {
            'datatype': 'str',
            'location': ['eum:EarthObservation', 'om:featureOfInterest', 'eop:Footprint', 'eop:centerOf', 'gml:Point', 'gml:pos']
        },
        'file_name': {
            'datatype': 'str',
            'location': ['eum:EarthObservation', 'om:result', 'eop:EarthObservationResult', 'eop:product', 'eop:ProductInformation', 'eop:fileName', 'ows:ServiceReference', '@xlink:href']
        },
        'file_size': {
            'datatype': 'int',
            'location': ['eum:EarthObservation', 'om:result', 'eop:EarthObservationResult', 'eop:product', 'eop:ProductInformation', 'eop:size', '#text']
        },
        'missing_pct': {
            'datatype': 'float',
            'location': ['eum:EarthObservation', 'eop:metaDataProperty', 'eum:EarthObservationMetaData', 'eum:missingData', '#text']
        },
    }
}


"""
Functions
"""
def request_access_token(user_key, user_secret):
    token_url = 'https://api.eumetsat.int/token'

    data = {
      'grant_type': 'client_credentials'
    }

    r = requests.post(token_url, data=data, auth=(user_key, user_secret))
    access_token = r.json()['access_token']

    return access_token

format_dt_str = lambda dt: pd.to_datetime(dt).strftime('%Y-%m-%dT%H:%M:%SZ')

def query_data_products(
    start_date='2020-01-01', 
    end_date='2020-01-02', 
    start_index=0, 
    num_features=10000,
    product_id='EO:EUM:DAT:MSG:MSG15-RSS'
):
    
    search_url = 'https://api.eumetsat.int/data/search-products/os'

    params = {
        'format': 'json',
        'pi': product_id,
        'si': start_index, 
        'c': num_features,
        'sort': 'start,time,0',
        'dtstart': format_dt_str(start_date),
        'dtend': format_dt_str(end_date)
    }

    r = requests.get(search_url, params=params)
    
    assert r.ok, f'Request was unsuccesful - Error code: {r.status_code}'
    
    return r

def identify_available_datasets(start_date: str, end_date: str, 
                                product_id='EO:EUM:DAT:MSG:MSG15-RSS'):
    
    num_features = 10000
    start_index = 0
    
    datasets = []
    all_results_returned = False
    
    while all_results_returned == False:
        r_json = query_data_products(start_date, end_date, 
                                     start_index=start_index, 
                                     num_features=num_features, 
                                     product_id='EO:EUM:DAT:MSG:MSG15-RSS').json()

        datasets += r_json['features']

        num_total_results = r_json['properties']['totalResults']
        num_returned_results = start_index + len(r_json['features'])

        if num_returned_results < num_total_results:
            start_index += num_features
        else:
            all_results_returned = True
            
        assert num_returned_results == len(datasets), 'Some features have not been appended'
        
    return datasets

dataset_id_to_link = lambda data_id: f'https://api.eumetsat.int/data/download/products/{data_id}'

def json_extract(json_obj:Union[dict, list], locators:list):
    extracted_obj = copy.deepcopy(json_obj)
    
    for locator in locators:
        extracted_obj = extracted_obj[locator]
        
    return extracted_obj

def extract_metadata(data_dir: str, product_id='EO:EUM:DAT:MSG:MSG15-RSS'):
    with open(f'{data_dir}/EOPMetadata.xml', 'r') as f:
        xml_str = f.read()
        
    raw_metadata = xmltodict.parse(xml_str)
    metadata_map = metadata_maps[product_id]
    
    datatypes_to_transform_func = {
        'datetime': pd.to_datetime,
        'str': str,
        'int': int,
        'float': float
    }
    
    cleaned_metadata = dict()

    for feature, attrs in metadata_map.items():
        location = attrs['location']
        datatype = attrs['datatype']

        value = json_extract(raw_metadata, location)
        formatted_value = datatypes_to_transform_func[datatype](value)

        cleaned_metadata[feature] = formatted_value

    return cleaned_metadata

class InvalidCredentials(Exception):
    pass

def check_valid_request(r):
    if r.ok == False:
        if 'Invalid Credentials' in r.text:
            raise InvalidCredentials('The access token passed in the API request is invalid')
        else:
            raise Exception('The API request was unsuccesful')
            
    return

def get_dir_size(directory='.'):
    total_size = 0
    
    for dirpath, dirnames, filenames in os.walk(directory):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size


"""
Download Manager
"""
class DownloadManager:
    def __init__(self, user_key: str, user_secret: str, data_dir: str, metadata_db_fp: str):
        # Requesting the API access token
        self.user_key = user_key
        self.user_secret = user_secret
        
        self.access_token = request_access_token(self.user_key, self.user_secret)
        
        # Configuring the data directory
        self.data_dir = data_dir
        
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        
        # Initialising the metadata database
        self.metadata_db = dataset.connect(f'sqlite:///{metadata_db_fp}')
        self.metadata_table = self.metadata_db['metadata']
        
        return
        
    def download_single_dataset(self, data_link: str):
        params = {
            'access_token': self.access_token
        }

        r = requests.get(data_link, params=params)

        check_valid_request(r)

        zipped_files = zipfile.ZipFile(io.BytesIO(r.content))
        zipped_files.extractall(f'{self.data_dir}')

        return

    def download_datasets(self, start_date:str, end_date:str, product_id='EO:EUM:DAT:MSG:MSG15-RSS'):
        # Identifying dataset ids to download
        datasets = identify_available_datasets(start_date, end_date, product_id=product_id)
        dataset_ids = sorted([dataset['id'] for dataset in datasets])

        # Downloading specified datasets
        for dataset_id in track(dataset_ids):
            dataset_link = dataset_id_to_link(dataset_id)

            if f'{dataset_id}.nat' not in os.listdir(self.data_dir):
                # Download the raw data
                try:
                    self.download_single_dataset(dataset_link)
                except:
                    self.access_token = request_access_token(self.user_key, self.user_secret)
                    self.download_single_dataset(dataset_link)

                # Extract and save metadata
                dataset_metadata = extract_metadata(self.data_dir, product_id=product_id)
                dataset_metadata.update({'downloaded': pd.Timestamp.now()})
                self.metadata_table.insert(dataset_metadata)

                # Delete old metadata files
                for xml_file in ['EOPMetadata.xml', 'manifest.xml']:
                    xml_filepath = f'{self.data_dir}/{xml_file}'

                    if os.path.isfile(xml_filepath):
                        os.remove(xml_filepath)
                        
        return
    
    get_df_metadata = lambda self: pd.DataFrame(self.metadata_table.all()).set_index('id')
