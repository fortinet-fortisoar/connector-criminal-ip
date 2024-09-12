# Edit the config_and_params.json file and add the necessary parameter values.
"""
Copyright start
Copyright (C) 2008 - 2024 Fortinet Inc.
All rights reserved.
FORTINET CONFIDENTIAL & FORTINET PROPRIETARY SOURCE CODE
Copyright end
"""

import os
import sys
import json
import pytest
import logging
import importlib
from connectors.core.connector import ConnectorError

with open('tests/config_and_params.json', 'r') as file:
    params = json.load(file)

current_directory = os.path.dirname(__file__)
parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
grandparent_directory = os.path.abspath(os.path.join(parent_directory, os.pardir))
sys.path.insert(0, str(grandparent_directory))

module_name = 'criminal-ip_1_0_0.operations'
conn_operations_module = importlib.import_module(module_name)
operations = conn_operations_module.operations

with open('info.json', 'r') as file:
    info_json = json.load(file)

logger = logging.getLogger(__name__)
    

# To test with different configuration values, adjust the index in the list below.
@pytest.fixture(scope="module")
def valid_configuration():
    return params.get('config')[0]
    
    
@pytest.fixture(scope="module")
def valid_configuration_with_token(valid_configuration):
    config = valid_configuration.copy()
    try:
        operations['check_health'](config)
    except TypeError:
        connector_info = config['connector_info']
        operations['check_health'](config, connector_info)
    return config
    

@pytest.mark.checkhealth     
def test_check_health_success(valid_configuration):
    config = valid_configuration.copy()
    try:
        result = operations['check_health'](config)
    except TypeError:
        connector_info = config['connector_info']
        result = operations['check_health'](config, connector_info)
    assert result  
    

@pytest.mark.checkhealth     
def test_check_health_invalid_server_url(valid_configuration):
    invalid_config = valid_configuration.copy()
    invalid_config['server_url'] = params.get('invalid_params')['text']
    with pytest.raises(ConnectorError):
        try:
            operations['check_health'](invalid_config)
        except TypeError:
            connector_info = invalid_config['connector_info']
            operations['check_health'](invalid_config, connector_info)
    

@pytest.mark.checkhealth     
def test_check_health_invalid_api_key(valid_configuration):
    invalid_config = valid_configuration.copy()
    invalid_config['api_key'] = params.get('invalid_params')['password']
    with pytest.raises(ConnectorError):
        try:
            operations['check_health'](invalid_config)
        except TypeError:
            connector_info = invalid_config['connector_info']
            operations['check_health'](invalid_config, connector_info)
    

@pytest.mark.get_url_reputation
@pytest.mark.parametrize("input_params", params['get_url_reputation'])
def test_get_url_reputation_success(valid_configuration_with_token, input_params):
    logger.info("params: {0}".format(input_params))
    assert operations['get_url_reputation'](valid_configuration_with_token.copy(), input_params.copy())
  
    
# Ensure that the provided input_params yield the correct output schema, or adjust the index in the list below.
# Add logic for validating conditional_output_schema or if schema is other than dict.
@pytest.mark.get_url_reputation
@pytest.mark.schema_validation
def test_validate_get_url_reputation_output_schema(valid_configuration_with_token):
    input_params = params.get('get_url_reputation')[0].copy()
    schema = {}
    for operation in info_json.get("operations"):
        if operation.get('operation') == 'get_url_reputation':
            if "conditional_output_schema" in operation or "api_output_schema" in operation:
                pytest.skip("Skipping test because conditional_output_schema or api_output_schema is not supported.")
            else:
                schema = operation.get('output_schema')
            break
    resp = operations['get_url_reputation'](valid_configuration_with_token.copy(), input_params)
    if isinstance(schema, dict) and isinstance(resp, dict):
        logger.info("output_schema: {0}".format(schema))
        assert resp.keys() == schema.keys()
    else:
        pytest.skip("Skipping test because output_schema is not a dict.")
    

