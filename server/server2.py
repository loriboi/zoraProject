from http.server import BaseHTTPRequestHandler, HTTPServer
from gpt import speechToText
from reduce_noise import reduceNoise
from base64 import b64decode
import unicodedata

hostName=''

# hostName = 'localhost'
serverPort = 12346

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes('Ciao a tutti'))

    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json; charset=utf-8")
        self.end_headers()
        content_len = int(self.headers.get('content-length'))
        post_body = self.rfile.read(content_len)

        audioFileEnc = eval(post_body)['file']
        audioFileDec = b64decode(audioFileEnc)

        wav_file = open("temp.m4a", "wb")
       
        wav_file.write(audioFileDec)
        wav_file.close()

        wav_file_red = reduceNoise('temp.m4a')
        
        wav_file = open(wav_file_red, "rb")

        text = speechToText(wav_file)
        
        print("Server 2",text)
        self.wfile.write(text.encode())
        
        

if __name__ == '__main__':
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    webServer.serve_forever()
        

