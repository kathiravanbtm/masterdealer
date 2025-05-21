from flask import Flask, request, jsonify, send_file
import mysql.connector
import csv
import io
from flask_cors import CORS,cross_origin
from config import DB_CONFIG
import pandas as pd
from werkzeug.utils import secure_filename
from datetime import datetime



app = Flask(__name__)
CORS(app)


def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'OK'})

@app.route('/api/dealers', methods=['GET'])
def list_dealers():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM dealers LIMIT 10")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rows)


# @app.route('/api/dealers/upload_csv', methods=['POST'])
# def import_csv():
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file part'}), 400
#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({'error': 'No selected file'}), 400

#     stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
#     csv_input = csv.DictReader(stream)

#     conn = get_db_connection()
#     cursor = conn.cursor()

#     def get_bool_int(val):
#         if val is None:
#             return 0
#         val = str(val).strip().lower()
#         return 1 if val in ['yes', '1', 'true'] else 0

#     try:
#         for row in csv_input:
#             gstin = (row.get('GSTIN') or row.get('gstin') or '').strip()
#             if not gstin:
#                 # Skip rows without GSTIN or handle as you want
#                 continue

#             # Dealers table
#             cursor.execute("""
#                 INSERT INTO dealers
#                 (gstin, trade_name, email, mobile, assigned_to, reg_date, suspension_date,
#                  taxpayer_type, constitution, is_migrated, jurisdiction, hsn_code,
#                  principal_address, created_at, updated_at)
#                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
#                 ON DUPLICATE KEY UPDATE
#                     trade_name=VALUES(trade_name),
#                     email=VALUES(email),
#                     mobile=VALUES(mobile),
#                     assigned_to=VALUES(assigned_to),
#                     reg_date=VALUES(reg_date),
#                     suspension_date=VALUES(suspension_date),
#                     taxpayer_type=VALUES(taxpayer_type),
#                     constitution=VALUES(constitution),
#                     is_migrated=VALUES(is_migrated),
#                     jurisdiction=VALUES(jurisdiction),
#                     hsn_code=VALUES(hsn_code),
#                     principal_address=VALUES(principal_address),
#                     updated_at=NOW()
#             """, (
#                 gstin,
#                 (row.get('Trade Name/ Legal Name') or row.get('trade_name') or '').strip(),
#                 (row.get('Email Id') or row.get('email') or '').strip(),
#                 (row.get('Mobile No.') or row.get('mobile') or '').strip(),
#                 (row.get('Assigned To') or row.get('assigned_to') or '').strip(),
#                 (row.get('Effective Date of Registration') or row.get('reg_date') or '').strip(),
#                 row.get('Suspension Date') or None,
#                 (row.get('Type of Taxpayer') or row.get('taxpayer_type') or '').strip(),
#                 (row.get('Constitution of Business') or row.get('constitution') or '').strip(),
#                 int(row.get('IS_MIGRATED', '0').strip() or 0),
#                 (row.get('Lowest Jurisdiction') or row.get('jurisdiction') or '').strip(),
#                 (row.get('HSN Code') or row.get('hsn_code') or '').strip(),
#                 (row.get('Address of Principal Place of Business') or row.get('principal_address') or '').strip(),
#             ))

#             # Get dealer_id
#             cursor.execute("SELECT id FROM dealers WHERE gstin = %s", (gstin,))
#             dealer_id = cursor.fetchone()[0]

#             # Address details
#             cursor.execute("""
#                 INSERT INTO address_details
#                 (dealer_id, survey_no, door_no, booth_no, floor, street, road, nagar,
#                  village, taluk, district, pincode, landmark)
#                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#                 ON DUPLICATE KEY UPDATE
#                     survey_no=VALUES(survey_no),
#                     door_no=VALUES(door_no),
#                     booth_no=VALUES(booth_no),
#                     floor=VALUES(floor),
#                     street=VALUES(street),
#                     road=VALUES(road),
#                     nagar=VALUES(nagar),
#                     village=VALUES(village),
#                     taluk=VALUES(taluk),
#                     district=VALUES(district),
#                     pincode=VALUES(pincode),
#                     landmark=VALUES(landmark)
#             """, (
#                 dealer_id,
#                 (row.get('SurveyNo') or row.get('survey_no') or '').strip(),
#                 (row.get('doorNo') or row.get('door_no') or '').strip(),
#                 (row.get('boothNumber') or row.get('booth_no') or '').strip(),
#                 (row.get('floor') or '').strip(),
#                 (row.get('street') or '').strip(),
#                 (row.get('road') or '').strip(),
#                 (row.get('nagar') or '').strip(),
#                 (row.get('village') or '').strip(),
#                 (row.get('taluk') or '').strip(),
#                 (row.get('district') or '').strip(),
#                 (row.get('pincode') or '').strip(),
#                 (row.get('landmark') or '').strip(),
#             ))

