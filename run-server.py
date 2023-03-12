from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import io
import os
import mimetypes

hostName = "localhost"
serverPort = 8080


class MyServer(BaseHTTPRequestHandler):
    html_file_path = os.path.dirname(os.path.abspath(__file__))+"/static"
    mimetype_ = "text/html"

    def do_GET(self):
        print("self.path", self.path)
        if "?" in self.path:
            sp = self.path.split("?")
            self.path = sp[0]
        if not "." in self.path:
            all = self.getHtml_Data(self.path+".html")
            if "404 not found" in all:
                return self.e404()
            return self.s200(all)
        else:
            all = self.getHtml_Data(self.path)
            if "image" in self.mimetype_:
                return self.s200(all)
            elif "404 not found" in all:
                return self.e404()
            return self.s200(all)

    def e404(self):
        self.send_response(404)
        self.send_header("Content-type", self.mimetype_)
        self.end_headers()
        self.wfile.write(bytes("404 not found", "utf-8"))
        return

    def s200(self, data):
        self.send_response(200)
        self.send_header("Content-type", self.mimetype_)
        self.end_headers()
        if "image" in self.mimetype_: 
            self.wfile.write(bytes(data))
        else:
            self.wfile.write(bytes(data, "utf-8"))

    def load_binary(self,filename):
        with open(filename, 'rb') as file_handle:
            return file_handle.read() 
    def getHtml_Data(self, fileName, default="404 not found"):
        if not os.path.isfile(self.html_file_path + fileName):
            return default
        self.mimetype_ = mimetypes.guess_type(
            self.html_file_path + fileName)[0]
        if "image" in self.mimetype_:
            return self.load_binary(self.html_file_path + fileName)
        f = io.open(self.html_file_path + fileName,
                    mode="r" )
         
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
