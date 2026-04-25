import argparse
import copy
import io
import os
import xml.etree.ElementTree as et


def _collect_codes_from_file(file_name):
    gcs5 = []
    gcs4 = []
    logs = []

    tree = et.parse(file_name)
    root = tree.getroot()

    if file_name.lower().endswith('.loc'):
        filt = 'name'
        for child in root.iter(filt):
            raw_id = child.get('id') or ''
            code = raw_id[2:] if raw_id.startswith('GC') else ''
            if len(code) == 5:
                gcs5.append(code)
            elif len(code) == 4:
                gcs4.append(code)
            elif code:
                logs.append(
                    f"Dropped {code}. Either your code is invalid or it is a very old cache "
                    '(Code length 3 or less) which this script does not consider.'
                )
    elif file_name.lower().endswith('.gpx'):
        xsi = root.tag[:-3]
        filt = xsi + 'name'
        for child in root.iter(filt):
            text = child.text or ''
            code = text[2:] if text[:2] == 'GC' else ''
            if len(code) == 5:
                gcs5.append(code)
            elif len(code) == 4:
                gcs4.append(code)
            elif code:
                logs.append(
                    f"Dropped {code}. Either your code is invalid or it is a very old cache "
                    '(Code length 3 or less) which this script does not consider.'
                )
    else:
        logs.append(f'Dropped {file_name}. Please give a .gpx or .loc file.')

    return tree, gcs5, gcs4, logs


def _remove_double_character_codes(codes):
    cleaned = list(set(codes))
    to_be_removed = []
    for gc in cleaned:
        if any(gc.count(c) - 1 for c in gc):
            to_be_removed.append(gc)
    for gc in to_be_removed:
        cleaned.remove(gc)
    return cleaned


def run(queries, write_routes=True, output_dir='.'):
    if not queries:
        raise ValueError('Please provide at least one .loc or .gpx file.')

    output = io.StringIO()
    gcs5 = []
    gcs4 = []
    base_tree = None

    for query in queries:
        if not os.path.exists(query):
            print(f'Dropped {query}. File not found.', file=output)
            continue

        tree, file_gcs5, file_gcs4, logs = _collect_codes_from_file(query)
        if base_tree is None and query.lower().endswith('.loc'):
            base_tree = tree

        gcs5.extend(file_gcs5)
        gcs4.extend(file_gcs4)
        for line in logs:
            print(line, file=output)

    print('Caches in all PQs:', len(gcs5) + len(gcs4), file=output)

    gcs5 = _remove_double_character_codes(gcs5)
    gcs4 = _remove_double_character_codes(gcs4)

    l5 = len(gcs5)
    l4 = len(gcs4)
    print('Caches without double characters:', l5 + l4, file=output)

    if l4 == 0:
        print('Progress: 100%', file=output)
        print('0 combinations found', file=output)
        return output.getvalue(), []

    combinations = []

    for i1 in range(l4):
        s = gcs4[i1]
        for i2 in range(i1, l4):
            if all(c not in s for c in gcs4[i2]):
                s += gcs4[i2]
                for i3 in range(i2, l4):
                    if all(c not in s for c in gcs4[i3]):
                        s += gcs4[i3]
                        for i4 in range(i3, l4):
                            if all(c not in s for c in gcs4[i4]):
                                s += gcs4[i4]
                                for i5 in range(l5):
                                    if all(c not in s for c in gcs5[i5]):
                                        s += gcs5[i5]
                                        for i6 in range(i5, l5):
                                            if all(c not in s for c in gcs5[i6]):
                                                s += gcs5[i6]
                                                for i7 in range(i6, l5):
                                                    if all(c not in s for c in gcs5[i7]):
                                                        s += gcs5[i7]
                                                        combinations.append([
                                                            gcs4[i1],
                                                            gcs4[i2],
                                                            gcs4[i3],
                                                            gcs4[i4],
                                                            gcs5[i5],
                                                            gcs5[i6],
                                                            gcs5[i7],
                                                        ])
                                                        s = s.replace(gcs5[i7], '')
                                                s = s.replace(gcs5[i6], '')
                                        s = s.replace(gcs5[i5], '')
                                s = s.replace(gcs4[i4], '')
                        s = s.replace(gcs4[i3], '')
                s = s.replace(gcs4[i2], '')

        progress = int((i1 + 1) / l4 * 100)
        print(f'Progress: {progress}%', file=output)

    print(f'{len(combinations)} combinations found', file=output)

    if write_routes and base_tree is not None:
        for i, combo in enumerate(combinations):
            route_tree = copy.deepcopy(base_tree)
            root = route_tree.getroot()
            for wp in root.findall('waypoint'):
                name = wp.find('name')
                if name is None or name.get('id') not in [f'GC{x}' for x in combo]:
                    root.remove(wp)
            route_tree.write(os.path.join(output_dir, f'Schmiederoute{i + 1}.loc'))

    return output.getvalue(), combinations


def main():
    parser = argparse.ArgumentParser(
        description='Finds seven caches fitting GC5C2AE from GPX or LOC files.'
    )
    parser.add_argument('queries', nargs='+', help='Input .loc and/or .gpx files')
    parser.add_argument(
        '--no-route-files',
        action='store_true',
        help='Do not write Schmiederoute*.loc output files',
    )
    args = parser.parse_args()

    output, _ = run(args.queries, write_routes=not args.no_route_files)
    print(output, end='')


if __name__ == '__main__':
    main()
