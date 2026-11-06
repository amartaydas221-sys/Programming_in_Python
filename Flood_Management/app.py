import json
import mimetypes
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlsplit

import mysql.connector

import mysql_database as database
from relief_distribution import relief_package


HOST = "127.0.0.1"
PORT = 8000
PROJECT_DIR = Path(__file__).resolve().parent
MAX_REQUEST_SIZE = 1_000_000


class FloodManagementHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlsplit(self.path)
        if parsed.path.startswith("/api/"):
            self._get_api(parsed.path, parse_qs(parsed.query))
            return
        self._serve_static(parsed.path)

    def do_POST(self):
        parsed = urlsplit(self.path)
        if not parsed.path.startswith("/api/"):
            self._send_json({"error": "Not found."}, 404)
            return
        self._write_api("POST", parsed.path)

    def do_PUT(self):
        parsed = urlsplit(self.path)
        if not parsed.path.startswith("/api/"):
            self._send_json({"error": "Not found."}, 404)
            return
        self._write_api("PUT", parsed.path)

    def do_DELETE(self):
        parsed = urlsplit(self.path)
        if not parsed.path.startswith("/api/"):
            self._send_json({"error": "Not found."}, 404)
            return
        self._write_api("DELETE", parsed.path)

    def _get_api(self, path, query):
        try:
            if path == "/api/families":
                result = database.get_families(query.get("q", [""])[0].strip())
            elif path == "/api/inventory":
                result = database.get_inventory()
            elif path == "/api/shelters":
                result = database.get_shelters()
            elif path == "/api/distributions":
                result = database.get_distributions()
            elif path == "/api/dashboard":
                result = database.get_dashboard()
            elif path == "/api/reports":
                result = database.get_reports()
            else:
                self._send_json({"error": "Not found."}, 404)
                return
            self._send_json(result)
        except mysql.connector.Error:
            self.log_error("Database request failed: %s", self.path)
            self._send_json(
                {"error": "Could not read the database. Check that XAMPP MySQL is running."},
                503,
            )

    def _write_api(self, method, path):
        try:
            data = self._read_json() if method in ("POST", "PUT") else {}
            parts = [unquote(part) for part in path.strip("/").split("/")]

            if parts == ["api", "families"] and method == "POST":
                self._require_fields(
                    data,
                    (
                        "familyId", "headName", "phone", "district", "upazila",
                        "village", "members", "children", "elderly",
                        "disabledMembers", "damageLevel", "shelterNeeded",
                    ),
                )
                database.create_family(data)
                self._send_json({"message": "Family registered."}, 201)
            elif len(parts) == 3 and parts[:2] == ["api", "families"] and method == "DELETE":
                if not database.delete_family(parts[2]):
                    raise LookupError("Family not found.")
                self._send_json({"message": "Family deleted."})
            elif parts == ["api", "inventory"] and method == "POST":
                self._require_fields(data, ("itemId", "itemName", "quantity", "unit", "minimumStock"))
                database.create_inventory(data)
                self._send_json({"message": "Inventory item added."}, 201)
            elif len(parts) == 3 and parts[:2] == ["api", "inventory"]:
                if method == "PUT":
                    self._require_fields(data, ("quantity", "minimumStock"))
                    changed = database.update_inventory(parts[2], data)
                elif method == "DELETE":
                    changed = database.delete_inventory(parts[2])
                else:
                    self._send_json({"error": "Method not allowed."}, 405)
                    return
                if not changed:
                    raise LookupError("Inventory item not found.")
                self._send_json({"message": "Inventory updated."})
            elif parts == ["api", "shelters"] and method == "POST":
                self._require_fields(data, ("shelterId", "shelterName", "district", "capacity"))
                database.create_shelter(data)
                self._send_json({"message": "Shelter added."}, 201)
            elif len(parts) == 3 and parts[:2] == ["api", "shelters"]:
                if method == "PUT":
                    self._require_fields(data, ("shelterName", "district", "capacity"))
                    changed = database.update_shelter(parts[2], data)
                    if not changed:
                        raise ValueError(
                            "Shelter not found, or capacity is less than current occupancy."
                        )
                elif method == "DELETE":
                    changed = database.delete_shelter(parts[2])
                    if not changed:
                        raise ValueError(
                            "Shelter not found or it still has families allocated."
                        )
                else:
                    self._send_json({"error": "Method not allowed."}, 405)
                    return
                self._send_json({"message": "Shelter updated."})
            elif parts == ["api", "distributions"] and method == "POST":
                self._require_fields(data, ("familyId",))
                distribution_id, package = database.distribute_relief(
                    str(data["familyId"]),
                    relief_package(),
                )
                self._send_json(
                    {
                        "message": f"{package} relief package distributed.",
                        "distributionId": distribution_id,
                    },
                    201,
                )
            else:
                self._send_json({"error": "Not found."}, 404)
        except (ValueError, TypeError, KeyError) as error:
            self._send_json({"error": str(error)}, 400)
        except LookupError as error:
            self._send_json({"error": str(error)}, 404)
        except mysql.connector.IntegrityError as error:
            self._send_json(
                {"error": f"That ID already exists or is referenced by other data: {error}"},
                409,
            )
        except mysql.connector.Error:
            self.log_error("Database request failed: %s", self.path)
            self._send_json(
                {"error": "Could not update the database. Check that XAMPP MySQL is running."},
                503,
            )

    def _read_json(self):
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError as error:
            raise ValueError("Invalid request length.") from error
        if length <= 0 or length > MAX_REQUEST_SIZE:
            raise ValueError("Request body is missing or too large.")
        try:
            data = json.loads(self.rfile.read(length))
        except (json.JSONDecodeError, UnicodeDecodeError) as error:
            raise ValueError("Request body must be valid JSON.") from error
        if not isinstance(data, dict):
            raise ValueError("Request body must be a JSON object.")
        return data

    @staticmethod
    def _require_fields(data, fields):
        missing = [field for field in fields if field not in data]
        if missing:
            raise ValueError(f"Missing required fields: {', '.join(missing)}")

    def _serve_static(self, request_path):
        relative = unquote(request_path).lstrip("/")
        if not relative:
            relative = "index.html"
        relative_path = Path(relative)
        is_index = relative_path.parts == ("index.html",)
        is_static = bool(relative_path.parts) and relative_path.parts[0] == "static"
        if not is_index and not is_static:
            self.send_error(404, "File not found.")
            return
        target = (PROJECT_DIR / relative_path).resolve()
        if (
            not target.is_relative_to(PROJECT_DIR)
            or not target.is_file()
            or (is_static and not target.is_relative_to(PROJECT_DIR / "static"))
        ):
            self.send_error(404, "File not found.")
            return
        content_type = mimetypes.guess_type(target.name)[0] or "application/octet-stream"
        body = target.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_json(self, payload, status=200):
        body = json.dumps(payload, ensure_ascii=False, default=str).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format_string, *args):
        print(f"{self.address_string()} - {format_string % args}")


def main():
    try:
        database.initialize_database()
    except mysql.connector.Error as error:
        raise SystemExit(
            "Could not connect to XAMPP MySQL. Start MySQL in the XAMPP Control "
            "Panel and check FLOOD_DB_HOST, FLOOD_DB_PORT, FLOOD_DB_USER, and "
            "FLOOD_DB_PASSWORD."
        ) from error
    server = ThreadingHTTPServer((HOST, PORT), FloodManagementHandler)
    print(f"Flood Management is running at http://{HOST}:{PORT}")
    print("Press Ctrl+C to stop the server.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Flood Management server.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