#             # Bank details
#             cursor.execute("""
#                 INSERT INTO bank_details
#                 (dealer_id, bank_name, bank_address, branch, bank_email,
#                  account_number, account_name, accountant_phone, accountant_email)
#                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
#                 ON DUPLICATE KEY UPDATE
#                     bank_name=VALUES(bank_name),
#                     bank_address=VALUES(bank_address),
#                     branch=VALUES(branch),
#                     bank_email=VALUES(bank_email),
#                     account_number=VALUES(account_number),
#                     account_name=VALUES(account_name),
#                     accountant_phone=VALUES(accountant_phone),
#                     accountant_email=VALUES(accountant_email)
#             """, (
#                 dealer_id,
#                 (row.get('Bank Name') or row.get('bank_name') or '').strip(),
#                 (row.get('Bank Address') or row.get('bank_address') or '').strip(),
#                 (row.get('Bank Branch') or row.get('branch') or '').strip(),
#                 (row.get('Bank Email ID') or row.get('bank_email') or '').strip(),
#                 (row.get('Account Number') or row.get('account_number') or '').strip(),
#                 (row.get('Account Name') or row.get('account_name') or '').strip(),
#                 (row.get('Accountant Phone Number') or row.get('accountant_phone') or '').strip(),
#                 (row.get('bank mail id') or row.get('accountant_email') or '').strip(),
#             ))

#             # Field visit status
#             visited = get_bool_int(row.get('visited'))
#             cursor.execute("""
#                 INSERT INTO field_visit_status
#                 (dealer_id, visited, visit_date, notes)
#                 VALUES (%s, %s, NOW(), %s)
#                 ON DUPLICATE KEY UPDATE
#                     visited=VALUES(visited),
#                     visit_date=VALUES(visit_date),
#                     notes=VALUES(notes)
#             """, (
#                 dealer_id,
#                 visited,
#                 '',  # Customize if you have notes field in CSV
#             ))

#         conn.commit()
#     except Exception as e:
#         conn.rollback()
#         return jsonify({'error': str(e)}), 500
#     finally:
#         cursor.close()
#         conn.close()

#     return jsonify({'message': 'CSV imported successfully'})




