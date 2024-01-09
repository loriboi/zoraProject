from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from gpt import apiCall

hostName = ''
# hostName = 'localhost'
serverPort = 12345

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes('Ciao a tutti'))

    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        content_len = int(self.headers.get('content-length'))
        post_body = self.rfile.read(content_len)
        
        try:
            request_data = json.loads(post_body.decode('utf-8'))
            if 'question' in request_data:
                question = request_data['question']
                ans = apiCall(question)
                print("Server 1",ans)
                response_data = {'answer': ans}
                self.wfile.write(json.dumps(response_data).encode('utf-8'))
            else:
                self.wfile.write("Richiesta non valida".encode('utf-8'))
        except json.JSONDecodeError as e:
            self.wfile.write(f"Errore nella richiesta: {str(e)}".encode('utf-8'))    

if __name__ == '__main__':
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    webServer.serve_forever()