@pytest.mark.get_url_reputation     
def test_get_url_reputation_invalid_query(valid_configuration_with_token):
    input_params = params.get('get_url_reputation')[0].copy()
    input_params['query'] = params.get('invalid_params')['text']
    with pytest.raises(ConnectorError):
        operations['get_url_reputation'](valid_configuration_with_token.copy(), input_params)
    

@pytest.mark.get_ip_reputation
@pytest.mark.parametrize("input_params", params['get_ip_reputation'])
def test_get_ip_reputation_success(valid_configuration_with_token, input_params):
    logger.info("params: {0}".format(input_params))
    assert operations['get_ip_reputation'](valid_configuration_with_token.copy(), input_params.copy())
  
    
# Ensure that the provided input_params yield the correct output schema, or adjust the index in the list below.
# Add logic for validating conditional_output_schema or if schema is other than dict.
@pytest.mark.get_ip_reputation
@pytest.mark.schema_validation
def test_validate_get_ip_reputation_output_schema(valid_configuration_with_token):
    input_params = params.get('get_ip_reputation')[0].copy()
    schema = {}
    for operation in info_json.get("operations"):
        if operation.get('operation') == 'get_ip_reputation':
            if "conditional_output_schema" in operation or "api_output_schema" in operation:
                pytest.skip("Skipping test because conditional_output_schema or api_output_schema is not supported.")
            else:
                schema = operation.get('output_schema')
            break
    resp = operations['get_ip_reputation'](valid_configuration_with_token.copy(), input_params)
    if isinstance(schema, dict) and isinstance(resp, dict):
        logger.info("output_schema: {0}".format(schema))
        assert resp.keys() == schema.keys()
    else:
        pytest.skip("Skipping test because output_schema is not a dict.")
    

@pytest.mark.get_ip_reputation     
def test_get_ip_reputation_invalid_query(valid_configuration_with_token):
    input_params = params.get('get_ip_reputation')[0].copy()
    input_params['query'] = params.get('invalid_params')['text']
    with pytest.raises(ConnectorError):
        operations['get_ip_reputation'](valid_configuration_with_token.copy(), input_params)
    

@pytest.mark.get_domain_reputation
@pytest.mark.parametrize("input_params", params['get_domain_reputation'])
def test_get_domain_reputation_success(valid_configuration_with_token, input_params):
    logger.info("params: {0}".format(input_params))
    assert operations['get_domain_reputation'](valid_configuration_with_token.copy(), input_params.copy())
  
    
# Ensure that the provided input_params yield the correct output schema, or adjust the index in the list below.
# Add logic for validating conditional_output_schema or if schema is other than dict.
@pytest.mark.get_domain_reputation
@pytest.mark.schema_validation
def test_validate_get_domain_reputation_output_schema(valid_configuration_with_token):
    input_params = params.get('get_domain_reputation')[0].copy()
    schema = {}
    for operation in info_json.get("operations"):
        if operation.get('operation') == 'get_domain_reputation':
            if "conditional_output_schema" in operation or "api_output_schema" in operation:
                pytest.skip("Skipping test because conditional_output_schema or api_output_schema is not supported.")
            else:
                schema = operation.get('output_schema')
            break
    resp = operations['get_domain_reputation'](valid_configuration_with_token.copy(), input_params)
    if isinstance(schema, dict) and isinstance(resp, dict):
        logger.info("output_schema: {0}".format(schema))
        assert resp.keys() == schema.keys()
    else:
        pytest.skip("Skipping test because output_schema is not a dict.")
    

@pytest.mark.get_domain_reputation     
def test_get_domain_reputation_invalid_query(valid_configuration_with_token):
    input_params = params.get('get_domain_reputation')[0].copy()
    input_params['query'] = params.get('invalid_params')['text']
    with pytest.raises(ConnectorError):
        operations['get_domain_reputation'](valid_configuration_with_token.copy(), input_params)
    
