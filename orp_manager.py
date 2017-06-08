import AWSIoTClient
import datetime
import json
import ORPI2C
import sys
import time

_data_filename = 'orp_data.csv'
_error_log_filename = 'error_log'

def get_target_range():
    # TODO: get this from the config file/thing shadow
    return [-50,50]

def get_polling_interval():
    """Return the configured polling interval in seconds as a float."""
    # TODO: get this from the config file/thing shadow
    return 15.0 * 60.0  # minutes converted to seconds


def get_sensor_id():
    """Return the configured sensor_id as an integer."""
    # TODO: get this from the config file
    return '123456789'


def get_upload_interval():
    """Return the configured data file upload interval as a datetime.timedelta.

    The datetime.timedelta is an object representing the difference between two datetimes.
    """
    # TODO: get this from the config file
    #return datetime.timedelta(seconds=15.0)
    interval = 1.0
    return datetime.timedelta(hours=interval)


def _append_local_data(data):
    """Append the local data csv file.
    
    This function returns True if successful or False if the file could not be opened.
    """
    try:
        with open(_data_filename, 'a') as data_file:
            data_file.write(str(sensor_id) + ',' + str(data[0]) + ',' + str(data[1]) + '\n')
            return True
    except IOError:
        _update_error_log(datetime.datetime.now(),
                          ('Could not open the local data file', _data_filename, 'for appending.'))
        return False


def _clear_local_data():
    """Erase the contents of the local data csv file.
    
    This function returns True if successful or False if the file could not be opened.
    """
    try:
        open(_data_filename, 'w').close()
        return True
    except IOError:
        _update_error_log(datetime.datetime.now(),
                          ('Could not open the local data file', _data_filename, 'for clearing.'))
        return False


def _read_local_data():
    """Return the contents of the local data csv file as a list."""
    data = []
    try:
        with open(_data_filename, 'r') as data_file:
            for line in data_file:
                line = line.split(',')
                data.append(line)
    except IOError:
        _update_error_log(datetime.datetime.now(),
                          ('Could not open the local data file for reading', _data_filename, 'for reading.'))
    return data


def _update_cloud_database():
    """Send the contents of the local database to the cloud and clear the local database."""
    data = _read_local_data()
    counter = 0  # need to have unique keys for each entry for AWS Lambda service to recognize them
    message = '{'
    for line in data:
        message += '"entry' + str(counter) + '":"'
        message += line[0].strip() + ','   # sensor_id
        message += '' + line[1].strip() + ','   # timestamp
        message += '' + line[2].strip() + '",'  # reading
        counter += 1
    message = message[:-1]  # remove the last index (extra comma)
    message += '}'
    print message
    client.publish('DataUpload', message)
    _clear_local_data()

    return True

def _update_error_log(error_timestamp, message):
    """Format and display an error and append the local error log file."""
    error = '[' + str(error_timestamp) + '] ' + message + '\n'
    print 'ERROR', error

    try:
        with open(_error_log_filename, 'a') as log:
            log.write(error)
    except IOError:
        print 'Could not open the error log file', _error_log_filename


if __name__ == '__main__':
    # Load configuration parameters
    host = 'a31wvqhbklkbzd.iot.us-west-2.amazonaws.com'  # TODO - make configurable
    sensor_id = get_sensor_id()                          # TODO - maybe put in same file as host path
    polling_interval = get_polling_interval()
    upload_interval = get_upload_interval()
    
    # Read command-line arguments and initialize AWS Iot Client
    usage = 'Usage:  python orp_manager.py <sensor_id>'
    if len(sys.argv) < 2:
        print usage
        exit(1)
    else:
        client = AWSIoTClient.AWSIoTClient(host, 'root-CA.crt', sensor_id + '.cert.pem', sensor_id + '.private.key')
        client.connect()

        # TODO: These are for debug
        client.subscribe('DataUploadConfirmation')
        time.sleep(2)

    # Initialize ORP I2C Sensor
    orp_sensor = ORPI2C.Probe()

    last_upload = None
    while True:
        # Take a reading from the probe and save it to the local data file
        reading = orp_sensor.poll()
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        _append_local_data([timestamp,reading])
        print timestamp, reading

        # Upload data to the cloud database if the update interval has elapsed.
        if not last_upload or datetime.datetime.now() - last_upload > upload_interval:
            _update_cloud_database()
            last_upload = datetime.datetime.now()
            print 'Data published to cloud.'


        time.sleep(polling_interval)
