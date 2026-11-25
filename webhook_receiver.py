from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class WebhookHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        body = self.rfile.read(content_length)

        data = json.loads(body.decode("utf-8"))

        print("\n=== BUDGET WEBHOOK RECEIVED ===")
        print(json.dumps(data, indent=4, ensure_ascii=False))

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        response = {"status": "received"}
        self.wfile.write(json.dumps(response).encode("utf-8"))


server = HTTPServer(("127.0.0.1", 9000), WebhookHandler)

print("Webhook server is running on http://127.0.0.1:9000")

server.serve_forever()
