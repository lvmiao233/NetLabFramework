def decode_probe(text, encodings=('utf8', 'ascii', 'latin1')):
    for encoding in encodings:
        try:
            decoded_body = text.decode(encoding=encoding, errors='ignore')
            return decoded_body
        except Exception as e:
            continue
    return ""