import os
import io
from flask import Flask, request, jsonify, send_from_directory, send_file
from data_fetcher import extract_company_data
from create_excel_model import create_reverse_dcf_workbook

app = Flask(__name__, static_folder=".")

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(".", filename)

@app.route("/api/fetch", methods=["GET"])
def api_fetch():
    query = request.args.get("query", "").strip()
    if not query:
        return jsonify({"success": False, "error": "Query parameter is required"}), 400
        
    try:
        data = extract_company_data(query)
        # Update the live downloadable Excel file with this company's exact data
        create_reverse_dcf_workbook("Reverse_DCF_Model.xlsx", data)
        ticker_file = f"Reverse_DCF_{data['ticker'].replace('/', '_')}.xlsx"
        create_reverse_dcf_workbook(ticker_file, data)
        data['download_filename'] = ticker_file
        return jsonify({"success": True, "data": data})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/export", methods=["POST"])
def api_export():
    try:
        payload = request.get_json() or {}
        ticker = payload.get("ticker", "MODEL").replace("/", "_")
        filename = f"Reverse_DCF_{ticker}.xlsx"
        create_reverse_dcf_workbook(filename, payload)
        return send_file(filename, as_attachment=True, download_name=filename)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    print("Starting Reverse DCF Dynamic Terminal on http://localhost:8080...")
    app.run(host="0.0.0.0", port=8080, debug=False)
