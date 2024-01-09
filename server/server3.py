from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from movement import IdentificaAzioneFirst


# hostName = 'localhost'
serverPort = 12347
hostName = ''
class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes('Ciao a tutti'))

    def do_POST(self):
        try:
            content_len = int(self.headers.get('content-length'))
            post_body = self.rfile.read(content_len)
            post_data = json.loads(post_body)
            question = post_data.get('sentence', '')
            
            if question:
                print(question)
                ans = IdentificaAzioneFirst(question)
                response = {"response":ans}
            else:
                response = {'error': 'Missing or invalid question'}
        except Exception as e:
            response = {'error': str(e)}
        
        response_json = json.dumps(response)
        print("Server 3",response)
        
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(response_json.encode())

if __name__ == '__main__':
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    webServer.serve_forever()