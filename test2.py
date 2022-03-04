import base64
import tempfile
import subprocess
import base64

with tempfile.NamedTemporaryFile(suffix='.txt') as tf:
    tf.write(base64.b64decode('SGVsbG8gU29uIE9mIEEgQml0Y2g='))
    tf.seek(0)
    with open(tf.name, 'r') as f:
        print(f.read())
    tf.close() 
