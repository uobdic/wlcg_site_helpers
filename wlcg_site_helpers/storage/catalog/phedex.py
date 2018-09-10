import requests
import six
from units import predefined, unit

predefined.define_computer_units()


def get_subscriptions(site, since=1481500800, phedex_instance='prod'):
    params = [
        ('create_since', since),
        ('node', site),
    ]
    query = _construct_query('subscriptions', params, phedex_instance)
    r = requests.get(query, verify=False)
    result = r.json()
    return _extract_dataset_info(result, site, phedex_instance)


def _construct_query(what, params, phedex_instance):
    phedex_api = 'https://cmsweb.cern.ch/phedex/datasvc/json'
    query = '{base}/{instance}/{what}'.format(
        base=phedex_api,
        instance=phedex_instance,
        what=what,
    )
    if params:
        query += '?' + _params_to_string(params)
    return query


def _params_to_string(params):
    '''
        Take a list of tuples and convert into query string
    '''
    tmp = ['{0}={1}'.format(k, v) for (k, v) in params]
    return '&'.join(tmp)


def _extract_dataset_info(result, site, phedex_instance):
    datasets = result['phedex']['dataset']
    retain = ['files', 'name', 'bytes', 'subscription']
    for dataset in datasets:
        subscription = None
        if 'block' in dataset:
            # block types have 1 or more blocks, each with a subscription
            subscription = dataset['block'][0]['subscription'][0]
        else:
            subscription = dataset['subscription'][0]
        dataset = _clean_dictionary(dataset, retain)
        dataset.update(
            _summarise_subscription(subscription, site, phedex_instance)
        )
        if 'subscription' in dataset:
            del dataset['subscription']
        dataset['bytes_raw'] = dataset['bytes']
        dataset['bytes'] = unit('B')(dataset['bytes'])
    return datasets


def _clean_dictionary(dictionary, keys_to_retain):
    unwanted = set(dictionary) - set(keys_to_retain)
    for unwanted_key in unwanted:
        del dictionary[unwanted_key]
    return dictionary


def _summarise_subscription(subscription, site, phedex_instance):
    retain = ['percent_files', 'time_create', 'group', 'request']
    subscription = _clean_dictionary(subscription, retain)

    request_id = subscription['request']
    request = _get_transfer_request_for_site(request_id, site, phedex_instance)
    subscription.update(request)
    subscription['request_id'] = request_id
    del subscription['request']

    return subscription


def _get_transfer_request_for_site(request_id, site, phedex_instance):
    request_id = str(request_id)
    params = [
        ('request', request_id),
        ('node', site),
    ]
    query = _construct_query('transferrequests', params, phedex_instance)
    r = requests.get(query, verify=False, params=params)
    result = r.json()['phedex']['request'][0]

    result['requested_by'] = _clean_dictionary(
        result['requested_by'], ['name', 'dn', 'email'])
    result = _clean_dictionary(result, ['time_create', 'requested_by'])
    # flatten result
    for k, v in six.iteritems(result['requested_by']):
        result['requested_by_' + k] = v
    del result['requested_by']
    return result
