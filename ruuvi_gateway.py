from datetime import datetime
from ruuvitag_sensor.ruuvi import RuuviTagSensor
from google.cloud import firestore

SCAN_TIMEOUT = 4

db = firestore.Client()

measurements_ref = db.collection(u'measurements')

timestamp = datetime.now()

def measurement_to_firestore(mac, payload):
    result = payload.copy()
    result["mac"] = mac
    result["timestamp"] = timestamp
    return result

datas = RuuviTagSensor.get_data_for_sensors(None, SCAN_TIMEOUT)
for mac, payload in datas.items():
    value = measurement_to_firestore(mac, payload)
    measurements_ref.add(value)
    print('[{0}] Measurement added for {1}'.format(timestamp.strftime('%Y-%m-%d %H:%M:%S'), mac))

