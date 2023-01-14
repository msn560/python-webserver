from http.server import BaseHTTPRequestHandler, HTTPServer
import time,io,os
import mimetypes

hostName = "localhost"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    html_file_path = os.path.dirname(os.path.abspath(__file__))+"/static"
    mimetype_ = "text/html"
    def do_GET(self):
        if "?" in self.path:
            sp = self.path.split("?")
            self.path= sp[0]
        if not "." in self.path:
            all = self.getHtml_Data(self.path+".html")
            if "404 not found" in all:
                return self.e404()
            return self.s200(all)
        else:
            all = self.getHtml_Data(self.path )
            if "404 not found" in all:
                return self.e404()
            return self.s200(all) 
    def e404(self):
        self.send_response(404)
        self.send_header("Content-type", self.mimetype_)
        self.end_headers()
        self.wfile.write(bytes("404 not found", "utf-8"))
        return
    def s200(self,data):
        self.send_response(200)
        self.send_header("Content-type", self.mimetype_)
        self.end_headers()
        self.wfile.write(bytes(data, "utf-8"))

    def getHtml_Data(self, fileName, default="404 not found"): 
        if not os.path.isfile(self.html_file_path  +fileName):
            return default
        f = io.open(self.html_file_path  +fileName,
                    mode="r", encoding="utf-8")
        self.mimetype_ = mimetypes.guess_type(self.html_file_path + fileName)[0]
        return f.read()

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort)) 
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")