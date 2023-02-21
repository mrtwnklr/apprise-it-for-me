import importlib
import re
from flask import abort

class ConverterLoader:
    def load(source):
        if not re.match(r'^[a-z0-9-]+$', source):
            abort(400, description='Invalid source key: ' + source)

        try:
            converterModule = importlib.import_module("{}.{}".format(__package__, source), __name__)
        except:
            abort(404, description='Cannot find converter for source key: ' + source)

        converterClass = getattr(converterModule, source.title() + 'Converter')
        converter = converterClass()

        return converter
