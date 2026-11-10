"""Check the manuscript's tabular figure data with the Python standard library."""
from pathlib import Path
import csv
import hashlib
import math
import statistics

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'source_data'


def read_csv(path):
    with path.open(encoding='utf-8-sig', newline='') as stream:
        return list(csv.DictReader(stream))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    manifest = read_csv(ROOT / 'MANIFEST_SHA256.csv')
    for item in manifest:
        path = ROOT / item['path']
        require(path.is_file(), 'Missing file ' + item['path'])
        require(hashlib.sha256(path.read_bytes()).hexdigest() == item['sha256'], 'File changed ' + item['path'])
    main_rows = read_csv(DATA / 'main_endpoints.csv')
    keys = [(r['dataset'], r['method'], r['task_id'], r['seed']) for r in main_rows]
    require(len(main_rows) == len(set(keys)) == 270, 'Expected 270 unique primary endpoints')
    values = {key: float(row['DAT_macro_f1']) for key, row in zip(keys, main_rows)}
    for row in read_csv(DATA / 'main_method_comparison.csv'):
        scores = [float(r['DAT_macro_f1']) for r in main_rows if r['dataset'] == row['dataset'] and r['method'] == row['method']]
        expected_count = 36 if row['dataset'] == 'Pump' else 18
        require(len(scores) == expected_count, 'Incomplete main comparison')
        require(abs(statistics.mean(scores) * 100 - float(row['manuscript_percent'])) < 0.0051, 'Main mean mismatch')
    for filename, dataset in [('pump_endpoints.csv', 'Pump'), ('rotor_endpoints.csv', 'Rotor')]:
        for row in read_csv(DATA / filename):
            matches = [r for r in main_rows if r['dataset'] == dataset and r['method'] == row['method'] and r['seed'] == row['seed'] and r['target_domain'] == row['target_domain']]
            require(len(matches) == 1, 'Figure endpoint mapping mismatch')
            require(math.isclose(float(row['target_DAT']), float(matches[0]['DAT_macro_f1']), abs_tol=1e-12), 'Figure score mismatch')
    for row in read_csv(DATA / 'pump_paired.csv'):
        full = values[('Pump', 'DARM_FULL', row['task_id'], row['seed'])]
        calibrated = values[('Pump', 'DARM_PP025', row['task_id'], row['seed'])]
        for name, expected in [('DARM_FULL', full), ('DARM_PP025', calibrated), ('delta', calibrated-full)]:
            require(math.isclose(float(row[name]), expected, abs_tol=1e-12), 'Paired data mismatch')
    components = read_csv(DATA / 'pump_component_calibration.csv')
    require(len(components) == 192 and len({(r['method'],r['task_id'],r['seed']) for r in components}) == 192, 'Expected 192 unique component/calibration endpoints')
    expected_components = {(30,'DARM_IP_ONLY'):48.10, (30,'DARM_IP_II'):62.04, (30,'DARM_FULL'):60.88, (40,'DARM_IP_II'):41.30, (40,'DARM_FULL'):43.06}
    for (speed, method), expected in expected_components.items():
        scores = [float(r['DAT_macro_f1']) for r in components if int(r['speed']) == speed and r['method'] == method]
        require(len(scores) == 12, 'Incomplete Figure 4 group')
        require(abs(statistics.mean(scores)*100 - expected) < 0.0051, 'Figure 4 mean mismatch')
    for row in read_csv(DATA / 'coefficient_comparison.csv'):
        scores = [float(r['DAT_macro_f1']) for r in components if r['method'] == row['method']]
        require(len(scores) == 36, 'Incomplete coefficient group')
        require(math.isclose(statistics.mean(scores), float(row['DAT_mean']), abs_tol=1e-12), 'Coefficient mean mismatch')
    print('PASS: file hashes, 270 primary endpoint scores, 192 component/calibration scores, main comparison means, and figure source data.')
    print('This checks supplied numeric CSVs. It does not execute model inference or training.')


if __name__ == '__main__':
    main()
