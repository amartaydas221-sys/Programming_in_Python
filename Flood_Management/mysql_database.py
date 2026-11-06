import json
import os
from datetime import date
from pathlib import Path

import mysql.connector


PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = PROJECT_DIR / "data"
DB_CONFIG = {
    "host": os.environ.get("FLOOD_DB_HOST", "127.0.0.1"),
    "port": int(os.environ.get("FLOOD_DB_PORT", "3306")),
    "user": os.environ.get("FLOOD_DB_USER", "root"),
    "password": os.environ.get("FLOOD_DB_PASSWORD", ""),
}
DB_NAME = os.environ.get("FLOOD_DB_NAME", "flood_management")
_initialized = False

TABLES = {
    "families": "families",
    "inventory": "inventory",
    "shelters": "shelters",
    "distribution": "distributions",
}
JSON_FILES = {
    "families": DATA_DIR / "families.json",
    "inventory": DATA_DIR / "inventory.json",
    "shelters": DATA_DIR / "shelters.json",
    "distribution": DATA_DIR / "distribution.json",
}

SCHEMA = (
    """CREATE TABLE IF NOT EXISTS migration_state (
        name VARCHAR(100) PRIMARY KEY
    )""",
    """CREATE TABLE IF NOT EXISTS families (
        familyId VARCHAR(100) PRIMARY KEY,
        headName VARCHAR(255) NOT NULL,
        phone VARCHAR(50) NOT NULL,
        district VARCHAR(255) NOT NULL,
        upazila VARCHAR(255) NOT NULL,
        village VARCHAR(255) NOT NULL,
        members INT NOT NULL,
        children INT NOT NULL DEFAULT 0,
        elderly INT NOT NULL DEFAULT 0,
        disabledMembers INT NOT NULL DEFAULT 0,
        damageLevel VARCHAR(30) NOT NULL,
        shelterNeeded BOOLEAN NOT NULL DEFAULT FALSE,
        receivedRelief BOOLEAN NOT NULL DEFAULT FALSE
    )""",
    """CREATE TABLE IF NOT EXISTS inventory (
        itemId VARCHAR(100) PRIMARY KEY,
        itemName VARCHAR(255) NOT NULL,
        quantity INT NOT NULL,
        unit VARCHAR(100) NOT NULL,
        minimumStock INT NOT NULL DEFAULT 0
    )""",
    """CREATE TABLE IF NOT EXISTS shelters (
        shelterId INT PRIMARY KEY,
        shelterName VARCHAR(255) NOT NULL,
        district VARCHAR(255) NOT NULL,
        capacity INT NOT NULL,
        currentOccupancy INT NOT NULL DEFAULT 0,
        families TEXT NOT NULL
    )""",
    """CREATE TABLE IF NOT EXISTS distributions (
        distributionId VARCHAR(30) PRIMARY KEY,
        date DATE NOT NULL,
        familyId VARCHAR(100) NOT NULL,
        headName VARCHAR(255) NOT NULL,
        package VARCHAR(50) NOT NULL
    )""",
    """CREATE TABLE IF NOT EXISTS distribution_items (
        id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        distributionId VARCHAR(30) NOT NULL,
        itemName VARCHAR(255) NOT NULL,
        quantity INT NOT NULL,
        unit VARCHAR(100) NOT NULL,
        FOREIGN KEY (distributionId) REFERENCES distributions(distributionId)
            ON DELETE CASCADE
    )""",
)


def _connect_server():
    return mysql.connector.connect(**DB_CONFIG)


def _connect():
    return mysql.connector.connect(**DB_CONFIG, database=DB_NAME)


