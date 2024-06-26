import json
from datetime import datetime
from pytz import timezone, all_timezones, utc
from wsgiref.simple_server import make_server

def application(environ, start_response):
    path = environ.get('PATH_INFO', '').lstrip('/')
    method = environ['REQUEST_METHOD']

    if method == 'GET':
        if path in all_timezones or path == '':
            current_time = get_current_time(path)
            response_body = f"<html><body><h1>Current time in {path or 'GMT'}: {current_time}</h1></body></html>"
            status = '200 OK'
            headers = [('Content-type', 'text/html; charset=utf-8')]
        else:
            response_body = f"<html><body><h1>Timezone {path} not found</h1></body></html>"
            status = '404 Not Found'
            headers = [('Content-type', 'text/html; charset=utf-8')]

    elif method == 'POST':
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        except (ValueError):
            request_body_size = 0

        request_body = environ['wsgi.input'].read(request_body_size)
        data = json.loads(request_body.decode('utf-8'))

        if path == 'api/v1/convert':
            response_body = convert_time(data)
            status = '200 OK'
            headers = [('Content-type', 'application/json')]

        elif path == 'api/v1/datediff':
            response_body = date_difference(data)
            status = '200 OK'
            headers = [('Content-type', 'application/json')]

        else:
            response_body = json.dumps({'error': 'Invalid API endpoint'})
            status = '404 Not Found'
            headers = [('Content-type', 'application/json')]

    else:
        response_body = f"<html><body><h1>Method {method} not allowed</h1></body></html>"
        status = '405 Method Not Allowed'
        headers = [('Content-type', 'text/html; charset=utf-8')]

    start_response(status, headers)
    return [response_body.encode('utf-8')]

def get_current_time(tz_name):
    if tz_name == '':
        tz = utc
    else:
        tz = timezone(tz_name)
    return datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')

def convert_time(data):
    date_str = data.get('date', '')
    source_tz_name = data.get('tz', '')
    target_tz_name = data.get('target_tz', '')

    if not date_str or not source_tz_name or not target_tz_name:
        return json.dumps({'error': 'Missing required parameters'})

    try:
        source_tz = timezone(source_tz_name)
        target_tz = timezone(target_tz_name)
        source_date = datetime.strptime(date_str, '%m.%d.%Y %H:%M:%S')
        source_date = source_tz.localize(source_date)
        target_date = source_date.astimezone(target_tz)
        return json.dumps({'converted_date': target_date.strftime('%Y-%m-%d %H:%M:%S')})
    except Exception as e:
        return json.dumps({'error': str(e)})

def date_difference(data):
    first_date_str = data.get('first_date', '')
    first_tz_name = data.get('first_tz', '')
    second_date_str = data.get('second_date', '')
    second_tz_name = data.get('second_tz', '')

    if not first_date_str or not first_tz_name or not second_date_str or not second_tz_name:
        return json.dumps({'error': 'Missing required parameters'})

    try:
        first_tz = timezone(first_tz_name)
        second_tz = timezone(second_tz_name)
        first_date = first_tz.localize(datetime.strptime(first_date_str, '%m.%d.%Y %H:%M:%S'))
        second_date = second_tz.localize(datetime.strptime(second_date_str, '%I:%M%p %Y-%m-%d'))
        difference = (second_date - first_date).total_seconds()
        return json.dumps({'difference_in_seconds': difference})
    except Exception as e:
        return json.dumps({'error': str(e)})

if __name__ == '__main__':
    port = 8000
    httpd = make_server('localhost', port, application)
    print(f"Serving on port {port}...")
    httpd.serve_forever()