@app.route('/api/dealers/upload_csv', methods=['POST'])
def import_csv():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    filename = secure_filename(file.filename)

    if filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Determine file type
    file_ext = filename.rsplit('.', 1)[-1].lower()

    try:
        if file_ext == 'csv':
            stream = io.StringIO(file.stream.read().decode("utf-8"), newline=None)
            records = list(csv.DictReader(stream))
        elif file_ext in ['xlsx', 'xls']:
            df = pd.read_excel(file, dtype=str)
            df = df.where(pd.notna(df), None)  # Replace NaN with None
            records = df.to_dict(orient='records')
        else:
            return jsonify({'error': 'Unsupported file format. Use .csv, .xls, or .xlsx'}), 400
    except Exception as e:
        return jsonify({'error': f'Failed to read file: {str(e)}'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    def get_str(val):
        return str(val).strip() if val is not None else ''

    def get_bool_int(val):
        val = str(val or '').strip().lower()
        return 1 if val in ['yes', '1', 'true'] else 0

    def safe_date(val):
        if not val or str(val).strip().lower() in ['nat', 'nan', 'none', '']:
            return None
        try:
            return str(pd.to_datetime(val).date())
        except Exception:
            return None

    try:
        for row in records:
            gstin = get_str(row.get('GSTIN') or row.get('gstin'))
            if not gstin:
                continue

            reg_date = safe_date(row.get('Effective Date of Registration') or row.get('reg_date'))
            susp_date = safe_date(row.get('Suspension Date'))

            cursor.execute("""
                INSERT INTO dealers
                (gstin, trade_name, email, mobile, assigned_to, reg_date, suspension_date,
                 taxpayer_type, constitution, is_migrated, jurisdiction, hsn_code,
                 principal_address, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
                ON DUPLICATE KEY UPDATE
                    trade_name=VALUES(trade_name),
                    email=VALUES(email),
                    mobile=VALUES(mobile),
                    assigned_to=VALUES(assigned_to),
                    reg_date=VALUES(reg_date),
                    suspension_date=VALUES(suspension_date),
                    taxpayer_type=VALUES(taxpayer_type),
                    constitution=VALUES(constitution),
                    is_migrated=VALUES(is_migrated),
                    jurisdiction=VALUES(jurisdiction),
                    hsn_code=VALUES(hsn_code),
                    principal_address=VALUES(principal_address),
                    updated_at=NOW()
            """, (
                gstin,
                get_str(row.get('Trade Name/ Legal Name') or row.get('trade_name')),
                get_str(row.get('Email Id') or row.get('email')),
                get_str(row.get('Mobile No.') or row.get('mobile')),
                get_str(row.get('Assigned To') or row.get('assigned_to')),
                reg_date,
                susp_date,
                get_str(row.get('Type of Taxpayer') or row.get('taxpayer_type')),
                get_str(row.get('Constitution of Business') or row.get('constitution')),
                get_bool_int(row.get('IS_MIGRATED', '0')),
                get_str(row.get('Lowest Jurisdiction') or row.get('jurisdiction')),
                get_str(row.get('HSN Code') or row.get('hsn_code')),
                get_str(row.get('Address of Principal Place of Business') or row.get('principal_address')),
            ))

            cursor.execute("SELECT id FROM dealers WHERE gstin = %s", (gstin,))
            result = cursor.fetchone()
            if not result:
                continue
            dealer_id = result[0]

            cursor.execute("""
                INSERT INTO address_details
                (dealer_id, survey_no, door_no, booth_no, floor, street, road, nagar,
                 village, taluk, district, pincode, landmark)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    survey_no=VALUES(survey_no),
                    door_no=VALUES(door_no),
                    booth_no=VALUES(booth_no),
                    floor=VALUES(floor),
                    street=VALUES(street),
                    road=VALUES(road),
                    nagar=VALUES(nagar),
                    village=VALUES(village),
                    taluk=VALUES(taluk),
                    district=VALUES(district),
                    pincode=VALUES(pincode),
                    landmark=VALUES(landmark)
            """, (
                dealer_id,
                get_str(row.get('SurveyNo') or row.get('survey_no')),
                get_str(row.get('doorNo') or row.get('door_no')),
                get_str(row.get('boothNumber') or row.get('booth_no')),
                get_str(row.get('floor')),
                get_str(row.get('street')),
                get_str(row.get('road')),
                get_str(row.get('nagar')),
                get_str(row.get('village')),
                get_str(row.get('taluk')),
                get_str(row.get('district')),
                get_str(row.get('pincode')),
                get_str(row.get('landmark')),
            ))

            cursor.execute("""
                INSERT INTO bank_details
                (dealer_id, bank_name, bank_address, branch, bank_email,
                 account_number, account_name, accountant_phone, accountant_email)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    bank_name=VALUES(bank_name),
                    bank_address=VALUES(bank_address),
                    branch=VALUES(branch),
                    bank_email=VALUES(bank_email),
                    account_number=VALUES(account_number),
                    account_name=VALUES(account_name),
                    accountant_phone=VALUES(accountant_phone),
                    accountant_email=VALUES(accountant_email)
            """, (
                dealer_id,
                get_str(row.get('Bank Name') or row.get('bank_name')),
                get_str(row.get('Bank Address') or row.get('bank_address')),
                get_str(row.get('Bank Branch') or row.get('branch')),
                get_str(row.get('Bank Email ID') or row.get('bank_email')),
                get_str(row.get('Account Number') or row.get('account_number')),
                get_str(row.get('Account Name') or row.get('account_name')),
                get_str(row.get('Accountant Phone Number') or row.get('accountant_phone')),
                get_str(row.get('bank mail id') or row.get('accountant_email')),
            ))

            visited = get_bool_int(row.get('visited'))
            cursor.execute("""
                INSERT INTO field_visit_status
                (dealer_id, visited, visit_date, notes)
                VALUES (%s, %s, NOW(), %s)
                ON DUPLICATE KEY UPDATE
                    visited=VALUES(visited),
                    visit_date=VALUES(visit_date),
                    notes=VALUES(notes)
            """, (
                dealer_id,
                visited,
                '',
            ))

        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

    return jsonify({'message': 'File imported successfully'})


@app.route('/api/dealers/<string:gstin>', methods=['GET'])
def get_dealer_with_bank(gstin):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Get dealer info
        cursor.execute("SELECT gstin, trade_name,mobile,taxpayer_type,assigned_to, jurisdiction, id FROM dealers WHERE gstin = %s", (gstin,))
        dealer = cursor.fetchone()
        if dealer is None:
            return jsonify({"error": "Dealer not found"}), 404
        dealer_id = dealer['id']
        # Get bank details
        cursor.execute("SELECT bank_name, bank_address, branch, bank_email, account_number, account_name, accountant_phone, accountant_email FROM bank_details WHERE dealer_id = %s", (dealer['id'],))
        bank = cursor.fetchone()
        
        # Combine
        dealer['bank_details'] = bank or {}
        
        return jsonify(dealer)
    finally:
        cursor.close()
        conn.close()


@app.route('/api/dealers/filter', methods=['GET'])
def filter_dealers():
    try:
        valid_keys = ['district', 'nagar', 'street', 'pincode']
        filters = {k: request.args.get(k) for k in valid_keys if request.args.get(k)}

        if not filters:
            return jsonify({"error": "No filter parameters provided"}), 400

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Build dynamic WHERE clause with OR
        where_clauses = []
        values = []
        for key, value in filters.items():
            where_clauses.append(f"a.{key} = %s")
            values.append(value)
        where_sql = " OR ".join(where_clauses)

        # JOIN query to get data from both tables
        query = f"""
            SELECT 
                d.gstin, d.trade_name, d.mobile,
                a.survey_no, a.door_no, a.booth_no, a.floor,
                a.street, a.road, a.nagar, a.village, a.taluk,
                a.district, a.pincode, a.landmark, d.jurisdiction
            FROM dealers d
            JOIN address_details a ON d.id = a.dealer_id
            WHERE {where_sql}
        """
        cursor.execute(query, tuple(values))
        result = cursor.fetchall()

        return jsonify(result)

    except Exception as e:
        print(f"Filter Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()


@app.route('/api/dealers/<gstin>/visit', methods=['POST'])
def update_visit_status(gstin):
    data = request.json
    visited = data.get('visited')

    if visited is None:
        return jsonify({'error': 'Missing "visited" field'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE dealers SET visited = %s WHERE gstin = %s", (int(visited), gstin))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'Visit status updated'})



@app.route('/api/suggestions/districts')
def suggest_districts():
    query = request.args.get('q', '').lower()
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Get distinct districts from DB
        cursor.execute("SELECT DISTINCT district FROM address_details WHERE district IS NOT NULL")
        all_districts = [row[0] for row in cursor.fetchall() if row[0]]

        # Filter based on query
        suggestions = [district for district in all_districts if query in district.lower()]
        return jsonify(suggestions)
    except Exception as e:
        print(f"District suggestion error: {str(e)}")
        return jsonify({'error': 'Unable to fetch suggestions'}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/api/suggestions/nagar')
def suggest_nagar():
    query = request.args.get('q', '').lower()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT nagar 
        FROM address_details 
        WHERE nagar LIKE %s
        LIMIT 20
    """, (query + '%',))
    results = [row[0] for row in cursor.fetchall() if row[0]]
    cursor.close()
    conn.close()
    return jsonify(results)

@app.route('/api/suggestions/street')
def suggest_street():
    query = request.args.get('q', '').lower()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT street 
        FROM address_details 
        WHERE street LIKE %s
        LIMIT 20
    """, (query + '%',))
    results = [row[0] for row in cursor.fetchall() if row[0]]
    cursor.close()
    conn.close()
    return jsonify(results)


@app.route('/api/districts/other')
def other_districts():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT d.gstin, d.trade_name, a.district
        FROM dealers d
        JOIN address_details a ON d.id = a.dealer_id
        WHERE LOWER(a.district) != %s
    """, ('thiruvannamalai',))

    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(results)

@app.route('/api/export/dealers', methods=[ 'POST'])
def export_filtered_dealers():
    # 1) Preflight: respond with 204 + CORS headers
    if request.method == 'OPTIONS':
        return ('', 204)

    filters = request.json or {}
    print(filters)

    # 1) Build the SELECT with explicit column order + window for Sr.No
    query = """
        SELECT
            ROW_NUMBER() OVER (ORDER BY d.gstin)               AS `Sr.No`,
            d.gstin                                            AS `GSTIN`,
            d.trade_name                                       AS `Trade Name/ Legal Name`,
            d.email                                            AS `Email Id`,
            d.mobile                                           AS `Mobile No.`,
            d.assigned_to                                      AS `Assigned To`,
            d.reg_date                                         AS `Effective Date of Registration`,
            d.suspension_date                                  AS `Suspension Date`,
            d.taxpayer_type                                    AS `Type of Taxpayer`,
            d.constitution                                     AS `Constitution of Business`,
            d.is_migrated                                      AS `IS_MIGRATED`,
            d.jurisdiction                                     AS `Lowest Jurisdiction`,
            d.hsn_code                                         AS `HSN Code`,
            d.principal_address                                AS `Address of Principal Place of Business`,
            # a.additional_place_count                           AS `No. of Additional Place of Business`,
            a.survey_no                                        AS `SurveyNo`,
            a.door_no                                          AS `doorNo`,
            a.booth_no                                         AS `boothNumber`,
            a.floor                                            AS `floor`,
            a.street                                           AS `street`,
            a.road                                             AS `road`,
            a.nagar                                            AS `nagar`,
            a.village                                          AS `village`,
            a.taluk                                            AS `taluk`,
            a.district                                         AS `district`,
            a.pincode                                          AS `pincode`,
            a.landmark                                         AS `landmark`,
            b.bank_name                                        AS `Bank Name`,
            b.bank_address                                     AS `Bank Address`,
            b.branch                                           AS `Bank Branch`,
            b.bank_email                                       AS `Bank Email ID`,
            b.account_number                                   AS `Account Number`,
            b.account_name                                     AS `Account Name`,
            b.accountant_phone                                 AS `Accountant Phone Number`,
            b.accountant_email                                 AS `accountant mail id`
        FROM dealers d
        LEFT JOIN address_details a ON d.id = a.dealer_id
        LEFT JOIN bank_details   b ON d.id = b.dealer_id
        WHERE 1=1
    """

    clauses = []
    params  = []

    if 'gstin' in filters:
        clauses.append("d.gstin = %s")
        params.append(filters['gstin'])

    if 'district' in filters:
        clauses.append("LOWER(a.district) = %s")
        params.append(filters['district'].lower())

    if 'exclude_district' in filters:
        clauses.append("LOWER(a.district) != %s")
        params.append(filters['exclude_district'].lower())

    if 'street' in filters:
        clauses.append("LOWER(a.street) = %s")
        params.append(filters['street'].lower())

    if 'nagar' in filters:
        clauses.append("LOWER(a.nagar) = %s")
        params.append(filters['nagar'].lower())

    if 'pincode' in filters:
        clauses.append("a.pincode = %s")
        params.append(filters['pincode'])

    # 2) Attach them with OR (any‐match)
    if clauses:
        query += " AND (" + " OR ".join(clauses) + ")"



    # 4) Run query and fetch
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    if not rows:
        return jsonify({"message": "No dealers found matching filters."}), 404

    # 5) Build DataFrame and write to Excel
    df = pd.DataFrame(rows)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Dealers')
        ws = writer.sheets['Dealers']
        # auto‐size columns:
        for idx, col in enumerate(df.columns):
            max_len = max(df[col].astype(str).map(len).max(), len(col))
            ws.set_column(idx, idx, min(max_len + 2, 40))

    output.seek(0)
    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name='filtered_dealers.xlsx'
    )


if __name__ == '__main__':
    app.run(debug=True)