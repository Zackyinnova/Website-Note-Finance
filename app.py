import mysql.connector
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

# Koneksi ke database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="db_notefinance"
)

#halaman pertama yang di kunjungi
@app.route('/')
@app.route('/homepage')
def homepage():
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT COALESCE(SUM(amount_transcation), 0) AS total
        FROM submit_note
        WHERE YEAR(date_transaction) = YEAR(CURDATE())
          AND MONTH(date_transaction) = MONTH(CURDATE())
    """)
    result = cursor.fetchone()
    total_amount = result["total"] if result and result["total"] is not None else 0

    cursor.close()

    return render_template(
        'index.html',
        total_amount=total_amount
    )



#form submit note transaksi
@app.route('/submit_note', methods=['POST'])
def submitnote():
    type_transaction = request.form['type_transaction']
    desc_transcation = request.form['desc_transcation']
    amount_transcation = request.form['amount_transcation']
    date_transaction = request.form['date_transaction']
    catogory_transcation = request.form['catogory_transcation']

    cursor = db.cursor()
    cursor.execute(
        'INSERT INTO submit_note (type_transaction, desc_transcation, amount_transcation, date_transaction, catogory_transcation)'
        'VALUES (%s, %s, %s, %s, %s)',
        (type_transaction, desc_transcation, amount_transcation, date_transaction, catogory_transcation)
    )
    db.commit()
    cursor.close()

    return redirect(url_for('table'))

@app.route('/table')
def table():
    cursor = db.cursor(dictionary=True)

    # 1) Mengambil seluruh data
    cursor.execute("""
        SELECT
            type_transaction,
            desc_transcation,
            amount_transcation,
            date_transaction,
            catogory_transcation
        FROM submit_note
        ORDER BY date_transaction DESC
    """) 

    table_data = cursor.fetchall() 

    # 2) Total bulan ini (pakai filter YEAR dan MONTH)
    cursor.execute("""
        SELECT COALESCE(SUM(amount_transcation), 0) AS total
        FROM submit_note
        WHERE YEAR(date_transaction) = YEAR(CURDATE())
          AND MONTH(date_transaction) = MONTH(CURDATE())
    """)
    result = cursor.fetchone()
    total_amount = result["total"] if result and result["total"] is not None else 0

    #mengambil data income
    cursor.execute("""
    SELECT
        type_transaction,
        desc_transcation,
        amount_transcation,
        date_transaction,
        catogory_transcation
        FROM submit_note
        where type_transaction = 'income'
    """)
    income_trans = cursor.fetchall()

    #mengambil data pengeluaran
    cursor.execute("""
    SELECT
        type_transaction,
        desc_transcation,
        amount_transcation,
        date_transaction,
        catogory_transcation
        FROM submit_note
        where type_transaction = 'Expense'
    """)

    expense_trans = cursor.fetchall()

    #Mengambil data dengan harga tetinggi di bulan ini
    cursor.execute("""
    SELECT
        type_transaction,
        desc_transcation,
        amount_transcation,
        date_transaction,
        catogory_transcation
        FROM submit_note
        where type_transaction = 'Expense'
        ORDER BY amount_transcation DESC,
        date_transaction DESC;  
    """)

    Order_high = cursor.fetchall()

    cursor.execute("""
    SELECT
        type_transaction,
        desc_transcation,
        amount_transcation,
        date_transaction,
        catogory_transcation
        FROM submit_note
        where type_transaction = 'Expense'
        ORDER BY amount_transcation ASC,
        date_transaction DESC;  
    """)

    Order_low = cursor.fetchall()

    #bulan ini amount termahal
    cursor.execute("""
    SELECT
        type_transaction,
        desc_transcation,
        amount_transcation,
        date_transaction,
        catogory_transcation
        FROM submit_note
        where type_transaction = 'Expense'
        AND YEAR(date_transaction) = YEAR(CURDATE())
        AND MONTH(date_transaction) = MONTH(CURDATE())
        ORDER BY amount_transcation DESC;
    """)

    now_high = cursor.fetchall()

    #bulan ini amount termurah
    cursor.execute("""
    SELECT
        type_transaction,
        desc_transcation,
        amount_transcation,
        date_transaction,
        catogory_transcation
        FROM submit_note
        where type_transaction = 'Expense'
        AND YEAR(date_transaction) = YEAR(CURDATE())
        AND MONTH(date_transaction) = MONTH(CURDATE())
        ORDER BY amount_transcation ASC;
    """)

    now_low = cursor.fetchall()


    cursor.close()

    return render_template(
        'Table.html',
        table_data = table_data,
        total_amount = total_amount,
        income_trans = income_trans,
        expense_trans = expense_trans,
        Order_high = Order_high,
        Order_low = Order_low,
        now_high = now_high,
        now_low = now_low
    )

@app.route("/api/income-monthly")
def income_monthly():
    return jsonify(_monthly_sum("income"))

@app.route("/api/expense-monthly")
def expense_monthly():
    return jsonify(_monthly_sum("expense"))


def _monthly_sum(tipe):
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            DATE_FORMAT(date_transaction, '%Y-%m') AS bulan,
            COALESCE(SUM(amount_transcation), 0) AS total
        FROM submit_note
        WHERE date_transaction >= DATE_SUB(CURDATE(), INTERVAL 5 MONTH)
          AND type_transaction = %s
        GROUP BY bulan
        ORDER BY bulan ASC;
    """, (tipe,))
    result = cursor.fetchall()
    cursor.close()
    for r in result:
        r["total"] = float(r["total"] or 0)
    return result

@app.route("/api/type-cost")
def type_cost():
    return jsonify(get_cost_type())

def get_cost_type():
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT
            catogory_transcation AS category,
            COALESCE(SUM(amount_transcation), 0) AS total
        FROM submit_note
        WHERE YEAR(date_transaction) = YEAR(CURDATE())
          AND MONTH(date_transaction) = MONTH(CURDATE())
          AND type_transaction = 'expense'
          AND catogory_transcation IS NOT NULL
          AND catogory_transcation != ''
        GROUP BY catogory_transcation
        ORDER BY total DESC
    """)
    rows = cursor.fetchall()
    cursor.close()

    for r in rows:
        r["total"] = float(r["total"] or 0)

    return rows

@app.route('/chatbot')
def chatbot():
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT COALESCE(SUM(amount_transcation), 0) AS total
        FROM submit_note
        WHERE YEAR(date_transaction) = YEAR(CURDATE())
          AND MONTH(date_transaction) = MONTH(CURDATE())
    """)
    result = cursor.fetchone()
    total_amount = result["total"] if result and result["total"] is not None else 0

    cursor.close()

    return render_template(
        'Chatbot.html',
        total_amount = total_amount
    )



if __name__ == "__main__":
    app.run(debug=True)