def _rows(cursor):
    columns = [column[0] for column in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def initialize_database():
    global _initialized
    server = _connect_server()
    try:
        cursor = server.cursor()
        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` "
            "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        )
        server.commit()
    finally:
        server.close()

    connection = _connect()
    try:
        cursor = connection.cursor()
        for statement in SCHEMA:
            cursor.execute(statement)
        connection.commit()
    finally:
        connection.close()

    _migrate_json()
    _initialized = True


def _ensure_initialized():
    if not _initialized:
        initialize_database()


def _migrate_json():
    connection = _connect()
    try:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT 1 FROM migration_state WHERE name = %s",
            ("json_import_v1",),
        )
        if cursor.fetchone():
            return

        imported = {}
        for collection, path in JSON_FILES.items():
            if not path.exists():
                imported[collection] = []
                continue
            try:
                with path.open(encoding="utf-8") as file:
                    records = json.load(file)
            except (OSError, json.JSONDecodeError) as error:
                raise RuntimeError(
                    f"Could not import legacy data from {path}"
                ) from error
            if not isinstance(records, list):
                raise ValueError(f"Expected a list of records in {path}")
            imported[collection] = records

        for collection, records in imported.items():
            table = TABLES[collection]
            cursor.execute(f"SELECT COUNT(*) FROM `{table}`")
            if records and cursor.fetchone()[0] == 0:
                _replace_records(cursor, collection, records)

        cursor.execute(
            "INSERT INTO migration_state (name) VALUES (%s)",
            ("json_import_v1",),
        )
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def _replace_records(cursor, collection, records):
    if collection == "families":
        cursor.execute("DELETE FROM families")
        cursor.executemany(
            """INSERT INTO families (
                familyId, headName, phone, district, upazila, village,
                members, children, elderly, disabledMembers, damageLevel,
                shelterNeeded, receivedRelief
            ) VALUES (
                %(familyId)s, %(headName)s, %(phone)s, %(district)s,
                %(upazila)s, %(village)s, %(members)s, %(children)s,
                %(elderly)s, %(disabledMembers)s, %(damageLevel)s,
                %(shelterNeeded)s, %(receivedRelief)s
            )""",
            [
                {
                    **record,
                    "shelterNeeded": bool(record.get("shelterNeeded", False)),
                    "receivedRelief": bool(record.get("receivedRelief", False)),
                }
                for record in records
            ],
        )
    elif collection == "inventory":
        cursor.execute("DELETE FROM inventory")
        cursor.executemany(
            """INSERT INTO inventory (itemId, itemName, quantity, unit, minimumStock)
               VALUES (%(itemId)s, %(itemName)s, %(quantity)s, %(unit)s,
                       %(minimumStock)s)""",
            records,
        )
    elif collection == "shelters":
        cursor.execute("DELETE FROM shelters")
        cursor.executemany(
            """INSERT INTO shelters (
                shelterId, shelterName, district, capacity, currentOccupancy, families
            ) VALUES (
                %(shelterId)s, %(shelterName)s, %(district)s, %(capacity)s,
                %(currentOccupancy)s, %(families)s
            )""",
            [
                {
                    **record,
                    "families": json.dumps(record.get("families", [])),
                }
                for record in records
            ],
        )
    elif collection == "distribution":
        cursor.execute("DELETE FROM distribution_items")
        cursor.execute("DELETE FROM distributions")
        for record in records:
            cursor.execute(
                """INSERT INTO distributions (
                    distributionId, date, familyId, headName, package
                ) VALUES (%s, %s, %s, %s, %s)""",
                (
                    record["distributionId"],
                    record["date"],
                    record["familyId"],
                    record["headName"],
                    record["package"],
                ),
            )
            cursor.executemany(
                """INSERT INTO distribution_items (
                    distributionId, itemName, quantity, unit
                ) VALUES (%s, %s, %s, %s)""",
                [
                    (
                        record["distributionId"],
                        item["itemName"],
                        item["quantity"],
                        item["unit"],
                    )
                    for item in record.get("items", [])
                ],
            )


def load_records(collection):
    if collection not in TABLES:
        raise ValueError(f"Unknown data collection: {collection}")
    _ensure_initialized()
    connection = _connect()
    try:
        cursor = connection.cursor(dictionary=True)
        if collection == "distribution":
            cursor.execute(
                "SELECT * FROM distributions ORDER BY date, distributionId"
            )
            records = cursor.fetchall()
            for record in records:
                record["date"] = str(record["date"])
                cursor.execute(
                    """SELECT itemName, quantity, unit FROM distribution_items
                       WHERE distributionId = %s ORDER BY id""",
                    (record["distributionId"],),
                )
                record["items"] = cursor.fetchall()
            return records
        cursor.execute(f"SELECT * FROM `{TABLES[collection]}`")
        records = cursor.fetchall()
        if collection == "families":
            for record in records:
                record["shelterNeeded"] = bool(record["shelterNeeded"])
                record["receivedRelief"] = bool(record["receivedRelief"])
        elif collection == "shelters":
            for record in records:
                record["families"] = json.loads(record["families"])
        return records
    finally:
        connection.close()


def replace_records(collection, records):
    if collection not in TABLES:
        raise ValueError(f"Unknown data collection: {collection}")
    _ensure_initialized()
    connection = _connect()
    try:
        cursor = connection.cursor()
        _replace_records(cursor, collection, records)
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def get_families(search=""):
    connection = _connect()
    try:
        cursor = connection.cursor()
        if search:
            term = f"%{search}%"
            cursor.execute(
                """SELECT * FROM families
                   WHERE familyId LIKE %s OR headName LIKE %s
                      OR phone LIKE %s OR district LIKE %s
                   ORDER BY familyId""",
                (term, term, term, term),
            )
        else:
            cursor.execute("SELECT * FROM families ORDER BY familyId")
        return _rows(cursor)
    finally:
        connection.close()


def create_family(record):
    connection = _connect()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """INSERT INTO families (
                familyId, headName, phone, district, upazila, village,
                members, children, elderly, disabledMembers, damageLevel,
                shelterNeeded, receivedRelief
            ) VALUES (
                %(familyId)s, %(headName)s, %(phone)s, %(district)s, %(upazila)s,
                %(village)s, %(members)s, %(children)s, %(elderly)s,
                %(disabledMembers)s, %(damageLevel)s, %(shelterNeeded)s, FALSE
            )""",
            {**record, "shelterNeeded": record["shelterNeeded"] in (True, "yes")},
        )
        connection.commit()
    finally:
        connection.close()


def delete_family(family_id):
    connection = _connect()
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM families WHERE familyId = %s", (family_id,))
        connection.commit()
        return cursor.rowcount > 0
    finally:
        connection.close()


def get_inventory():
    connection = _connect()
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM inventory ORDER BY itemName")
        return _rows(cursor)
    finally:
        connection.close()


def create_inventory(record):
    connection = _connect()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """INSERT INTO inventory (itemId, itemName, quantity, unit, minimumStock)
               VALUES (%(itemId)s, %(itemName)s, %(quantity)s, %(unit)s,
                       %(minimumStock)s)""",
            record,
        )
        connection.commit()
    finally:
        connection.close()


def update_inventory(item_id, record):
    connection = _connect()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """UPDATE inventory SET quantity = %s, minimumStock = %s
               WHERE itemId = %s""",
            (record["quantity"], record["minimumStock"], item_id),
        )
        connection.commit()
        return cursor.rowcount > 0
    finally:
        connection.close()


def delete_inventory(item_id):
    connection = _connect()
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM inventory WHERE itemId = %s", (item_id,))
        connection.commit()
        return cursor.rowcount > 0
    finally:
        connection.close()


def get_shelters():
    connection = _connect()
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM shelters ORDER BY shelterId")
        shelters = _rows(cursor)
        for shelter in shelters:
            shelter["families"] = json.loads(shelter["families"])
        return shelters
    finally:
        connection.close()


def create_shelter(record):
    connection = _connect()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """INSERT INTO shelters (
                shelterId, shelterName, district, capacity, currentOccupancy, families
            ) VALUES (%s, %s, %s, %s, 0, '[]')""",
            (
                record["shelterId"],
                record["shelterName"],
                record["district"],
                record["capacity"],
            ),
        )
        connection.commit()
    finally:
        connection.close()


def update_shelter(shelter_id, record):
    connection = _connect()
    try:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT currentOccupancy FROM shelters WHERE shelterId = %s",
            (shelter_id,),
        )
        shelter = cursor.fetchone()
        if shelter is None or int(record["capacity"]) < shelter[0]:
            return False
        cursor.execute(
            """UPDATE shelters SET shelterName = %s, district = %s, capacity = %s
               WHERE shelterId = %s""",
            (
                record["shelterName"],
                record["district"],
                record["capacity"],
                shelter_id,
            ),
        )
        connection.commit()
        return cursor.rowcount > 0
    finally:
        connection.close()


def delete_shelter(shelter_id):
    connection = _connect()
    try:
        cursor = connection.cursor()
        cursor.execute(
            "DELETE FROM shelters WHERE shelterId = %s AND currentOccupancy = 0",
            (shelter_id,),
        )
        connection.commit()
        return cursor.rowcount > 0
    finally:
        connection.close()


def get_distributions():
    connection = _connect()
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM distributions ORDER BY date DESC, distributionId")
        records = _rows(cursor)
        for record in records:
            record["date"] = str(record["date"])
            cursor.execute(
                """SELECT itemName, quantity, unit FROM distribution_items
                   WHERE distributionId = %s ORDER BY id""",
                (record["distributionId"],),
            )
            record["items"] = _rows(cursor)
        return records
    finally:
        connection.close()


def distribute_relief(family_id, packages):
    _ensure_initialized()
    connection = _connect()
    try:
        connection.start_transaction()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM families WHERE familyId = %s FOR UPDATE",
            (family_id,),
        )
        family = cursor.fetchone()
        if family is None:
            raise ValueError("Family not found.")
        if family["receivedRelief"]:
            raise ValueError("This family has already received relief.")

        package_name = {
            "Low": "Small",
            "Medium": "Medium",
            "High": "Large",
            "Extreme": "Extreme",
        }.get(family["damageLevel"])
        if package_name is None:
            raise ValueError("The family's damage level is invalid.")

        package = packages[package_name]
        items = []
        for item_name, quantity in package.items():
            cursor.execute(
                """SELECT itemName, quantity, unit FROM inventory
                   WHERE itemName = %s COLLATE utf8mb4_unicode_ci FOR UPDATE""",
                (item_name,),
            )
            item = cursor.fetchone()
            if item is None:
                raise ValueError(f"{item_name} is not available in inventory.")
            if item["quantity"] < quantity:
                raise ValueError(f"There is not enough {item_name} in inventory.")
            items.append((item["itemName"], quantity, item["unit"]))

        for item_name, quantity, _ in items:
            cursor.execute(
                """UPDATE inventory SET quantity = quantity - %s
                   WHERE itemName = %s COLLATE utf8mb4_unicode_ci""",
                (quantity, item_name),
            )

        cursor.execute(
            """SELECT COALESCE(MAX(CAST(SUBSTRING(distributionId, 2) AS UNSIGNED)), 0) + 1
               AS next_id FROM distributions"""
        )
        distribution_id = f"D{cursor.fetchone()['next_id']:03}"
        cursor.execute(
            "UPDATE families SET receivedRelief = TRUE WHERE familyId = %s",
            (family_id,),
        )
        cursor.execute(
            """INSERT INTO distributions (
                distributionId, date, familyId, headName, package
            ) VALUES (%s, %s, %s, %s, %s)""",
            (
                distribution_id,
                date.today().isoformat(),
                family_id,
                family["headName"],
                package_name,
            ),
        )
        cursor.executemany(
            """INSERT INTO distribution_items (
                distributionId, itemName, quantity, unit
            ) VALUES (%s, %s, %s, %s)""",
            [
                (distribution_id, item_name, quantity, unit)
                for item_name, quantity, unit in items
            ],
        )
        connection.commit()
        return distribution_id, package_name
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def get_dashboard():
    connection = _connect()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """SELECT COUNT(*) AS family_count,
                      COALESCE(SUM(members), 0) AS people_count,
                      COALESCE(SUM(receivedRelief), 0) AS served_count
               FROM families"""
        )
        summary = _rows(cursor)[0]
        for key, query in (
            ("shelter_count", "SELECT COUNT(*) AS count FROM shelters"),
            ("inventory_count", "SELECT COUNT(*) AS count FROM inventory"),
            ("distribution_count", "SELECT COUNT(*) AS count FROM distributions"),
        ):
            cursor.execute(query)
            summary[key] = cursor.fetchone()[0]
        return summary
    finally:
        connection.close()


def get_reports():
    connection = _connect()
    try:
        cursor = connection.cursor()
        result = {}
        cursor.execute(
            """SELECT district, COUNT(*) AS count FROM families
               GROUP BY district ORDER BY district"""
        )
        result["by_district"] = _rows(cursor)
        cursor.execute(
            """SELECT damageLevel AS damage, COUNT(*) AS count FROM families
               GROUP BY damageLevel ORDER BY damageLevel"""
        )
        result["by_damage"] = _rows(cursor)
        return result
    finally:
        connection.close()
